#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""手动执行一次抓取与热度分析"""

from config import Config
from app import db
from flask import Flask
import app.models  # noqa: F401
import importlib

flask_app = Flask(__name__)
flask_app.config.from_object(Config)

with flask_app.app_context():
    db.init_app(flask_app)
    db.create_all()
    
    # 导入并执行抓取与分析
    news_fetcher = importlib.import_module('app.news_fetcher')
    hot_analysis = importlib.import_module('app.hot_analysis')
    
    print("\n开始抓取新闻...\n")
    news_fetcher.fetch_all_sources(flask_app, db.session)
    
    print("\n开始计算热度...\n")
    hot_analysis.calculate_hotness(db.session, flask_app.config)
    
    print("\n抓取与分析完成！\n")
    
    # 查询并显示结果
    from app.models import News
    total = News.query.count()
    print(f"✓ 数据库中共有 {total} 条新闻\n")
    
    if total > 0:
        print("热度最高的前 10 条:")
        for idx, item in enumerate(News.query.order_by(News.hotness.desc()).limit(10).all(), 1):
            print(f"{idx}. 【{item.source}】{item.category} | 热度: {item.hotness:.6f}")
            print(f"   {item.title[:80]}")
            print()
