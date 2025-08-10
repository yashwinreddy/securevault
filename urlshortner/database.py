import sqlalchemy
from databases import Database

DATABASE_URL = "sqlite:///./url_shortener.db"

database = Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
