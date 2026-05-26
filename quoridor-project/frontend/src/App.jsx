import { useEffect, useState } from "react";
import { CirclePlay, RotateCcw } from "lucide-react";
import { createGame, movePlayer, placeWall } from "./api";
import "./styles.css";

const directions = [
  ["UP", "Up"],
  ["LEFT", "Left"],
  ["RIGHT", "Right"],
  ["DOWN", "Down"],
];

export default function App() {
  const [game, setGame] = useState(null);
  const [wallMode, setWallMode] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    startGame();
  }, []);

  async function startGame() {
    setError("");
    setWallMode(null);
    setGame(await createGame());
  }

  async function handleMove(direction) {
    if (!game || game.winner) {
      return;
    }

    try {
      setError("");
      setGame(await movePlayer(game.id, game.current_player, direction));
    } catch (err) {
      setError("Invalid move");
    }
  }

  async function handleCellClick(x, y) {
    if (!game || !wallMode || game.winner || x > 7 || y > 7) {
      return;
    }

    try {
      setError("");
      setGame(await placeWall(game.id, game.current_player, x, y, wallMode));
      setWallMode(null);
    } catch (err) {
      setError("Invalid wall placement");
    }
  }

  function playerAt(x, y) {
    if (!game) {
      return null;
    }

    return Object.entries(game.players).find(([, player]) => player.x === x && player.y === y)?.[0] ?? null;
  }

  return (
    <main className="shell">
      <section className="topbar">
        <div>
          <p className="eyebrow">Quoridor Arena</p>
          <h1>{game?.winner ? `${game.winner} wins` : `${game?.current_player ?? "P1"} to move`}</h1>
        </div>
        <button className="iconButton" onClick={startGame} title="New game">
          <RotateCcw size={20} />
        </button>
      </section>

      <section className="gameLayout">
        <div className="board" aria-label="Quoridor board">
          {Array.from({ length: 9 }).map((_, y) =>
            Array.from({ length: 9 }).map((__, x) => {
              const player = playerAt(x, y);
              return (
                <button
                  className={`cell ${player ? `cell${player}` : ""}`}
                  key={`${x}-${y}`}
                  onClick={() => handleCellClick(x, y)}
                  title={`Cell ${x}, ${y}`}
                >
                  {player}
                </button>
              );
            })
          )}

          {game?.walls.map((wall, index) => (
            <span
              className={`wall wall${wall.orientation}`}
              key={`${wall.x}-${wall.y}-${index}`}
              style={{
                "--x": wall.x,
                "--y": wall.y,
              }}
            />
          ))}
        </div>

        <aside className="panel">
          <button className="primaryAction" onClick={startGame}>
            <CirclePlay size={18} />
            New Match
          </button>

          <div className="controlGrid">
            {directions.map(([value, label]) => (
              <button key={value} onClick={() => handleMove(value)}>
                {label}
              </button>
            ))}
          </div>

          <div className="wallControls">
            <button className={wallMode === "H" ? "selected" : ""} onClick={() => setWallMode("H")}>
              Horizontal Wall
            </button>
            <button className={wallMode === "V" ? "selected" : ""} onClick={() => setWallMode("V")}>
              Vertical Wall
            </button>
          </div>

          <div className="stats">
            <p>P1 walls: {game?.players.P1.walls ?? 10}</p>
            <p>P2 walls: {game?.players.P2.walls ?? 10}</p>
            {wallMode && <p>Click a board square to place a {wallMode} wall.</p>}
            {error && <p className="error">{error}</p>}
          </div>
        </aside>
      </section>
    </main>
  );
}

