"""
测试基础设施

核心思路：
1. 用 SQLite 内存数据库替代 MySQL（无需外部依赖，每个测试会话隔离）
2. 用 FakeRedis 替代真实 Redis（mock 所有缓存/限流/黑名单操作）
3. 在导入 app 模块之前完成 patch，确保所有模块拿到的是 fake 对象
"""

import sys
from pathlib import Path
from unittest.mock import patch

# ── 1. FakeRedis ──────────────────────────────────────────


class FakeRedis:
    """模拟 Redis 接口，所有操作都是空操作或返回安全默认值"""

    def get(self, key):
        return None

    def set(self, key, value, ex=None):
        pass

    def setex(self, key, ttl, value):
        pass

    def delete(self, *keys):
        pass

    def exists(self, key):
        return 0

    def incr(self, key):
        return 1

    def expire(self, key, ttl):
        pass

    def scan(self, cursor=0, match=None, count=100):
        return (0, [])

    def ping(self):
        return True

    def zincrby(self, key, amount, member):
        pass

    def zrevrange(self, key, start, end, withscores=False):
        return []

    def hincrby(self, key, field, amount):
        pass

    def hgetall(self, key):
        return {}


# ── 2. 在导入 app 之前 patch redis_client ─────────────────

# app.services.cache 模块顶层创建了 redis_client = Redis.from_url(...)
# 我们用一个假的替换它，这样所有 import redis_client 的模块都拿到 FakeRedis
import app.services.cache as _cache_module

_cache_module.redis_client = FakeRedis()

# 同时 patch 模块属性，确保后续 from ... import 也拿到 fake
patch.object(_cache_module, "redis_client", FakeRedis()).start()


# ── 3. 现在安全导入 app 模块 ──────────────────────────────

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.api.deps import get_db
from app.main import app
from app.models.user import User, Role
from app.models.category import Category
from app.models.tag import Tag
from app.models.article import Article, ArticleStatus, ArticleTag
from app.models.comment import Comment
from app.models.ad import AdSlot, AdStatus
from app.core.security import create_access_token, hash_password


# ── 4. SQLite 引擎 ────────────────────────────────────────

# SQLite 内存数据库是 per-connection 的，每个新连接拿到的是空库。
# 用 StaticPool 让所有 session 共享同一个连接，这样 create_all 建的表
# 在 TestClient 请求里也能看到。
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine)


# ── 5. FastAPI 依赖覆盖 ───────────────────────────────────


def _override_get_db():
    """每个请求使用独立的 SQLite 会话，测试结束后自动关闭"""
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


# ── 6. Fixtures ────────────────────────────────────────────


@pytest.fixture(autouse=True)
def setup_db():
    """每个测试前建表，测试后删表 — 保证测试之间互不影响"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    """提供一个直接的 DB 会话（用于 fixture 里创建测试数据）"""
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def reader(db_session):
    user = User(email="reader@test.com", password=hash_password("123456"), name="Reader", role=Role.READER)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def editor(db_session):
    user = User(email="editor@test.com", password=hash_password("123456"), name="Editor", role=Role.EDITOR)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def admin(db_session):
    user = User(email="admin@test.com", password=hash_password("123456"), name="Admin", role=Role.ADMIN)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture()
def category(db_session):
    cat = Category(name="AI工具", slug="ai-tools", description="AI 工具资讯")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)
    return cat


@pytest.fixture()
def tag(db_session):
    t = Tag(name="ChatGPT", slug="chatgpt")
    db_session.add(t)
    db_session.commit()
    db_session.refresh(t)
    return t


@pytest.fixture()
def article(db_session, editor, category):
    art = Article(
        title="测试文章",
        slug="test-article-001",
        content="<p>这是测试文章的内容</p>",
        summary="测试摘要",
        status=ArticleStatus.PUBLISHED,
        author_id=editor.id,
        category_id=category.id,
    )
    db_session.add(art)
    db_session.commit()
    db_session.refresh(art)
    return art


# ── 7. 辅助函数 ────────────────────────────────────────────


def auth_header(user: User) -> dict:
    """生成 Bearer token 请求头"""
    token = create_access_token(user.id, user.email, user.role.value)
    return {"Authorization": f"Bearer {token}"}


# 让测试文件可以直接 from conftest import auth_header
# 也支持 pytest 的 conftest 自动发现


from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    """FastAPI TestClient — 模拟 HTTP 请求"""
    return TestClient(app)
