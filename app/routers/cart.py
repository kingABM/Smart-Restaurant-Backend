import json
from fastapi import APIRouter, HTTPException, BackgroundTasks, status, Depends
from redis import Redis
from app.repositories.cart_repository import save_cart, get_cart
from redis_client import get_redis  # تأكد من مسار الاستيراد الصحيح حسب مكان ملفك
import time

router = APIRouter(prefix="/cart", tags=["Cart"])

# 1. مسار حفظ وتحديث السلة (يمكننا أيضاً تحديث الـ Cache هنا إن أردنا)
@router.post("/{user_id}")
def add_to_cart_endpoint(user_id: int, cart_data: dict, redis: Redis = Depends(get_redis)):
    # حفظ في قاعدة البيانات الأساسية
    result = save_cart(user_id=user_id, cart_dictionary=cart_data)
    
    # تحديث الـ Cache فوراً (Cache Invalidation / Update)
    redis.setex(f"cart:{user_id}", 60, json.dumps(cart_data))
    
    return result

# 2. مسار استخراج وقراءة السلة (مع تفعيل الـ Redis Caching)
@router.get("/{user_id}")
def get_cart_endpoint(user_id: int, redis: Redis = Depends(get_redis)):
    cache_key = f"cart:{user_id}"
    
    # أ. البحث أولاً في ذاكرة التخزين المؤقت (Redis)
    cached_cart = redis.get(cache_key)
    if cached_cart:
        return {
            "source": "redis_cache",
            "data": json.loads(cached_cart)
        }
    
    # ب. إذا لم تكن موجودة في الـ Cache، نجلبها من قاعدة البيانات
    cart = get_cart(user_id=user_id)
    if cart is None:
        raise HTTPException(status_code=404, detail="السلة فارغة أو انتهت صلاحيتها")
    
    # ج. حفظ البيانات في Redis لمدة 60 ثانية لتسهيل الطلبات القادمة
    redis.setex(cache_key, 60, json.dumps(cart))
    
    return {
        "source": "database",
        "data": cart
    }

# 1. دالة خلفية تحاكي معالجة وإرسال البريد الإلكتروني (Background Function)
def send_order_confirmation_email(user_email: str, order_id: int, total_price: float):
    try:
        time.sleep(4)
        print(f"[بريد الخلفية] تم إرسال تأكيد الطلب رقم #{order_id} إلى: {user_email}")
    except Exception as e:
        print(f"[خطأ في الخلفية] فشل إرسال البريد للطلب #{order_id}: {str(e)}")

# 2. نقطة نهاية إتمام الشراء (Checkout Endpoint)
@router.post("/checkout/{user_id}")
async def checkout_cart(
    user_id: int, 
    user_email: str, 
    background_tasks: BackgroundTasks
):
    cart_items = [{"item": "بيتزا ببروني", "price": 150.0}]
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="السلة فارغة، لا يمكن إتمام الشراء"
        )

    simulated_order_id = 1052
    total_amount = sum(item["price"] for item in cart_items)
    
    background_tasks.add_task(
        send_order_confirmation_email, 
        user_email=user_email, 
        order_id=simulated_order_id, 
        total_price=total_amount
    )
    
    return {
        "status": "success",
        "message": "تم إتمام الطلب بنجاح وتفريغ السلة، وجاري إرسال الفاتورة لإيميلك.",
        "order_id": simulated_order_id,
        "total": total_amount
    }

