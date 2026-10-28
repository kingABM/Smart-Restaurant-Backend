from app.jwt_manager import create_access_token
from fastapi import APIRouter , Depends
from sqlalchemy.orm import Session
from app.schemas import schema
from app import database
from app.repositories import user as user_repo


# تهيئة الموجه الخاص بالمستخدمين شغل تنظيمي 
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# مسار إنشاء حساب جديد (المنفذ)
@router.post("/register")
def register_user (request : schema.UserCreate , db : Session = Depends(database.get_db)):
    # توجيه الطلب النظيف وجلسة قاعدة البيانات إلى المخزن مباشرة
    return user_repo.create_user(request=request, db=db)


# مسار تسجيل الدخول وإصدار التصريح
@router.post("/login")
def login(request: schema.UserLogin, db: Session = Depends(database.get_db)):
    # 1. إرسال البيانات للمخزن للتحقق من صحة البريد وكلمة المرور
    user = user_repo.login_user(request=request, db=db)
    
    # 2. إذا مرت البيانات بسلام، نطلب من المصنع إصدار تصريح مرور يحمل هوية المستخدم
    access_token = create_access_token(data={"sub": user.email})
    
    # 3. تسليم التصريح للعميل في الشكل القياسي المعتمد عالميا
    return {"access_token": access_token, "token_type": "bearer"}