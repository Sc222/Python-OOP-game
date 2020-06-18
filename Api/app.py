from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return [];

if __name__ == '__main__':
    app.run(debug=True)