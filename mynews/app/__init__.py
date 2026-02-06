from flask_sqlalchemy import SQLAlchemy

# 包级别的数据库实例，其他模块通过 `from app import db` 使用
db = SQLAlchemy()
