from datetime import datetime, timedelta
import random
from app.models import News


def calculate_hotness(db_session, config):
    """
    简易热度计算：结合发布时间（越新越热）与随机模拟的互动量，生成 hotness 分数并写回数据库。
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(days=7)
    items = db_session.query(News).filter(News.published_at >= cutoff).all()

    for item in items:
        # 时间权重：最近一小时最高，随时间衰减
        age_seconds = (now - (item.published_at or now)).total_seconds()
        recency_score = max(0.0, 1.0 - age_seconds / (7 * 24 * 3600))

        # 模拟互动（如果没有真实数据），可替换为真实指标
        simulated_interactions = random.uniform(0, 1)

        hotness = config.get('HOTNESS_WEIGHT_RECENCY', 0.7) * recency_score + config.get('HOTNESS_WEIGHT_RANDOM', 0.3) * simulated_interactions
        item.hotness = round(hotness, 6)
        db_session.add(item)

    db_session.commit()
