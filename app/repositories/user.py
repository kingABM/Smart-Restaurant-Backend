from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app import models
from app.schemas import schema
from hashing import Hash

def create_user (request: schema.UserCreate , db: Session):
    # 1. تغليف البيانات النظيفة في النموذج العميق مع تشفير كلمة المرور فوراً
    new_user = models.User(
        name=request.name,
        phone_number=request.phone_number,
        email=request.email,
        password=Hash.bcrypt(request.password)  # هنا تتدخل فرامة التشفير!
    )

    # 2. وضع المستخدم في عربة النقل (Identity Map)
    db.add(new_user)

    # 3. الاعتماد النهائي وإرسال أمر الحفظ الفعلي لـ PostgreSQL
    db.commit()

    # 4. تحديث الكائن لكي نجلب الـ id الذي تم توليده تلقائياً من قاعدة البيانات
    db.refresh(new_user)

    return new_user

def login_user(request: schema.UserLogin, db: Session):
    # 1. البحث عن المستخدم في قاعدة البيانات باستخدام البريد الإلكتروني
    user = db.query(models.User).filter(models.User.email == request.email).first()
    
    # 2. التحقق من وجود المستخدم أساسا في النظام
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بيانات الدخول غير صحيحة")
        
    # 3. مطابقة كلمة المرور القادمة من العميل مع الكلمة المشفرة في قاعدة البيانات
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="بيانات الدخول غير صحيحة")
        
    # 4. إذا مرت كل الفحوصات بسلام، نرجع كائن المستخدم
    return user