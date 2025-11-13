# Notes: curl for API work

This file contains documentation and practical examples for the curl command-line tool, intended for API debugging, testing and quick requests. Keep this separate from the main README.

## What is curl?
curl is a command-line tool to transfer data to or from a server using URL syntax. It supports many protocols (HTTP, HTTPS, FTP, etc.) and is widely used to interact with web APIs.

## Basic syntax
curl [options] <URL>

Example:
curl https://api.example.com/resource

## Commonly used options

- -X, --request <METHOD>
  Specify HTTP method (GET, POST, PUT, DELETE, PATCH...). curl chooses GET by default; use -X to override.

- -d, --data <DATA>
  Send data in a POST request. Automatically sets content-type to application/x-www-form-urlencoded unless you set headers.

  Example: curl -X POST -d "a=1&b=2" https://...

- --data-raw / --data-binary
  Send raw or binary data without curl stripping newlines or special characters.

- -H, --header <HEADER>
  Add a header (can be used multiple times).

  Example: curl -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" ...

- -u, --user <user:password>
  Basic authentication.

  Example: curl -u username:password https://...

- -b, --cookie
  Send cookies. -c to save cookies to a file.

- -F, --form <name=content>
  Submit multipart/form-data (useful for file uploads).

  Example: curl -F "file=@/path/to/file" https://...

- -I, --head
  Fetch HTTP headers only (send HEAD request).

- -L, --location
  Follow redirects. Useful when endpoints redirect to another URL.

- -v, --verbose
  Show request/response details (headers, TLS handshake). Good for debugging.

- -s, --silent
  Suppress progress meter and error messages (combine with -S to show errors).

- -o <file>
  Write output to a file instead of stdout.

- -O
  Save with remote filename.

- --max-time <seconds>
  Set a timeout for the whole operation.

- --insecure / -k
  Allow insecure server connections when using SSL (skip certificate verification). Use only for testing.

- --data-urlencode
  URL-encode data values automatically (useful for query-like data in POST).

- --compressed
  Request compressed response (adds Accept-Encoding: gzip).

## Working with JSON APIs

GET with query parameters:
curl "https://api.example.com/sum?a=3&b=5"

POST JSON:
curl -X POST https://api.example.com/sum \
  -H "Content-Type: application/json" \
  -d '{"a":3,"b":5}'

Note: Use single quotes in many shells to avoid interpolation; on Windows use double quotes and escape as needed.

POST with file contents as JSON:
curl -X POST https://api.example.com/ingest \
  -H "Content-Type: application/json" \
  --data-binary "@/path/to/file.json"

POST form data (application/x-www-form-urlencoded):
curl -X POST https://api.example.com/login \
  -d "username=alice&password=secret"

Multipart/form-data (file upload):
curl -X POST https://api.example.com/upload \
  -F "file=@./image.png" \
  -F "description=Sample image"

## Authentication and headers

Bearer token:
curl -H "Authorization: Bearer <TOKEN>" https://api.example.com/protected

Basic auth:
curl -u user:pass https://api.example.com/secure

Custom headers:
curl -H "X-Request-ID: 12345" -H "Accept: application/json" https://...

## Inspecting requests and responses

Verbose mode:
curl -v https://api.example.com

Show only response headers:
curl -I https://api.example.com

Show headers and response body (quiet progress):
curl -s -D - https://api.example.com

Save headers to file and body to another:
curl -s -D headers.txt -o body.bin https://...

## Handling redirects, retries and timeouts

Follow redirects:
curl -L http://short.url

Limit total time:
curl --max-time 10 https://api.example.com

Retry on transient failures:
curl --retry 3 --retry-delay 2 https://api.example.com

## Useful tips

- When troubleshooting, combine -v with -H to inspect exact headers sent.
- Use --data-binary when you need to send raw payload without modification.
- Use --data-urlencode for values that may contain special characters.
- Prefer -sS when scripting (silent but show errors).
- For reproducible API tests, script curl calls in shell scripts or use tools like httpie/Postman for richer UIs.

## Examples summary

1) Simple GET:
curl "https://api.example.com/users?limit=10"

2) POST JSON:
curl -X POST https://api.example.com/items -H "Content-Type: application/json" -d '{"name":"item"}'

3) Upload file:
curl -X POST https://api.example.com/upload -F "file=@./path/to/file.txt"

4) Authenticated request:
curl -H "Authorization: Bearer $TOKEN" https://api.example.com/me

5) Debugging:
curl -v -H "Content-Type: application/json" -d '{"a":1}' https://api.example.com/test

---

Keep this notes file for quick reference while developing and testing APIs locally or remotely.

# Notes: API tools & curl (quick reference)

## pytest — testing framework

pytest is a popular Python testing framework that simplifies writing and running automated tests. It discovers test files, runs test functions, and provides clear output and powerful fixtures.

### What pytest does
- Auto-discovers test files (test_*.py or *_test.py) and test functions (test_*).
- Runs tests in parallel or serially with clear pass/fail/skip reporting.
- Provides fixtures (reusable setup/teardown) and parametrization (run same test with different inputs).
- Integrates with CI/CD systems (GitHub Actions, GitLab CI, Jenkins).

### Installation
```bash
pip install pytest
```

### Basic usage
- Run all tests:
  pytest
- Run with verbose output:
  pytest -v
- Run quiet (minimal output):
  pytest -q
- Run a specific file:
  pytest tests/test_sum.py
- Run tests matching a name pattern:
  pytest -k "test_sum"

### Writing tests

Basic test function:
```python
def test_addition():
    assert 1 + 1 == 2
```

Test with parametrization (run same logic with multiple inputs):
```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (10, 20, 30),
    (-1, 1, 0),
])
def test_sum_values(a, b, expected):
    assert a + b == expected
```

Test with fixtures (shared setup/teardown):
```python
@pytest.fixture
def client(app):
    return app.test_client()

def test_endpoint(client):
    resp = client.get('/health')
    assert resp.status_code == 200
```

### Common assertions
- assert x == y — equality
- assert x != y — inequality
- assert x is None — None check
- assert x — truthiness
- assert "text" in response — membership
- pytest.raises(Exception) — exception handling

Example:
```python
def test_validation_error(client):
    resp = client.post('/sum', json={"a": "invalid"})
    assert resp.status_code == 422
    assert "errors" in resp.get_json()
```

### Fixtures

A fixture is a reusable setup function. Common patterns:

```python
# setup and teardown
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    yield app  # test runs here
    # cleanup after test (if needed)

# use fixture in test
def test_something(app):
    # app is injected by pytest
    assert app.config['TESTING']
```

Fixture scope:
- function (default): create/destroy per test
- class: per test class
- module: per test file
- session: once per test run

### Skipping and marking tests

Skip a test:
```python
@pytest.mark.skip(reason="not ready")
def test_future():
    pass
```

Mark as xfail (expected to fail):
```python
@pytest.mark.xfail
def test_broken():
    assert False
```

Custom markers (useful for CI):
```python
@pytest.mark.slow
def test_slow_operation():
    pass

# Run only fast tests: pytest -m "not slow"
```

### Configuration (pytest.ini)

Create a pytest.ini file in project root to customize behavior:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

Common options:
- testpaths: where to find tests
- python_files: pattern for test files
- addopts: default command-line arguments
- markers: define custom markers

### GitHub Actions CI configuration

Create a .github/workflows/tests.yml to run pytest on every push/PR:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest -v
```

What this does:
- Triggers on pushes to main/develop and PRs.
- Tests on Python 3.9, 3.10, and 3.11 (matrix).
- Installs dependencies.
- Runs pytest with verbose output.

Advanced: add coverage report
```yaml
      - name: Run tests with coverage
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### Common pytest plugins
- pytest-cov: code coverage reporting
- pytest-xdist: parallel test execution
- pytest-timeout: set test timeouts
- pytest-mock: mock fixtures

Install:
```bash
pip install pytest-cov pytest-xdist
```

### Tips
- Keep tests focused and isolated (each test should be independent).
- Use fixtures to DRY up common setup.
- Parametrize to test multiple scenarios with one test function.
- Use meaningful test names: test_<function>_<condition>_<expected_outcome>.
- In CI, test against multiple Python versions.
