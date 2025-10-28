from dataclasses import dataclass

from mqtt_app import MqttConfig


@dataclass
class Config:
    mqtt_broker_config: MqttConfig
    server_host: str

    def __post_init__(self):
        self.mqtt_broker_config = MqttConfig(**self.mqtt_broker_config)

    @staticmethod
    def load():
        try:
            return Config(**{
                "mqtt_broker_config": {
                    "ip": "drone-game.coderdojo-nijmegen.nl",
                    "port": 443,
                    "websocket_path": "/mqtt",
                    "username": "ninja",
                    "password": "welkom!",
                },
                "server_host": "http://localhost:4000"
            })
        except KeyError as e:
            print(str(e.add_note("Did you set the environment variables?")))
            raise e
