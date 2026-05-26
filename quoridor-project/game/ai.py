import random
from collections import deque

from game.board import Cell
from game.rules import is_blocked, is_inside_board, move_player, place_wall
from game.walls import Wall


DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]


def clone_board(board):
    board_copy = []

    for y in range(9):
        row = []

        for x in range(9):
            cell = Cell(x, y)
            cell.player = board[y][x].player
            row.append(cell)

        board_copy.append(row)

    return board_copy


def clone_walls(walls):
    return [Wall(wall.x, wall.y, wall.orientation) for wall in walls]


def clone_players(players):
    return {
        "P1": {"x": players["P1"]["x"], "y": players["P1"]["y"]},
        "P2": {"x": players["P2"]["x"], "y": players["P2"]["y"]},
    }


def clone_player_walls(player_walls):
    return {"P1": player_walls["P1"], "P2": player_walls["P2"]}


def opponent_of(player):
    return "P1" if player == "P2" else "P2"


def goal_row(player):
    return 8 if player == "P1" else 0


def shortest_path_distance(walls, start_x, start_y, player):
    visited = {(start_x, start_y)}
    queue = deque([(start_x, start_y, 0)])

    while queue:
        current_x, current_y, distance = queue.popleft()

        if current_y == goal_row(player):
            return distance

        for direction in DIRECTIONS:
            if is_blocked(walls, current_x, current_y, direction):
                continue

            if direction == "UP":
                new_x, new_y = current_x, current_y - 1
            elif direction == "DOWN":
                new_x, new_y = current_x, current_y + 1
            elif direction == "LEFT":
                new_x, new_y = current_x - 1, current_y
            else:
                new_x, new_y = current_x + 1, current_y

            if is_inside_board(new_x, new_y) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                queue.append((new_x, new_y, distance + 1))

    return 99


def legal_move_actions(board, walls, players, player):
    actions = []

    for direction in DIRECTIONS:
        board_copy = clone_board(board)
        walls_copy = clone_walls(walls)
        x = players[player]["x"]
        y = players[player]["y"]
        moved, new_x, new_y = move_player(board_copy, walls_copy, x, y, direction, player)

        if moved:
            actions.append({"type": "move", "direction": direction, "x": new_x, "y": new_y})

    return actions


def wall_search_positions(players):
    positions = set()

    for player in players:
        player_x = players[player]["x"]
        player_y = players[player]["y"]

        for y in range(player_y - 2, player_y + 3):
            for x in range(player_x - 2, player_x + 3):
                if 0 <= x <= 7 and 0 <= y <= 7:
                    positions.add((x, y))

    return positions


def legal_wall_actions(board, walls, player_walls, players, player, nearby_only):
    if player_walls[player] <= 0:
        return []

    if nearby_only:
        positions = wall_search_positions(players)
    else:
        positions = [(x, y) for y in range(8) for x in range(8)]

    actions = []

    for x, y in positions:
        for orientation in ["H", "V"]:
            board_copy = clone_board(board)
            walls_copy = clone_walls(walls)
            walls_left_copy = clone_player_walls(player_walls)
            players_copy = clone_players(players)

            if place_wall(board_copy, walls_copy, walls_left_copy, players_copy, player, x, y, orientation):
                actions.append({"type": "wall", "x": x, "y": y, "orientation": orientation})

    return actions


def evaluate_position(walls, player_walls, players, ai_player):
    opponent = opponent_of(ai_player)
    ai_distance = shortest_path_distance(walls, players[ai_player]["x"], players[ai_player]["y"], ai_player)
    opponent_distance = shortest_path_distance(walls, players[opponent]["x"], players[opponent]["y"], opponent)
    wall_score = (player_walls[ai_player] - player_walls[opponent]) * 0.2

    return opponent_distance - ai_distance + wall_score


def score_action(board, walls, player_walls, players, ai_player, action):
    board_copy = clone_board(board)
    walls_copy = clone_walls(walls)
    walls_left_copy = clone_player_walls(player_walls)
    players_copy = clone_players(players)

    if action["type"] == "move":
        moved, new_x, new_y = move_player(
            board_copy,
            walls_copy,
            players_copy[ai_player]["x"],
            players_copy[ai_player]["y"],
            action["direction"],
            ai_player,
        )

        if not moved:
            return -999

        players_copy[ai_player]["x"] = new_x
        players_copy[ai_player]["y"] = new_y

        if new_y == goal_row(ai_player):
            return 999
    else:
        placed = place_wall(
            board_copy,
            walls_copy,
            walls_left_copy,
            players_copy,
            ai_player,
            action["x"],
            action["y"],
            action["orientation"],
        )

        if not placed:
            return -999

    return evaluate_position(walls_copy, walls_left_copy, players_copy, ai_player)


def choose_shortest_path_move(board, walls, players, player):
    moves = legal_move_actions(board, walls, players, player)

    if not moves:
        return None

    best_distance = 99
    best_moves = []

    for move in moves:
        distance = shortest_path_distance(walls, move["x"], move["y"], player)

        if distance < best_distance:
            best_distance = distance
            best_moves = [move]
        elif distance == best_distance:
            best_moves.append(move)

    return random.choice(best_moves)


def choose_ai_action(board, walls, player_walls, players, ai_player="P2", level="medium"):
    level = level.lower()
    moves = legal_move_actions(board, walls, players, ai_player)

    if not moves:
        return None

    if level == "easy":
        if random.random() < 0.8 or player_walls[ai_player] <= 0:
            return random.choice(moves)

        walls_available = legal_wall_actions(board, walls, player_walls, players, ai_player, True)
        return random.choice(walls_available) if walls_available else random.choice(moves)

    best_move = max(moves, key=lambda action: score_action(board, walls, player_walls, players, ai_player, action))

    if level == "medium":
        opponent = opponent_of(ai_player)
        opponent_distance = shortest_path_distance(walls, players[opponent]["x"], players[opponent]["y"], opponent)

        if player_walls[ai_player] > 0 and opponent_distance <= 4:
            wall_actions = legal_wall_actions(board, walls, player_walls, players, ai_player, True)

            if wall_actions:
                best_wall = max(
                    wall_actions,
                    key=lambda action: score_action(board, walls, player_walls, players, ai_player, action),
                )

                if score_action(board, walls, player_walls, players, ai_player, best_wall) > score_action(
                    board, walls, player_walls, players, ai_player, best_move
                ):
                    return best_wall

        shortest_move = choose_shortest_path_move(board, walls, players, ai_player)
        return shortest_move if shortest_move is not None else best_move

    wall_actions = legal_wall_actions(board, walls, player_walls, players, ai_player, False)
    all_actions = moves + wall_actions

    return max(all_actions, key=lambda action: score_action(board, walls, player_walls, players, ai_player, action))
