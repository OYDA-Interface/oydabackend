from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.connection_manager import connections_bp
    from app.routes.table_manager import table_manager_bp
    from app.routes.data_manager import data_bp

    app.register_blueprint(connections_bp)
    app.register_blueprint(table_manager_bp)
    app.register_blueprint(data_bp)
    
    return app