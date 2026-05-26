# Quoridor Arena Architecture

## Current Prototype

The existing project is a working Pygame prototype. It has useful rule logic, but rendering, input handling, mutable board state, and game flow are tightly coupled. That is fine for learning and testing movement, but it is not enough for a scalable online game.

## Target Stack

- Backend: FastAPI, WebSockets, PostgreSQL, SQLAlchemy, Alembic, JWT auth.
- Frontend: React with Vite, component-based UI, responsive CSS, later WebSocket state sync.
- Game engine: Pure Python rules module with deterministic state transitions.
- Deployment: Docker Compose for local development, Docker images for production, Nginx/HTTPS at the edge.

## Folder Direction

- `backend/app`: API, WebSocket gateway, config, game engine, persistence.
- `frontend/src`: React UI, API client, components, themes, game board.
- `docs`: engineering decisions, roadmap, deployment notes.
- Original Pygame files remain available as a prototype while the web app matures.

## Major Decision

Game rules must live on the backend. The frontend can animate and predict, but the backend is the source of truth. This helps multiplayer fairness, anti-cheat checks, replays, and match history later.

