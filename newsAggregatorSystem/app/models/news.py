from app.models import db
from datetime import datetime

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False, unique=True)
    publish_time = db.Column(db.DateTime, nullable=False)
    crawl_time = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    hotness_score = db.Column(db.Float, default=0.0)
    sentiment_score = db.Column(db.Float, default=0.0)
    view_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    share_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<News {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'url': self.url,
            'publish_time': self.publish_time.isoformat() if self.publish_time else None,
            'crawl_time': self.crawl_time.isoformat() if self.crawl_time else None,
            'category': self.category,
            'hotness_score': self.hotness_score,
            'sentiment_score': self.sentiment_score,
            'view_count': self.view_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count
        }