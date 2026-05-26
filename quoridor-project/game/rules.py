from game.walls import Wall


def move_player(board, walls, x, y, direction, player):
    new_x = x
    new_y = y
#condition if there is adjacent player
#y+2
    if direction == "UP":   # Update the new coordinates based on the direction
        new_y -= 1
    elif direction == "DOWN": # Update the new coordinates based on the direction
        new_y += 1
    elif direction == "LEFT": # Update the new coordinates based on the direction
        new_x -= 1
    elif direction == "RIGHT": # Update the new coordinates based on the direction
        new_x += 1
    else:
        return False

    if new_x < 0 or new_x > 8 or new_y < 0 or new_y > 8: # Check if the new coordinates are within the bounds of the board
        return False

    # Check if the move is blocked by a wall
    if is_blocked(walls, x, y, direction):
        return False
    # Check if the current cell is occupied by the player and the new cell is not occupied by another player
    if board[y][x].player != player:
        return False

    if board[new_y][new_x].player is not None: #check if the new cell is occupied by another player    
        return False

    board[y][x].player = None
    board[new_y][new_x].player = player

    return True

     
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

