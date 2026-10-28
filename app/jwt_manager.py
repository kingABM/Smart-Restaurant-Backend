import os
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

# تحميل المتغيرات المخفية
load_dotenv()

# ثوابت التشفير (إعدادات المصنع)
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-for-development")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    # 1. أخذ نسخة من البيانات المراد تشفيرها
    to_encode = data.copy()
    
    # 2. حساب وقت انتهاء صلاحية التصريح
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 3. إضافة وقت الانتهاء إلى البيانات
    to_encode.update({"exp": expire})
    
    # 4. إصدار التصريح المشفر النهائي
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt