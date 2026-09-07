from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:5178",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5178",
]

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
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
