from dataclasses import dataclass
from random import randint


@dataclass
class Drone:
    drone_id: str
    position: tuple[int, int] = (0, 0)
    has_book: bool = False
    path: list[tuple[int, int]] = None
    position_next: tuple[int, int] = None
    idx: int = 0

    def __post_init__(self):
        self.position_next = self.path[0] if self.path else self.random_position()

    @staticmethod
    def random_position():
        return randint(0, 100), randint(0, 60)

    def next_position(self) -> None:
        path_idx = self.idx % len(self.path) if self.path else 0
        if self.position == self.position_next:
            self.idx += 1
            self.position_next = self.path[path_idx] if self.path else self.random_position()
        next_pos_x, next_pos_y = self.position_next
        x, y = self.position
        if x == next_pos_x:
            x_dir = 0
        elif next_pos_x > x:
            x_dir = 1
        else:
            x_dir = -1
        dy = next_pos_y - y
        dx = next_pos_x - x
        a = dy / dx if dx != 0 else 100000
        b = next_pos_y - a * next_pos_x
        next_x = x + x_dir
        next_y = int(a * next_x + b)
        self.position = (next_x, next_y)

    def as_dict(self) -> dict:
        return {
            "drone_id": self.drone_id,
            "position": {
                "x": self.position[0],
                "y": self.position[1]
            },
            "hasBook": self.has_book
        }

    def __eq__(self, other):
        return self.drone_id == other.drone_id
