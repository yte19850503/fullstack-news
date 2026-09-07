from contextlib import asynccontextmanager
from datetime import datetime

import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, article, category, comment, tag, admin, ad, seo
from app.services.rate_limiter import rate_limiter
from app.services.view_counter import view_counter
from app.core.security_headers import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    view_counter.start_auto_sync(60000)
    yield


app = FastAPI(
    title="News API",
    version="1.0.0",
    description="AI 工具 + 短剧 资讯平台后端接口，包含用户认证、文章管理、评论、分类/标签、广告、后台管理等模块。",
    contact={"name": "Dev Team", "email": "dev@news.local"},
    openapi_tags=[
        {"name": "auth", "description": "用户认证：注册、登录、登出"},
        {"name": "articles", "description": "文章：列表、搜索、详情、CRUD"},
        {"name": "categories", "description": "分类管理"},
        {"name": "tags", "description": "标签查询"},
        {"name": "comments", "description": "评论：按文章查看、发布、删除"},
        {"name": "admin", "description": "后台管理：统计、用户/文章/分类/标签/评论/日志"},
        {"name": "ads", "description": "广告：公开投放、事件上报、后台 CRUD、统计"},
    ],
    lifespan=lifespan,
)

_cors_env = os.getenv("CORS_ORIGINS", "")
ALLOWED_ORIGINS = (
    [o.strip() for o in _cors_env.split(",") if o.strip()]
    if _cors_env
    else [
        "http://localhost:5173",
        "http://localhost:5178",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5178",
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.add_middleware(SecurityHeadersMiddleware)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    rate_limiter(request)
    return await call_next(request)


app.include_router(auth.router, prefix="/api")
app.include_router(article.router, prefix="/api")
app.include_router(category.router, prefix="/api")
app.include_router(comment.router, prefix="/api")
app.include_router(tag.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(ad.router, prefix="/api")
app.include_router(seo.router)


@app.get("/api/health", summary="健康检查")
def health():
    db_ok = False
    try:
        from app.database import engine
        with engine.connect() as conn:
            conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_ok = True
    except Exception as e:
        db_ok = False
    return {
        "status": "ok" if db_ok else "degraded",
        "database": "connected" if db_ok else "unreachable",
        "timestamp": datetime.now().isoformat(),
    }


# ---------- 生产环境：托管前端静态文件 ----------
_base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
_frontend_dist = os.path.normpath(os.path.join(_base_dir, "frontend", "dist"))
_admin_dist = os.path.normpath(os.path.join(_base_dir, "admin", "dist"))

print(f"[static] _admin_dist={_admin_dist} exists={os.path.isdir(_admin_dist)}")
print(f"[static] _frontend_dist={_frontend_dist} exists={os.path.isdir(_frontend_dist)}")

if os.path.isdir(_admin_dist):
    app.mount("/admin", StaticFiles(directory=_admin_dist, html=True), name="admin-static")
else:
    print(f"[static] WARNING: admin dist not found at {_admin_dist}, /admin will not be served")

if os.path.isdir(_frontend_dist):
    from fastapi.responses import FileResponse

    @app.get("/{full_path:path}")
    def _serve_spa(full_path: str):
        if full_path.startswith("admin"):
            admin_file = os.path.join(_admin_dist, full_path[len("admin"):].lstrip("/"))
            if os.path.isfile(admin_file):
                return FileResponse(admin_file)
            if os.path.isdir(_admin_dist):
                return FileResponse(os.path.join(_admin_dist, "index.html"))
        file_path = os.path.join(_frontend_dist, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(_frontend_dist, "index.html"))
