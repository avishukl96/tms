from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from config.db import meta, engine
from datetime import datetime

admin = Table(
    "administrator", meta,
    Column("admin_id", Integer, primary_key=True, autoincrement=True),
    Column("admin_name", String(255), nullable=False),
    Column("admin_email", String(255)),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)

meta.create_all(engine)
      