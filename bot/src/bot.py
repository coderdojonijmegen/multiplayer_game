#!/usr/bin/env python3
import logging
from json import dumps, loads

from book import Book, Position
from config import Config
from drone import Drone
from mqtt_app import MqttApp
from random import Random

CLIENTS_DRONE_GAME = "clients/drone-game/"
FALL_RATE = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config.load()

drones = []
books = []
book_shelf_x = 0

def reset_books():
    global books
    global book_shelf_x
    books.clear()
    book_shelf_x = Random().randint(1, 70)
    books = [
        Book(Position(book_shelf_x * 20, 700), True)
    ]


def publish_state(mqtt: MqttApp):
    if len(books) > 25:
        reset_books()
    books_y_that_reached_bottom = [b.position.y for b in books if b.reached_bottom is True]
    books_max_y = min(books_y_that_reached_bottom) if books_y_that_reached_bottom else 700
    for book in books:
        if not book.reached_bottom and book.position.y < (books_max_y - FALL_RATE):
            book.position.y += FALL_RATE
        elif not book.reached_bottom:
            book.reached_bottom = True
            logger.info(book)
    for drone in drones:
        mqtt.publish(f"drone-game/client/{drone.drone_id}", dumps({
            "drone": drone.as_dict(),
            "game": {
                "drone_positions": [d.as_dict() for d in drones],
                "books": [b.as_dict() for b in books],
            },
        }))


def stijgen(drone: Drone):
    drone.position.y += 1


def dalen(drone: Drone):
    drone.position.y -= 1


def naar_links(drone: Drone):
    drone.position.x -= 1


def naar_rechts(drone: Drone):
    drone.position.x += 1


def nop(drone: Drone):
    pass


direction = {
    "stijgen": stijgen,
    "dalen": dalen,
    "links": naar_links,
    "rechts": naar_rechts,
    "hangen": nop,
}

def release_book(drone: Drone):
    books.append(Book(Position(drone.position.x * 20, drone.position.y * 20 + 13)))
    drone.has_book = False
    logger.info(f"added book: {books[-1]}")

def fetch_book(drone: Drone):
    drone.has_book = True

actions = {
    "laatboekvallen": release_book,
    "pakboek": fetch_book,
    "geen": nop
}


def on_drone_message(topic, message):
    if topic.startswith(CLIENTS_DRONE_GAME):
        drone_id = topic.replace(CLIENTS_DRONE_GAME, "")
        drone = Drone(drone_id, Position(0,0))
        if message != "disconnected" and drone not in drones:
            drone = Drone(drone_id, Position(*Drone.random_position()))
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
            direction[action["richting"].lower()](drone)
            actions[action["actie"].lower()](drone)

    if topic.startswith("drone-game/client/") and topic.endswith("/config"):
        drone_id = topic.replace("drone-game/client/", "").replace("/config", "")
        if matched_drones := [d for d in drones if d.drone_id == drone_id]:
            drone = matched_drones[0]
            drone_config = loads(message)
            drone.name = drone_config["name"]
            drone.color = drone_config["color"]


if __name__ == '__main__':
    mqtt_app = MqttApp(config.mqtt_broker_config, config.client_id)
    mqtt_app.loop_func = publish_state, config.interval
    mqtt_app.on_message = on_drone_message, [
        (f"clients/drone-game/#", 0),
        (f"drone-game/client/#", 0)
    ]
    reset_books()
    mqtt_app.start()
