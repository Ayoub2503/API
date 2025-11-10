from flask import Flask, request, jsonify

app = Flask(__name__)

def parse_number(value):
    try:
        # allow integers and floats
        if isinstance(value, (int, float)):
            return value
        return float(value)
    except Exception:
        return None

@app.route('/sum', methods=['GET', 'POST'])
def sum_endpoint():
    if request.method == 'GET':
        a = request.args.get('a', None)
        b = request.args.get('b', None)
    else:
        data = request.get_json(silent=True) or {}
        a = data.get('a')
        b = data.get('b')

    a_num = parse_number(a)
    b_num = parse_number(b)

    if a_num is None or b_num is None:
        return (
            jsonify({"error": "Both 'a' and 'b' are required and must be numbers."}),
            400,
        )

    result = a_num + b_num
    # if both were ints-like, return int; otherwise float
    if float(result).is_integer():
        result = int(result)

    return jsonify({"a": a_num, "b": b_num, "sum": result})

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
    a_num = parse_number(a_raw)
    b_num = parse_number(b_raw)

    if a_num is None or b_num is None:
        return jsonify({"error": "Both 'a' and 'b' are required and must be numbers."}), 400

    result = a_num * b_num
    if float(result).is_integer():
        result = int(result)

    return jsonify({"a": a_num, "b": b_num, "product": result}), 200

@app.route('/divide', methods=['GET', 'POST'])
def divide_endpoint():
    a_raw, b_raw = _get_a_b_from_request()
    a_num = parse_number(a_raw)
    b_num = parse_number(b_raw)

    if a_num is None or b_num is None:
        return jsonify({"error": "Both 'a' and 'b' are required and must be numbers."}), 400

    if b_num == 0:
        return jsonify({"error": "Division by zero is not allowed."}), 400

    result = a_num / b_num
    if float(result).is_integer():
        result = int(result)

    return jsonify({"a": a_num, "b": b_num, "quotient": result}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
