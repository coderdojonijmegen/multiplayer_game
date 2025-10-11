from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

@dataclass
class Book:
    position: Position
    reached_bottom: bool = False

    def as_dict(self) -> dict:
        return {
            "position": {
                "x": self.position.x,
                "y": self.position.y
            },
            "reachedBottom": self.reached_bottom
        }
