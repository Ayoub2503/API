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

if __name__ == '__main__':
    app.run(debug=True)
