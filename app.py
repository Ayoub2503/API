from flask import Flask, request, jsonify
from werkzeug.exceptions import UnprocessableEntity, BadRequest, HTTPException

app = Flask(__name__)

# replace the old parse_number with a stricter parser that returns (value, error_code)
def _parse_number_strict(value):
    if isinstance(value, (int, float)):
        return value, None
    if value is None:
        return None, 'required'
    s = str(value).strip()
    if s == '':
        return None, 'required'
    try:
        # prefer int when appropriate
        if '.' not in s and 'e' not in s and 'E' not in s:
            return int(s), None
        return float(s), None
    except ValueError:
        return None, 'invalid'

def validate_and_parse(a_raw, b_raw):
    """
    Validate raw inputs a_raw and b_raw.
    On success returns (a_num, b_num).
    On validation errors raises UnprocessableEntity with description {'errors': {...}}.
    """
    errors = {}
    a_num, a_err = _parse_number_strict(a_raw)
    if a_err:
        errors['a'] = a_err
    b_num, b_err = _parse_number_strict(b_raw)
    if b_err:
        errors['b'] = b_err

    if errors:
        # raise 422 with structured error body
        raise UnprocessableEntity(description={'errors': errors})

    return a_num, b_num

@app.route('/sum', methods=['GET', 'POST'])
def sum_endpoint():
    # re-use existing extractor
    if request.method == 'GET':
        a_raw = request.args.get('a', None)
        b_raw = request.args.get('b', None)
    else:
        data = request.get_json(silent=True) or {}
        a_raw = data.get('a')
        b_raw = data.get('b')

    a_num, b_num = validate_and_parse(a_raw, b_raw)

    result = a_num + b_num
    if float(result).is_integer():
        result = int(result)

    return jsonify({"a": a_num, "b": b_num, "sum": result}), 200

def _get_a_b_from_request():
    # helper to extract a and b from GET query params or POST JSON
    if request.method == 'GET':
        a = request.args.get('a', None)
        b = request.args.get('b', None)
    else:
        data = request.get_json(silent=True) or {}
        a = data.get('a')
        b = data.get('b')
    return a, b

@app.route('/multiply', methods=['GET', 'POST'])
def multiply_endpoint():
    a_raw, b_raw = _get_a_b_from_request()
    a_num, b_num = validate_and_parse(a_raw, b_raw)

    result = a_num * b_num
    if float(result).is_integer():
        result = int(result)

    return jsonify({"a": a_num, "b": b_num, "product": result}), 200

@app.route('/divide', methods=['GET', 'POST'])
def divide_endpoint():
    a_raw, b_raw = _get_a_b_from_request()
    a_num, b_num = validate_and_parse(a_raw, b_raw)

    if b_num == 0:
        # use werkzeug BadRequest for a 400 response with a clear message
        raise BadRequest(description={'error': 'Division by zero is not allowed.'})

    result = a_num / b_num
    if float(result).is_integer():
        result = int(result)

    return jsonify({"a": a_num, "b": b_num, "quotient": result}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.errorhandler(Exception)
def handle_exception(e):
    """
    Global exception handler that returns JSON for both HTTPExceptions and unexpected errors.
    - For HTTPException: return the provided code and use description (if dict, return as-is).
    - For other exceptions: log and return generic 500 JSON response.
    """
    if isinstance(e, HTTPException):
        code = e.code or 500
        desc = getattr(e, 'description', None)
        if isinstance(desc, dict):
            body = desc
        else:
            body = {'error': str(desc) if desc else e.name}
        return jsonify(body), code

    # unexpected error
    app.logger.exception(e)
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
