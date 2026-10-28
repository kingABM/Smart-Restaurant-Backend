import json 
import os
import redis

# جلب عنوان الـ Redis من المتغيرات البيئية أو استخدام اسم الخدمة داخل دوكر تلقائياً
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST, 
    port=REDIS_PORT, 
    db=0, 
    decode_responses=True,
    protocol=2
)

def save_cart(user_id: int, cart_dictionary: dict):
    redis_key = f"cart:{user_id}"
    text_data = json.dumps(cart_dictionary)
    redis_client.setex(name=redis_key, time=1800, value=text_data)
    return {"message": "Cart saved successfully", "expires_in": "30 minutes"}

def get_cart(user_id: int):
    redis_key = f"cart:{user_id}"
    
    # 1. قراءة النص من الذاكرة السريعة (Redis)
    text_data = redis_client.get(name=redis_key)
    
    # 2. التحقق من وجود السلة
    if not text_data:
        return None
        
    # 3. تحويل النص العائد إلى قاموس وإرجاعه
    return json.loads(text_data)