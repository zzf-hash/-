from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

from config import Config
from app import db

flask_app = Flask(__name__, template_folder='templates', static_folder='static')
flask_app.config.from_object(Config)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mynews')

# 初始化 db
with flask_app.app_context():
    db.init_app(flask_app)
    # 导入 models 以确保模型类被注册
    import app.models  # noqa: F401
    db.create_all()

# 延迟导入其他模块以避免循环依赖
import importlib
news_fetcher = importlib.import_module('app.news_fetcher')
hot_analysis = importlib.import_module('app.hot_analysis')
api = importlib.import_module('app.api')

flask_app.register_blueprint(api.bp)


def fetch_and_analyze():
    # 在 Flask 应用上下文中运行以确保 `current_app`、配置和 DB 可用
    with flask_app.app_context():
        logger.info('开始抓取并分析新闻：%s', datetime.utcnow().isoformat())
        try:
            news_fetcher.fetch_all_sources(flask_app, db.session)
            hot_analysis.calculate_hotness(db.session, flask_app.config)
            logger.info('抓取与分析完成')
        except Exception as e:
            logger.exception('抓取/分析失败: %s', e)


if __name__ == '__main__':
    # 定时任务
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_analyze, 'interval', hours=Config.FETCH_INTERVAL_HOURS, next_run_time=datetime.utcnow())
    scheduler.start()
    logger.info('调度器已启动，间隔 %s 小时', Config.FETCH_INTERVAL_HOURS)

    try:
        print('\nMyNews 服务启动在 http://127.0.0.1:5001')
        print('  首页: http://127.0.0.1:5001')
        print('  排行榜: http://127.0.0.1:5001/hot-rank')
        print('  API: http://127.0.0.1:5001/api/news\n')
        flask_app.run(debug=False, port=5001, threaded=True)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
