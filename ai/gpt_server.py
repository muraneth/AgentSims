from flask import Flask, request, jsonify
from flask_cors import CORS
# from app import App
import time
import os
from config import Config
from gpt.GPTClient import GPTClient

class App:
    def __init__(self, flask):
        self.flask = flask
        self.logger = flask.logger
        self.abs_path = os.path.dirname(os.path.realpath(__file__))

        # Load main configuration file.
        self.config = Config(os.path.join(self.abs_path, 'config', 'app.json'))
        self.gpt_client = GPTClient(self.config)

        # Set up log level.
        self.logger.setLevel(self.config.log_level)

        # Cached configration data.
        self.config_cache = {}

    # Call a command.
    def call_command(self, model, params=None):
        msg = list()
        if params.get("system"):
            msg.append({"role": "system", "content": params.get("system")})
        if params.get("user"):
            msg.append({"role": "user", "content": params.get("user")})
        return {"data": self.gpt_client.send_and_recv(msg, model)}

    # Get current timestamp, milliseconds.
    def get_nowtime(self):
        return int(time.time() * 1000)

    # Get current timestamp, seconds.
    def get_nowtime_seconds(self):
        return int(time.time())

# Create the flask object.
flask = Flask(__name__)
# TODO Real CORS.
CORS(flask)

# Create the app object.
app = App(flask)


# Route - /api
@flask.route('/api/<model>', methods=['POST'])
def api(model):
    resp = app.call_command(model, request.json)
    if 'error' in resp:
        return {'__error__': resp['error'], 'refresh': resp.get('doRefresh', True)}
    # print(resp['data'])
    return jsonify(resp['data'])


# Entrance
if __name__ == '__main__':
    app.logger.info("----------CryptoPro PyServer Started.----------")
    app.flask.run(host=app.config.gpt_host, port=app.config.gpt_port, debug=True)
    app.logger.info("----------CryptoPro PyServer Stopped.----------")
