# AI 资讯站 (Fullstack News)

科技资讯站全栈项目 — 聚焦 AI 工具教程与短剧制作，支持文章发布、评论互动、广告管理、后台管理等完整功能。

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **后端** | Python 3.11 + FastAPI | RESTful API，自动 Swagger 文档 |
| **ORM** | SQLAlchemy 2.0 + Alembic | 数据库模型 + 迁移管理 |
| **数据库** | MySQL 8.0 | 主存储，支持全文搜索 |
| **缓存** | Redis 7 | 缓存 / 会话 / 限流 / 浏览量计数 |
| **前台** | Vue 3 + TypeScript + Vite | 资讯站前端，Pinia 状态管理 |
| **后台** | Vue 3 + Element Plus + ECharts | 管理面板，数据可视化 |
| **测试** | pytest + Playwright | 111 个单元测试 + E2E 测试 |
| **容器化** | Docker + docker-compose | 多阶段构建，4 容器编排 |
| **反向代理** | Nginx | HTTPS / Gzip / 静态资源缓存 |
| **CI/CD** | Gitee Go | 自动 lint + test + deploy |
| **部署** | Railway | 自动从 Git 仓库构建部署 |

## 项目结构

```
fullstack-news/
├── backend-py/                  # 后端 (FastAPI)
│   ├── app/
│   │   ├── main.py              # 应用入口
│   │   ├── config.py            # 配置管理 (环境变量)
│   │   ├── database.py          # 数据库连接
│   │   ├── models/              # SQLAlchemy 数据模型
│   │   │   ├── user.py          #   用户 (READER/EDITOR/ADMIN)
│   │   │   ├── article.py       #   文章 (DRAFT/PUBLISHED/ARCHIVED)
│   │   │   ├── category.py      #   分类
│   │   │   ├── tag.py           #   标签
│   │   │   ├── comment.py       #   评论 (支持嵌套)
│   │   │   ├── ad.py            #   广告位 + 广告统计
│   │   │   └── operation_log.py #   操作日志
│   │   ├── schemas/             # Pydantic 请求/响应模型
│   │   ├── api/
│   │   │   ├── routes/          # API 路由 (9 个模块)
│   │   │   │   ├── auth.py      #   注册/登录/登出
│   │   │   │   ├── article.py   #   文章 CRUD + 搜索 + 分页
│   │   │   │   ├── comment.py   #   评论 CRUD
│   │   │   │   ├── category.py  #   分类管理
│   │   │   │   ├── tag.py       #   标签管理
│   │   │   │   ├── ad.py        #   广告展示 + 事件上报
│   │   │   │   ├── admin.py     #   后台管理 (用户/文章/统计/日志)
│   │   │   │   └── seo.py       #   sitemap/robots.txt/RSS
│   │   │   └── deps.py          # 依赖注入 (JWT认证/RBAC权限)
│   │   ├── services/            # 业务逻辑层
│   │   │   ├── cache.py         #   Redis 缓存封装
│   │   │   ├── rate_limiter.py  #   IP 限流 (60次/分钟)
│   │   │   ├── token_blacklist.py # Token 黑名单
│   │   │   └── view_counter.py  #   浏览量计数 (Redis INCR)
│   │   └── core/
│   │       ├── security.py      # 密码哈希 + JWT
│   │       ├── sanitizer.py     # 输入消毒 (防 XSS)
│   │       ├── security_headers.py # 安全响应头
│   │       └── exceptions.py    # 统一异常处理
│   ├── alembic/                 # 数据库迁移
│   ├── tests/                   # 单元测试 (111 个)
│   ├── nginx/                   # Nginx 配置 + SSL 证书
│   ├── Dockerfile               # 多阶段构建
│   ├── docker-compose.yml       # 4 容器编排
│   ├── entrypoint.sh            # 启动脚本 (迁移 + 启动)
│   └── requirements.txt
│
├── frontend/                    # 前台 (Vue 3)
│   ├── src/
│   │   ├── views/               # 页面视图
│   │   │   ├── HomeView.vue     #   首页 (文章列表 + 分页)
│   │   │   ├── ArticleView.vue  #   文章详情 + 评论
│   │   │   ├── SearchView.vue   #   搜索结果
│   │   │   └── LoginView.vue    #   登录/注册
│   │   ├── components/          # 通用组件
│   │   │   ├── SiteHeader.vue   #   导航栏
│   │   │   ├── SiteFooter.vue   #   页脚
│   │   │   ├── ArticleCard.vue  #   文章卡片
│   │   │   ├── CommentSection.vue # 评论区
│   │   │   ├── Pagination.vue   #   分页
│   │   │   └── AdSlot.vue       #   广告位 (懒加载)
│   │   ├── api/                 # API 请求封装
│   │   ├── stores/              # Pinia 状态管理
│   │   ├── composables/         # 组合式函数 (SEO 等)
│   │   └── router/              # 路由配置
│   └── vite.config.ts
│
├── admin/                       # 后台管理 (Vue 3 + Element Plus)
│   ├── src/
│   │   ├── views/               # 管理页面
│   │   │   ├── DashboardView.vue    # 统计面板 (ECharts)
│   │   │   ├── ArticleListView.vue  # 文章管理
│   │   │   ├── ArticleFormView.vue  # 文章编辑
│   │   │   ├── UserListView.vue     # 用户管理
│   │   │   ├── CommentListView.vue  # 评论管理
│   │   │   ├── CategoryListView.vue # 分类管理
│   │   │   ├── TagListView.vue      # 标签管理
│   │   │   ├── AdManageView.vue     # 广告管理
│   │   │   └── LogListView.vue      # 操作日志
│   │   ├── layouts/             # 管理布局 (侧边栏 + 顶栏)
│   │   ├── api/                 # API 请求封装
│   │   └── router/              # 路由配置 (含权限守卫)
│   └── vite.config.ts
│
├── e2e/                         # E2E 测试 (Playwright)
│   ├── specs/
│   │   ├── admin.spec.ts        # 后台管理 E2E
│   │   └── frontend.spec.ts     # 前台 E2E
│   └── playwright.config.ts
│
├── .gitee/pipelines/            # Gitee Go CI/CD 流水线
├── .gitignore
└── fullstack-learning-plan.md   # 14 天学习计划
```

## 功能模块

### 用户端 (前台)

- 文章浏览：首页列表、分类筛选、分页、排序（最新/最热）
- 全文搜索：标题 + 内容模糊匹配，热门搜索词缓存
- 文章详情：Markdown 渲染、浏览量统计、相关推荐
- 评论系统：发表评论、嵌套回复
- 用户认证：注册、登录、JWT Token
- SEO：sitemap.xml、robots.txt、RSS 订阅、JSON-LD 结构化数据、Open Graph
- 广告位：banner / 信息流 / 文中广告，IntersectionObserver 懒加载

### 管理端 (后台)

- 统计面板：文章/用户/评论总数、今日新增、热门文章图表
- 文章管理：创建/编辑/审核/发布/归档、批量操作
- 用户管理：列表、禁用/启用、角色修改 (READER/EDITOR/ADMIN)
- 评论管理：查看/删除、审核
- 分类/标签管理：CRUD
- 广告管理：广告位 CRUD、展示统计、事件上报 (impression/click)
- 操作日志：记录所有管理员操作

### 安全特性

- JWT 认证 + RBAC 三级角色权限
- 密码强度校验 (8+ 字符，含字母和数字)
- 输入消毒 (防 XSS)
- 安全响应头 (X-Frame-Options, CSP, HSTS 等)
- CORS 白名单
- IP 限流 (60 次/分钟)
- Token 黑名单 (登出失效)
- 文件上传校验 (类型/大小限制)

## 快速开始

### 前置条件

- Python 3.11+
- Node.js 18+
- Docker Desktop (用于 MySQL + Redis)
- Git

### 1. 克隆项目

```bash
git clone https://gitee.com/yte19850503/fullstack-news.git
cd fullstack-news
```

### 2. 启动数据库

```bash
# MySQL
docker run -d --name news-mysql \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_USER=news \
  -e MYSQL_PASSWORD=news123 \
  -e MYSQL_DATABASE=news_db \
  -p 3306:3306 \
  mysql:8

# Redis
docker run -d --name news-redis -p 6379:6379 redis:7
```

### 3. 启动后端

```bash
cd backend-py

# 创建虚拟环境
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # Mac/Linux

# 安装依赖
pip install -r requirements.txt

# 复制环境变量
cp .env.example .env

# 数据库迁移
alembic upgrade head

# 启动服务
uvicorn app.main:app --reload
```

后端运行在 `http://localhost:8000`，API 文档在 `http://localhost:8000/docs`

### 4. 启动前台

```bash
cd frontend
npm install
npm run dev
```

前台运行在 `http://localhost:5173`

### 5. 启动后台管理

```bash
cd admin
npm install
npm run dev
```

后台运行在 `http://localhost:5174`

### 默认账号

| 角色 | 邮箱 | 密码 |
|------|------|------|
| 管理员 | admin@news.com | Admin1234 |
| 编辑 | editor@news.com | Editor1234 |
| 读者 | reader@news.com | Reader1234 |

## Docker 一键部署

```bash
cd backend-py
docker-compose up -d --build
```

启动 4 个容器：

| 容器 | 端口 | 说明 |
|------|------|------|
| mysql | 3306 | MySQL 8.0 数据库 |
| redis | 6379 | Redis 7 缓存 |
| app | 8000 | FastAPI 应用 |
| nginx | 8080/8443 | Nginx 反向代理 (HTTP/HTTPS) |

## 测试

### 单元测试 (111 个)

```bash
cd backend-py
pip install -r requirements-dev.txt

# 运行所有测试
pytest tests/ -v

# 覆盖率报告
pytest tests/ --cov=app --cov-report=term-missing
```

测试使用 SQLite 内存库 + FakeRedis，无需外部依赖。

### E2E 测试

```bash
cd e2e
npm install
npx playwright install chromium
npx playwright test
```

### 代码检查

```bash
cd backend-py
ruff check backend-py/
ruff format --check backend-py/
```

## API 概览

共 44+ 个 API 端点，按模块分组：

| 模块 | 前缀 | 说明 |
|------|------|------|
| 认证 | `/api/auth/` | 注册、登录、登出 |
| 文章 | `/api/articles/` | CRUD、搜索、分页、筛选 |
| 评论 | `/api/comments/` | CRUD、嵌套评论 |
| 分类 | `/api/categories/` | CRUD |
| 标签 | `/api/tags/` | CRUD |
| 广告 | `/api/ads/` | 获取广告、上报事件 |
| 管理 | `/api/admin/` | 用户/文章/评论/统计/日志管理 |
| SEO | `/api/seo/` | sitemap.xml、robots.txt、RSS |

完整文档：启动后端后访问 `http://localhost:8000/docs`

## CI/CD

使用 Gitee Go 流水线，push 到 main 分支自动触发：

```
push → lint (Ruff) → test (pytest) → build (Docker) → deploy (Railway)
```

配置文件：`.gitee/pipelines/pipeline.yml`

## 架构设计

```
浏览器
  │
  ▼
Nginx (反向代理 + HTTPS + Gzip + 静态资源)
  │
  ├── /api/*  →  FastAPI (Uvicorn :8000)
  │                │
  │                ├── routes  →  services  →  models  →  MySQL
  │                │                │
  │                │                └── Redis (缓存/限流/会话)
  │                │
  │                └── JWT 认证 + RBAC 权限
  │
  └── /uploads/*  →  静态文件 (30天缓存)
```

请求流程：
1. 用户请求 → Nginx 接收
2. Nginx 反向代理到 FastAPI
3. `deps.py` 验证 JWT Token + 检查角色权限
4. `routes` 接收请求，调用 `services`
5. `services` 查 Redis 缓存，未命中则查 MySQL
6. 结果写入 Redis 缓存，返回响应

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | MySQL 连接地址 | `mysql+pymysql://news:news123@localhost:3306/news_db` |
| `REDIS_URL` | Redis 连接地址 | `redis://localhost:6379` |
| `SECRET_KEY` | 应用密钥 | 随机生成 |
| `JWT_SECRET_KEY` | JWT 签名密钥 | 随机生成 |
| `JWT_ALGORITHM` | JWT 算法 | `HS256` |
| `JWT_EXPIRE_MINUTES` | Token 过期时间 | `1440` (24小时) |
| `ENVIRONMENT` | 运行环境 | `development` |
| `CORS_ORIGINS` | CORS 允许的源 | `*` |

## 开发进度

14 天学习计划，Day 0-12 已完成，Day 13-14 进行中。

| 天数 | 内容 | 状态 |
|------|------|------|
| Day 0 | 环境搭建 | ✅ |
| Day 1 | 后端初始化 (FastAPI + SQLAlchemy + CRUD) | ✅ |
| Day 2 | Redis 缓存 + 会话 + 限流 | ✅ |
| Day 3 | 文件上传 + 图片处理 | ✅ |
| Day 4 | 搜索 + 分页优化 | ✅ |
| Day 5 | 后台管理 + RBAC 权限 | ✅ |
| Day 6 | 广告模块 + API 文档 | ✅ |
| Day 7 | Docker 化 | ✅ |
| Day 8 | Nginx + HTTPS | ✅ |
| Day 9 | 单元测试 (pytest) | ✅ |
| Day 10 | E2E 测试 (Playwright) | ✅ |
| Day 11 | 性能 + 安全测试 + SEO | ✅ |
| Day 12 | CI/CD (Gitee Go) | ✅ |
| Day 13 | 部署上线 | 🔄 |
| Day 14 | 广告组件 + 项目总结 | ⬜ |

## License

MIT
