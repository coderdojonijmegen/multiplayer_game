#!/usr/bin/env python3

from json import dumps

from flask import Flask, request, jsonify, render_template
import base64

from config import Config
from mqtt_app import MqttApp

config = Config.load()


def init(mqtt_app: MqttApp):
    app = Flask(__name__)

    @app.route('/')
    def dashboard():
        return render_template("index.html"), 200

    @app.route('/game_client.html')
    def game_client():
        return render_template("game_client.html"), 200

    @app.route('/register', methods=['POST'])
    def register_player():
        client_ip = request.remote_addr
        client_id = base64.b64encode(client_ip.encode("ascii")).decode("ascii")
        mqtt_app.publish("drone-game/client/register", dumps({"client_id": client_id}))
        return jsonify({"client_id": client_id}), 200

    app.run(host="0.0.0.0", port=4000, debug=False)


if __name__ == '__main__':
    mqtt_app = MqttApp(config.mqtt_broker_config, "drone-game/server")
    mqtt_app.func = init
    mqtt_app.start()
