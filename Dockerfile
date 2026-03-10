FROM python:3.14-rc-slim

# הגדרת תיקיית העבודה בתוך הקונטיינר
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#העתקת התיקייה
COPY . .

# שלב 5: הרצת השרת
# בגלל שאתה ב-OmerProject, ודא ש-main.py נמצא בתיקייה הראשית
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]