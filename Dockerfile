# 1. Base Image: استدعاء نظام تشغيل مصغر جداً يحتوي على بايثون
FROM python:3.11-slim

# 2. Working Directory: تحديد مجلد العمل الداخلي للحاوية
WORKDIR /app

# 3. Cache Optimization: نسخ ملف المكتبات أولاً لتسريع عملية البناء مستقبلاً
COPY requirements.txt .

# 4. Dependencies: تثبيت المكتبات المطلوبة بدون حفظ ملفات مؤقتة لتقليل مساحة الحاوية
RUN pip install --no-cache-dir -r requirements.txt

# 5. Source Code: نسخ باقي ملفات المشروع بالكامل إلى داخل الحاوية
COPY . .

# 6. Network: فتح المنفذ الذي سيستقبل عليه الخادم الطلبات
EXPOSE 8000

# 7. Execution Command: الأمر التنفيذي لتشغيل الخادم عند بدء عمل الحاوية
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]