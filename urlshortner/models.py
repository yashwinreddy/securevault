import sqlalchemy
from database import metadata
import datetime
import string
import random

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

urls = sqlalchemy.Table(
    "urls",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("original_url", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("short_code", sqlalchemy.String, unique=True, index=True, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column("expire_at", sqlalchemy.DateTime, nullable=True),  # expiration datetime
)

clicks = sqlalchemy.Table(
    "clicks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("url_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("urls.id")),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime, default=datetime.datetime.utcnow),
    sqlalchemy.Column("ip_address", sqlalchemy.String(45)),
    sqlalchemy.Column("user_agent", sqlalchemy.String(256)),
)
