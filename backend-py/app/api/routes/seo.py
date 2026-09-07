from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.article import Article, ArticleStatus

router = APIRouter(tags=["seo"])

SITE_URL = "https://localhost"
SITE_NAME = "AI 资讯站"
SITE_DESCRIPTION = "聚焦 AI 工具、短剧资讯的科技新闻平台"


@router.get("/robots.txt", summary="robots.txt")
def robots_txt():
    content = f"""User-agent: *
Allow: /
Disallow: /api/admin/
Disallow: /login

Sitemap: {SITE_URL}/sitemap.xml
"""
    from fastapi.responses import PlainTextResponse

    return PlainTextResponse(content)


@router.get("/sitemap.xml", summary="sitemap.xml")
def sitemap_xml(db: Session = Depends(get_db)):
    articles = (
        db.query(Article)
        .filter(Article.status == ArticleStatus.PUBLISHED)
        .order_by(Article.created_at.desc())
        .limit(1000)
        .all()
    )

    urls = [
        _url_entry(SITE_URL, changefreq="daily", priority="1.0"),
        _url_entry(f"{SITE_URL}/search", changefreq="weekly", priority="0.6"),
    ]

    for a in articles:
        lastmod = a.updated_at or a.created_at
        urls.append(
            _url_entry(
                f"{SITE_URL}/article/{a.slug}",
                lastmod=lastmod.strftime("%Y-%m-%d") if lastmod else None,
                changefreq="weekly",
                priority="0.8",
            )
        )

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "\n".join(urls)
    xml += "\n</urlset>"

    from fastapi.responses import Response

    return Response(content=xml, media_type="application/xml")


@router.get("/rss.xml", summary="RSS 订阅")
def rss_feed(db: Session = Depends(get_db)):
    articles = (
        db.query(Article)
        .filter(Article.status == ArticleStatus.PUBLISHED)
        .order_by(Article.created_at.desc())
        .limit(20)
        .all()
    )

    items_xml = []
    for a in articles:
        pub_date = ""
        if a.created_at:
            pub_date = a.created_at.strftime("%a, %d %b %Y %H:%M:%S +0800")

        summary = a.summary or ""
        items_xml.append(f"""    <item>
      <title><![CDATA[{a.title}]]></title>
      <link>{SITE_URL}/article/{a.slug}</link>
      <guid>{SITE_URL}/article/{a.slug}</guid>
      <description><![CDATA[{summary}]]></description>
      <pubDate>{pub_date}</pubDate>
    </item>""")

    now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{SITE_NAME}</title>
    <link>{SITE_URL}</link>
    <description>{SITE_DESCRIPTION}</description>
    <language>zh-CN</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items_xml)}
  </channel>
</rss>"""

    from fastapi.responses import Response

    return Response(content=xml, media_type="application/xml")


@router.get("/api/seo/article/{slug}", summary="文章 SEO 元数据")
def article_seo_meta(slug: str, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.slug == slug, Article.status == ArticleStatus.PUBLISHED).first()
    if not article:
        from app.core.exceptions import AppError

        raise AppError("Article not found", 404)

    tags = [at.tag.name for at in article.tags if at.tag] if article.tags else []
    category_name = article.category.name if article.category else ""

    return {
        "title": f"{article.title} - {SITE_NAME}",
        "description": article.summary or article.title,
        "keywords": ",".join(tags) if tags else category_name,
        "og_title": article.title,
        "og_description": article.summary or article.title,
        "og_image": article.cover_image or "",
        "og_type": "article",
        "og_url": f"{SITE_URL}/article/{slug}",
        "json_ld": {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article.title,
            "description": article.summary or article.title,
            "image": article.cover_image or "",
            "datePublished": article.created_at.isoformat() if article.created_at else "",
            "dateModified": article.updated_at.isoformat() if article.updated_at else "",
            "author": {
                "@type": "Person",
                "name": article.author.name if article.author else "",
            },
            "publisher": {
                "@type": "Organization",
                "name": SITE_NAME,
            },
        },
    }


def _url_entry(loc: str, lastmod: str | None = None, changefreq: str = "daily", priority: str = "0.8") -> str:
    parts = ["  <url>", f"    <loc>{loc}</loc>"]
    if lastmod:
        parts.append(f"    <lastmod>{lastmod}</lastmod>")
    parts.append(f"    <changefreq>{changefreq}</changefreq>")
    parts.append(f"    <priority>{priority}</priority>")
    parts.append("  </url>")
    return "\n".join(parts)
