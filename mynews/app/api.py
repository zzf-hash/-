from flask import Blueprint, jsonify, render_template, current_app, request
from app.models import News

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    # 展示热度前20
    items = News.query.order_by(News.hotness.desc()).limit(20).all()
    return render_template('index.html', items=items)


@bp.route('/hot-rank')
def hot_rank_page():
    items = News.query.order_by(News.hotness.desc()).limit(100).all()
    return render_template('hot_rank.html', items=items)


@bp.route('/api/news')
def api_news():
    page = int(request.args.get('page', 1))
    per = int(request.args.get('per', 20))
    q = News.query.order_by(News.published_at.desc())
    total = q.count()
    items = q.offset((page-1)*per).limit(per).all()
    return jsonify({'total': total, 'items': [i.to_dict() for i in items]})


@bp.route('/api/analysis/hot-rank')
def api_hot_rank():
    n = int(request.args.get('n', 50))
    items = News.query.order_by(News.hotness.desc()).limit(n).all()
    return jsonify({'items': [i.to_dict() for i in items]})
