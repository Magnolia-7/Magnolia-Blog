"""Magnolia Nook 2.0 content and media schema.

Revision ID: 20260826_0001
Revises:
Create Date: 2026-08-26
"""
from alembic import op
import sqlalchemy as sa


revision = "20260826_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("posts") as batch:
        batch.alter_column(
            "cover_image",
            existing_type=sa.String(length=255),
            type_=sa.String(length=500),
            existing_nullable=True,
        )
        batch.add_column(sa.Column("tags", sa.String(length=500), nullable=True))
        batch.add_column(sa.Column("is_pinned", sa.Boolean(), nullable=False, server_default=sa.false()))
        batch.add_column(sa.Column("published_at", sa.DateTime(), nullable=True))
        batch.create_index("ix_posts_is_pinned", ["is_pinned"])
        batch.create_index("ix_posts_published_at", ["published_at"])

    op.execute(
        "UPDATE posts SET published_at = created_at "
        "WHERE status = 'published' AND published_at IS NULL"
    )

    with op.batch_alter_table("about") as batch:
        batch.add_column(sa.Column("current_song", sa.String(length=200), nullable=True))
        batch.add_column(sa.Column("current_song_url", sa.String(length=500), nullable=True))
        batch.add_column(sa.Column("profile_tags", sa.Text(), nullable=True))
        batch.add_column(sa.Column("hero_subtitle", sa.String(length=500), nullable=True))
        batch.add_column(sa.Column("home_thought", sa.Text(), nullable=True))

    op.create_table(
        "media_assets",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("storage_provider", sa.String(20), nullable=False),
        sa.Column("object_key", sa.String(500), nullable=False, unique=True),
        sa.Column("thumbnail_key", sa.String(500), nullable=True),
        sa.Column("original_name", sa.String(255), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_media_assets_storage_provider", "media_assets", ["storage_provider"])

    op.create_table("social_links",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(80), nullable=False),
        sa.Column("url", sa.String(500), nullable=False), sa.Column("icon", sa.String(80)),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_table("tech_stacks",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(80), nullable=False),
        sa.Column("url", sa.String(500)), sa.Column("icon", sa.String(80)),
        sa.Column("level", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()))
    op.create_table("learning_nodes",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()), sa.Column("status", sa.String(20), nullable=False, server_default="locked"),
        sa.Column("lit_at", sa.DateTime()), sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("parent_id", sa.Integer(), sa.ForeignKey("learning_nodes.id", ondelete="SET NULL")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_learning_nodes_status", "learning_nodes", ["status"])
    op.create_index("ix_learning_nodes_sort_order", "learning_nodes", ["sort_order"])
    op.create_table("library_items",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("item_type", sa.String(20), nullable=False),
        sa.Column("title", sa.String(200), nullable=False), sa.Column("cover_image", sa.String(500)),
        sa.Column("external_url", sa.String(500)), sa.Column("status", sa.String(20), nullable=False, server_default="completed"),
        sa.Column("rating", sa.Float()), sa.Column("note", sa.Text()), sa.Column("finished_at", sa.Date()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_library_items_item_type", "library_items", ["item_type"])
    op.create_index("ix_library_items_status", "library_items", ["status"])
    op.create_table("albums",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text()), sa.Column("cover_image", sa.String(500)),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_table("photos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("album_id", sa.Integer(), sa.ForeignKey("albums.id", ondelete="CASCADE"), nullable=False),
        sa.Column("media_id", sa.Integer(), sa.ForeignKey("media_assets.id", ondelete="SET NULL")),
        sa.Column("image_url", sa.String(500), nullable=False), sa.Column("thumbnail_url", sa.String(500)),
        sa.Column("caption", sa.String(500)), sa.Column("taken_at", sa.Date()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_photos_album_id", "photos", ["album_id"])
    op.create_table("guestbook_messages",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nickname", sa.String(80), nullable=False),
        sa.Column("website", sa.String(500)), sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"), sa.Column("admin_reply", sa.Text()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_guestbook_messages_status", "guestbook_messages", ["status"])
    op.create_table("changelog_entries",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("version", sa.String(40), nullable=False),
        sa.Column("title", sa.String(200), nullable=False), sa.Column("content", sa.Text(), nullable=False),
        sa.Column("change_type", sa.String(20), nullable=False, server_default="feature"),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("published_at", sa.DateTime()),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
    op.create_index("ix_changelog_entries_version", "changelog_entries", ["version"])
    op.create_index("ix_changelog_entries_status", "changelog_entries", ["status"])
    op.create_index("ix_changelog_entries_published_at", "changelog_entries", ["published_at"])


def downgrade() -> None:
    op.drop_index("ix_changelog_entries_published_at", table_name="changelog_entries")
    op.drop_index("ix_changelog_entries_status", table_name="changelog_entries")
    op.drop_index("ix_changelog_entries_version", table_name="changelog_entries")
    op.drop_index("ix_guestbook_messages_status", table_name="guestbook_messages")
    op.drop_index("ix_photos_album_id", table_name="photos")
    op.drop_index("ix_library_items_status", table_name="library_items")
    op.drop_index("ix_library_items_item_type", table_name="library_items")
    op.drop_index("ix_learning_nodes_sort_order", table_name="learning_nodes")
    op.drop_index("ix_learning_nodes_status", table_name="learning_nodes")
    for table in ["changelog_entries", "guestbook_messages", "photos", "albums", "library_items", "learning_nodes", "tech_stacks", "social_links", "media_assets"]:
        op.drop_table(table)
    with op.batch_alter_table("about") as batch:
        for column in ["home_thought", "hero_subtitle", "profile_tags", "current_song_url", "current_song"]:
            batch.drop_column(column)
    with op.batch_alter_table("posts") as batch:
        batch.drop_index("ix_posts_published_at")
        batch.drop_index("ix_posts_is_pinned")
        batch.drop_column("published_at")
        batch.drop_column("is_pinned")
        batch.drop_column("tags")
        batch.alter_column(
            "cover_image",
            existing_type=sa.String(length=500),
            type_=sa.String(length=255),
            existing_nullable=True,
        )
