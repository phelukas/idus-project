FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    postgresql-client \
    && apt-get clean
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh
COPY . /app/
EXPOSE 8000
CMD ["./wait-for-db.sh", "db", "python", "manage.py", "runserver", "0.0.0.0:8000"]
