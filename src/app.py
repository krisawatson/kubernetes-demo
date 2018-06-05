from flask import Flask
from flask import request
import json
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
    with open(FILE, mode='w') as f:
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
    config_file = os.environ['CONFIG']
    if config_file.startswith('file:'):
        config_file = config_file.replace('file:', '', 1)
    with open(config_file) as conf:
        config = json.load(conf)
        try:
            config_value = config[value]
        except KeyError:
            return '{} does not exist'.format(value)
    return config_value


# @app.route('/delete', methods=['DELETE'])
# def delete_from_file():
#     if os.path.isfile(FILE):
#         os.remove(FILE)
#     return "Success"


def _read_file():
    content = None
    if os.path.isfile(FILE):
        with open(FILE, 'r') as file:
            content = file.read()
    return content


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8237)
