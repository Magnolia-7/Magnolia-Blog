"""Integration checks with isolated SQLite storage; never touches the configured database."""
import os
import sys
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "isolated-test-secret-not-for-production"
os.environ["DEBUG"] = "false"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from alembic import command
from alembic.config import Config

from app.main import app
from app.core.database import Base, get_db
from app.api.deps import get_current_admin
from app.api import content
from app.models.activity import SiteSettings, SiteVisit
from app.models.post import Post


class MangaFeaturesTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine)

        def test_db():
            with self.sessions() as db:
                yield db

        app.dependency_overrides[get_db] = test_db
        app.dependency_overrides[get_current_admin] = lambda: object()
        self.clock = patch("app.api.activity.today", return_value=date(2026, 10, 29))
        self.clock.start()
        content._message_attempts.clear()
        self.client = TestClient(app)
        with self.sessions.begin() as db:
            db.add(SiteSettings(id=1, started_on=date(2026, 5, 8)))

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        self.clock.stop()
        self.engine.dispose()

    def save_log(self, day, entries):
        return self.client.put(f"/api/admin/activity/time-logs/{day}", json={"entries": entries})

    def test_daily_log_replacement_calendar_and_aggregates(self):
        self.assertEqual(self.save_log("2026-10-28", [{"category": "C++", "minutes": 90}, {"category": "阅读", "minutes": 30}]).status_code, 200)
        self.assertEqual(self.save_log("2026-10-28", [{"category": "C++", "minutes": 120}, {"category": "阅读", "minutes": 30}]).json()["total_minutes"], 150)
        self.save_log("2026-10-01", [{"category": "阅读", "minutes": 45}])
        self.save_log("2026-09-30", [{"category": "英语", "minutes": 60}])
        logs = self.client.get("/api/activity/time-logs", params={"month": "2026-10"}).json()
        self.assertEqual([log["total_minutes"] for log in logs], [45, 150])
        month = self.client.get("/api/activity/time-summary", params={"period": "month"}).json()
        self.assertEqual((month["total_minutes"], month["tracked_days"]), (195, 2))
        self.assertEqual(next(row for row in month["categories"] if row["category"] == "阅读"), {"category": "阅读", "minutes": 75, "days": 2})
        self.assertEqual(self.client.get("/api/activity/time-summary?period=week").json()["total_minutes"], 150)
        self.assertEqual(self.client.get("/api/activity/time-summary?period=all").json()["total_minutes"], 255)

    def test_time_validation_does_not_overwrite_existing_data(self):
        self.save_log("2026-10-28", [{"category": "C++", "minutes": 30}])
        invalid = [
            [{"category": " ", "minutes": 30}],
            [{"category": "C++", "minutes": -1}],
            [{"category": "C++", "minutes": 1.5}],
            [{"category": "C++", "minutes": 1000}, {"category": "阅读", "minutes": 500}],
            [{"category": "C++", "minutes": 30}, {"category": " C++ ", "minutes": 30}],
        ]
        for entries in invalid:
            with self.subTest(entries=entries):
                self.assertEqual(self.save_log("2026-10-28", entries).status_code, 422)
        self.assertEqual(self.client.get("/api/admin/activity/time-logs/2026-10-28").json()["total_minutes"], 30)
        self.assertEqual(self.save_log("2026-10-30", [{"category": "阅读", "minutes": 30}]).status_code, 422)
        self.assertEqual(self.client.get("/api/activity/time-logs?month=2026-13").status_code, 422)
        self.assertEqual(self.client.get("/api/activity/time-logs?month=9999-12").status_code, 422)

    def test_empty_and_deleted_days_do_not_count(self):
        self.save_log("2026-10-28", [])
        self.assertEqual(self.client.get("/api/activity/time-summary").json()["tracked_days"], 0)
        self.save_log("2026-10-28", [{"category": "阅读", "minutes": 30}])
        self.assertEqual(self.client.delete("/api/admin/activity/time-logs/2026-10-28").status_code, 204)
        self.assertEqual(self.client.get("/api/activity/time-logs?month=2026-10").json(), [])

    def test_anonymous_visitors_unique_but_page_views_count_navigation(self):
        visitor = str(uuid4())
        event = {"visitor_id": visitor, "event_id": str(uuid4()), "path": "/records?secret=not-stored"}
        self.assertEqual(self.client.post("/api/activity/visits", json=event).status_code, 204)
        self.assertEqual(self.client.post("/api/activity/visits", json=event).status_code, 204)
        self.client.post("/api/activity/visits", json={**event, "event_id": str(uuid4()), "path": "/about"})
        self.client.post("/api/activity/visits", json={**event, "visitor_id": str(uuid4()), "event_id": str(uuid4())})
        with self.sessions.begin() as db:
            db.add_all([Post(title="公开", content="内容", summary="", category="thought", status="published"), Post(title="草稿", content="内容", summary="", category="life", status="draft")])
        stats = self.client.get("/api/activity/stats").json()
        self.assertEqual((stats["visitors"], stats["page_views"], stats["articles"]), (2, 3, 1))
        self.assertEqual(stats["running_days"], (date(2026, 10, 29) - date(2026, 5, 8)).days)
        with self.sessions() as db:
            visit = db.get(SiteVisit, event["event_id"])
            self.assertNotEqual(visit.visitor_hash, visitor)
            self.assertEqual(visit.path, "/records")

    def test_private_routes_and_invalid_visitor_ids_are_rejected(self):
        for path in ["/admin", "/login", "/api/auth", "https://example.com"]:
            self.assertEqual(self.client.post("/api/activity/visits", json={"visitor_id": str(uuid4()), "event_id": str(uuid4()), "path": path}).status_code, 422)
        self.assertEqual(self.client.post("/api/activity/visits", json={"visitor_id": "bad", "event_id": "bad", "path": "/"}).status_code, 422)

    def test_time_and_site_writes_require_admin(self):
        del app.dependency_overrides[get_current_admin]
        self.assertIn(self.save_log("2026-10-28", []).status_code, [401, 403])
        self.assertIn(self.client.put("/api/admin/activity/site", json={"started_on": "2026-05-08"}).status_code, [401, 403])
        self.assertIn(self.client.delete("/api/admin/activity/time-logs/2026-10-28").status_code, [401, 403])

    def test_wishes_require_approval_and_keep_their_type(self):
        created = self.client.post("/api/content/guestbook", json={"nickname": "  访客  ", "content": "希望期末顺利", "message_type": "wish"})
        self.assertEqual(created.status_code, 201)
        self.assertEqual(self.client.get("/api/content/guestbook").json(), [])
        pending = self.client.get("/api/admin/content/guestbook").json()[0]
        self.assertEqual((pending["nickname"], pending["message_type"]), ("访客", "wish"))
        self.client.patch(f"/api/admin/content/guestbook/{pending['id']}", json={"status": "approved"})
        self.assertEqual(self.client.get("/api/content/guestbook").json()[0]["message_type"], "wish")
        self.client.patch(f"/api/admin/content/guestbook/{pending['id']}", json={"status": "hidden"})
        self.assertEqual(self.client.get("/api/content/guestbook").json(), [])

    def test_guestbook_validation_and_default_message_type(self):
        for extra in [{"website": "javascript:alert(1)"}, {"message_type": "other"}, {"message_type": "wish", "content": "许" * 201}, {"content": "   "}]:
            self.assertEqual(self.client.post("/api/content/guestbook", json={"nickname": "访客", "content": "你好", **extra}).status_code, 422)
        self.client.post("/api/content/guestbook", json={"nickname": "访客", "content": "你好"})
        self.assertEqual(self.client.get("/api/admin/content/guestbook").json()[0]["message_type"], "message")

    def test_thought_posts_publish_filter_search_and_legacy_categories(self):
        for category in ["life", "study", "thought"]:
            response = self.client.post("/api/admin/posts/", json={"title": f"{category} 标题", "content": "正文", "category": category, "status": "published"})
            self.assertEqual(response.status_code, 200)
        listing = self.client.get("/api/posts/?category=thought").json()
        self.assertEqual(listing["total"], 1)
        self.assertEqual(listing["items"][0]["category"], "thought")
        self.assertEqual(len(self.client.get("/api/search/?category=thought&q=标题").json()), 1)
        self.assertEqual(self.client.get("/api/admin/posts/?category=thought").json()["total"], 1)

    def test_site_settings_persist_and_reject_future_dates(self):
        response = self.client.put("/api/admin/activity/site", json={"started_on": "2026-04-01", "avatar_url": "/media/sanji.webp", "hero_image_url": "https://example.com/crew.jpg"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/api/activity/site").json()["avatar_url"], "/media/sanji.webp")
        self.assertEqual(self.client.put("/api/admin/activity/site", json={"started_on": "2027-01-01"}).status_code, 422)


class MigrationTest(unittest.TestCase):
    def test_upgrade_preserves_existing_message_and_adds_defaults(self):
        engine = create_engine("sqlite://")
        with engine.begin() as db:
            db.execute(text("CREATE TABLE guestbook_messages (id INTEGER PRIMARY KEY, content TEXT NOT NULL)"))
            db.execute(text("INSERT INTO guestbook_messages (id, content) VALUES (1, '原有留言')"))
        config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
        config.set_main_option("script_location", str(Path(__file__).resolve().parents[1] / "alembic"))
        config.attributes["connection"] = engine
        command.stamp(config, "20261002_0002")
        command.upgrade(config, "head")
        with engine.connect() as db:
            self.assertEqual(db.execute(text("SELECT content, message_type FROM guestbook_messages WHERE id=1")).one(), ("原有留言", "message"))
            self.assertEqual(db.execute(text("SELECT count(*) FROM site_settings")).scalar(), 1)
        self.assertIn("daily_time_logs", inspect(engine).get_table_names())
        engine.dispose()


if __name__ == "__main__":
    unittest.main()
