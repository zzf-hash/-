# 自动化新闻聚合与热度分析系统

一个基于Python Flask的自动化新闻聚合与热度分析系统，能够从多个新闻来源获取最新资讯，并通过智能算法分析新闻热度趋势。

## 功能特性

### 核心功能
- **多源新闻聚合**：从腾讯新闻、网易新闻、新浪新闻、央视新闻等多个来源自动抓取新闻
- **智能热度分析**：基于浏览量、评论数、分享数等指标计算新闻热度
- **热度趋势分析**：分析24小时和每日热度变化趋势
- **分类热度分析**：按新闻分类分析热度分布
- **热度排行榜**：生成热度排行榜，展示最热门的新闻
- **新闻详情查看**：支持查看新闻详细内容
- **来源管理**：支持启用/禁用新闻来源，调整抓取间隔

### 技术特性
- **基于Flask框架**：轻量级Web框架，易于扩展
- **数据存储**：使用SQLAlchemy ORM，支持PostgreSQL数据库
- **异步抓取**：支持异步抓取新闻，提高效率
- **数据可视化**：使用Chart.js实现数据可视化
- **响应式设计**：适配PC端和移动端
- **API接口**：提供RESTful API接口，支持第三方集成

## 项目结构

```
newsAggregatorSystem/
├── app.py              # Flask应用入口
├── config.py           # 配置文件
├── requirements.txt    # 依赖项
├── README.md           # 项目说明
├── app/                # 应用主目录
│   ├── news_fetcher/   # 新闻抓取模块
│   │   └── fetcher.py  # 新闻抓取核心逻辑
│   ├── hot_analysis/   # 热度分析模块
│   │   └── analyzer.py # 热度分析核心逻辑
│   ├── models/         # 数据模型
│   │   ├── __init__.py
│   │   ├── news.py     # 新闻模型
│   │   ├── analysis.py # 分析结果模型
│   │   └── source.py   # 新闻来源模型
│   ├── api/            # API接口
│   │   ├── __init__.py
│   │   ├── news.py     # 新闻相关API
│   │   ├── analysis.py # 分析相关API
│   │   └── sources.py  # 来源相关API
│   ├── templates/      # 前端模板
│   │   ├── base.html   # 基础模板
│   │   ├── index.html  # 首页
│   │   ├── news_list.html # 新闻列表
│   │   ├── hot_rank.html # 热度排行榜
│   │   ├── analysis.html # 数据分析
│   │   └── settings.html # 设置页面
│   └── static/         # 静态资源
│       ├── css/        # CSS样式
│       │   └── style.css
│       ├── js/         # JavaScript脚本
│       └── images/     # 图片资源
└── migrations/         # 数据库迁移文件
```

## 安装与配置

### 环境要求
- Python 3.7+
- PostgreSQL 10+
- pip 20.0+

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd newsAggregatorSystem
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置数据库**
   - 修改`config.py`文件中的数据库连接信息
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://admin:password@localhost:5432/example_db'
   ```

4. **初始化数据库**
   ```bash
   python -c "from app.models import db; from app import app; with app.app_context(): db.create_all()"
   ```

5. **初始化新闻来源**
   - 启动应用后，访问`/api/sources/init`接口初始化新闻来源

### 运行应用

1. **开发模式**
   ```bash
   python app.py
   ```

2. **生产模式**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## API接口

### 新闻相关接口
- **GET /api/news**：获取新闻列表
- **GET /api/news/<id>**：获取新闻详情
- **POST /api/news/refresh**：刷新新闻
- **POST /api/news/<id>/interact**：更新新闻互动数据

### 分析相关接口
- **GET /api/analysis/hotness**：分析热度
- **GET /api/analysis/hot-rank**：获取热度排行榜
- **GET /api/analysis/trend**：获取热度趋势
- **GET /api/analysis/category**：获取分类热度
- **GET /api/analysis/history**：获取历史分析结果

### 来源相关接口
- **GET /api/sources**：获取新闻来源列表
- **PUT /api/sources/<id>/status**：更新新闻来源状态
- **PUT /api/sources/<id>/interval**：更新新闻来源抓取间隔
- **POST /api/sources/init**：初始化新闻来源
- **GET /api/sources/status**：获取来源抓取状态

## 使用指南

### 首页
- 系统概览：查看系统功能和支持的新闻来源
- 最近新闻：查看最新抓取的新闻
- 系统状态：查看新闻来源的启用状态
- 热度概览：查看热度排行榜前5名
- 快速操作：刷新新闻、分析热度、初始化来源等

### 新闻列表
- 查看所有新闻：按时间顺序查看所有新闻
- 筛选新闻：按来源、分类筛选新闻
- 排序新闻：按发布时间、热度排序
- 分页浏览：支持分页查看新闻
- 查看详情：点击新闻标题查看详情

### 热度排行榜
- 热度排行：查看按热度排序的新闻
- 时间范围：选择不同时间范围的热度排行
- 热度详情：查看每条新闻的热度指标

### 数据分析
- 热度趋势：查看24小时和每日热度变化趋势
- 分类热度：查看不同分类的热度分布
- 历史分析：查看历史分析结果
- 数据可视化：通过图表直观展示数据

### 设置
- 来源管理：启用/禁用新闻来源
- 抓取设置：调整新闻来源的抓取间隔
- 系统配置：修改系统相关配置

## 注意事项

1. **数据抓取频率**：为了避免对新闻网站造成过大负担，请合理设置抓取间隔
2. **数据库性能**：随着新闻数据的积累，建议定期清理过期数据
3. **API使用限制**：建议对API接口设置访问频率限制，防止滥用
4. **系统稳定性**：建议使用进程管理工具（如Supervisor）管理应用进程

## 常见问题

### Q: 新闻抓取失败怎么办？
A: 检查网络连接，确认新闻来源网站是否可访问，查看系统日志了解具体错误信息

### Q: 热度分析不准确怎么办？
A: 可以调整热度计算的权重参数，或增加更多的热度指标

### Q: 系统运行缓慢怎么办？
A: 检查数据库性能，优化SQL查询，增加服务器资源，或使用缓存技术

### Q: 如何添加新的新闻来源？
A: 在`app/news_fetcher/fetcher.py`中添加新的抓取方法，在`init_news_sources`函数中添加新的来源配置

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系项目维护者。

---

**提示**：本系统仅用于学习和研究目的，使用时请遵守相关法律法规，尊重新闻网站的robots.txt规则。