def test_sum_get_happy(client):
    resp = client.get('/sum?a=3&b=5')
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json() == {"a": 3, "b": 5, "sum": 8}

def test_sum_post_json_happy(client):
    resp = client.post('/sum', json={"a": 3, "b": 5})
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.get_json() == {"a": 3, "b": 5, "sum": 8}

def test_sum_get_missing_a(client):
    resp = client.get('/sum?b=2')
    assert resp.status_code == 422
    assert resp.is_json
    body = resp.get_json()
    assert "errors" in body and body["errors"].get("a") == "required"

def test_sum_post_missing_b(client):
    resp = client.post('/sum', json={"a": 1})
    assert resp.status_code == 422
    assert resp.is_json
    body = resp.get_json()
    assert "errors" in body and body["errors"].get("b") == "required"

def test_sum_invalid_number(client):
    resp = client.post('/sum', json={"a": "x", "b": 2})
    assert resp.status_code == 422
    assert resp.is_json
    body = resp.get_json()
    assert "errors" in body and body["errors"].get("a") == "invalid"

def test_sum_float_result_non_integer(client):
    resp = client.post('/sum', json={"a": 2.5, "b": 1.2})
    assert resp.status_code == 200
    assert resp.is_json
    body = resp.get_json()
    # floating sum preserved when not integer
    assert abs(body["sum"] - 3.7) < 1e-9
