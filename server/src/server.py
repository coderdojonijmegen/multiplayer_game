#!/usr/bin/env python3
import base64
import logging
from json import dumps

from flask import Flask, request, jsonify, render_template

from config import Config
from mqtt_app import MqttApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config.load()


def init(mqtt_app: MqttApp):
    app = Flask(__name__)
    app.logger.handlers = logger.handlers

    @app.route('/')
    def dashboard():
        return render_template("index.html"), 200

    @app.route('/game_client.html')
    def game_client():
        return render_template("game_client.html"), 200

    @app.route('/register', methods=['POST'])
    def register_player():
        ip_behind_proxy = request.headers.environ[
            "HTTP_X_FORWARDED_FOR"] if "HTTP_X_FORWARDED_FOR" in request.headers.environ else None
        client_ip = ip_behind_proxy if ip_behind_proxy else request.remote_addr
        client_id = base64.b64encode(client_ip.encode("ascii")).decode("ascii")
        logger.info(f"client connected from {client_ip} with id {client_id}")
        mqtt_app.publish("drone-game/client/register", dumps({"client_id": client_id}))
        return jsonify({"client_id": client_id}), 200

    app.run(host="0.0.0.0", port=4000, debug=False)


if __name__ == '__main__':
    mqtt_app = MqttApp(config.mqtt_broker_config, config.client_id)
    mqtt_app.func = init
    mqtt_app.start()
