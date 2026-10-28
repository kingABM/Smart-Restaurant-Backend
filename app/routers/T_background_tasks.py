import time
from fastapi import APIRouter , BackgroundTasks

router = APIRouter()

# 1. دالة تحاكي عملية ثقيلة تستغرق وقتاً (مثل إرسال البريد)
def send_email_simulation(email:str):
    time.sleep(5) # محاكاة انتظار لمدة 5 ثوانٍ
    print(f"[الخلفية] تم إرسال البريد بنجاح إلى: {email}")

# 2. نقطة النهاية التي تفوض المهمة للخلفية
@router.post("/test-background/{email}")
async def test_background_endpoint(email: str, background_tasks: BackgroundTasks):    # إضافة المهمة لقائمة الانتظار في الخلفية
    background_tasks.add_task(send_email_simulation, email)
    # إرجاع الاستجابة فوراً دون انتظار الـ 5 ثوانٍ
    return {
        "status": "success",
        "message": "تم استلام طلبك بنجاح، وجاري معالجة الإشعار في الخلفية."
    }