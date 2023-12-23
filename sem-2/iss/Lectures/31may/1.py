from flask import Flask, jsonify, request
app = Flask(__name__)


@app.route('/')
def home():
    return "<h2>hello world<h2>"


@app.route('/json')
def json():
    return jsonify({'key': 'value', 'key2': [1, 2, 3]})


stores = [
    {
        'name': 'Tesco',
        'items': [
            {
                'name': 'My item',
                'price': 15.99
            }
        ]
    }
]


@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'], 'items': request_data['items']}
    stores.append(new_store)
    return jsonify(new_store)


if __name__ == '__main__':
    app.run(port=500)
