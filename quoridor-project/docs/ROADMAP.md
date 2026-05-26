# Development Roadmap

## Phase 1: Foundation

- Extract game rules into a backend game engine.
- Add REST endpoints for creating games, moving players, and placing walls.
- Build a React board UI connected to the backend.
- Keep Pygame prototype as a reference.

## Phase 2: Complete Rules

- Add full Quoridor wall validation.
- Prevent walls that remove all paths to goal.
- Add explicit diagonal move selection.
- Add move history and replay-ready events.

## Phase 3: Product Systems

- Add accounts, JWT auth, profiles, and sessions.
- Add PostgreSQL persistence.
- Add match history, player statistics, leaderboards, and achievements.
- Add AI difficulty levels.

## Phase 4: Online Multiplayer

- Add WebSocket rooms.
- Add matchmaking and private lobbies.
- Add spectator mode.
- Add reconnect handling and server-authoritative timers.

## Phase 5: Polish And Launch

- Add sound settings, themes, onboarding, and accessibility improvements.
- Add Docker, GitHub Actions, deployment docs, logging, monitoring, and rate limiting.
- Add production Nginx and HTTPS guidance.

