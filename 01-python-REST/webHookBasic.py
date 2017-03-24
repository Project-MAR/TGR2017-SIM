from flask import Flask, request, abort, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        return jsonify({'echo from server':request.json['data']})
    else:
        abort(400)


if __name__ == '__main__':
    app.run(port=8888, debug=True)