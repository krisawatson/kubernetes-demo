from flask import Flask
from flask import request
import json
import os
import os.path


FILE = '/tmp/data/test.txt'
app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return json.dumps({"status": "UP"}, indent=4)


@app.route('/write', methods=['POST'])
def write_to_file():
    content = _read_file()

    values = []
    if content:
        values = content.split(",")
    values.append(request.data)
    line = ','.join(str(v) for v in values)
    with open(FILE, mode='w+') as f:
        f.write(line)

    return "Success"


@app.route('/read/file', methods=['GET'])
def read_from_file():
    content = _read_file()

    values = []
    if content:
        values = content.split(",")

    return '\n'.join(values)


@app.route('/read/config/<value>', methods=['GET'])
def read_from_config(value):
    config_file = _get_config_file()
    with open(config_file) as conf:
        config = json.load(conf)
        try:
            config_value = config[value]
        except KeyError:
            return '{} does not exist'.format(value)
    return config_value


@app.route('/hello/<name>', methods=['GET'])
def say_hello(name):
    return 'Hello ' + name


@app.route('/secret', methods=['GET'])
def get_secret():
    return _get_secret()


@app.route('/crash', methods=['GET'])
def crash():
    os._exit(0)


def _read_file():
    content = None
    if os.path.isfile(FILE):
        with open(FILE, 'r') as file:
            content = file.read()
    return content


def _get_config_file():
    config_file = '/etc/config/config.json'
    return config_file


def _get_secret():
    with open('/etc/demo-secret/guilty-secret') as secret:
        return secret.read()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8237)
