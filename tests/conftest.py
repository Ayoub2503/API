import os
import sys

# ensure project root is on sys.path so 'app' package can be imported when pytest runs
_here = os.path.abspath(os.path.dirname(__file__))
_project_root = os.path.abspath(os.path.join(_here, os.pardir))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    # ensure no persistent side-effects
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
