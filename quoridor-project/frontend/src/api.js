const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }

  return response.json();
}

export function createGame() {
  return request("/api/games", { method: "POST" });
}

export function movePlayer(gameId, player, direction) {
  return request(`/api/games/${gameId}/move`, {
    method: "POST",
    body: JSON.stringify({ player, direction }),
  });
}

export function placeWall(gameId, player, x, y, orientation) {
  return request(`/api/games/${gameId}/wall`, {
    method: "POST",
    body: JSON.stringify({ player, x, y, orientation }),
  });
}

