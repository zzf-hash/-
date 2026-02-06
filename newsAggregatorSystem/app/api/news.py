from flask import request, jsonify
from app.api import api_bp
from app.models import News
from app.news_fetcher.fetcher import NewsFetcher
import logging

logger = logging.getLogger(__name__)

# 获取新闻列表
@api_bp.route('/news', methods=['GET'])
def get_news_list():
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        source = request.args.get('source')
        category = request.args.get('category')
        sort_by = request.args.get('sort_by', 'publish_time')
        order = request.args.get('order', 'desc')
        
        # 构建查询
        query = News.query
        
        # 按来源过滤
        if source:
            query = query.filter_by(source=source)
        
        # 按分类过滤
        if category:
            query = query.filter_by(category=category)
        
        # 排序
        if sort_by == 'hotness':
            if order == 'desc':
                query = query.order_by(News.hotness_score.desc())
            else:
                query = query.order_by(News.hotness_score.asc())
        else:
            if order == 'desc':
                query = query.order_by(News.publish_time.desc())
            else:
                query = query.order_by(News.publish_time.asc())
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        news_list = pagination.items
        
        # 转换为字典格式
        news_data = [news.to_dict() for news in news_list]
        
        return jsonify({
            'code': 200,
            'data': {
                'news_list': news_data,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            },
            'message': '获取新闻列表成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting news list: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取新闻列表失败'
        })

# 获取新闻详情
@api_bp.route('/news/<int:news_id>', methods=['GET'])
def get_news_detail(news_id):
    try:
        news = News.query.get(news_id)
        if not news:
            return jsonify({
                'code': 404,
                'data': {},
                'message': '新闻不存在'
            })
        
        # 增加浏览量
        news.view_count += 1
        from app.models import db
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': news.to_dict(),
            'message': '获取新闻详情成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting news detail: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取新闻详情失败'
        })

# 刷新新闻
@api_bp.route('/news/refresh', methods=['POST'])
def refresh_news():
    try:
        # 创建新闻抓取器实例
        fetcher = NewsFetcher()
        
        # 抓取新闻
        news_list = fetcher.fetch_all_news()
        
        return jsonify({
            'code': 200,
            'data': {
                'fetched_count': len(news_list),
                'message': f'成功抓取{len(news_list)}条新闻'
            },
            'message': '刷新新闻成功'
        })
        
    except Exception as e:
        logger.error(f'Error refreshing news: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '刷新新闻失败'
        })

# 更新新闻互动数据
@api_bp.route('/news/<int:news_id>/interact', methods=['POST'])
def update_news_interaction(news_id):
    try:
        news = News.query.get(news_id)
        if not news:
            return jsonify({
                'code': 404,
                'data': {},
                'message': '新闻不存在'
            })
        
        # 获取互动数据
        data = request.json or {}
        view_count = data.get('view_count', 0)
        comment_count = data.get('comment_count', 0)
        share_count = data.get('share_count', 0)
        
        # 更新互动数据
        if view_count > 0:
            news.view_count = view_count
        if comment_count > 0:
            news.comment_count = comment_count
        if share_count > 0:
            news.share_count = share_count
        
        from app.models import db
        db.session.commit()
        
        return jsonify({
            'code': 200,
            'data': news.to_dict(),
            'message': '更新互动数据成功'
        })
        
    except Exception as e:
        logger.error(f'Error updating news interaction: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '更新互动数据失败'
        })