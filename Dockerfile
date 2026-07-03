FROM python:3.9-slim

# הגדרת תיקיית עבודה
WORKDIR /app

# העתקת דרישות והתקנתן בתוך האימג'
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת הקוד עצמו
COPY . .

# הרצת האפליקציה
CMD ["python", "app.py"]
