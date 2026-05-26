from game.walls import Wall


def get_direction_delta(direction):
    if direction == "UP":
        return 0, -1
    if direction == "DOWN":
        return 0, 1
    if direction == "LEFT":
        return -1, 0
    if direction == "RIGHT":
        return 1, 0

    return None


def get_diagonal_directions(direction):
    if direction == "UP" or direction == "DOWN":
        return ["LEFT", "RIGHT"]
    if direction == "LEFT" or direction == "RIGHT":
        return ["UP", "DOWN"]

    return []


def is_inside_board(x, y):
    return 0 <= x <= 8 and 0 <= y <= 8


def move_player(board, walls, x, y, direction, player):
    direction_delta = get_direction_delta(direction)

    if direction_delta is None:
        return False, x, y

    dx, dy = direction_delta
    new_x = x + dx
    new_y = y + dy

    if not is_inside_board(new_x, new_y): # Check if the new coordinates are within the bounds of the board
        return False, x, y

    # Check if the move is blocked by a wall
    if is_blocked(walls, x, y, direction):
        return False, x, y
    
    # Check if the current cell is occupied by the player and the new cell is not occupied by another player
    if board[y][x].player != player:
        return False, x, y

    if board[new_y][new_x].player is not None: #check if the new cell is occupied by another player jump two steps   
        jump_x = new_x + dx
        jump_y = new_y + dy

        can_jump_straight = (
            is_inside_board(jump_x, jump_y)
            and not is_blocked(walls, new_x, new_y, direction)
            and board[jump_y][jump_x].player is None
        )

        if can_jump_straight:
            board[y][x].player = None
            board[jump_y][jump_x].player = player

            return True, jump_x, jump_y

        for side_direction in get_diagonal_directions(direction):
            side_dx, side_dy = get_direction_delta(side_direction)
            diagonal_x = new_x + side_dx
            diagonal_y = new_y + side_dy

            if not is_inside_board(diagonal_x, diagonal_y):
                continue

            if is_blocked(walls, new_x, new_y, side_direction):
                continue

            if board[diagonal_y][diagonal_x].player is not None:
                continue

            board[y][x].player = None
            board[diagonal_y][diagonal_x].player = player

            return True, diagonal_x, diagonal_y

        return False, x, y

    board[y][x].player = None
    board[new_y][new_x].player = player

    return True, new_x, new_y

     
# Check if a player has won by reaching the opposite side of the board
def check_winner(player, y):
    if player == "P1" and y == 8:
        return True

    if player == "P2" and y == 0:
        return True

    return False

# Function to place a wall on the board
def place_wall(walls, player_walls, player, x, y, orientation):

    if player_walls[player] <= 0: # Check if the player has any walls left to place
        return False

    if orientation != "H" and orientation != "V": # Check if the orientation is valid
        return False

    if x < 0 or x > 7 or y < 0 or y > 7:# Check if the wall coordinates are within the bounds of the board (walls can only be placed between cells, so max coordinate is 7)
        return False

    for wall in walls:
        if wall.x == x and wall.y == y:
            return False

    walls.append(Wall(x, y, orientation))
    player_walls[player] -= 1

    return True

# Function to check if a move is blocked by a wall
def is_blocked(walls, x, y, direction):

    for wall in walls:
        if wall.orientation == "H":
            # Check if the wall blocks movement in the specified direction
            if direction == "UP":
                if y == wall.y + 1 and (x == wall.x or x == wall.x + 1):
                    return True
            # Check if the wall blocks movement in the specified direction
            elif direction == "DOWN":
                if y == wall.y and (x == wall.x or x == wall.x + 1):
                    return True

        elif wall.orientation == "V":
            # Check if the wall blocks movement in the specified direction
            if direction == "LEFT":
                if x == wall.x + 1 and (y == wall.y or y == wall.y + 1):
                    return True
            # Check if the wall blocks movement in the specified direction
            elif direction == "RIGHT":
                if x == wall.x and (y == wall.y or y == wall.y + 1):
                    return True

    return False

