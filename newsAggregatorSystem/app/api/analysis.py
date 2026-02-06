from flask import request, jsonify
from app.api import api_bp
from app.hot_analysis.analyzer import HotnessAnalyzer
from app.models import AnalysisResult
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# 分析热度
@api_bp.route('/analysis/hotness', methods=['GET'])
def analyze_hotness():
    try:
        # 获取分析天数
        days = int(request.args.get('days', 7))
        
        # 创建分析器实例
        analyzer = HotnessAnalyzer()
        
        # 执行热度分析
        result = analyzer.analyze_hotness(days=days)
        
        if not result:
            return jsonify({
                'code': 404,
                'data': {},
                'message': f'过去{days}天内没有新闻数据'
            })
        
        return jsonify({
            'code': 200,
            'data': result,
            'message': '热度分析成功'
        })
        
    except Exception as e:
        logger.error(f'Error analyzing hotness: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '热度分析失败'
        })

# 获取热度排行榜
@api_bp.route('/analysis/hot-rank', methods=['GET'])
def get_hot_rank():
    try:
        # 获取查询参数
        limit = int(request.args.get('limit', 20))
        days = int(request.args.get('days', 7))
        
        # 创建分析器实例
        analyzer = HotnessAnalyzer()
        
        # 执行热度分析
        result = analyzer.analyze_hotness(days=days)
        
        if not result or 'top_news' not in result:
            return jsonify({
                'code': 404,
                'data': {},
                'message': f'过去{days}天内没有新闻数据'
            })
        
        # 获取前N条
        top_news = result['top_news'][:limit]
        
        return jsonify({
            'code': 200,
            'data': {
                'top_news': top_news,
                'limit': limit,
                'analysis_period': f'过去{days}天'
            },
            'message': '获取热度排行榜成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting hot rank: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取热度排行榜失败'
        })

# 获取热度趋势
@api_bp.route('/analysis/trend', methods=['GET'])
def get_hotness_trend():
    try:
        # 获取查询参数
        days = int(request.args.get('days', 7))
        trend_type = request.args.get('type', 'hourly')  # hourly, daily
        
        # 创建分析器实例
        analyzer = HotnessAnalyzer()
        
        # 执行热度分析
        result = analyzer.analyze_hotness(days=days)
        
        if not result or 'trend_data' not in result:
            return jsonify({
                'code': 404,
                'data': {},
                'message': f'过去{days}天内没有新闻数据'
            })
        
        # 获取趋势数据
        trend_data = result['trend_data']
        if trend_type == 'daily':
            trend_data = trend_data.get('daily', [])
        else:
            trend_data = trend_data.get('hourly', [])
        
        return jsonify({
            'code': 200,
            'data': {
                'trend_data': trend_data,
                'trend_type': trend_type,
                'analysis_period': f'过去{days}天'
            },
            'message': '获取热度趋势成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting hotness trend: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取热度趋势失败'
        })

# 获取分类热度
@api_bp.route('/analysis/category', methods=['GET'])
def get_category_hotness():
    try:
        # 获取查询参数
        days = int(request.args.get('days', 7))
        
        # 创建分析器实例
        analyzer = HotnessAnalyzer()
        
        # 执行热度分析
        result = analyzer.analyze_hotness(days=days)
        
        if not result or 'category_data' not in result:
            return jsonify({
                'code': 404,
                'data': {},
                'message': f'过去{days}天内没有新闻数据'
            })
        
        return jsonify({
            'code': 200,
            'data': {
                'category_data': result['category_data'],
                'analysis_period': f'过去{days}天'
            },
            'message': '获取分类热度成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting category hotness: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取分类热度失败'
        })

# 获取历史分析结果
@api_bp.route('/analysis/history', methods=['GET'])
def get_analysis_history():
    try:
        # 获取查询参数
        analysis_type = request.args.get('type')
        days = int(request.args.get('days', 30))
        
        # 计算开始日期
        start_date = datetime.utcnow().date() - timedelta(days=days)
        
        # 构建查询
        query = AnalysisResult.query.filter(
            AnalysisResult.analysis_date >= start_date
        )
        
        # 按类型过滤
        if analysis_type:
            query = query.filter_by(analysis_type=analysis_type)
        
        # 排序
        query = query.order_by(AnalysisResult.analysis_date.desc())
        
        # 执行查询
        results = query.all()
        
        # 转换为字典格式
        analysis_data = []
        for result in results:
            analysis_data.append({
                'id': result.id,
                'analysis_type': result.analysis_type,
                'analysis_date': result.analysis_date.isoformat(),
                'analysis_time': result.analysis_time.isoformat() if result.analysis_time else None,
                'summary': result.summary,
                'result_data': result.result_data
            })
        
        return jsonify({
            'code': 200,
            'data': {
                'analysis_history': analysis_data,
                'total': len(analysis_data),
                'analysis_period': f'{start_date} to {datetime.utcnow().date()}'
            },
            'message': '获取历史分析结果成功'
        })
        
    except Exception as e:
        logger.error(f'Error getting analysis history: {e}')
        return jsonify({
            'code': 500,
            'data': {},
            'message': '获取历史分析结果失败'
        })