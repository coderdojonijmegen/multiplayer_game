#!/usr/bin/env python3
import logging
from json import dumps, loads

from config import Config
from drone import Drone
from mqtt_app import MqttApp

CLIENTS_DRONE_GAME = "clients/drone-game/"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config.load()

drones = [
]


def publish_state(mqtt: MqttApp):
    for drone in drones:
        mqtt.publish(f"drone-game/client/{drone.drone_id}", dumps({
            "drone": drone.as_dict(),
            "game": {
                "drone_positions": [d.as_dict() for d in drones]
            }
        }))


def on_drone_message(topic, message):
    if topic.startswith(CLIENTS_DRONE_GAME):
        drone_id = topic.replace(CLIENTS_DRONE_GAME, "")
        drone = Drone(drone_id)
        if message != "disconnected" and drone not in drones:
            drone = Drone(drone_id, Drone.random_position())
            drones.append(drone)
            logger.info(f"added drone {drone.drone_id}")
        elif message == "disconnected" and drone in drones:
            drones.remove(drone)
            logger.info(f"removed drone {drone.drone_id}")

    if topic.startswith("drone-game/client/") and topic.endswith("/action"):
        drone_id = topic.replace("drone-game/client/", "").replace("/action", "")
        if matched_drones := [d for d in drones if d.drone_id == drone_id]:
            drone = matched_drones[0]
            action = loads(message)
            drone.position = action["position"]["x"], action["position"]["y"]


if __name__ == '__main__':
    mqtt_app = MqttApp(config.mqtt_broker_config, config.client_id)
    mqtt_app.loop_func = publish_state, config.interval
    mqtt_app.on_message = on_drone_message, [
        (f"clients/drone-game/#", 0),
        (f"drone-game/client/#", 0)
    ]
    mqtt_app.start()
