from flask import Flask

from .api_view import bp_api
from .admin_view import bp_admin




def init_app(app: Flask) -> Flask:
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_admin)
