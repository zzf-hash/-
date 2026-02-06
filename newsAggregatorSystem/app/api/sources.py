from flask import request, jsonify
from app.api import api_bp
from app.models import NewsSource
from app.models import db
import logging
from app.news_fetcher.fetcher import init_news_sources

logger = logging.getLogger(__name__)

# 获取新闻来源列表
@api_bp.route('/sources', methods=['GET'])
def get_news_sources():
    try:
        # 查询所有新闻来源
        sources = NewsSource.query.all()
        
        # 转换为字典格式
        source_data = []
        for source in sources:
            source_data.append(source.to_dict())
        
        return jsonify({
            'code': 200,
            'data': {
                'sources': source_data,
                'total': len(source_data)
            },
            'message': '获取新闻来源列表成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting news sources: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取新闻来源列表失败'
        })

# 更新新闻来源状态
@api_bp.route('/sources/<int:source_id>/status', methods=['PUT'])
def update_source_status(source_id):
    try:
        # 获取来源
        source = NewsSource.query.get(source_id)
        if not source:
            return jsonify({
                'code': 404,
                'data': {},
                'message': '新闻来源不存在'
            })
        
        # 获取状态数据
        data = request.json or {}
        enabled = data.get('enabled')
        
        if enabled is not None:
            source.enabled = enabled
            db.session.commit()
            
            return jsonify({
                'code': 200,
                'data': {
                    'source_id': source.id,
                    'name': source.name,
                    'enabled': source.enabled
                },
                'message': f'{source.name}已{"启用" if enabled else "禁用"}'
            })
        else:
            return jsonify({
                'code': 400,
                'data': {},
                'message': '请提供enabled参数'
            })
        
    except Exception as e:
        logger.error(f'Error updating source status: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '更新新闻来源状态失败'
        })

# 更新新闻来源抓取间隔
@api_bp.route('/sources/<int:source_id>/interval', methods=['PUT'])
def update_source_interval(source_id):
    try:
        # 获取来源
        source = NewsSource.query.get(source_id)
        if not source:
            return jsonify({
                'code': 404,
                'data': {},
                'message': '新闻来源不存在'
            })
        
        # 获取间隔数据
        data = request.json or {}
        crawl_interval = data.get('crawl_interval')
        
        if crawl_interval and isinstance(crawl_interval, int) and crawl_interval > 0:
            source.crawl_interval = crawl_interval
            db.session.commit()
            
            return jsonify({
                'code': 200,
                'data': {
                    'source_id': source.id,
                    'name': source.name,
                    'crawl_interval': source.crawl_interval
                },
                'message': f'{source.name}的抓取间隔已更新为{source.crawl_interval}分钟'
            })
        else:
            return jsonify({
                'code': 400,
                'data': {},
                'message': '请提供有效的crawl_interval参数（正整数）'
            })
        
    except Exception as e:
        logger.error(f'Error updating source interval: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '更新新闻来源抓取间隔失败'
        })

# 初始化新闻来源
@api_bp.route('/sources/init', methods=['POST'])
def initialize_sources():
    try:
        # 执行初始化
        init_news_sources()
        
        # 查询初始化后的来源
        sources = NewsSource.query.all()
        source_count = len(sources)
        
        return jsonify({
            'code': 200,
            'data': {
                'initialized_count': source_count,
                'message': f'成功初始化{source_count}个新闻来源'
            },
            'message': '初始化新闻来源成功'
        })
        
    except Exception as e:
        logger.error(f'Error initializing sources: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '初始化新闻来源失败'
        })

# 获取来源抓取状态
@api_bp.route('/sources/status', methods=['GET'])
def get_sources_status():
    try:
        # 查询所有新闻来源
        sources = NewsSource.query.all()
        
        # 转换为状态格式
        status_data = []
        for source in sources:
            status_data.append({
                'id': source.id,
                'name': source.name,
                'enabled': source.enabled,
                'crawl_status': source.crawl_status,
                'last_crawl_time': source.last_crawl_time.isoformat() if source.last_crawl_time else None,
                'error_message': source.error_message
            })
        
        return jsonify({
            'code': 200,
            'data': {
                'status_list': status_data,
                'total': len(status_data)
            },
            'message': '获取新闻来源状态成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting sources status: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取新闻来源状态失败'
        })