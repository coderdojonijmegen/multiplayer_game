from dataclasses import dataclass
from os import environ

from mqtt_app import MqttConfig


@dataclass
class Config:
    mqtt_broker_config: MqttConfig
    client_id: str
    dashboard_client_id: str
    gamer_client_id: str
    interval: float

    def __post_init__(self):
        self.mqtt_broker_config = MqttConfig(**self.mqtt_broker_config)

    @staticmethod
    def load():
        try:
            return Config(**{
                "mqtt_broker_config": {
                    "ip": environ["mqtt_ip"],
                    "port": int(environ["mqtt_port"]),
                    "websocket_path": environ.get("mqtt_websocket_path", None),
                    "username": environ["mqtt_username"],
                    "password": environ["mqtt_password"],
                },
                "client_id": environ.get("client_id", "drone-game/bot"),
                "interval": float(environ.get("interval", 0.2)),
                "dashboard_client_id": environ.get("dashboard_client_id", "86.95.210.251/dashboard"),
                "gamer_client_id": environ.get("gamer_client_id", "86.95.210.251/gamer"),
            })
        except KeyError as e:
            print(str(e.add_note("Did you set the environment variables?")))
            raise e
