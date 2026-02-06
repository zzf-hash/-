# MyNews - 简易新闻聚合与热度排行

这是一个最小可运行的新闻聚合示例项目（Flask），包含：
- 每2小时抓取一次 RSS/源并计算热度
- 将新闻按热度排序并在页面展示

启动：

```bash
pip install -r requirements.txt
python run.py
```

访问 http://127.0.0.1:5001 查看热度排行页面。

- 首页：http://127.0.0.1:5001
- 排行榜：http://127.0.0.1:5001/hot-rank
- API：http://127.0.0.1:5001/api/news (JSON 格式)
