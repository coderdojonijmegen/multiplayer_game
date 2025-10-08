#!/usr/bin/env python3
import logging

from flask import Flask, request, jsonify, render_template

from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config.load()


def init():
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
        body = request.json
        ip_behind_proxy = request.headers.environ[
            "HTTP_X_FORWARDED_FOR"] if "HTTP_X_FORWARDED_FOR" in request.headers.environ else None
        client_ip = ip_behind_proxy if ip_behind_proxy else request.remote_addr
        client_id = f"{client_ip}/{body['role']}/{body['platform']}"
        logger.info(f"client connected from {client_ip} with id {client_id}")
        return jsonify({"client_id": client_id}), 200

    app.run(host="0.0.0.0", port=4000, debug=False)


if __name__ == '__main__':
    init()
