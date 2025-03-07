# === BACKEND STAGE ===
FROM python:3.10-slim AS backend

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libstdc++6 \
    libblas3 \
    liblapack3 \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các dependency backend
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn backend
COPY code/ code/
COPY data/ data/
COPY api.py .
COPY chunks.json .
COPY faiss_index.bin .

# === FRONTEND STAGE ===
FROM node:18 AS frontend

# Làm việc tại thư mục frontend
WORKDIR /frontend
COPY front-end/ ./
RUN npm install
RUN npm run build

# === FINAL STAGE ===
FROM python:3.10-slim

# Cài đặt thư viện hệ thống cho runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libblas3 \
    liblapack3 \
    nodejs \
    npm \
    gcc \
    g++ \
    libstdc++6 \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g serve

# Làm việc tại thư mục app
WORKDIR /app

# Copy backend từ stage trước
COPY --from=backend /app /app

# Cài đặt lại các dependency Python trong Final Stage
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend build
COPY --from=frontend /frontend/dist /app/front-end/dist

# Mở cổng
EXPOSE 8000 5173

# Chạy backend (uvicorn) và frontend (serve)
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 & serve -s /app/front-end/dist -l 5173"]