import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'url_shortener.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
