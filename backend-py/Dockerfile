# ============================================
# 第 1 阶段：构建阶段 — 安装依赖
# ============================================
# python:3.11-slim 体积小（~120MB），包含运行 Python 所需的最小系统库
FROM python:3.11-slim AS builder

WORKDIR /build

# 先复制 requirements.txt，利用 Docker 缓存层
# 只要 requirements.txt 没变，pip install 这层就会被缓存，不用每次重新安装
COPY requirements.txt .

# 创建虚拟环境并安装依赖
# --no-cache-dir: 不缓存下载的包，减小镜像体积
# --prefix=/install: 把包安装到指定目录，方便后续复制
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ============================================
# 第 2 阶段：运行阶段 — 只复制必要文件
# ============================================
FROM python:3.11-slim AS runtime

# 设置环境变量
# PYTHONDONTWRITEBYTECODE: 不生成 .pyc 文件，减小镜像体积
# PYTHONUNBUFFERED: 关闭输出缓冲，让日志实时可见（Docker 日志需要）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 从构建阶段复制安装好的依赖
# 这样运行阶段不需要 pip，也不需要编译工具，镜像更小
COPY --from=builder /install /usr/local

# 复制应用代码
COPY . .

# 创建上传文件目录
RUN mkdir -p /app/uploads

# 复制启动脚本并设置可执行权限
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 创建非 root 用户（安全最佳实践）
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# 启动脚本：先跑数据库迁移，再启动服务
CMD ["/entrypoint.sh"]
