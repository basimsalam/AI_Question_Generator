import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
CACHE_TTL = 86400  # 24 hours

def add_to_question_pool(user_id: str, question: str):
    key = f"used_questions:{user_id}"
    redis_client.sadd(key, question)
    redis_client.expire(key, 86400)  # 24 hours


def is_duplicate_question(user_id: str, question: str) -> bool:
    key = f"used_questions:{user_id}"
    return redis_client.sismember(key, question)


def clear_question_pool(user_id: str):
    key = f"used_questions:{user_id}"
    redis_client.delete(key)



def build_cache_key(topic: str, difficulty: str, question_type: str) -> str:
    return f"question_cache:{topic}:{difficulty.lower()}:{question_type.lower()}"

def get_cached_question(topic: str, difficulty: str, question_type: str) -> str | None:
    key = build_cache_key(topic, difficulty, question_type)
    return redis_client.get(key)

def cache_question(topic: str, difficulty: str, question_type: str, question_text: str):
    key = build_cache_key(topic, difficulty, question_type)
    redis_client.setex(key, CACHE_TTL, question_text)

def clear_all_cached_questions():
    keys = redis_client.keys("question_cache:*")
    if keys:
        redis_client.delete(*keys)