#!/usr/bin/env python3

from game_client import GameClient
from game_client.game_state import Drone, Action

x_dir = "rechts"


def on_status_update(client: GameClient, drone: Drone, game: dict) -> None:
    global x_dir
    released_book = False
    has_book = drone.hasBook
    book_shelf_x = int(game["books"][0]["position"]["x"]/20)
    book_shelf_y = int(min([b["position"]["y"]/20 for b in game["books"] if b["reachedBottom"] == True]))

    if x_dir == "stijgen" and drone.position.y < book_shelf_y:
        x_dir = "links"

    if drone.position.x <= 0:
        x_dir = "rechts"
    elif drone.position.x > 80:
        x_dir = "links"
    elif drone.position.y <= 0:
        x_dir = "dalen"
    elif drone.position.y >= 35:
        x_dir = "stijgen"

    if drone.position.x == 0 and not has_book:
        has_book = True

    if drone.position.x == book_shelf_x:
        if has_book:
            x_dir = "hangen"
            released_book = True
        else:
            x_dir = "links"

    action = Action(x_dir, has_book, released_book)
    print(drone)
    print(action)
    client.send_action(action)


(GameClient()
 .name("Octopus")
 .color("orange")
 .on_status_update(on_status_update)
 .start())
