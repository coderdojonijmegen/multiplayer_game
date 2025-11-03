from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def as_dict(self):
        return {
            "x": self.x,
            "y": self.y
        }

@dataclass
class Drone:
    drone_id: str
    name: str
    color: str
    hasBook: bool
    position: Position

    def __post_init__(self):
        self.position = Position(**self.position)


@dataclass
class Action:
    direction: str
    fetch_book: bool = False
    released_book: bool = False

    def as_dict(self):
        return {
            "richting": self.direction,
            "actie": "laatBoekVallen" if self.released_book else "pakBoek" if self.fetch_book else "geen"
        }
