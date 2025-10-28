from json import loads, dumps

from requests import post

from game_client.config import Config
from game_client.game_state import Drone, Action
from mqtt_app import MqttApp


class GameClient:

    def __init__(self, allow_multiple=False):
        self.config = Config.load()
        self._name = None
        self._color = None
        self.allow_multiple = allow_multiple
        self._on_message = None
        self._mqtt_client = None
        self._register_client()

    def _register_client(self):
        r = post(f"{self.config.server_host}/register", json={
            "role": "gamer",
            "platform": "py",
            "allowMultiple": self.allow_multiple
        })
        r.raise_for_status()
        self.client_id = r.json()["client_id"]

    def on_status_update(self, callback):
        self._on_message = callback
        return self

    def _handle_on_message(self, _, message):
        if self._on_message:
            state = loads(message)
            self._on_message(self, Drone(**state["drone"]), state["game"])

    def name(self, name: str):
        self._name = name
        return self

    def color(self, color: str):
        self._color = color
        return self

    def send_action(self, action: Action):
        # print(action)
        self._mqtt_client.publish(f"drone-game/client/{self.client_id}/action", dumps(action.as_dict()))

    def start(self) -> None:
        if not self._name or not self._color:
            raise RuntimeError("Name and color are required")
        self._mqtt_client = MqttApp(self.config.mqtt_broker_config, self.client_id)
        self._mqtt_client.on_message = self._handle_on_message, f"drone-game/client/{self.client_id}"
        self._mqtt_client.publish(f"drone-game/client/{self.client_id}/config",
                                  dumps({"name": self._name, "color": self._color}))
        self._mqtt_client.start()
