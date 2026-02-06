print('Starting Flask application...')

# 导入必要的模块
try:
    from flask import Flask, render_template
    print('Flask imported successfully')
except ImportError as e:
    print(f'Error importing Flask: {e}')
    exit(1)

try:
    from flask_cors import CORS
    print('Flask-CORS imported successfully')
except ImportError as e:
    print(f'Error importing Flask-CORS: {e}')
    exit(1)

try:
    from config import Config
    print('Config imported successfully')
except ImportError as e:
    print(f'Error importing Config: {e}')
    exit(1)

try:
    from app.models import db
    print('Database imported successfully')
except ImportError as e:
    print(f'Error importing database: {e}')
    exit(1)

try:
    from app.api import api_bp
    print('API blueprint imported successfully')
except ImportError as e:
    print(f'Error importing API blueprint: {e}')
    exit(1)

# 创建Flask应用实例
try:
    print('Creating Flask app instance...')
    # 配置模板目录路径
    import os
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'static'))
    print(f'Template directory: {template_dir}')
    print(f'Static directory: {static_dir}')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    print('Flask app instance created successfully')
except Exception as e:
    print(f'Error creating Flask app: {e}')
    exit(1)

# 加载配置
try:
    print('Loading configuration...')
    app.config.from_object(Config)
    print('Configuration loaded successfully')
except Exception as e:
    print(f'Error loading configuration: {e}')
    exit(1)

# 启用CORS
try:
    print('Enabling CORS...')
    CORS(app)
    print('CORS enabled successfully')
except Exception as e:
    print(f'Error enabling CORS: {e}')
    exit(1)

# 初始化数据库
try:
    print('Initializing database...')
    with app.app_context():
        db.init_app(app)
        print('Database initialized successfully')
        
        print('Creating database tables...')
        db.create_all()
        print('Database tables created successfully')
except Exception as e:
    print(f'Database error: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

# 注册蓝图
try:
    print('Registering API blueprint...')
    app.register_blueprint(api_bp, url_prefix='/api')
    print('API blueprint registered successfully')
except Exception as e:
    print(f'Error registering blueprint: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

# 首页路由
@app.route('/')
def index():
    print('Serving index page')
    return render_template('index.html')

# 新闻列表路由
@app.route('/news')
def news_list():
    print('Serving news list page')
    try:
        return render_template('news_list.html')
    except Exception as e:
        print(f'Error rendering news_list.html: {e}')
        return f'Error: {e}'

# 热度排行榜路由
@app.route('/hot-rank')
def hot_rank():
    print('Serving hot rank page')
    try:
        return render_template('hot_rank.html')
    except Exception as e:
        print(f'Error rendering hot_rank.html: {e}')
        return f'Error: {e}'

# 数据分析路由
@app.route('/analysis')
def analysis():
    print('Serving analysis page')
    try:
        return render_template('analysis.html')
    except Exception as e:
        print(f'Error rendering analysis.html: {e}')
        return f'Error: {e}'

# 设置页面路由
@app.route('/settings')
def settings():
    print('Serving settings page')
    try:
        return render_template('settings.html')
    except Exception as e:
        print(f'Error rendering settings.html: {e}')
        return f'Error: {e}'

# 运行应用程序
if __name__ == '__main__':
    try:
        print('Starting Flask development server...')
        print(f'Server will run on http://127.0.0.1:5000')
        print('Press Ctrl+C to stop the server')
        app.run(debug=True)
    except Exception as e:
        print(f'Error starting server: {e}')
        import traceback
        traceback.print_exc()
        exit(1)