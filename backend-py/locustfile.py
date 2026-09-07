"""
Locust 性能测试脚本

运行方式：
1. 安装 locust: pip install locust
2. 确保后端运行在 http://localhost:8003
3. 命令行模式: locust -f locustfile.py --headless -u 100 -r 10 --run-time 30s --host http://localhost:8003
4. Web UI 模式: locust -f locustfile.py --host http://localhost:8003
   然后打开 http://localhost:8089

参数说明：
  -u 100    模拟 100 个并发用户
  -r 10     每秒增加 10 个用户
  --run-time 30s  运行 30 秒
"""

from locust import HttpUser, task, between


class ArticleUser(HttpUser):
    wait_time = between(0.5, 2)

    @task(5)
    def list_articles(self):
        self.client.get("/api/articles/?page=1&page_size=20&sort=newest", name="/api/articles/")

    @task(3)
    def list_articles_popular(self):
        self.client.get("/api/articles/?page=1&page_size=20&sort=popular", name="/api/articles/ [popular]")

    @task(2)
    def search_articles(self):
        self.client.get("/api/articles/?q=AI&page=1&page_size=20", name="/api/articles/ [search]")

    @task(4)
    def get_article_detail(self):
        self.client.get("/api/articles/test-article-001", name="/api/articles/{slug}")

    @task(1)
    def list_categories(self):
        self.client.get("/api/categories/", name="/api/categories/")

    @task(1)
    def list_tags(self):
        self.client.get("/api/tags/", name="/api/tags/")

    @task(1)
    def health_check(self):
        self.client.get("/api/health", name="/api/health")
