# ============================================
# 全栈生产镜像 — 构建前端 + 后端，单容器部署
# ============================================

# --- 阶段 1：构建前端 ---
FROM node:20-alpine AS frontend-builder
WORKDIR /build/frontend
COPY frontend/ .
RUN npm install && npm run build

# --- 阶段 2：构建管理后台 ---
FROM node:20-alpine AS admin-builder
WORKDIR /build/admin
COPY admin/ .
RUN npm install && npm run build

# --- 阶段 3：安装 Python 依赖 ---
FROM python:3.11-slim AS builder
WORKDIR /build
COPY backend-py/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- 阶段 4：运行镜像 ---
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Python 依赖
COPY --from=builder /install /usr/local

# 后端代码
COPY backend-py/ ./backend-py/

# 前端构建产物
COPY --from=frontend-builder /build/frontend/dist ./frontend/dist

# 管理后台构建产物
COPY --from=admin-builder /build/admin/dist ./admin/dist

# 入口脚本
COPY entrypoint.prod.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /app/uploads
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["/entrypoint.sh"]
