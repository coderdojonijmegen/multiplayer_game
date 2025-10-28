from dataclasses import dataclass


@dataclass
class MqttConfig:
    ip: str
    port: int
    username: str
    password: str
    websocket_path: str = None
    keep_alive_s: int = 10
