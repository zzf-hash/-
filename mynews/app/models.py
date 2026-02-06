from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from app import db


class News(db.Model):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    summary = Column(Text)
    url = Column(String(1024))
    source = Column(String(128))
    category = Column(String(64))
    published_at = Column(DateTime, default=datetime.utcnow)
    fetched_at = Column(DateTime, default=datetime.utcnow)
    hotness = Column(Float, default=0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'url': self.url,
            'source': self.source,
            'category': self.category,
            'published_at': self.published_at.isoformat() if self.published_at else None,
            'hotness': self.hotness
        }
