import feedparser
import requests
from datetime import datetime
from app.models import News

def fetch_from_feed(feed_url, source_name, category, session, user_agent='MyNewsBot/1.0'):
    print(f'  [*] 抓取 {source_name} from {feed_url}')
    headers = {'User-Agent': user_agent}
    try:
        parsed = feedparser.parse(feed_url)
        print(f'  [✓] feedparser 直接解析成功，{len(parsed.entries)} 条')
    except Exception as e:
        print(f'  [!] feedparser 直接解析失败: {e}')
        # fallback to requests then feedparser
        try:
            r = requests.get(feed_url, headers=headers, timeout=10)
            print(f'  [✓] requests 获取成功 (状态码 {r.status_code})')
            parsed = feedparser.parse(r.content)
            print(f'  [✓] fallback 解析成功，{len(parsed.entries)} 条')
        except Exception as e2:
            print(f'  [!] fallback 也失败: {e2}')
            return

    count = 0
    for entry in parsed.entries[:20]:
        title = entry.get('title', '')
        link = entry.get('link') or entry.get('id')
        summary = entry.get('summary', '')
        published = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6])

        if not title or not link:
            continue

        # deduplicate by url
        existing = session.query(News).filter(News.url == link).first()
        if existing:
            existing.fetched_at = datetime.utcnow()
            session.add(existing)
            continue

        news = News(
            title=title,
            summary=summary,
            url=link,
            source=source_name,
            category=category,
            published_at=published or datetime.utcnow(),
            fetched_at=datetime.utcnow()
        )
        session.add(news)
        count += 1

    session.commit()
    print(f'  [+] {source_name} 新增 {count} 条新闻')


def fetch_all_sources(app, session):
    cfg = app.config
    sources = cfg.get('NEWS_SOURCES', [])
    print(f'\n[*] 开始抓取所有来源，共 {len(sources)} 个来源\n')
    for src in sources:
        if not src.get('enabled', True):
            print(f'[-] 跳过禁用来源: {src.get("name")}')
            continue
        try:
            fetch_from_feed(src['url'], src.get('name', src['id']), src.get('category', ''), session, user_agent=cfg.get('USER_AGENT'))
        except Exception as e:
            print(f'  [!] 抓取 {src.get("url")} 失败: {e}')
