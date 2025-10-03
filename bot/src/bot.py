#!/usr/bin/env python3
import logging
from json import dumps

from config import Config
from drone import Drone
from mqtt_app import MqttApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config.load()

drones = [
    Drone("ODYuOTUuMjEwLjI1MQ==", (0, 0), []),
]
for i in range(5):
    drones.append(Drone(f"drone{i}", Drone.random_position(), []))


def publish_state(mqtt: MqttApp):
    for drone in drones:
        drone.next_position()

        mqtt.publish(f"drone-game/client/{drone.drone_id}", dumps({
            "drone": drone.as_dict(),
            "game": {
                "drone_positions": [d.as_dict() for d in drones]
            }
        }))


if __name__ == '__main__':
    mqtt_app = MqttApp(config.mqtt_broker_config, config.client_id)
    mqtt_app.loop_func = publish_state, config.interval
    mqtt_app.start()
