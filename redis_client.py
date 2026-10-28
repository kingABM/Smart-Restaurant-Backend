import os
from redis import Redis

# جلب بيانات الاتصال من المتغيرات البيئية التي عرفناها في Docker Compose
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# إنشاء كائن الاتصال بقاعدة بيانات الذاكرة السريعة
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def get_redis():
    return redis_client