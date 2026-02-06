import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'mynews.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 抓取配置（RSS 或页面）
    NEWS_SOURCES = [
        {'id': 'hacker', 'name': 'Hacker News', 'url': 'https://news.ycombinator.com/rss', 'category': '科技', 'enabled': True},
        {'id': 'techcrunch', 'name': 'TechCrunch', 'url': 'http://feeds.feedburner.com/TechCrunch/', 'category': '科技', 'enabled': True},
        {'id': 'bbc', 'name': 'BBC', 'url': 'http://feeds.bbc.co.uk/news/rss.xml', 'category': '国际', 'enabled': True},
    ]

    # 调度配置
    FETCH_INTERVAL_HOURS = int(os.environ.get('FETCH_INTERVAL_HOURS', '2'))  # 每多少小时抓取一次

    # 热度计算权重
    HOTNESS_WEIGHT_RECENCY = float(os.environ.get('HOTNESS_WEIGHT_RECENCY', '0.7'))
    HOTNESS_WEIGHT_RANDOM = float(os.environ.get('HOTNESS_WEIGHT_RANDOM', '0.3'))

    USER_AGENT = os.environ.get('USER_AGENT', 'MyNewsBot/1.0')
