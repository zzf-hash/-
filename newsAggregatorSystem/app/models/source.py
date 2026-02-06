from app.models import db

class NewsSource(db.Model):
    __tablename__ = 'news_sources'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source_id = db.Column(db.String(50), unique=True, nullable=False)  # 外部来源ID
    name = db.Column(db.String(100), nullable=False)  # 来源名称
    url = db.Column(db.String(500), nullable=False)  # 来源URL
    enabled = db.Column(db.Boolean, default=True)  # 是否启用
    crawl_interval = db.Column(db.Integer, default=30)  # 抓取间隔（分钟）
    last_crawl_time = db.Column(db.DateTime)  # 上次抓取时间
    crawl_status = db.Column(db.String(20), default='idle')  # 抓取状态：idle, crawling, error
    error_message = db.Column(db.String(500))  # 错误信息
    
    def __repr__(self):
        return f'<NewsSource {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'source_id': self.source_id,
            'name': self.name,
            'url': self.url,
            'enabled': self.enabled,
            'crawl_interval': self.crawl_interval,
            'last_crawl_time': self.last_crawl_time.isoformat() if self.last_crawl_time else None,
            'crawl_status': self.crawl_status,
            'error_message': self.error_message
        }