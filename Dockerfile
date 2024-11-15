# Gunakan image Python yang sudah ada
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Salin file requirements.txt dan install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Salin seluruh kode aplikasi
COPY . .

# Set environment variables
ENV FLASK_APP=api_gold.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose port
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["flask", "run"]
