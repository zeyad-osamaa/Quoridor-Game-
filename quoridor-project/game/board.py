class Cell:                 # Represents a single cell on the board
    def __repr__(self):
        return f"Cell({self.x}, {self.y}, Player: {self.player})"  

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player = None

board = []

for y in range(9): # creating a 9x9 board each cell is represented by an instance of the Cell class and have (x,y) coordinates 
    row = []

    for x in range(9):
        row.append(Cell(x,y))

    board.append(row)

# Walls will be stored as a list of wall objects, each with its own position and orientation
walls = []

player_walls = {
    "P1": 10,
    "P2": 10,
}

board[0][4].player = "P1"
board[8][4].player = "P2"    
