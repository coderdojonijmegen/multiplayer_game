from dataclasses import dataclass


@dataclass
class MqttConfig:
    ip: str
    port: int
    username: str = None
    password: str = None
    keep_alive_s: int = 10
