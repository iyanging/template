from app.settings import REDIS_URL
from .client import Redis

redis = Redis(REDIS_URL)
