from app.game.engine import GameState


class GameStore:
    def __init__(self) -> None:
        self._games: dict[str, GameState] = {}

    def create_game(self) -> GameState:
        game = GameState.create()
        self._games[game.id] = game
        return game

    def get_game(self, game_id: str) -> GameState | None:
        return self._games.get(game_id)


game_store = GameStore()

