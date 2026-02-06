#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""快速检查数据库中的新闻数据"""

from config import Config
from app import db
from flask import Flask
import app.models  # noqa: F401

flask_app = Flask(__name__)
flask_app.config.from_object(Config)

with flask_app.app_context():
    db.init_app(flask_app)
    from app.models import News
    
    print("\n=== 数据库中的新闻数据 ===\n")
    
    # 统计总数
    total = News.query.count()
    print(f"总条数: {total}\n")
    
    if total > 0:
        # 显示热度最高的前 5 条
        print("热度最高的前 5 条:")
        for idx, item in enumerate(News.query.order_by(News.hotness.desc()).limit(5).all(), 1):
            print(f"{idx}. 【{item.source}】{item.category}")
            print(f"   标题: {item.title}")
            print(f"   热度: {item.hotness:.6f}")
            print(f"   URL: {item.url}")
            print(f"   发布时间: {item.published_at}")
            print()
        
        # 显示最近发布的前 5 条
        print("\n最近发布的前 5 条:")
        for idx, item in enumerate(News.query.order_by(News.published_at.desc()).limit(5).all(), 1):
            print(f"{idx}. 【{item.source}】{item.category}")
            print(f"   标题: {item.title}")
            print(f"   热度: {item.hotness:.6f}")
            print(f"   发布时间: {item.published_at}")
            print()
    else:
        print("⚠️  数据库为空，暂无新闻数据。请等待首次抓取完成或手动运行抓取任务。")
