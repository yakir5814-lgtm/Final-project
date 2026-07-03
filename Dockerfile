FROM python:3.9-slim

# התקנת curl לצורך המשימה (כפי שהיה לך)
RUN apt-get update && apt-get install -y curl && \
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

WORKDIR /app

# העתקת ה-requirements (כמו שעשית)
COPY requirements.txt .

# --- כאן התיקון: התקנה ידנית של yfinance בנוסף ל-requirements ---
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir yfinance

COPY . .

EXPOSE 5001
CMD ["python", "app.py"]
