from flask_sqlalchemy import SQLAlchemy

# 创建数据库实例
db = SQLAlchemy()

# 导入所有模型
from app.models.news import News
from app.models.analysis import AnalysisResult
from app.models.source import NewsSource