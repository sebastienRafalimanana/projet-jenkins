#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/hello/')
def hello_world():
    return 'Hello World!\n'

@app.route('/hello/<string:username>')
def hello_user(username):
    return f'Hello {username}!\n'

@app.route('/feature/<string:username>')
def feature_user(username):
    return f'this is a future for {username}!\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
