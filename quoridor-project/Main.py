import pygame
import sys
from game.rules import move_player , check_winner , place_wall
from game.board import board , player_walls, walls



pygame.init()
# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BOARD_SIZE = 720
CELL_SIZE = 80
MARGIN = 40
# Set the title of the window
pygame.display.set_caption("Quoridor")


# Define the players and their Initial positions
players = {
    "P1": {"x": 4, "y": 0},
    "P2": {"x": 4, "y": 8},
}


current_player = "P1"
selected_wall_orientation = None

running = True


def get_wall_position(mouse_x, mouse_y, orientation):
    local_x = mouse_x - MARGIN
    local_y = mouse_y - MARGIN

    if local_x < 0 or local_x > BOARD_SIZE or local_y < 0 or local_y > BOARD_SIZE:
        return None

    if orientation == "H":
        grid_line = round(local_y / CELL_SIZE)

        if grid_line < 1 or grid_line > 8:
            return None

        if abs(local_y - grid_line * CELL_SIZE) > 15:
            return None

        wall_x = int(local_x // CELL_SIZE)
        wall_y = grid_line - 1

    elif orientation == "V":
        grid_line = round(local_x / CELL_SIZE)

        if grid_line < 1 or grid_line > 8:
            return None

        if abs(local_x - grid_line * CELL_SIZE) > 15:
            return None

        wall_x = grid_line - 1
        wall_y = int(local_y // CELL_SIZE)

    else:
        return None

    if wall_x < 0 or wall_x > 7 or wall_y < 0 or wall_y > 7:
        return None

    return wall_x, wall_y


while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses for player movement
        if event.type == pygame.KEYDOWN:
            direction = None

            #Map arrow keys to movement direction
            if event.key == pygame.K_UP: 
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            elif event.key == pygame.K_h:
                selected_wall_orientation = "H"

            elif event.key == pygame.K_v:
                selected_wall_orientation = "V"


            # If a direction was chosen, attempt to move the current player
            if direction is not None:
                x = players[current_player]["x"]
                y = players[current_player]["y"]

                # Attempt to move the player and update the board and player position if successful
                moved = move_player(board, walls, x, y, direction, current_player)

                if moved:
                    if direction == "UP":
                        players[current_player]["y"] -= 1 # Update the player's position in the players dictionary
                    elif direction == "DOWN":
                        players[current_player]["y"] += 1 # Update the player's position in the players dictionary
                    elif direction == "LEFT":
                        players[current_player]["x"] -= 1 # Update the player's position in the players dictionary
                    elif direction == "RIGHT":
                        players[current_player]["x"] += 1 # Update the player's position in the players dictionary

                    if check_winner(current_player, players[current_player]["y"]): # Check if the current player has won after the move
                        print(current_player, "wins!"  )
                        running = False
                    else:
                        current_player = "P2" if current_player == "P1" else "P1"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if selected_wall_orientation is not None:
                wall_position = get_wall_position(event.pos[0], event.pos[1], selected_wall_orientation)

                if wall_position is not None:
                    x, y = wall_position
                    placed = place_wall(walls, player_walls, current_player, x, y, selected_wall_orientation)

                    if placed:
                        selected_wall_orientation = None
                        current_player = "P2" if current_player == "P1" else "P1"

    # Draw the board and players
    for y in range(9):
        for x in range(9):
            cell = board[y][x]

            if cell.player == "P1":
                color = (255, 0, 0)
            elif cell.player == "P2":
                color = (0, 0, 255)
            else:
                color = (200, 200, 200)

            pygame.draw.rect(
                screen,
                color,
                (MARGIN + x * CELL_SIZE,MARGIN + y * CELL_SIZE, CELL_SIZE - 2,CELL_SIZE - 2,),
            )

    # Draw walls
    for wall in walls:
        if wall.orientation == "H":
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    MARGIN + wall.x * CELL_SIZE,
                    MARGIN + (wall.y + 1) * CELL_SIZE - 6,
                    CELL_SIZE * 2,
                    12,
                ),
            )

        elif wall.orientation == "V":
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (
                    MARGIN + (wall.x + 1) * CELL_SIZE - 6,
                    MARGIN + wall.y * CELL_SIZE,
                    12,
                    CELL_SIZE * 2,
                ),
            )


    pygame.display.update()

pygame.quit()
sys.exit()
