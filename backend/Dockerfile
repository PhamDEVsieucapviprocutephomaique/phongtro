# ==================================
# Stage 1: Builder
# ==================================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# SỬA TẠI ĐÂY: Cài đặt vào folder /install thay vì --user
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==================================
# Stage 2: Production
# ==================================
FROM python:3.11-slim

WORKDIR /app

# SỬA TẠI ĐÂY: Copy từ /install vào /usr/local (nơi hệ thống mặc định cho phép đọc)
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Tạo user (Giữ nguyên phần này của bạn)
RUN addgroup --system --gid 1001 appuser && \
    adduser --system --uid 1001 --gid 1001 appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# SỬA TẠI ĐÂY: Healthcheck không nên dùng 'requests' vì bạn phải cài thêm thư viện đó.
# Nên dùng lệnh thuần python hoặc curl/wget nếu có sẵn.
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -m uvicorn.workers || exit 1 
  # Hoặc đơn giản là kiểm tra port 8000 có mở không

# SỬA TẠI ĐÂY: Dùng python -m uvicorn để chắc chắn gọi đúng module
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]