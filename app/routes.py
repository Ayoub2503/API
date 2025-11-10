from flask import Blueprint, request, jsonify
from werkzeug.exceptions import UnprocessableEntity, BadRequest

bp = Blueprint('api', __name__)

# strict parser returning (value, error_code)
def _parse_number_strict(value):
    if isinstance(value, (int, float)):
        return value, None
    if value is None:
        return None, 'required'
    s = str(value).strip()
    if s == '':
        return None, 'required'
    try:
        if '.' not in s and 'e' not in s and 'E' not in s:
            return int(s), None
        return float(s), None
    except ValueError:
        return None, 'invalid'

def validate_and_parse(a_raw, b_raw):
    errors = {}
    a_num, a_err = _parse_number_strict(a_raw)
    if a_err:
        errors['a'] = a_err
    b_num, b_err = _parse_number_strict(b_raw)
    if b_err:
        errors['b'] = b_err

    if errors:
        raise UnprocessableEntity(description={'errors': errors})

    return a_num, b_num

def _get_a_b_from_request():
    if request.method == 'GET':
        a = request.args.get('a', None)
        b = request.args.get('b', None)
    else:
        data = request.get_json(silent=True) or {}
        a = data.get('a')
        b = data.get('b')
    return a, b

@bp.route('/sum', methods=['GET', 'POST'])
def sum_endpoint():
    a_raw, b_raw = _get_a_b_from_request()
    a_num, b_num = validate_and_parse(a_raw, b_raw)
    result = a_num + b_num
    if float(result).is_integer():
        result = int(result)
    return jsonify({"a": a_num, "b": b_num, "sum": result}), 200

@bp.route('/multiply', methods=['GET', 'POST'])
def multiply_endpoint():
    a_raw, b_raw = _get_a_b_from_request()
    a_num, b_num = validate_and_parse(a_raw, b_raw)
    result = a_num * b_num
    if float(result).is_integer():
        result = int(result)
    return jsonify({"a": a_num, "b": b_num, "product": result}), 200

@bp.route('/divide', methods=['GET', 'POST'])
def divide_endpoint():
    a_raw, b_raw = _get_a_b_from_request()
    a_num, b_num = validate_and_parse(a_raw, b_raw)
    if b_num == 0:
        raise BadRequest(description={'error': 'Division by zero is not allowed.'})
    result = a_num / b_num
    if float(result).is_integer():
        result = int(result)
    return jsonify({"a": a_num, "b": b_num, "quotient": result}), 200

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200
