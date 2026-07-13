import os
import tempfile
from flask import Flask

def create_app(test_config=None):
    # Ajustamos las carpetas estáticas y de templates relativas a main.py
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max
    
    if test_config is not None:
        app.config.update(test_config)
        
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app
