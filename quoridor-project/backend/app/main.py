from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.schemas import MoveRequest, WallRequest
from app.store import game_store


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name}


@app.post("/api/games")
def create_game() -> dict:
    return game_store.create_game().serialize()


@app.get("/api/games/{game_id}")
def get_game(game_id: str) -> dict:
    game = game_store.get_game(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.serialize()


@app.post("/api/games/{game_id}/move")
def move_player(game_id: str, request: MoveRequest) -> dict:
    game = game_store.get_game(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game.move(request.player, request.direction):
        raise HTTPException(status_code=400, detail="Invalid move")

    return game.serialize()


@app.post("/api/games/{game_id}/wall")
def place_wall(game_id: str, request: WallRequest) -> dict:
    game = game_store.get_game(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if not game.place_wall(request.player, request.x, request.y, request.orientation):
        raise HTTPException(status_code=400, detail="Invalid wall placement")

    return game.serialize()


@app.websocket("/ws/games/{game_id}")
async def game_socket(websocket: WebSocket, game_id: str) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.receive_text()
            game = game_store.get_game(game_id)
            if game is None:
                await websocket.send_json({"error": "Game not found"})
            else:
                await websocket.send_json(game.serialize())
    except WebSocketDisconnect:
        return

