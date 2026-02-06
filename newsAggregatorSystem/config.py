import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # 数据库配置 - 使用SQLite数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///news_aggregator.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 新闻聚合配置
    NEWS_SOURCES = [
        {
            'id': '1',
            'name': '腾讯新闻',
            'url': 'https://news.qq.com',
            'enabled': True
        },
        {
            'id': '2',
            'name': '网易新闻',
            'url': 'https://news.163.com',
            'enabled': True
        },
        {
            'id': '3',
            'name': '新浪新闻',
            'url': 'https://news.sina.com.cn',
            'enabled': True
        },
        {
            'id': '4',
            'name': '央视新闻',
            'url': 'https://news.cctv.com',
            'enabled': True
        }
    ]
    
    # 热度分析配置
    HOTNESS_WEIGHT = 0.7
    TREND_WEIGHT = 0.3
    REFRESH_INTERVAL = 60  # 分钟
    
    # API配置
    API_RATE_LIMIT = 100  # 每分钟请求数
    
    # 其他配置
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'