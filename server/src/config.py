from dataclasses import dataclass
from os import environ

from mqtt_app import MqttConfig


@dataclass
class Config:
    mqtt_broker_config: MqttConfig

    def __post_init__(self):
        self.mqtt_broker_config = MqttConfig(**self.mqtt_broker_config)

    @staticmethod
    def load():
        try:
            return Config(**{
                "mqtt_broker_config": {
                    "ip": environ["mqtt_ip"],
                    "port": int(environ["mqtt_port"]),
                    "username": environ["mqtt_username"],
                    "password": environ["mqtt_password"],
                },
            })
        except KeyError as e:
            print(str(e.add_note("Did you set the environment variables?")))
            raise e
