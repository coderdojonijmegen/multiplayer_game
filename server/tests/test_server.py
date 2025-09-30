from json import dumps

from flask.cli import load_dotenv
from requests import post

from config import Config
from mqtt_app import MqttApp

load_dotenv()


def test_register_player():
    r = post("http://127.0.0.1:4000/register")
    r.raise_for_status()
    client_id = r.json()["client_id"]

    assert client_id == "MTI3LjAuMC4x"  # 127.0.0.1


def test_publish_status():
    def publish_state(mqttApp: MqttApp):
        mqttApp.publish("drone-game/client/state/MTcyLjMwLjAuMQ==", dumps({"status": "flying"}))

    config = Config.load()
    mqtt_app = MqttApp(config.mqtt_broker_config, "drone-game/server/test")
    mqtt_app.loop_func = publish_state, 1
    mqtt_app.start()
