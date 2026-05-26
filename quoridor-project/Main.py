import pygame
import sys
from game.rules import move_player , check_winner , place_wall
from game.board import board , player_walls, walls
from game.ai import choose_ai_action
import os

#This game was developed by Ain Shams University students as a project for the course "Artificial Intelligence 1" in the Spring semester of 2026
#The game is based on the board game "Quoridor" and 
# includes both player vs player and player vs AI modes, 
# with three difficulty levels for the AI. We hope you enjoy playing it as much as we enjoyed creating it!


pygame.init()
pygame.mixer.init()

#sound_path = os.path.join( "Assets", "win.mp3")

#pygame.mixer.music.load(sound_path)

# Set up the display
WIDTH, HEIGHT = 1000, 820
screen = pygame.display.set_mode((WIDTH, HEIGHT))
BOARD_SIZE = 720
CELL_SIZE = 80
MARGIN = 40
PANEL_X = MARGIN + BOARD_SIZE + 30
CLOSE_BUTTON_RECT = pygame.Rect(PANEL_X + 118, MARGIN + 14, 28, 28)
RESTART_BUTTON_RECT = pygame.Rect(PANEL_X + 18, MARGIN + 655, 124, 42)
PVP_BUTTON_RECT = pygame.Rect(PANEL_X + 18, MARGIN + 365, 56, 30)
AI_BUTTON_RECT = pygame.Rect(PANEL_X + 84, MARGIN + 365, 58, 30)
EASY_BUTTON_RECT = pygame.Rect(PANEL_X + 18, MARGIN + 430, 42, 30)
MEDIUM_BUTTON_RECT = pygame.Rect(PANEL_X + 64, MARGIN + 430, 48, 30)
HARD_BUTTON_RECT = pygame.Rect(PANEL_X + 116, MARGIN + 430, 42, 30)
# Set the title of the window
pygame.display.set_caption("Quoridor")

TITLE_FONT = pygame.font.SysFont("arial", 32, bold=True)
HUD_FONT = pygame.font.SysFont("arial", 22, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 18)
WIN_FONT = pygame.font.SysFont("arial", 46, bold=True)

BACKGROUND_COLOR = (24, 27, 33)
BOARD_BACKGROUND = (72, 58, 47)
CELL_COLOR = (213, 205, 190)
CELL_HOVER_COLOR = (228, 220, 205)
P1_COLOR = (220, 60, 60)
P2_COLOR = (55, 120, 230)
WALL_COLOR = (55, 35, 20)
TEXT_COLOR = (235, 235, 235)
MUTED_TEXT_COLOR = (170, 175, 185)
PANEL_COLOR = (38, 43, 52)
ERROR_COLOR = (255, 120, 120)
BUTTON_COLOR = (60, 74, 95)
BUTTON_HOVER_COLOR = (78, 96, 124)


# Define the players and their Initial positions
players = {
    "P1": {"x": 4, "y": 0},
    "P2": {"x": 4, "y": 8},
}


current_player = "P1"
selected_wall_orientation = None
status_message = "P1 turn"
status_color = TEXT_COLOR
game_over = False
winner = None
game_mode = "PVP"
ai_level = "Medium"
AI_PLAYER = "P2"

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


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def is_ai_turn():
    return game_mode == "HVA" and current_player == AI_PLAYER and not game_over


def next_turn_message():
    if is_ai_turn():
        return "AI thinking..."

    return current_player + " turn"


def switch_turn():
    global current_player, selected_wall_orientation, status_message, status_color

    current_player = "P2" if current_player == "P1" else "P1"
    selected_wall_orientation = None
    status_message = next_turn_message()
    status_color = TEXT_COLOR


def apply_win(player):
    global selected_wall_orientation, status_message, status_color, game_over, winner

    print(player, "wins!")
    status_message = player + " wins!"
    status_color = TEXT_COLOR
    selected_wall_orientation = None
    winner = player
    game_over = True
    #pygame.mixer.music.play(start=30)


def perform_ai_turn():
    global status_message, status_color

    if not is_ai_turn():
        return

    action = choose_ai_action(board, walls, player_walls, players, AI_PLAYER, ai_level)

    if action is None:
        status_message = "AI has no move"
        status_color = ERROR_COLOR
        return

    action_done = False

    if action["type"] == "move":
        x = players[AI_PLAYER]["x"]
        y = players[AI_PLAYER]["y"]
        moved, new_x, new_y = move_player(board, walls, x, y, action["direction"], AI_PLAYER)

        if moved:
            players[AI_PLAYER]["x"] = new_x
            players[AI_PLAYER]["y"] = new_y
            action_done = True

    elif action["type"] == "wall":
        action_done = place_wall(
            board,
            walls,
            player_walls,
            players,
            AI_PLAYER,
            action["x"],
            action["y"],
            action["orientation"],
        )

    if not action_done:
        status_message = "AI move failed"
        status_color = ERROR_COLOR
        return

    if check_winner(AI_PLAYER, players[AI_PLAYER]["y"]):
        apply_win(AI_PLAYER)
    else:
        switch_turn()


def reset_game():
    global current_player, selected_wall_orientation, status_message, status_color, game_over, winner

    for row in board:
        for cell in row:
            cell.player = None

    board[0][4].player = "P1"
    board[8][4].player = "P2"

    players["P1"]["x"] = 4
    players["P1"]["y"] = 0
    players["P2"]["x"] = 4
    players["P2"]["y"] = 8

    walls.clear()
    player_walls["P1"] = 10
    player_walls["P2"] = 10

    current_player = "P1"
    selected_wall_orientation = None
    status_message = "P1 turn"
    status_color = TEXT_COLOR
    game_over = False
    winner = None


def draw_small_button(rect, label, active):
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if rect.collidepoint(mouse_pos) else BUTTON_COLOR

    if active:
        color = P2_COLOR

    pygame.draw.rect(screen, color, rect, border_radius=6)
    label_surface = SMALL_FONT.render(label, True, TEXT_COLOR)
    label_rect = label_surface.get_rect(center=rect.center)
    screen.blit(label_surface, label_rect)


def draw_win_celebration():
    if not game_over or winner is None:
        return

    winner_color = P1_COLOR if winner == "P1" else P2_COLOR
    pulse = (pygame.time.get_ticks() // 250) % 2
    border_width = 7 if pulse == 0 else 11

    pygame.draw.rect(
        screen,
        winner_color,
        (MARGIN - 14, MARGIN - 14, BOARD_SIZE + 28, BOARD_SIZE + 28),
        border_width,
        border_radius=12,
    )

    overlay = pygame.Surface((BOARD_SIZE, 170), pygame.SRCALPHA)
    overlay.fill((18, 20, 26, 220))
    screen.blit(overlay, (MARGIN, MARGIN + BOARD_SIZE // 2 - 85))

    title = WIN_FONT.render("Congratulations!", True, TEXT_COLOR)
    title_rect = title.get_rect(center=(MARGIN + BOARD_SIZE // 2, MARGIN + BOARD_SIZE // 2 - 25))
    screen.blit(title, title_rect)

    message = HUD_FONT.render(winner + " wins the match", True, winner_color)
    message_rect = message.get_rect(center=(MARGIN + BOARD_SIZE // 2, MARGIN + BOARD_SIZE // 2 + 25))
    screen.blit(message, message_rect)

    hint = SMALL_FONT.render("Click Restart to play again", True, MUTED_TEXT_COLOR)
    hint_rect = hint.get_rect(center=(MARGIN + BOARD_SIZE // 2, MARGIN + BOARD_SIZE // 2 + 65))
    screen.blit(hint, hint_rect)


def draw_panel():
    pygame.draw.rect(screen, PANEL_COLOR, (PANEL_X, MARGIN, 160, BOARD_SIZE), border_radius=8)

    close_color = ERROR_COLOR if CLOSE_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()) else (95, 55, 60)
    pygame.draw.rect(screen, close_color, CLOSE_BUTTON_RECT, border_radius=6)
    close_label = HUD_FONT.render("X", True, TEXT_COLOR)
    close_label_rect = close_label.get_rect(center=CLOSE_BUTTON_RECT.center)
    screen.blit(close_label, close_label_rect)

    draw_text("Quoridor", TITLE_FONT, TEXT_COLOR, PANEL_X + 18, MARGIN + 20)
    draw_text("Current turn", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 85)

    turn_color = P1_COLOR if current_player == "P1" else P2_COLOR
    pygame.draw.circle(screen, turn_color, (PANEL_X + 34, MARGIN + 128), 13)
    draw_text(current_player, HUD_FONT, TEXT_COLOR, PANEL_X + 58, MARGIN + 115)

    draw_text("Walls left", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 175)
    draw_text("P1: " + str(player_walls["P1"]), HUD_FONT, P1_COLOR, PANEL_X + 18, MARGIN + 205)
    draw_text("P2: " + str(player_walls["P2"]), HUD_FONT, P2_COLOR, PANEL_X + 18, MARGIN + 235)

    draw_text("Wall mode", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 295)
    if selected_wall_orientation == "H":
        mode_text = "Horizontal"
    elif selected_wall_orientation == "V":
        mode_text = "Vertical"
    else:
        mode_text = "None"
    draw_text(mode_text, HUD_FONT, TEXT_COLOR, PANEL_X + 18, MARGIN + 325)

    draw_text("Game mode", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 345)
    draw_small_button(PVP_BUTTON_RECT, "PvP", game_mode == "PVP")
    draw_small_button(AI_BUTTON_RECT, "AI", game_mode == "HVA")

    draw_text("AI level", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 410)
    draw_small_button(EASY_BUTTON_RECT, "Easy", ai_level == "Easy")
    draw_small_button(MEDIUM_BUTTON_RECT, "Med", ai_level == "Medium")
    draw_small_button(HARD_BUTTON_RECT, "Hard", ai_level == "Hard")

    draw_text("Controls", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 485)
    draw_text("Arrows: move", SMALL_FONT, TEXT_COLOR, PANEL_X + 18, MARGIN + 515)
    draw_text("H: horizontal", SMALL_FONT, TEXT_COLOR, PANEL_X + 18, MARGIN + 545)
    draw_text("V: vertical", SMALL_FONT, TEXT_COLOR, PANEL_X + 18, MARGIN + 575)
    draw_text("Click: place", SMALL_FONT, TEXT_COLOR, PANEL_X + 18, MARGIN + 605)

    draw_text("Status", SMALL_FONT, MUTED_TEXT_COLOR, PANEL_X + 18, MARGIN + 620)
    draw_text(status_message, SMALL_FONT, status_color, PANEL_X + 18, MARGIN + 640)

    restart_color = BUTTON_HOVER_COLOR if RESTART_BUTTON_RECT.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
    pygame.draw.rect(screen, restart_color, RESTART_BUTTON_RECT, border_radius=8)
    restart_label = SMALL_FONT.render("Restart", True, TEXT_COLOR)
    restart_label_rect = restart_label.get_rect(center=RESTART_BUTTON_RECT.center)
    screen.blit(restart_label, restart_label_rect)


while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key presses for player movement
        if event.type == pygame.KEYDOWN:
            direction = None

            #Map arrow keys to movement direction
            if not game_over and not is_ai_turn():
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
                    status_message = "Click to place H wall"
                    status_color = TEXT_COLOR

                elif event.key == pygame.K_v:
                    selected_wall_orientation = "V"
                    status_message = "Click to place V wall"
                    status_color = TEXT_COLOR


            # If a direction was chosen, attempt to move the current player
            if direction is not None:
                x = players[current_player]["x"]
                y = players[current_player]["y"]

                # Attempt to move the player and update the board and player position if successful
                moved, new_x, new_y = move_player(board, walls, x, y, direction, current_player)

                if moved:
                    players[current_player]["x"] = new_x
                    players[current_player]["y"] = new_y

                    if check_winner(current_player, players[current_player]["y"]): # Check if the current player has won after the move
                        apply_win(current_player)

                    else:
                        switch_turn()
                else:
                    status_message = "Invalid move"
                    status_color = ERROR_COLOR

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if CLOSE_BUTTON_RECT.collidepoint(event.pos):
                running = False
            elif RESTART_BUTTON_RECT.collidepoint(event.pos):
                reset_game()
                pygame.mixer.music.stop()
            elif PVP_BUTTON_RECT.collidepoint(event.pos):
                game_mode = "PVP"
                reset_game()
                pygame.mixer.music.stop()
            elif AI_BUTTON_RECT.collidepoint(event.pos):
                game_mode = "HVA"
                reset_game()
                pygame.mixer.music.stop()
            elif EASY_BUTTON_RECT.collidepoint(event.pos):
                ai_level = "Easy"
                reset_game()
                pygame.mixer.music.stop()
            elif MEDIUM_BUTTON_RECT.collidepoint(event.pos):
                ai_level = "Medium"
                reset_game()
                pygame.mixer.music.stop()
            elif HARD_BUTTON_RECT.collidepoint(event.pos):
                ai_level = "Hard"
                reset_game()
                pygame.mixer.music.stop()
            elif selected_wall_orientation is not None and not game_over and not is_ai_turn():
                wall_position = get_wall_position(event.pos[0], event.pos[1], selected_wall_orientation)

                if wall_position is not None:
                    x, y = wall_position
                    placed = place_wall(board, walls, player_walls, players, current_player, x, y, selected_wall_orientation)

                    if placed:
                        switch_turn()
                    else:
                        status_message = "Invalid wall"
                        status_color = ERROR_COLOR
                else:
                    status_message = "Click between cells"
                    status_color = ERROR_COLOR

    perform_ai_turn()


    # Draw the board and players
    pygame.draw.rect(screen, BOARD_BACKGROUND, (MARGIN - 8, MARGIN - 8, BOARD_SIZE + 16, BOARD_SIZE + 16), border_radius=8)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for y in range(9):
        for x in range(9):
            cell = board[y][x]
            rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2)
            color = CELL_HOVER_COLOR if rect.collidepoint(mouse_x, mouse_y) else CELL_COLOR

            pygame.draw.rect(screen, color, rect, border_radius=4)

            if cell.player == "P1" or cell.player == "P2":
                player_color = P1_COLOR if cell.player == "P1" else P2_COLOR
                center = (MARGIN + x * CELL_SIZE + CELL_SIZE // 2, MARGIN + y * CELL_SIZE + CELL_SIZE // 2)
                radius = 25
                if game_over and cell.player == winner:
                    radius = 29 + ((pygame.time.get_ticks() // 250) % 2) * 3

                pygame.draw.circle(screen, player_color, center, radius)
                pygame.draw.circle(screen, TEXT_COLOR, center, 25, 2)
                label = HUD_FONT.render(cell.player, True, TEXT_COLOR)
                label_rect = label.get_rect(center=center)
                screen.blit(label, label_rect)

    # Draw walls
    for wall in walls:
        if wall.orientation == "H":
            pygame.draw.rect(
                screen,
                WALL_COLOR,
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
                WALL_COLOR,
                (
                    MARGIN + (wall.x + 1) * CELL_SIZE - 6,
                    MARGIN + wall.y * CELL_SIZE,
                    12,
                    CELL_SIZE * 2,
                ),
            )

    draw_panel()
    draw_win_celebration()

    pygame.display.update()

pygame.quit()
sys.exit()
