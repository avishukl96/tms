# from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
# from config.db import meta, engine
# from datetime import datetime

# tasks = Table(
#     "tasks", meta,
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("title", String(255), nullable=False),
#     Column("description", String(255)),
#     Column("status", String(50), default="To-do"),
#     Column("assigned_to", Integer, ForeignKey("users.id")),
#     Column("admin_id", Integer, ForeignKey("administrator.id")),  # New column for admin ID
#     Column("created_at", DateTime, default=datetime.utcnow),
#     Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
# )

# meta.create_all(engine)

from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from config.db import engine, meta
from datetime import datetime

tasks = Table(
    "tasks", meta,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(255)),
    Column("status", String(50), default="To-do"),
    Column("assigned_to", Integer, ForeignKey("users.id"), nullable=True),  # Foreign key to users
    Column("admin_id", Integer, ForeignKey("administrator.admin_id"), nullable=True),  # Foreign key to admin
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)

meta.create_all(engine)





