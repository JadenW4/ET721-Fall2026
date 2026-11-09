from flask import Flask, request, jsonify, render_template
from itertools import count

app = Flask(__name__)
items = {
    "1": {"name": "computer", "price": 980},
    "2": {"name": "bookbag", "price": 135},
    "3": {"name": "notebook", "price": 42},
}
next_id = count(4)
STUDENT_NAME = "Jaden Wiltshire"

@app.context_processor
def student_context():
    return {"student_name": STUDENT_NAME}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/items', methods=['POST', 'GET'])
def collection():
    if request.method == 'GET':
        return jsonify(items)
    data = request.get_json(silent=True) or {}
    name, price = data.get('name'), data.get('price')
    if not isinstance(name, str) or not name.strip() or isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return jsonify(error='Provide a name and a nonnegative numeric price.'), 400
    item_id = str(next(next_id))
    items[item_id] = {'name': name.strip(), 'price': price}
    return jsonify(id=item_id, item=items[item_id]), 201

@app.route('/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    if item_id not in items:
        if request.method == 'GET':
            return jsonify(error='Item not found'), 404
        return render_template('error.html', message='Item not found', item_id=item_id), 404
    if request.method == 'GET':
        return jsonify(items[item_id])
    if request.method == 'DELETE':
        deleted_item = items.pop(item_id)
        return render_template('delete.html', item_id=item_id, deleted_item=deleted_item)
    data = request.get_json(silent=True) or {}
    name, price = data.get('name'), data.get('price')
    if not isinstance(name, str) or not name.strip() or isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return render_template('error.html', message='Invalid item name or price', item_id=item_id), 400
    items[item_id] = {'name': name.strip(), 'price': price}
    return render_template('update.html', item_id=item_id, item=items[item_id])

if __name__ == '__main__':
    app.run(debug=True)
