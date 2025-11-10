# API
This repository has as purpose an introduction to build API using python from scratch and the associated steps and methods available to build one.

## What is an API?
An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other. It defines the methods and data formats that applications can use to request and exchange information.

## Why Use APIs?
1. **Integration**: Enables different systems to work together seamlessly
2. **Modularity**: Allows for separate development of different components
3. **Security**: Provides controlled access to resources and data
4. **Scalability**: Makes it easier to update and maintain systems independently
5. **Efficiency**: Reduces development time by reusing existing services

## Building APIs with Python
### Popular Frameworks
- **Flask**: Lightweight and flexible
- **FastAPI**: Modern, fast, and async-capable
- **Django REST Framework**: Full-featured framework for Django

### Basic Implementation Steps
1. **Setup Environment**
   ```python
   pip install flask
   pip install fastapi
   ```

2. **Choose Architecture**

There are many kinds, but you’ll mostly deal with web APIs (also called HTTP APIs or REST APIs):
   - **RESTful API**
     - Representational State Transfer (REST)
     - Uses standard HTTP methods (GET, POST, PUT, DELETE)
     - Stateless communication
     - Resource-based URLs (e.g., /users, /products)
     - Best for: Web services, mobile apps, public APIs
   
   - **GraphQL**
     - Query language for APIs
     - Single endpoint for all data requests
     - Clients specify exactly what data they need
     - Reduces over-fetching and under-fetching of data
     - Best for: Complex data relationships, flexible data requirements
   
   - **RPC (Remote Procedure Call)**
     - Action-based instead of resource-based
     - Focuses on operations rather than data
     - Uses POST methods to execute procedures
     - Example: XML-RPC, gRPC
     - Best for: Microservices, internal APIs, real-time communication

3. **Key Components**
   - Endpoints (URLs)
   - HTTP Methods (GET, POST, PUT, DELETE)
   - Request/Response formats (JSON, XML)
   - Authentication/Authorization
   - Error handling

4. **Best Practices**
   - Use proper HTTP status codes
   - Implement input validation
   - Document your API
   - Include rate limiting
   - Follow security guidelines

## Simple sum API (example)

This repository includes a minimal example API that returns the sum of two numbers.

Features:
- GET /sum?a=1&b=2 — returns JSON { "a": 1, "b": 2, "sum": 3 }
- POST /sum with JSON body { "a": 1, "b": 2 } — returns the same JSON response
- Validates inputs and returns 400 for missing or non-numeric values

Run locally:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python app.py
   ```
   The server listens on http://127.0.0.1:5000 by default.

Example requests:
- GET:
  ```bash
  curl.exe "http://127.0.0.1:5000/sum?a=3&b=5" # we may need to add .exe sometimes
  ```
- POST:
  ```bash
  curl.exe -X POST -H "Content-Type: application/json" -d "{\"a\":3,\"b\":5}" http://127.0.0.1:5000/sum # in cmd the "" and '' may cause a problem in how cmd parse json
  ```

  ```bash
  Invoke-RestMethod -Uri "http://127.0.0.1:5000/sum" -Method POST -ContentType "application/json" -Body '{"a":3,"b":5}' # in powershell 
  ```
Response example:
```json
{ "a": 3, "b": 5, "sum": 8 }
```

## Flask components explained

This section explains the common Flask components you will encounter in the example app and in most Flask projects. Each item includes what it is, when to use it, and short example snippets.

1. Initialization (Flask instance)
   - What: Create the application object that holds configuration, URL map, views, and extensions.
   - When: Always at app startup.
   - Basic example:
     ```python
     from flask import Flask
     app = Flask(__name__)  # __name__ helps locate static files and templates
     ```
   - Factory pattern (recommended for larger apps):
     ```python
     def create_app(config_object=None):
         app = Flask(__name__)
         if config_object:
             app.config.from_object(config_object)
         # register blueprints, extensions here
         return app
     ```

2. Configuration
   - What: app.config stores settings (SECRET_KEY, DATABASE_URI, DEBUG, etc.).
   - Load methods: from_object, from_envvar, from_mapping, dotenv.
   - Example:
     ```python
     app.config.from_mapping(
         DEBUG=False,
         SECRET_KEY='change-me',
     )
     # or
     app.config.from_envvar('MYAPP_SETTINGS')
     ```

3. Routes and view functions (routing)
   - What: @app.route maps a URL and HTTP methods to a Python function.
   - Methods parameter restricts allowed HTTP verbs.
   - Example:
     ```python
     @app.route('/sum', methods=['GET', 'POST'])
     def sum_endpoint():
         # handle request
         return jsonify({...})
     ```
   - Use url_for('endpoint_name') to build URLs instead of hardcoding.

4. Request object
   - What: flask.request gives access to incoming HTTP data.
   - Common attributes:
     - request.args — query parameters (GET)
     - request.form — form-encoded POST data
     - request.get_json() — parsed JSON body
     - request.headers, request.cookies, request.method
   - Example:
     ```python
     a = request.args.get('a')          # GET /sum?a=1
     data = request.get_json(silent=True)  # POST JSON body
     ```

5. Responses and jsonify
   - What: Return values from view functions are converted to HTTP responses.
   - Use jsonify to produce proper application/json responses and correct headers.
   - Example:
     ```python
     from flask import jsonify
     return jsonify({"a": 1, "b": 2, "sum": 3}), 200
     ```

6. Error handling and abort
   - Use abort to raise HTTP errors, and register error handlers for custom responses.
   - Example:
     ```python
     from flask import abort

     if a is None:
         abort(400, description="Missing parameter 'a'")

     @app.errorhandler(400)
     def bad_request(e):
         return jsonify({"error": str(e)}), 400
     ```

7. Hooks (middleware-like)
   - before_request: run code before each request (auth, open DB session).
   - after_request: modify response globally (headers, logging).
   - teardown_request: cleanup (close DB connection) even on exceptions.
   - Example:
     ```python
     @app.before_request
     def before():
         # perform auth checks or set up resources
         pass

     @app.after_request
     def after(response):
         response.headers['X-App'] = 'MyAPI'
         return response
     ```

8. Application and request contexts
   - Flask uses contexts to make objects like current_app and request available globally inside a thread.
   - Use with app.app_context(): to run code that needs app resources outside a request (e.g., CLI, migrations).
   - Example:
     ```python
     from flask import current_app
     with app.app_context():
         print(current_app.name)
     ```

9. Blueprints (modular routing)
   - What: Encapsulate groups of routes, templates, static files; register them on the app.
   - Good for: larger apps, plugins, separating concerns.
   - Example:
     ```python
     from flask import Blueprint

     bp = Blueprint('math', __name__, url_prefix='/math')

     @bp.route('/sum')
     def sum():
         return jsonify({...})

     # in create_app:
     app.register_blueprint(bp)
     ```

### Blueprints — how they work and how to use them

Blueprints are Flask's mechanism for organizing related routes, templates and static files into reusable components. They let you define routes and handlers outside the main application object and register those groups on an app instance later. This promotes modularity, avoids circular imports and makes testing easier.

How they work (brief)
- Create a Blueprint object in a module and decorate functions with @bp.route(...).
- Register the Blueprint in your application factory with app.register_blueprint(bp, url_prefix=...).
- After registration the Blueprint's routes become part of the application's URL map.

Common patterns
- Group related endpoints (e.g., auth, api, admin) into separate blueprints.
- Use url_prefix to namespace routes (e.g., '/api', '/admin').
- Keep route logic in blueprints and app configuration/extensions in the factory.

Minimal example
```python
# app/routes.py
from flask import Blueprint, jsonify
bp = Blueprint('api', __name__)

@bp.route('/health')
def health():
    return jsonify({"status": "ok"})
```

```python
# app/__init__.py
from flask import Flask
from .routes import bp as api_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
```

Benefits
- Clear separation of concerns and easier collaboration on larger projects.
- Reusable route groups and simpler unit testing.
- Helps scale the application structure as features grow.

### Application factory pattern — brief explanation

The application factory is a function (commonly named create_app) that builds and returns a configured Flask application instance. Use it to create app instances for different environments (development, testing, production) and to delay registering extensions and blueprints until an app exists.

Why use it
- Enables per-environment configuration without global state.
- Makes testing easier (create a test app in your test setup).
- Avoids circular imports by postponing registration until runtime.
- Works cleanly with the Flask CLI (e.g., FLASK_APP="app:create_app").

Minimal example:
```python
# app/__init__.py
from flask import Flask

def create_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
```

10. Static files and templates
    - Flask serves static files placed in a "static" folder and renders templates using Jinja2 in the "templates" folder.
    - Example rendering:
      ```python
      from flask import render_template
      return render_template('index.html', title='Welcome')
      ```

11. Extensions and common tools
    - Many extensions exist: Flask-SQLAlchemy, Flask-Migrate, Flask-Login, Flask-CORS, Flask-Marshmallow.
    - Initialize extensions in factory pattern for better testability:
      ```python
      db = SQLAlchemy()
      def create_app():
          app = Flask(__name__)
          db.init_app(app)
          return app
      ```

12. Input validation and serialization
    - Validate and deserialize request payloads using libraries like Marshmallow, Pydantic (with FastAPI), or manual checks.
    - Example with simple check:
      ```python
      try:
          a = float(request.json['a'])
      except Exception:
          abort(400, description='a must be a number')
      ```

13. Logging and monitoring
    - Configure Python logging for the app and use structured logs for production.
    - Example:
      ```python
      import logging
      logging.basicConfig(level=logging.INFO)
      app.logger.info('App started')
      ```

14. Running and deployment
    - Development: use flask run (FLASK_APP=app.py) or python app.py with debug=True.
    - Production: use a WSGI server (gunicorn, uWSGI) and avoid debug mode.
    - Example gunicorn command:
      ```bash
      gunicorn -w 4 -b 0.0.0.0:8000 app:app
      ```

15. Testing
    - Use app.test_client() to simulate requests without running a server.
    - Example:
      ```python
      with app.test_client() as client:
          resp = client.get('/sum?a=1&b=2')
          assert resp.status_code == 200
      ```

16. Security considerations
    - Use HTTPS in production; protect secret keys; validate/escape user input; limit uploaded file types and sizes; apply rate limiting; enable CORS rules carefully.

17. Minimal sum endpoint explained (ties to example app.py)
    - GET: uses request.args to fetch query parameters a and b.
    - POST: uses request.get_json() to parse JSON body.
    - parse_number helper: converts values to numeric types and returns None for invalid input.
    - Return: a JSON payload with original numbers and their sum, or 400 with an error message if validation fails.

## New components (app factory, blueprints, validation & error handling)

This project was reorganized to use a Flask application factory and Blueprints to separate responsibilities and make the app easier to test and deploy.

- app/ (package)
  - Purpose: contains the application factory and route definitions so the app can be created/configured from code or by the Flask CLI.
  - Files:
    - app/__init__.py — create_app(config) factory
      - Creates and configures the Flask app (env-aware: FLASK_ENV).
      - Registers the routes Blueprint.
      - Registers a global JSON error handler so all HTTPExceptions and unexpected errors are returned as JSON.
    - app/routes.py — routes Blueprint (registered as "api")
      - Contains endpoint handlers: /sum, /multiply, /divide, /health.
      - Implements input validation helpers that raise werkzeug HTTP exceptions (e.g., UnprocessableEntity for validation errors).
      - Validation returns structured 422 responses for missing/invalid fields, e.g.
        { "errors": { "a": "required" } }

- app.py (root)
  - Purpose: a small entry script that calls app.create_app() to create the Flask app instance.
  - Allows running with `python app.py` and also supports the Flask CLI when using FLASK_APP=app:create_app.

- Validation & error handling
  - Validation:
    - Inputs are parsed with a stricter parser that rejects missing or non-numeric values.
    - Missing/invalid fields trigger a 422 Unprocessable Entity with a body like:
      { "errors": { "a": "required", "b": "invalid" } }
  - Error handling:
    - The factory registers a global exception handler that:
      - Converts werkzeug HTTPExceptions into JSON responses (honoring provided description dicts).
      - Logs unexpected exceptions and returns a 500 JSON response: { "error": "Internal server error" }.
    - Specific cases (e.g., division by zero) raise BadRequest (400) with JSON description.

- Running the app
  - Flask CLI (recommended)
    - Unix/macOS:
      export FLASK_APP="app:create_app"
      export FLASK_ENV=development   # optional
      flask run
    - Windows (cmd.exe):
      set FLASK_APP=app:create_app
      set FLASK_ENV=development
      flask run
    - Windows (PowerShell):
      $env:FLASK_APP = "app:create_app"
      $env:FLASK_ENV = "development"
      flask run
  - Direct:
    - python app.py

- Notes
  - The app now returns consistent JSON errors for validation and HTTP errors.
  - The separate routes file and factory pattern make it easier to add configuration, testing, or extensions (e.g., DB) later.
  - See notes/README.md for quick API tooling tips (curl, httpie, jq).

Additions above are concise guidance for maintainers and contributors to understand the new structure and how to run and extend the application.