import hashlib
import hmac
from collections import defaultdict
from datetime import date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import distinct, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.config import settings
from app.core.database import get_db
from app.models.activity import DailyTimeLog, SiteSettings, SiteVisit
from app.models.post import Post
from app.schemas.activity import (
    DailyTimeLogResponse, DailyTimeLogWrite, SiteSettingsResponse,
    SiteSettingsWrite, SiteStatsResponse, TimeSummaryResponse, VisitCreate,
)

router = APIRouter(prefix="/api/activity", tags=["Activity"])
admin_router = APIRouter(
    prefix="/api/admin/activity", tags=["Admin Activity"],
    dependencies=[Depends(get_current_admin)],
)


def today():
    return datetime.now(ZoneInfo("Asia/Shanghai")).date()


def site_settings(db):
    return db.get(SiteSettings, 1) or SiteSettings(id=1, started_on=today())


def serialize_log(log):
    return {"date": log.date, "entries": log.entries,
            "total_minutes": sum(entry["minutes"] for entry in log.entries)}


def month_bounds(month):
    try:
        start = date.fromisoformat(month + "-01")
        end = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    except (ValueError, OverflowError):
        raise HTTPException(422, "月份格式应为 YYYY-MM")
    return start, end


@router.get("/site", response_model=SiteSettingsResponse)
def get_site(db: Session = Depends(get_db)):
    return site_settings(db)


@admin_router.put("/site", response_model=SiteSettingsResponse)
def update_site(payload: SiteSettingsWrite, db: Session = Depends(get_db)):
    if payload.started_on > today():
        raise HTTPException(422, "上线日期不能晚于今天")
    item = db.get(SiteSettings, 1)
    if item is None:
        item = SiteSettings(id=1)
        db.add(item)
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.get("/stats", response_model=SiteStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    visitors, views = db.query(func.count(distinct(SiteVisit.visitor_hash)), func.count()).select_from(SiteVisit).one()
    started = site_settings(db).started_on
    return {
        "visitors": visitors, "page_views": views,
        "articles": db.query(Post).filter(Post.status == "published").count(),
        "started_on": started, "running_days": max(0, (today() - started).days),
    }


@router.post("/visits", status_code=204)
def record_visit(payload: VisitCreate, db: Session = Depends(get_db)):
    # The random browser identifier is hashed; no IP address or query string is stored.
    visitor_hash = hmac.new(settings.SECRET_KEY.encode(), str(payload.visitor_id).encode(), hashlib.sha256).hexdigest()
    visit = SiteVisit(event_id=str(payload.event_id), visitor_hash=visitor_hash, path=payload.path)
    db.add(visit)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()  # Retrying the same navigation must not add another page view.
        if db.get(SiteVisit, str(payload.event_id)) is None:
            raise
    return Response(status_code=204)


@router.get("/time-logs", response_model=list[DailyTimeLogResponse])
@admin_router.get("/time-logs", response_model=list[DailyTimeLogResponse])
def get_time_logs(
    month: str = Query(pattern=r"^\d{4}-\d{2}$"), db: Session = Depends(get_db),
):
    start, end = month_bounds(month)
    logs = db.query(DailyTimeLog).filter(DailyTimeLog.date >= start, DailyTimeLog.date < end).order_by(DailyTimeLog.date).all()
    return [serialize_log(log) for log in logs]


@admin_router.get("/time-logs/{log_date}", response_model=DailyTimeLogResponse)
def get_daily_log(log_date: date, db: Session = Depends(get_db)):
    item = db.get(DailyTimeLog, log_date)
    return serialize_log(item) if item else {"date": log_date, "entries": [], "total_minutes": 0}


@admin_router.put("/time-logs/{log_date}", response_model=DailyTimeLogResponse)
def save_daily_log(log_date: date, payload: DailyTimeLogWrite, db: Session = Depends(get_db)):
    if log_date > today():
        raise HTTPException(422, "不能填写未来日期的投入时间")
    item = db.get(DailyTimeLog, log_date)
    if item is None:
        item = DailyTimeLog(date=log_date)
        db.add(item)
    item.entries = [entry.model_dump() for entry in payload.entries]
    db.commit()
    db.refresh(item)
    return serialize_log(item)


@admin_router.delete("/time-logs/{log_date}", status_code=204)
def delete_daily_log(log_date: date, db: Session = Depends(get_db)):
    item = db.get(DailyTimeLog, log_date)
    if item:
        db.delete(item)
        db.commit()
    return Response(status_code=204)


@router.get("/time-summary", response_model=TimeSummaryResponse)
def get_time_summary(
    period: Literal["week", "month", "all"] = "month", db: Session = Depends(get_db),
):
    end = today()
    start = end - timedelta(days=end.weekday()) if period == "week" else end.replace(day=1) if period == "month" else None
    query = db.query(DailyTimeLog).filter(DailyTimeLog.date <= end)
    if start:
        query = query.filter(DailyTimeLog.date >= start)
    logs = query.order_by(DailyTimeLog.date).all()
    totals = defaultdict(lambda: {"minutes": 0, "days": 0})
    tracked_days = 0
    for log in logs:
        if log.entries:
            tracked_days += 1
        for entry in log.entries:
            totals[entry["category"]]["minutes"] += entry["minutes"]
            totals[entry["category"]]["days"] += 1
    return {
        "total_minutes": sum(value["minutes"] for value in totals.values()),
        "tracked_days": tracked_days, "start_date": start or (logs[0].date if logs else None), "end_date": end,
        "categories": [{"category": key, **value} for key, value in sorted(totals.items(), key=lambda pair: (-pair[1]["minutes"], pair[0]))],
    }
