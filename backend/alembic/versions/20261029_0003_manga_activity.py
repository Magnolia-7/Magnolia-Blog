"""Add daily time records, site statistics, and guestbook wishes.

Revision ID: 20261029_0003
Revises: 20261002_0002
"""
from datetime import datetime
from zoneinfo import ZoneInfo

from alembic import op
import sqlalchemy as sa

revision = "20261029_0003"
down_revision = "20261002_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("guestbook_messages", sa.Column("message_type", sa.String(20), nullable=False, server_default="message"))
    op.create_table("daily_time_logs",
        sa.Column("date", sa.Date(), primary_key=True),
        sa.Column("entries", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    site = op.create_table("site_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("started_on", sa.Date(), nullable=False),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("hero_image_url", sa.String(500), nullable=True),
    )
    # Set the original launch date in Admin > Site settings after upgrading.
    op.bulk_insert(site, [{"id": 1, "started_on": datetime.now(ZoneInfo("Asia/Shanghai")).date()}])
    op.create_table("site_visits",
        sa.Column("event_id", sa.String(36), primary_key=True),
        sa.Column("visitor_hash", sa.String(64), nullable=False),
        sa.Column("path", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_site_visits_visitor_hash", "site_visits", ["visitor_hash"])


def downgrade():
    op.drop_index("ix_site_visits_visitor_hash", table_name="site_visits")
    op.drop_table("site_visits")
    op.drop_table("site_settings")
    op.drop_table("daily_time_logs")
    op.drop_column("guestbook_messages", "message_type")
