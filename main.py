from fastapi import FastAPI
from app.database import engine, Base
from app import models
# 1. استدعاء ملفات الـ Routers بالكامل وليس المتغيرات لتجنب التداخل
from app.routers import health, user 
# 1. استيراد المسار من مجلد المسارات
from app.routers import cart
from app.routers import T_background_tasks



Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(health.router)
app.include_router(user.router)

app.include_router(cart.router)


app.include_router(T_background_tasks.router)