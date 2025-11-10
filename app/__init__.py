import os
import logging
import time
from flask import Flask, jsonify, request, g
from werkzeug.exceptions import HTTPException

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=False)

    # simple env-based config
    env = os.environ.get('FLASK_ENV', 'production')
    if env == 'development':
        app.config.update(DEBUG=True, ENV='development')
    else:
        app.config.update(DEBUG=False, ENV='production')

    # Configure logging: handler + formatter, level depends on DEBUG
    level = logging.DEBUG if app.config.get('DEBUG') else logging.INFO
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(level)

    # Ensure app.logger has the handler and level set
    app.logger.setLevel(level)
    # Avoid adding duplicate handlers on repeated create_app calls
    if not any(isinstance(h, logging.StreamHandler) for h in app.logger.handlers):
        app.logger.addHandler(handler)

    # Reduce werkzeug's verbosity in production, still INFO in dev
    logging.getLogger('werkzeug').setLevel(logging.INFO if not app.config.get('DEBUG') else logging.DEBUG)

    # register routes blueprint
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # request timing and structured request logging
    @app.before_request
    def _start_timer():
        g.start_time = time.time()

    @app.after_request
    def _log_request(response):
        try:
            duration_ms = int((time.time() - getattr(g, 'start_time', time.time())) * 1000)
        except Exception:
            duration_ms = 0
        app.logger.info(
            f"method={request.method} path={request.path} status={response.status_code} duration_ms={duration_ms}"
        )
        return response

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
