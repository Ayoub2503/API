import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=False)

    # simple env-based config
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        app.config.update(DEBUG=True)
    else:
        app.config.update(DEBUG=False)

    # register routes blueprint
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # global JSON exception handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            code = e.code or 500
            desc = getattr(e, 'description', None)
            if isinstance(desc, dict):
                body = desc
            else:
                body = {'error': str(desc) if desc else e.name}
            return jsonify(body), code

        app.logger.exception(e)
        return jsonify({'error': 'Internal server error'}), 500

    return app
