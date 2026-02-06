from app.models import db
from datetime import datetime

class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    analysis_type = db.Column(db.String(50), nullable=False)  # hotness, trend, category
    analysis_date = db.Column(db.Date, nullable=False, default=lambda: datetime.utcnow().date())
    analysis_time = db.Column(db.DateTime, default=datetime.utcnow)
    result_data = db.Column(db.JSON, nullable=False)  # 存储分析结果的JSON数据
    summary = db.Column(db.String(500))  # 分析结果摘要
    
    def __repr__(self):
        return f'<AnalysisResult {self.analysis_type} on {self.analysis_date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'analysis_type': self.analysis_type,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'analysis_time': self.analysis_time.isoformat() if self.analysis_time else None,
            'result_data': self.result_data,
            'summary': self.summary
        }