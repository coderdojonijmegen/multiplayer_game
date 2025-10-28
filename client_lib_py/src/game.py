#!/usr/bin/env python3

from game_client import GameClient
from game_client.game_state import Drone, Action

x_dir = "h"


def on_status_update(client: GameClient, drone: Drone, game: dict) -> None:
    global x_dir
    released_book = False
    has_book = drone.hasBook
    book_shelf_x = game["books"][0]["position"]["x"]/20
    book_shelf_y = min([b["position"]["y"]/20 for b in game["books"] if b["reachedBottom"] == True])

    if drone.position.y > book_shelf_y:
        x_dir = "s"
    elif drone.position.x > 80:
        x_dir = "l"
        has_book = False
    elif has_book and drone.position.x < book_shelf_x:
        x_dir = "r"
    elif has_book and drone.position.x == book_shelf_x:
        x_dir = "h"
        has_book = False
        released_book = True
    elif not has_book and drone.position.x > 0:
        x_dir = "l"
    elif not has_book and drone.position.x == 0:
        x_dir = "r"
        has_book = True

    action = Action(x_dir, has_book, released_book)
    print(action)
    client.send_action(action)


(GameClient(allow_multiple=True)
 .name("Octopus")
 .color("orange")
 .on_status_update(on_status_update)
 .start())
