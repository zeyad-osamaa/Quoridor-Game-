from dataclasses import dataclass, field
from uuid import uuid4


BOARD_SIZE = 9
MAX_WALL_COORD = 7
PLAYERS = ("P1", "P2")
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}


@dataclass
class Wall:
    x: int
    y: int
    orientation: str


@dataclass
class PlayerState:
    x: int
    y: int
    walls: int = 10


@dataclass
class GameState:
    id: str = field(default_factory=lambda: str(uuid4()))
    players: dict[str, PlayerState] = field(default_factory=dict)
    walls: list[Wall] = field(default_factory=list)
    current_player: str = "P1"
    winner: str | None = None

    @classmethod
    def create(cls) -> "GameState":
        return cls(
            players={
                "P1": PlayerState(x=4, y=0),
                "P2": PlayerState(x=4, y=8),
            }
        )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "players": {
                player: {"x": state.x, "y": state.y, "walls": state.walls}
                for player, state in self.players.items()
            },
            "walls": [
                {"x": wall.x, "y": wall.y, "orientation": wall.orientation}
                for wall in self.walls
            ],
            "current_player": self.current_player,
            "winner": self.winner,
        }

    def move(self, player: str, direction: str) -> bool:
        if self.winner is not None or player != self.current_player:
            return False

        if direction not in DIRECTIONS:
            return False

        state = self.players[player]
        dx, dy = DIRECTIONS[direction]
        target_x = state.x + dx
        target_y = state.y + dy

        if not is_inside_board(target_x, target_y):
            return False

        if self.is_blocked(state.x, state.y, direction):
            return False

        if self.player_at(target_x, target_y) is None:
            return self.finish_move(player, target_x, target_y)

        jump_x = target_x + dx
        jump_y = target_y + dy

        can_jump_straight = (
            is_inside_board(jump_x, jump_y)
            and not self.is_blocked(target_x, target_y, direction)
            and self.player_at(jump_x, jump_y) is None
        )

        if can_jump_straight:
            return self.finish_move(player, jump_x, jump_y)

        for side_direction in diagonal_directions(direction):
            side_dx, side_dy = DIRECTIONS[side_direction]
            diagonal_x = target_x + side_dx
            diagonal_y = target_y + side_dy

            if not is_inside_board(diagonal_x, diagonal_y):
                continue

            if self.is_blocked(target_x, target_y, side_direction):
                continue

            if self.player_at(diagonal_x, diagonal_y) is not None:
                continue

            return self.finish_move(player, diagonal_x, diagonal_y)

        return False

    def place_wall(self, player: str, x: int, y: int, orientation: str) -> bool:
        if self.winner is not None or player != self.current_player:
            return False

        if self.players[player].walls <= 0:
            return False

        if orientation not in ("H", "V"):
            return False

        if not (0 <= x <= MAX_WALL_COORD and 0 <= y <= MAX_WALL_COORD):
            return False

        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return False

        self.walls.append(Wall(x=x, y=y, orientation=orientation))
        self.players[player].walls -= 1
        self.switch_turn()
        return True

    def finish_move(self, player: str, x: int, y: int) -> bool:
        self.players[player].x = x
        self.players[player].y = y

        if has_won(player, y):
            self.winner = player
        else:
            self.switch_turn()

        return True

    def switch_turn(self) -> None:
        self.current_player = "P2" if self.current_player == "P1" else "P1"

    def player_at(self, x: int, y: int) -> str | None:
        for player, state in self.players.items():
            if state.x == x and state.y == y:
                return player
        return None

    def is_blocked(self, x: int, y: int, direction: str) -> bool:
        for wall in self.walls:
            if wall.orientation == "H":
                if direction == "UP" and y == wall.y + 1 and x in (wall.x, wall.x + 1):
                    return True
                if direction == "DOWN" and y == wall.y and x in (wall.x, wall.x + 1):
                    return True

            if wall.orientation == "V":
                if direction == "LEFT" and x == wall.x + 1 and y in (wall.y, wall.y + 1):
                    return True
                if direction == "RIGHT" and x == wall.x and y in (wall.y, wall.y + 1):
                    return True

        return False


def is_inside_board(x: int, y: int) -> bool:
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def diagonal_directions(direction: str) -> list[str]:
    if direction in ("UP", "DOWN"):
        return ["LEFT", "RIGHT"]
    if direction in ("LEFT", "RIGHT"):
        return ["UP", "DOWN"]
    return []


def has_won(player: str, y: int) -> bool:
    return (player == "P1" and y == 8) or (player == "P2" and y == 0)

