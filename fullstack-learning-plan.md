# 全栈学习计划 + 资讯站项目完整方案

> 目标：通过做一个「AI工具 + 短剧制作」资讯站 + 后台管理系统，14 天学会全栈开发
> 环境：Windows | AI 工具：Qoder + Kiro | 已有技能：前端基础
> 学习方式：不读文档，用 AI 生成代码，读代码学概念

## 当前进度

| 天数 | 内容 | 状态 |
|---|---|---|
| 第 0 天 | 环境搭建 | ✅ 完成 |
| 第 1 天 | 后端项目初始化（FastAPI + SQLAlchemy + CRUD） | ✅ 完成 |
| 第 2 天 | Redis 缓存 + 会话管理 + 限流 | ✅ 完成 |
| 第 3 天 | 文件上传 + 图片处理 | ✅ 完成 |
| 第 4 天 | 搜索 + 分页优化 | ✅ 完成 |
| 第 5 天 | 后台管理系统后端 + RBAC | ✅ 完成 |
| 第 6 天 | 广告模块 + API 文档 + 后端总结 | ✅ 完成 |
| 第 7 天 | Docker 化 | ✅ 完成 |
| 第 8 天 | Nginx + HTTPS | ✅ 完成 |
| 第 9 天 | 单元测试（pytest + 覆盖率） | ✅ 完成 |
| 第 10 天 | E2E 测试（Playwright） | ✅ 完成 |
| 第 11 天 | 性能 + 安全测试 + SEO | ✅ 完成 |
| 第 12 天 | GitHub Actions CI/CD | ✅ 完成 |
| 第 13 天 | 部署上线 + ICP 备案 | 🔧 进行中 |
| 第 14 天 | 广告组件 + 项目总结 | ⬜ 待开始 |

---

## 一、项目定位

### 网站方向

**科技资讯站**，聚焦两个高搜索量赛道：

| 板块 | 占比 | 内容 |
|---|---|---|
| **AI 工具** | 60% | 工具教程（下载/安装/使用）、对比评测、提示词模板、行业资讯 |
| **短剧制作** | 30% | 制作教程、工具推荐、变现攻略、行业分析 |
| **专题** | 10% | "2026 AI 工具大全"、"零基础做短剧系列"、热点追踪 |

### 为什么选这两个方向

- **AI 工具**：搜索量暴涨（ChatGPT/Midjourney/Suno/可灵等），科技类广告单价高
- **短剧制作**：短剧行业爆发，竞争度还不算高，可接课程/工具推广
- 两个方向都有明确的变现路径（广告 + 工具推广 + 付费教程）

### 选题示例

```
AI 工具：
├── "Midjourney 下载安装完整教程 2026"
├── "Stable Diffusion 本地部署图文教程"
├── "Kimi 高级提示词模板大全（附案例）"
├── "2026 最好用的免费 AI 工具排名"
├── "ChatGPT vs Kimi vs 通义千问 对比"
└── "AI 短剧生成工具对比"

短剧制作：
├── "零基础做短剧 完整流程"
├── "短剧剪辑软件推荐"
├── "AI 一键生成短剧 教程"
├── "短剧 CPS 分销赚钱完整攻略"
└── "2026 短剧行业趋势分析"
```

### 变现模式

| 变现方式 | 说明 | 收益 | 启动条件 |
|---|---|---|---|
| 广告联盟 | 百度联盟 + 穿山甲 + 腾讯优量汇 | 千次展示 5-50 元 | 1000+ PV/天 |
| 工具推广（CPS） | 推广 AI 工具，按注册/付费分成 | 每单 10-100 元 | 有内容即可 |
| 付费教程 | 卖 AI 工具教程、短剧制作课 | 单课 99-499 元 | 有一定粉丝 |
| 直客广告 | 品牌广告 | 单条 500-5000 元 | 10000+ PV/天 |
| 付费社群 | 知识星球/微信群 | 年费 199-599 元 | 有稳定读者 |

### 变现路径

```
第 1 阶段（0-1000 PV/天）：做内容，不接广告，专注 SEO
第 2 阶段（1000-5000 PV/天）：接入百度联盟 + 工具推广
第 3 阶段（5000-20000 PV/天）：接入穿山甲 + 腾讯优量汇 + 付费教程
第 4 阶段（20000+ PV/天）：直客广告 + 付费社群
```

---

## 二、技术栈

```
前端（你已有）：
├── Vue 3（资讯站前台）
├── Vue 3 + Element Plus（后台管理系统）
└── Vite 构建

后端（要学的）：
├── Python + FastAPI
├── SQLAlchemy ORM + Alembic 迁移
├── MySQL（主数据库）
├── Redis（缓存 + 会话 + 限流）
├── JWT 认证
├── python-multipart（文件上传）
└── Pillow（图片处理）

运维（要学的）：
├── Docker + docker-compose
├── Nginx 反向代理
├── GitHub Actions CI/CD
└── Railway / 阿里云部署

测试（要学的）：
├── pytest（单元测试 + API 测试）
├── httpx（异步 API 测试客户端）
└── Playwright（E2E 测试）

SEO：
├── SSR / SSG（服务端渲染）
├── sitemap.xml + robots.txt + RSS
├── JSON-LD 结构化数据
└── Open Graph 标签
```

---

## 三、工具链（Windows 环境）

### 必装工具

| 工具 | 用途 | 安装方式 |
|---|---|---|
| **WSL2** | Docker 依赖 | `wsl --install`（PowerShell 管理员） |
| **Docker Desktop** | 容器化 | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Kiro** | AI 编程工具 | [kiro.dev](https://kiro.dev) |
| **DBeaver** | 数据库管理 | [dbeaver.io](https://dbeaver.io/download/) |
| **RedisInsight** | Redis 管理 | [redis.io/insight](https://redis.io/insight/) |
| **Bruno** | API 调试 | [usebruno.com](https://www.usebruno.com/) |
| **Git** | 版本控制 | [git-scm.com](https://git-scm.com/download/win) |
| **Node.js** | 前端构建 | [nodejs.org](https://nodejs.org/)（已有） |
| **Python** | 后端运行环境 | [python.org](https://www.python.org/)（3.11+） |

### 关于 JDK

**不需要装。** JDK 是给 Java/Spring Boot 后端用的。用 Python 就够了。

### 数据库和缓存

**不需要单独安装**，用 Docker 一条命令搞定：

```powershell
# 启动 MySQL
docker run -d --name news-mysql `
  -e MYSQL_ROOT_PASSWORD=root123 `
  -e MYSQL_USER=news `
  -e MYSQL_PASSWORD=news123 `
  -e MYSQL_DATABASE=news_db `
  -p 3306:3306 `
  -v news_mysqldata:/var/lib/mysql `
  mysql:8

# 启动 Redis
docker run -d --name news-redis `
  -p 6379:6379 `
  redis:7

# 验证
docker ps
docker exec -it news-redis redis-cli ping
```

### Windows 特有注意事项

| 事项 | Linux | Windows |
|---|---|---|
| PowerShell 换行 | `\` | `` ` `` |
| 文件路径 | `/` | `\` 或 `path.join()` |
| 环境变量 | `export VAR=value` | `$env:VAR = "value"` |
| 终端 | bash | PowerShell / Git Bash |

---

## 四、14 天详细学习计划

### 第 0 天：环境搭建（2-3 小时）

#### 步骤 1：安装 WSL2

打开 PowerShell（管理员）：

```powershell
wsl --install
```

安装完成后**重启电脑**。重启后验证：

```powershell
wsl --version
```

#### 步骤 2：安装 Docker Desktop

- 下载：[docker.com](https://www.docker.com/products/docker-desktop/)
- 安装时勾选 **"Use WSL 2 based engine"**
- 安装后打开 Docker Desktop，等待左下角状态变绿

#### 步骤 3：启动数据库和缓存

```powershell
# 创建项目目录
mkdir D:\projects\fullstack-news
cd D:\projects\fullstack-news

# 启动 MySQL
docker run -d --name news-mysql `
  -e MYSQL_ROOT_PASSWORD=root123 `
  -e MYSQL_USER=news `
  -e MYSQL_PASSWORD=news123 `
  -e MYSQL_DATABASE=news_db `
  -p 3306:3306 `
  -v news_mysqldata:/var/lib/mysql `
  mysql:8

# 启动 Redis
docker run -d --name news-redis `
  -p 6379:6379 `
  redis:7

# 验证
docker ps
docker exec -it news-redis redis-cli ping
```

#### 步骤 4：安装辅助工具

- 下载 [DBeaver](https://dbeaver.io/download/)，连接 MySQL
  - Host: `localhost`，Port: `3306`，Username: `news`，Password: `news123`，Database: `news_db`
- 下载 [RedisInsight](https://redis.io/insight/)，连接 Redis
  - Host: `localhost`，Port: `6379`
- 下载 [Bruno](https://www.usebruno.com/)
- 下载 [Kiro](https://kiro.dev)

#### 验证清单

- [ ] `docker ps` 显示两个容器运行中
- [ ] `docker exec -it news-redis redis-cli ping` 返回 PONG
- [ ] DBeaver 能连上 MySQL
- [ ] RedisInsight 能连上 Redis

---

### 第 1 天：后端项目初始化（3 小时） ✅

**目标：** 用 Qoder 生成资讯站后端骨架

**已完成：**
- [x] 项目骨架创建（FastAPI + SQLAlchemy + Alembic）
- [x] 数据模型定义（User, Article, Category, Tag, ArticleTag, Comment）
- [x] 三层架构（routes → services → models）
- [x] JWT 认证依赖注入
- [x] 统一异常处理
- [x] 所有 CRUD 接口验证通过

#### 创建项目

```powershell
mkdir D:\projects\fullstack-news\backend-py
cd D:\projects\fullstack-news\backend-py
```

#### Qoder Prompt

```
帮我创建一个科技资讯站的后端项目，技术栈：
- Python + FastAPI
- SQLAlchemy 2.0 ORM + Alembic 迁移
- MySQL（连接地址：mysql+pymysql://news:news123@localhost:3306/news_db）
- 项目结构：

backend-py/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── api/
│   │   ├── routes/
│   │   └── deps.py
│   ├── services/
│   ├── core/
│   └── utils/
├── alembic/
├── alembic.ini
├── requirements.txt
├── .env
└── .gitignore

数据库模型：
1. User（用户）：id, email, password, name, role(READER/EDITOR/ADMIN), avatar, created_at
2. Article（文章）：id, title, slug, content, summary, cover_image,
   status(DRAFT/PUBLISHED/ARCHIVED), view_count, author_id, category_id,
   created_at, updated_at
3. Category（分类）：id, name, slug, description
4. Tag（标签）：id, name, slug
5. ArticleTag（文章-标签关联）：article_id, tag_id
6. Comment（评论）：id, content, article_id, user_id, parent_id(嵌套评论), created_at

请生成所有文件的完整代码，并解释每个文件的作用和它们之间的调用关系。
```

#### 运行验证

```powershell
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

打开浏览器访问 `http://localhost:8000/docs` 确认 Swagger 文档正常。

#### 读懂重点

- `app/models/` — 所有 SQLAlchemy 模型定义和关联关系
- `app/main.py` — FastAPI 应用初始化、中间件注册、路由挂载
- `app/api/routes/` → `app/services/` → `app/models/` — 三层架构
- `app/api/deps.py` — JWT 认证依赖注入
- `app/core/exceptions.py` — 统一异常处理

---

### 第 2 天：Redis 缓存 + 会话管理（2 小时） ✅

**目标：** 理解 Redis 在资讯站中的应用

**已完成：**
- [x] 文章列表缓存（cache.py）
- [x] 文章详情缓存
- [x] JWT Token 黑名单（token_blacklist.py）
- [x] 接口限流（rate_limiter.py，每分钟 60 次）
- [x] 文章浏览量计数（view_counter.py，Redis INCR + 定时同步）

#### Qoder Prompt

```
基于昨天的资讯站项目，添加 Redis：
1. 文章列表缓存：热门分类的文章列表缓存 5 分钟
2. 文章详情缓存：按文章 ID 缓存，更新/删除时清除缓存
3. JWT 黑名单：退出登录时 token 存入 Redis，验证时检查黑名单
4. 接口限流：每个 IP 每分钟最多 60 次请求
5. 文章浏览量计数：用 Redis INCR 计数，定时同步到数据库
6. 热门搜索词缓存

Redis 连接地址：redis://localhost:6379

请生成代码并解释：
- Redis key 的命名规范
- 缓存策略（什么时候读缓存、什么时候写缓存、什么时候清缓存）
- 为什么用 Redis 而不是直接查数据库
```

#### 读懂重点

- `app/services/cache.py` — Redis 缓存封装
- `app/services/rate_limiter.py` — 限流服务
- `app/api/deps.py` — token 黑名单检查
- Redis key 命名：`article:list:category:{id}`, `article:detail:{id}`, `token:blacklist:{token}`

#### 验证

用 Bruno 连续请求同一接口，观察第二次请求是否明显更快。

---

### 第 3 天：文件上传 + 图片处理（2 小时）

**目标：** 理解文件上传流程

#### Qoder Prompt

```
给资讯站添加文件上传功能：
1. 用 python-multipart 处理文件上传
2. 上传文章封面图（限制 5MB，只允许 jpg/png/webp）
3. 上传用户头像
4. 图片存储到 uploads/ 目录
5. 用 Pillow 生成缩略图
6. 返回可访问的图片 URL
7. 配置 FastAPI 静态文件服务（StaticFiles）

注意：这是 Windows 系统，文件路径用 os.path.join 处理。

请生成代码并解释文件上传的完整流程：
浏览器 → python-multipart 解析 → 存储 → 返回 URL
```

#### 验证

用 Bruno 上传一张图片，确认返回的 URL 能在浏览器打开。

---

### 第 4 天：搜索 + 分页优化（2 小时） ✅

**目标：** 理解全文搜索和数据库分页

**已完成：**
- [x] 文章全文搜索（标题 + 内容 LIKE 模糊匹配）
- [x] 搜索结果分页
- [x] 热门搜索词缓存（Redis ZSET）
- [x] 高级筛选：分类、标签、作者、时间范围、排序（最新/最热）

#### Qoder Prompt

```
给资讯站添加搜索功能：
1. 文章搜索：按标题和内容模糊搜索（MySQL LIKE）
2. 搜索结果分页
3. 热门搜索词缓存（Redis）
4. 高级筛选：按分类、标签、作者、时间范围、排序（最新/最热）
5. 解释 MySQL LIKE 和全文索引（FULLTEXT）的区别

请生成代码并解释。
```

---

### 第 5 天：后台管理系统后端 + RBAC（3 小时） ✅

**目标：** 理解角色权限管理

**已完成：**
- [x] OperationLog 模型 + User 增加 is_active 字段
- [x] RBAC 权限：require_role() 依赖注入
- [x] Admin 管理后端：用户/文章/分类/标签/评论/统计/日志
- [x] 文章审核流程（DRAFT → PUBLISHED → ARCHIVED）
- [x] 批量操作接口
- [x] Admin 前端（Vue 3 + Element Plus）全部页面

#### Qoder Prompt

```
给资讯站添加后台管理系统的后端接口：
1. 角色权限（RBAC）：
   - ADMIN：管理用户、管理分类、管理所有文章、查看统计
   - EDITOR：管理自己的文章、查看评论
   - READER：阅读文章、发表评论
2. 权限中间件：检查用户角色是否有权限访问接口
3. 管理接口：
   - 用户管理：列表、禁用/启用、修改角色
   - 文章管理：审核（草稿→发布→归档）、批量操作
   - 分类管理、标签管理
   - 评论管理：删除、审核
   - 统计面板：文章总数、用户总数、今日新增、热门文章
4. 操作日志：记录管理员的每个操作

请生成代码并解释 RBAC 的实现方式。
```

#### 读懂重点

- `app/api/deps.py` — 角色权限检查（require_role）
- `app/api/routes/` — 管理接口
- `app/models/` — 操作日志模型

---

### 第 6 天：广告模块 + API 文档 + 后端总结（3 小时） ✅

**目标：** 添加广告管理模块，生成 API 文档

**已完成：**
- [x] AdSlot + AdStat 数据模型（枚举：位置/类型/平台/状态）
- [x] 广告位 CRUD 接口（ADMIN 权限）
- [x] 公开广告接口（按权重随机选择）
- [x] 广告事件上报（impression/click）
- [x] 广告统计接口（按天分组，修复 MySQL DATE_SUB 兼容性）
- [x] Swagger 文档增强：全局描述 + 7 个标签分组 + 44 个端点 summary
- [x] Bearer token 认证配置

#### Qoder Prompt（广告模块）

```
给资讯站后端添加广告管理模块：
1. AdSlot 模型：id, name, position(header/sidebar/infeed/inarticle/footer),
   type(banner/infeed/native), platform(baidu/pangle/tencent),
   code(广告代码), status(active/inactive), weight(权重)
2. 广告位 CRUD 接口
3. 广告展示统计：记录每次展示和点击
4. 广告位按权重随机分配
5. 广告位懒加载配置

请生成代码并解释。
```

#### Qoder Prompt（API 文档）

```
给资讯站后端完善 Swagger 文档：
1. FastAPI 自带 Swagger UI（/docs）和 ReDoc（/redoc）
2. 为所有接口添加 Pydantic schema 文档和响应示例
3. 配置 Bearer token 认证
4. 按模块分组（认证、文章、评论、管理、广告）

并帮我总结这个后端项目的完整架构图，
包括请求从进入到返回的完整流程。
```

#### 后端完成验证清单

- [x] 所有 CRUD 接口能调通
- [x] JWT 认证正常（注册→登录→带 token 访问）
- [x] Redis 缓存生效（第二次请求明显更快）
- [x] 文件上传正常
- [x] 搜索正常
- [x] RBAC 权限正常（不同角色访问不同接口）
- [x] 广告位管理正常
- [x] Swagger 文档能打开（`http://localhost:8000/docs`）

---

### 第 7 天：Docker 化（3 小时） ✅

**目标：** 理解 Docker 镜像、容器、Dockerfile

**已完成：**
- [x] Dockerfile 多阶段构建（builder + runtime，非 root 用户）
- [x] docker-compose.yml（app + mysql + redis，health check + depends_on）
- [x] .dockerignore 排除无关文件
- [x] entrypoint.sh 启动脚本（等待 MySQL → alembic 迁移 → uvicorn）
- [x] .env.example 环境变量模板
- [x] alembic/env.py 改为从环境变量读取数据库地址（Docker 网络用 mysql 而非 localhost）
- [x] 三个容器全部启动验证通过，健康检查正常

#### Qoder Prompt

```
帮我把资讯站后端项目 Docker 化：
1. 编写 Dockerfile（多阶段构建：构建阶段 + 运行阶段）
2. 编写 docker-compose.yml，包含：
   - app（Python + FastAPI 应用）
   - mysql（数据库）
   - redis（缓存）
   - 数据持久化（volume）
   - 网络（同一网络内互相访问）
3. 编写 .dockerignore
4. 编写启动脚本：先运行 alembic upgrade head，再启动 uvicorn
5. 编写 .env.example 和 .env 配置
6. 解释 Dockerfile 每一行的作用
7. 解释 docker-compose 每个配置项的作用

请生成所有文件并详细解释。
```

#### 运行验证

```powershell
cd D:\projects\fullstack-news\backend-py
docker-compose up -d --build
```

访问 `http://localhost:8000/docs` 验证。

---

### 第 8 天：Nginx + HTTPS（2 小时） ✅

**目标：** 理解反向代理、SSL 证书

**已完成：**
- [x] nginx.conf 反向代理配置（/api/ → app:8000）
- [x] 自签名 SSL 证书（openssl 生成，CN=localhost，365 天有效）
- [x] HTTP → HTTPS 自动跳转（301）
- [x] Gzip 压缩（JSON/CSS/JS/SVG 等，level 6）
- [x] 安全响应头（X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy）
- [x] SSL/TLS 配置（TLSv1.2+，强加密套件，session cache）
- [x] 静态文件服务（/uploads/ 由 Nginx 直接返回，30 天缓存）
- [x] 请求体大小限制（client_max_body_size 10M）
- [x] Nginx 加入 docker-compose（4 容器：mysql + redis + app + nginx）
- [x] Windows 端口适配（8080→80, 8443→443，因 80/443 被系统保留）
- [x] 前端 Vite 代理更新（admin + frontend → https://localhost:8443）
- [x] Let's Encrypt ACME 路径预留（生产环境自动续期证书）

#### Qoder Prompt

```
帮我配置 Nginx：
1. 编写 nginx.conf，反向代理到 FastAPI 应用（端口 8000）
2. 配置 gzip 压缩
3. 配置静态资源缓存（图片、CSS、JS）
4. 配置 HTTPS（本地自签名证书，生产用 certbot）
5. 配置请求体大小限制（文件上传需要）
6. 把 Nginx 加入 docker-compose
7. 解释反向代理的工作原理：
   用户请求 → Nginx(80/443) → Uvicorn(8000)

请生成所有配置文件并解释。
```

---

### 第 9 天：单元测试（3 小时）

**目标：** 理解单元测试、Mock、断言

#### Qoder Prompt

```
给资讯站后端写完整的单元测试：
1. 使用 pytest + httpx
2. 测试所有 API 接口：
   - 认证：注册、登录、无 token 访问、过期 token
   - 文章：创建、编辑、删除、列表（分页/排序/筛选）、详情
   - 评论：发表、嵌套评论、删除
   - 管理：不同角色的权限测试
   - 广告：广告位获取
3. 使用测试数据库（每次测试前清空）
4. 测试覆盖率目标 > 80%
5. 解释每个测试用例的目的

请生成所有测试文件并解释。
```

#### 运行

```powershell
pytest
pytest --cov=app --cov-report=term-missing
```

---

### 第 10 天：E2E 测试（2 小时）

**目标：** 理解端到端测试

#### Qoder Prompt

```
给资讯站写 E2E 测试：
1. 使用 Playwright
2. 测试完整用户流程：
   - 读者：注册 → 登录 → 浏览文章 → 发表评论
   - 编辑：登录 → 创建文章 → 编辑 → 发布
   - 管理员：登录 → 审核文章 → 管理用户 → 查看统计
3. 测试错误流程：
   - 密码错误登录失败
   - 无权限访问管理接口
   - 提交空表单报错

请生成测试文件并解释。
```

---

### 第 11 天：性能 + 安全测试 + SEO（3 小时）

**目标：** 性能测试、安全加固、SEO 支持

#### Qoder Prompt（性能 + 安全）

```
给资讯站添加：
1. 性能测试：用 locust 测试文章列表接口的 QPS
2. 安全测试：
   - SQL 注入测试（在搜索框输入恶意 SQL）
   - XSS 测试（在评论内容中输入 <script>）
   - 认证绕过测试
   - 文件上传漏洞测试
3. 安全加固：
   - 安全响应头（X-Content-Type-Options, X-Frame-Options 等）
   - CORS 白名单
   - 输入消毒（sanitize）
   - 密码强度校验

请生成代码并解释。
```

#### Qoder Prompt（SEO）

```
给资讯站添加完整的 SEO 支持：

后端：
1. 每篇文章自动生成：
   - SEO 标题（title）：包含关键词，不超过 60 字符
   - SEO 描述（description）：不超过 160 字符
   - 关键词（keywords）
   - JSON-LD 结构化数据（Article schema）
   - Open Graph 标签
2. 自动生成 sitemap.xml
3. 自动生成 robots.txt
4. RSS 订阅（feed.xml）
5. 文章 URL 用 slug（如 /article/midjourney-tutorial-2026）
6. 面包屑导航

前端：
1. SSR 或 SSG（服务端渲染，百度爬虫需要）
2. 每篇文章页面独立的 meta 标签
3. 图片懒加载 + alt 属性
4. 页面加载速度优化

请生成所有代码并解释。
```

---

### 第 12 天：GitHub Actions CI/CD（2 小时）

**目标：** 理解 CI/CD 流程

#### Qoder Prompt

```
帮我创建 GitHub Actions CI/CD：
1. 代码推送时自动运行：
   - pip install
   - Ruff 代码检查
   - pytest 运行测试
   - 构建 Docker 镜像
2. 推送到 GitHub Container Registry
3. 自动部署到 Railway
4. 使用 GitHub Secrets 管理环境变量
5. 解释 workflow 每个步骤

请生成 .github/workflows/ci.yml 并解释。
```

---

### 第 13 天：部署上线 + ICP 备案（3 小时）

**目标：** 将项目部署到真实服务器

#### 方案 A：Railway（最简单）

Qoder Prompt：
```
帮我把资讯站部署到 Railway：
1. 项目配置
2. 环境变量设置
3. MySQL 和 Redis 配置
4. 给出详细的部署步骤（从注册 Railway 到项目上线）
```

#### 方案 B：阿里云（更完整）

Qoder Prompt：
```
帮我把资讯站部署到阿里云服务器：
1. 服务器选购建议（配置、价格）
2. 服务器初始化（安装 Docker、docker-compose、Nginx）
3. 用 docker-compose 部署项目
4. 配置域名 + HTTPS
5. 配置自动更新（git pull + docker-compose up）
6. 配置日志收集
7. 给出完整的部署命令
```

#### ICP 备案

- 在阿里云/腾讯云提交备案申请
- 需要域名 + 服务器
- 审核时间：7-15 天
- 备案通过后才能接入国内广告平台

---

### 第 14 天：广告组件 + 项目总结（3 小时）

**目标：** 添加广告组件，总结项目

#### Qoder Prompt（广告组件）

```
帮我在资讯站前台添加广告位组件：
1. 创建 AdSlot.vue 组件，支持以下广告类型：
   - banner（横幅 728x90）
   - infeed（信息流，插在文章列表中）
   - inarticle（文中，插在文章第 3 段后）
   - sidebar（侧边栏 300x250 / 300x600）
2. 支持懒加载（IntersectionObserver，广告位进入可视区域才加载）
3. 支持广告位配置（从后端接口获取广告代码）
4. 广告加载失败时显示占位符
5. 支持按权重随机展示不同平台的广告

请生成代码并解释。
```

#### Qoder Prompt（项目总结）

```
帮我总结这个资讯站项目的完整架构：
1. 画出系统架构图（文字描述）
2. 列出所有技术栈和它们的作用
3. 列出所有学到的后端/运维/测试知识点
4. 列出可以优化的方向
5. 列出下一步的内容运营计划
```

---

## 五、广告平台接入指南

### 国内主流广告平台

| 平台 | 适合场景 | 收益水平 | 门槛 | 推荐度 |
|---|---|---|---|---|
| **百度联盟** | 内容站、搜索流量 | 千次展示 5-30 元 | 备案 + 日均 1000PV | 最先接 |
| **穿山甲（字节）** | 信息流、视频内容 | 千次展示 15-50 元 | 备案 + 日均 5000PV | 收益最高 |
| **腾讯优量汇** | 综合流量 | 千次展示 10-40 元 | 备案 + 企业资质优先 | 补充 |
| **阿里妈妈** | 电商导购内容 | CPS 分成 | 门槛低 | 有带货内容时 |
| **360 广告联盟** | 综合内容 | 较低 | 门槛低 | 备选 |

### 接入前提

| 条件 | 说明 | 怎么办 |
|---|---|---|
| ICP 备案 | 所有国内广告平台都要求 | 阿里云/腾讯云免费备案，7-15 天 |
| 域名 | 已备案域名 | 阿里云/腾讯云购买 |
| 日均流量 | 百度联盟 1000PV，穿山甲 5000PV | 初期先用门槛低的 |
| 内容合规 | 无违规内容 | 资讯站天然合规 |

### 广告位布局

```
┌─────────────────────────────────────────────────┐
│  顶部横幅广告（728x90）                  百度联盟  │
├─────────────────────────────────────────────────┤
│  文章列表                        │  侧边栏广告    │
│  ┌─────────────────────┐      │  (300x250)    │
│  │ 文章1               │      │  腾讯优量汇    │
│  ├─────────────────────┤      ├──────────────┤
│  │ 信息流广告（原生）     │      │  侧边栏广告2   │
│  │                     │      │  (300x600)   │
│  ├─────────────────────┤      │  穿山甲       │
│  │ 文章2               │      ├──────────────┤
│  ├─────────────────────┤      │  粘性广告     │
│  │ 文章3               │      │  (跟随滚动)   │
│  └─────────────────────┘      │              │
├─────────────────────────────────────────────────┤
│  文章详情页                                      │
│  文章标题                                        │
│  文章内容...                                     │
│  ┌─────────────────────────────────────┐       │
│  │ 文中广告（第3段后）        穿山甲      │       │
│  └─────────────────────────────────────┘       │
│  文章内容继续...                                  │
│  ┌─────────────────────────────────────┐       │
│  │ 文末广告                   百度联盟   │       │
│  └─────────────────────────────────────┘       │
├─────────────────────────────────────────────────┤
│  底部横幅广告（728x90）              腾讯优量汇   │
└─────────────────────────────────────────────────┘
```

### 广告位优先级（按收益排序）

| 广告位 | 位置 | 收益 | 推荐平台 |
|---|---|---|---|
| 文中信息流 | 文章第 3 段后 | 最高 | 穿山甲 |
| 文末推荐 | 文章底部 | 高 | 百度联盟 |
| 列表信息流 | 每 5 篇文章插 1 条 | 高 | 穿山甲 |
| 侧边栏 | 右侧固定 | 中等 | 腾讯优量汇 |
| 顶部横幅 | 页面顶部 | 较低 | 百度联盟 |
| 底部横幅 | 页面底部 | 最低 | 腾讯优量汇 |

### 广告代码示例

```html
<!-- 百度联盟 -->
<script type="text/javascript">
  var cpro_id = "u1234567";
</script>
<script type="text/javascript"
  src="https://cpro.baidustatic.com/cpro/ui/c.js"></script>

<!-- 腾讯优量汇 -->
<script async
  src="https://qzs.qq.com/qzone/biz/gdt/mod/gdt_loader.js"></script>
<div id="gdt_ad_container" data-ad-slot="1234567890"></div>

<!-- 穿山甲 -->
<script src="https://lf-cdn-tos.bytescm.com/obj/union-fe/union/js/pangle.js">
</script>
<div id="pangle_ad" data-slot="1234567890"></div>
```

---

## 六、SEO 策略

### 核心原则

**写用户会搜索的内容，不是你想写的内容。**

### 关键词策略

```
高搜索量 + 低竞争 = 优先写
高搜索量 + 高竞争 = 后期写
低搜索量 + 低竞争 = 凑数写
低搜索量 + 高竞争 = 不写
```

工具：5118、百度关键词规划师、百度下拉框

### 标题公式

```
"{工具名} + {动作} + {教程/指南/方法} + {年份}"

示例：
- "Midjourney 下载安装完整教程 2026"
- "AI 短剧制作零基础入门指南"
- "Kimi 高级提示词模板大全（附案例）"
- "免费 AI 绘画工具推荐 2026（亲测有效）"
- "短剧 CPS 分销赚钱完整攻略"
```

### 技术 SEO 清单

- [ ] 每篇文章有独立的 title、description、keywords
- [ ] JSON-LD 结构化数据（Article schema）
- [ ] Open Graph 标签（社交分享）
- [ ] sitemap.xml 自动更新
- [ ] robots.txt 正确配置
- [ ] RSS 订阅
- [ ] 文章 URL 用 slug（语义化）
- [ ] 面包屑导航
- [ ] 图片有 alt 属性
- [ ] 页面加载速度 < 3 秒
- [ ] 移动端适配

### 内容发布节奏

| 阶段 | 频率 | 内容类型 |
|---|---|---|
| 第 1-2 个月 | 每天 2-3 篇 | 工具教程、使用指南（长尾词） |
| 第 3-4 个月 | 每天 1-2 篇 | 对比评测、行业分析（中腰部词） |
| 第 5-6 个月 | 每天 1 篇 | 深度专题、系列教程（头部词） |
| 6 个月后 | 每周 3-5 篇 | 维护更新 + 新热点 |

**前 3 个月至少积累 100-200 篇高质量文章，百度才会开始收录。**

### 内容生产流程（用 AI 辅助）

```
1. 找关键词 → 5118 / 百度下拉框 / Qoder
2. 让 Qoder 生成文章大纲
3. 让 Qoder 生成文章初稿
4. 你审核修改（加入实操截图、个人经验）
5. 发布
```

#### 文章生成 Qoder Prompt 示例

```
帮我写一篇关于 "Midjourney 下载安装教程 2026" 的文章：
1. 标题要包含关键词
2. 文章结构：
   - 什么是 Midjourney
   - 注册流程（图文步骤）
   - 订阅方案对比
   - 基础使用方法
   - 常见问题解答
3. 每个步骤都要详细
4. 在合适的位置标注 [图片：步骤X截图]
5. 文章结尾加相关推荐
6. 生成 SEO 标题、描述、关键词
```

---

## 七、收益预估

| 日均 PV | 百度联盟 | 穿山甲 | 腾讯优量汇 | 月收益估算 |
|---|---|---|---|---|
| 1,000 | 5-15 元/天 | - | 3-10 元/天 | 240-750 元 |
| 10,000 | 50-150 元/天 | 80-200 元/天 | 30-100 元/天 | 4,800-13,500 元 |
| 50,000 | 250-750 元/天 | 400-1000 元/天 | 150-500 元/天 | 24,000-67,500 元 |
| 100,000+ | 500-1500 元/天 | 800-2000 元/天 | 300-1000 元/天 | 48,000-135,000 元 |

> 以上为估算，实际收益取决于内容质量、用户画像、广告位布局。

---

## 八、14 天时间线总览

```
第 0 天    → 环境搭建（WSL2 + Docker + MySQL + Redis + 辅助工具）
第 1 天    → 后端骨架（FastAPI + SQLAlchemy + 数据模型 + CRUD）
第 2 天    → Redis 缓存 + 会话 + 限流
第 3 天    → 文件上传 + 图片处理
第 4 天    → 搜索 + 分页
第 5 天    → 后台管理后端（RBAC 权限）
第 6 天    → 广告模块 + API 文档 + 后端总结
第 7 天    → Docker 化
第 8 天    → Nginx + HTTPS
第 9 天    → GitHub Actions CI/CD
第 10 天   → 部署上线 + ICP 备案
第 11 天   → 单元测试
第 12 天   → E2E 测试
第 13 天   → 性能 + 安全 + SEO
第 14 天   → 前端对接 + 广告组件 + 项目总结
```

**总计约 40 小时，按每天 2-3 小时，14 天完成。**

---

## 九、核心原则

1. **不读文档** — 所有知识通过 Qoder 生成的代码来理解
2. **不装 JDK** — 用 Python 就够了
3. **数据库用 Docker 跑** — 不用单独安装
4. **Redis 必学** — 缓存、会话、限流都离不开
5. **项目驱动** — 资讯站 + 后台管理系统覆盖所有知识点
6. **每个功能都跑通** — 代码能跑通才算学会
7. **技术用 AI 搞定，精力放在选题 + SEO + 内容质量上**
8. **前 3-6 个月别指望广告赚钱** — 先做内容和流量

---

## 十、项目文件结构（最终版）

```
fullstack-news/
├── backend-py/                  # 后端（Python + FastAPI）
│   ├── app/
│   │   ├── main.py              # FastAPI 应用入口
│   │   ├── config.py            # 配置管理
│   │   ├── database.py          # 数据库连接
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── article.py
│   │   │   ├── category.py
│   │   │   ├── comment.py
│   │   │   └── ad.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── article.py
│   │   │   ├── category.py
│   │   │   ├── comment.py
│   │   │   ├── ad.py
│   │   │   └── common.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── article.py
│   │   │   │   ├── comment.py
│   │   │   │   ├── category.py
│   │   │   │   ├── admin.py
│   │   │   │   └── ad.py
│   │   │   └── deps.py          # 依赖注入（认证、权限）
│   │   ├── services/
│   │   │   ├── cache.py
│   │   │   ├── rate_limiter.py
│   │   │   ├── token_blacklist.py
│   │   │   └── view_counter.py
│   │   ├── core/
│   │   │   └── exceptions.py
│   │   └── utils/
│   │       └── jwt.py
│   ├── alembic/                 # 数据库迁移
│   ├── uploads/                 # 上传文件
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── nginx.conf
│   ├── .github/
│   │   └── workflows/
│   │       └── ci.yml
│   ├── .env
│   ├── .env.example
│   ├── .gitignore
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/                   # 资讯站前台
│   ├── src/
│   │   ├── components/
│   │   │   └── AdSlot.vue
│   │   ├── pages/
│   │   ├── layouts/
│   │   └── ...
│   └── ...
│
└── admin/                      # 后台管理系统
    ├── src/
    │   ├── views/
    │   │   ├── ArticleManage.vue
    │   │   ├── CategoryManage.vue
    │   │   ├── CommentManage.vue
    │   │   ├── UserManage.vue
    │   │   ├── AdManage.vue
    │   │   └── Dashboard.vue
    │   ├── components/
    │   ├── router/
    │   ├── api/
    │   └── ...
    └── ...
```
