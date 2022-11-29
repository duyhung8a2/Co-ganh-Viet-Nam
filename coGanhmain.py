"""
Handling user input and display current GameState object.
"""

import pygame as p
import CoGanhEngine

WIDTH = HEIGHT = 600
BORDER = 44
DIMENSION = 5 #ban co ganh la 5x5
BOARD_DIMENSION = 4 #co ganh co 4 o thoi
SQ_SIZE = (HEIGHT - BORDER * 2) // BOARD_DIMENSION
PIECE_SIZE = (HEIGHT - BORDER * 4) // DIMENSION
MAX_FPS = 15 #animation
IMAGES = {}


'''
Initialize a global dictionary. Load images are expensive, load once is preferable.
'''
def loadImages():
    pieces = ["1", "-1"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png").convert_alpha(), (PIECE_SIZE, PIECE_SIZE))
        # Setting alpha color (transparency)
        colorkey = IMAGES[piece].get_at((0, 0))
        IMAGES[piece].set_colorkey(colorkey)
        IMAGES[piece].set_alpha(256)
    #Access image by calling IMAGES[1]

'''
Main driver: handle user input and update graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = CoGanhEngine.GameState()
    #print(gs.board)
    loadImages()
    running = True

    pieceSelected = () # no piece is selected, keep track of last click (row, column)
    playerClicks = [] # keep track of player clicks (two tuple[(5, 4), (4, 6)])
    validMoves = gs.getValidMoves()
    moveMade = False  # Flag var for when a move is made
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE 
                row = location[1] // SQ_SIZE 
                print("Location of mouse: ", location, " in row, col: ", row, col)
                #print(location, col, row)
                #what if user click on two piece THAT FUCKING THE SAME, yes stupid user
                if pieceSelected == (row, col):
                    # basically just reset
                    pieceSelected = ()
                    playerClicks = [] 
                else:
                    pieceSelected = (row, col)
                    playerClicks.append(pieceSelected)
                if len(playerClicks) == 2: # after 2nd click
                    move = CoGanhEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print("Notation ", move.getNotation())
                    #print("Valid moves: ", validMoves)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(move)
                            moveMade = True
                            #reset clicks
                            pieceSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [pieceSelected]

                    
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        
        if moveMade == True:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)

        if gs.isGameOver():
            gameOver = True 
            if gs.xanhToMove == True:
                drawText(screen, "Do thang")
            else:
                drawText(screen, "Xanh thang")

        clock.tick(MAX_FPS)
        p.display.flip()


'''
Responsible for all graphics within game state
'''
def drawGameState(screen, gs):
    drawBoard(screen) # Draw square on the board
    # Piece highlight, move suggest etc
    drawPieces(screen, gs.board) # Draw pieces on top of the board

'''
Draw square and line on board
'''
def drawBoard(screen):
    line_color = p.Color("Black")
    fill_color = p.Color("Gray")
    
    border_thickness = 5
    p.draw.rect(screen, fill_color, (0, 0, WIDTH, HEIGHT))
    for r in range(BOARD_DIMENSION):
        for c in range(BOARD_DIMENSION):
            (x, y, width, height) = (c*SQ_SIZE + BORDER, r*SQ_SIZE + BORDER, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, fill_color, p.Rect(x, y, width, height))
            #draw border
            top_left = (x, y)
            top_right = (x + width, y)
            bottom_right =  (x + width, y + height)
            bottom_left = (x, y + height)
            border_coords = (top_left, top_right, bottom_right, bottom_left )
            p.draw.lines(screen, line_color, True, (border_coords), border_thickness)
            if (r % 2 == 0):
                if (c % 2 == 0):
                    p.draw.line(screen, line_color, top_left, bottom_right, border_thickness)
                else:
                    p.draw.line(screen, line_color, bottom_left, top_right, border_thickness)
            else:
                if (c % 2 == 0):
                    p.draw.line(screen, line_color, bottom_left, top_right , border_thickness)
                else:
                    p.draw.line(screen, line_color, top_left, bottom_right, border_thickness)


'''
Draw pieces on the board using current GameState.board
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "0": #not empty square
                adjust = 2 # custom adjust, nhin khong vua mat                  
                (x, y, width, height) = (c*SQ_SIZE + adjust, r*SQ_SIZE + adjust, PIECE_SIZE, PIECE_SIZE)
        
                screen.blit(IMAGES[piece], (x, y, width, height))


'''
Draw text print on the screen
'''
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 64, True, False)
    textObject = font.render(text, 1, p.Color("White"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()