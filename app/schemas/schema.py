from pydantic import BaseModel

# الكلاس الأول: مخصص لإنشاء حساب جديد
class UserCreate (BaseModel):
    name :str
    phone_number :str
    email :str
    password :str

# الكلاس الثاني: مخصص لتسجيل الدخول فقط
class UserLogin (BaseModel):
    email:str
    password :str