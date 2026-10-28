from passlib.context import CryptContext

# إعداد محرك التشفير وتحديد الخوارزمية
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    # دالة لتشفير كلمة المرور الجديدة عند إنشاء الحساب
    def bcrypt(password: str):
        return pwd_cxt.hash(password)
        
    # دالة لمقارنة كلمة المرور القادمة من العميل مع الكلمة المشفرة في قاعدة البيانات عند تسجيل الدخول
    def verify(plain_password, hashed_password):
        return pwd_cxt.verify(plain_password, hashed_password)