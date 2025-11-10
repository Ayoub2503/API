from app import create_app

# create app with default config (FLASK_ENV can influence behavior)
app = create_app()

if __name__ == '__main__':
    # keep debug mode aligned with config
    app.run(debug=app.config.get('DEBUG', False))
