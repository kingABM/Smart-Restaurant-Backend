import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv

# هنا أمرت النظام بقراءة الملف المخفي وتحميل المتغيرات الحساسة منه
load_dotenv()

# هنا استدعي الرابط من البيئة المخفية بأمان تام
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:8434487@db:5432/Restaurant_database')

# هنا اصنع المحرك الذي سينفذ الأوامر
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# هنا اصنع مصنع الجلسات الذي سيعطي كل مسار جلسة خاصة به
SessionLocal = sessionmaker(autocommit = False , autoflush= False , bind = engine)

# هذا هو الكلاس الأساسي الذي سأبنى عليه النماذج لاحقا
Base = declarative_base()


# دالة أمين المخزن (لفتح وإغلاق مسار الاتصال مع كل طلب بشكل آمن)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()