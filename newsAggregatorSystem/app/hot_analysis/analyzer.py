import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging
from app.models import db, News, AnalysisResult
from config import Config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置matplotlib中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class HotnessAnalyzer:
    def __init__(self):
        self.hotness_weight = Config.HOTNESS_WEIGHT
        self.trend_weight = Config.TREND_WEIGHT
    
    def analyze_hotness(self, days=7):
        """分析新闻热度"""
        try:
            # 获取指定天数内的新闻
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            news_list = News.query.filter(
                News.publish_time >= start_date,
                News.publish_time <= end_date
            ).all()
            
            if not news_list:
                logger.warning(f'No news found in the last {days} days')
                return {}
            
            # 计算热度
            hot_news = []
            for news in news_list:
                hotness_score = self.calculate_hotness(news)
                news.hotness_score = hotness_score
                db.session.commit()
                
                hot_news.append({
                    'id': news.id,
                    'title': news.title,
                    'source': news.source,
                    'publish_time': news.publish_time,
                    'hotness_score': hotness_score,
                    'view_count': news.view_count,
                    'comment_count': news.comment_count,
                    'share_count': news.share_count,
                    'category': news.category
                })
            
            # 按热度排序
            hot_news.sort(key=lambda x: x['hotness_score'], reverse=True)
            
            # 生成热度排行榜
            top_news = hot_news[:20]  # 取前20条
            
            # 分析热度趋势
            trend_data = self.analyze_hotness_trend(news_list)
            
            # 分析分类热度
            category_data = self.analyze_category_hotness(news_list)
            
            # 存储分析结果
            analysis_result = AnalysisResult(
                analysis_type='hotness',
                analysis_date=end_date.date(),
                result_data={
                    'top_news': top_news,
                    'trend_data': trend_data,
                    'category_data': category_data,
                    'total_news_count': len(news_list),
                    'analysis_period': f'{start_date.date()} to {end_date.date()}'
                },
                summary=f'共分析{len(news_list)}条新闻，生成热度排行榜前20条'
            )
            
            db.session.add(analysis_result)
            db.session.commit()
            
            logger.info(f'Analyzed hotness for {len(news_list)} news articles')
            
            return {
                'top_news': top_news,
                'trend_data': trend_data,
                'category_data': category_data,
                'total_news_count': len(news_list)
            }
            
        except Exception as e:
            logger.error(f'Error analyzing hotness: {e}')
            return {}
    
    def calculate_hotness(self, news):
        """计算新闻热度分数"""
        # 基础热度分数 = 浏览量 * 0.1 + 评论数 * 0.3 + 分享数 * 0.6
        base_score = (news.view_count * 0.1) + (news.comment_count * 0.3) + (news.share_count * 0.6)
        
        # 时间衰减因子：越新的新闻热度越高
        time_factor = self.calculate_time_factor(news.publish_time)
        
        # 来源权重
        source_weight = self.get_source_weight(news.source)
        
        # 标题权重：标题长度适中的新闻可能更吸引人
        title_weight = self.calculate_title_weight(news.title)
        
        # 综合计算热度分数
        hotness_score = (base_score * time_factor * source_weight * title_weight)
        
        # 归一化到0-100分
        hotness_score = min(hotness_score, 100)
        
        return round(hotness_score, 2)
    
    def calculate_time_factor(self, publish_time):
        """计算时间衰减因子"""
        now = datetime.utcnow()
        hours_since_publish = (now - publish_time).total_seconds() / 3600
        
        # 时间衰减函数：指数衰减
        # 1小时内：1.0
        # 1-6小时：0.8
        # 6-24小时：0.5
        # 24-72小时：0.3
        # 72小时以上：0.1
        if hours_since_publish <= 1:
            return 1.0
        elif hours_since_publish <= 6:
            return 0.8
        elif hours_since_publish <= 24:
            return 0.5
        elif hours_since_publish <= 72:
            return 0.3
        else:
            return 0.1
    
    def get_source_weight(self, source):
        """获取来源权重"""
        source_weights = {
            '腾讯新闻': 1.0,
            '网易新闻': 0.9,
            '新浪新闻': 0.9,
            '央视新闻': 1.1
        }
        return source_weights.get(source, 0.8)
    
    def calculate_title_weight(self, title):
        """计算标题权重"""
        title_length = len(title)
        
        # 标题长度在15-30字之间的权重较高
        if 15 <= title_length <= 30:
            return 1.2
        elif 10 <= title_length < 15 or 30 < title_length <= 40:
            return 1.0
        elif title_length < 10:
            return 0.8
        else:
            return 0.7
    
    def analyze_hotness_trend(self, news_list):
        """分析热度趋势"""
        # 按小时分组分析热度
        df = pd.DataFrame([
            {
                'hour': news.publish_time.hour,
                'hotness': self.calculate_hotness(news),
                'date': news.publish_time.date()
            }
            for news in news_list
        ])
        
        if df.empty:
            return []
        
        # 按小时计算平均热度
        hourly_trend = df.groupby('hour')['hotness'].mean().reset_index()
        hourly_trend = hourly_trend.sort_values('hour')
        
        # 转换为列表格式
        trend_data = []
        for _, row in hourly_trend.iterrows():
            trend_data.append({
                'hour': int(row['hour']),
                'average_hotness': float(row['hotness'])
            })
        
        # 按日期分析热度趋势
        daily_trend = df.groupby('date')['hotness'].mean().reset_index()
        daily_trend = daily_trend.sort_values('date')
        
        daily_trend_data = []
        for _, row in daily_trend.iterrows():
            daily_trend_data.append({
                'date': row['date'].isoformat(),
                'average_hotness': float(row['hotness'])
            })
        
        return {
            'hourly': trend_data,
            'daily': daily_trend_data
        }
    
    def analyze_category_hotness(self, news_list):
        """分析分类热度"""
        # 按分类分组分析热度
        category_dict = {}
        
        for news in news_list:
            category = news.category or '其他'
            if category not in category_dict:
                category_dict[category] = {
                    'count': 0,
                    'total_hotness': 0,
                    'news_list': []
                }
            
            category_dict[category]['count'] += 1
            category_dict[category]['total_hotness'] += news.hotness_score
            category_dict[category]['news_list'].append(news)
        
        # 计算每个分类的平均热度
        category_data = []
        for category, data in category_dict.items():
            avg_hotness = data['total_hotness'] / data['count'] if data['count'] > 0 else 0
            
            # 获取每个分类的热门新闻
            hot_news_in_category = sorted(
                data['news_list'],
                key=lambda x: x.hotness_score,
                reverse=True
            )[:5]  # 每个分类取前5条
            
            hot_news_list = []
            for news in hot_news_in_category:
                hot_news_list.append({
                    'id': news.id,
                    'title': news.title,
                    'hotness_score': news.hotness_score
                })
            
            category_data.append({
                'category': category,
                'count': data['count'],
                'average_hotness': round(avg_hotness, 2),
                'total_hotness': round(data['total_hotness'], 2),
                'hot_news': hot_news_list
            })
        
        # 按平均热度排序
        category_data.sort(key=lambda x: x['average_hotness'], reverse=True)
        
        return category_data
    
    def generate_hotness_chart(self, trend_data, output_path=None):
        """生成热度趋势图表"""
        try:
            # 准备数据
            hourly_data = trend_data.get('hourly', [])
            if not hourly_data:
                logger.warning('No hourly trend data available')
                return None
            
            hours = [item['hour'] for item in hourly_data]
            hotness_values = [item['average_hotness'] for item in hourly_data]
            
            # 创建图表
            plt.figure(figsize=(12, 6))
            sns.lineplot(x=hours, y=hotness_values, marker='o')
            plt.title('24小时热度趋势', fontsize=16)
            plt.xlabel('小时', fontsize=12)
            plt.ylabel('平均热度', fontsize=12)
            plt.xticks(range(0, 24, 2))
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            # 保存图表
            if output_path:
                plt.savefig(output_path)
                logger.info(f'Saved hotness trend chart to {output_path}')
                return output_path
            else:
                # 如果没有指定输出路径，返回图表数据
                import io
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                return buffer
        
        except Exception as e:
            logger.error(f'Error generating hotness chart: {e}')
            return None
    
    def analyze_sentiment(self, news_list):
        """分析新闻情感倾向"""
        # 简单的情感分析实现
        # 实际项目中可以使用更复杂的NLP模型
        positive_words = ['好', '优秀', '成功', '上涨', '创新', '进步', '胜利', '高兴', '繁荣']
        negative_words = ['坏', '失败', '下跌', '危机', '问题', '困难', '错误', '悲伤', '衰退']
        
        sentiment_data = []
        
        for news in news_list:
            text = news.title + ' ' + news.content
            positive_count = sum(1 for word in positive_words if word in text)
            negative_count = sum(1 for word in negative_words if word in text)
            
            # 计算情感分数：(正面词数 - 负面词数) / (总词数 + 1)
            total_words = len(text) // 2  # 粗略估计词数
            sentiment_score = (positive_count - negative_count) / (total_words + 1)
            sentiment_score = max(-1, min(1, sentiment_score))  # 限制在-1到1之间
            
            # 更新新闻的情感分数
            news.sentiment_score = sentiment_score
            db.session.commit()
            
            sentiment_data.append({
                'id': news.id,
                'title': news.title,
                'sentiment_score': sentiment_score,
                'positive_count': positive_count,
                'negative_count': negative_count
            })
        
        # 分析情感分布
        positive_news = [item for item in sentiment_data if item['sentiment_score'] > 0.1]
        negative_news = [item for item in sentiment_data if item['sentiment_score'] < -0.1]
        neutral_news = [item for item in sentiment_data if -0.1 <= item['sentiment_score'] <= 0.1]
        
        return {
            'sentiment_data': sentiment_data,
            'sentiment_distribution': {
                'positive': len(positive_news),
                'negative': len(negative_news),
                'neutral': len(neutral_news)
            },
            'average_sentiment': sum(item['sentiment_score'] for item in sentiment_data) / len(sentiment_data) if sentiment_data else 0
        }