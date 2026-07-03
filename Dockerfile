FROM python:3.9-slim

# התקנת curl וניקוי שאריות של apt מיד אחרי כדי לחסוך מקום
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# מעתיקים רק את ה-requirements
COPY requirements.txt .

# מתקינים הכל בבת אחת - הכי מהיר והכי נקי
RUN pip install --no-cache-dir -r requirements.txt

# מעתיקים את שאר הקוד
COPY . .

EXPOSE 5001
CMD ["python", "app.py"]
