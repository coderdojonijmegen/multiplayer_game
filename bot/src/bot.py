#!/usr/bin/env python3
import logging
from json import dumps, loads

from config import Config
from drone import Drone
from mqtt_app import MqttApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config.load()

gamer_drone = Drone("127.0.0.1/gamer", (0, 0), [])
drones = [
    Drone(config.dashboard_client_id, (0, 0), []),
]
for i in range(5):
    drones.append(Drone(f"drone{i}", Drone.random_position(), []))


def publish_state(mqtt: MqttApp):
    for drone in drones:
        if drone.drone_id != "127.0.0.1/gamer":
            drone.next_position()

        mqtt.publish(f"drone-game/client/{drone.drone_id}", dumps({
            "drone": drone.as_dict(),
            "game": {
                "drone_positions": [d.as_dict() for d in drones]
            }
        }))


def on_drone_message(topic, message):
    if topic == "clients/drone-game/127.0.0.1/gamer":
        gamer_drone.position = (0, 10)
        if gamer_drone not in drones:
            drones.append(gamer_drone)
            logger.info(f"added drone {gamer_drone.drone_id}")
    if topic == "drone-game/client/127.0.0.1/gamer/action":
        action = loads(message)
        gamer_drone.position = action["position"]["x"], action["position"]["y"]
        # logger.info(gamer_drone)


if __name__ == '__main__':
    mqtt_app = MqttApp(config.mqtt_broker_config, config.client_id)
    mqtt_app.loop_func = publish_state, config.interval
    mqtt_app.on_message = on_drone_message, [
        ("clients/drone-game/127.0.0.1/gamer", 0),
        ("drone-game/client/127.0.0.1/gamer/action", 0)
    ]
    mqtt_app.start()
