"""
Storing all info about current state of the game. Responsible for determining valid move. Keep move log.
"""

class GameState():
    def __init__(self):
        # 1 la quan do, -1 la quan xanh, 0 la cho trong
        self.board = [
                        [ "1" , "1",  "1",  "1",  "1"],
                        [ "1" , "0",  "0",  "0",  "1"],
                        [ "-1",  "0",  "0",  "0",  "1"],
                        [ "-1",  "0",  "0",  "0",  "-1"],
                        [ "-1",  "-1",  "-1",  "-1",  "-1"]
                     ]
        self.xanhToMove = True
        self.moveLog = []
    
    '''
    Take a Move as a parameter and execute it
    '''
    def makeMove(self, move ):
        self.board[move.startRow][move.startCol] = "0"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log move if we want to undo
        # Capture
        captured = self.checkCapture(move.endRow, move.endCol)
        if captured:
            print("here")
            for capture in captured:
                firstPiece = capture[0] 
                secondPiece = capture[1] 
                if (self.xanhToMove == True):
                    self.board[firstPiece[0]][firstPiece[1]] = "-1"
                    self.board[secondPiece[0]][secondPiece[1]] = "-1"
                else:
                    self.board[firstPiece[0]][firstPiece[1]] = "1"
                    self.board[secondPiece[0]][secondPiece[1]] = "1"

        self.xanhToMove = not self.xanhToMove # swap player
        


    '''
    Undo the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:  #Just making sure that there is a move
            move = self.moveLog.pop()

            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.piecePlaced
            self.xanhToMove = not self.xanhToMove #switch turn back

    '''
    All moves consider not get losing
    '''
    def getValidMoves(self):
        return self.getAllPossibleMoves() #not implement yet

    def getAllPossibleMoves(self):
        moves = []
        # Go through all the chess table to check for pieces
        for r in range(len(self.board)):    # check row then
            for c in range(len(self.board[r])):     #for each row check column then
                piece = self.board[r][c] 
                if (piece == "-1" and self.xanhToMove) or (piece == "1" and not self.xanhToMove):
                    self.getPieceMoves(r, c, moves)
        return moves

    def getPieceMoves(self, r, c, moves):
        #up, left, down, right, up_left, up_right, down_left, down_right
        direction = ((-1,0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)) 
        for d in direction:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 5 and 0 <= endCol < 5:
                endPiece = self.board[endRow][endCol]
                if endPiece ==  "0":   #empty space that valid
                    if ((d == (1, 1) or d == (-1, -1) or d == (1, -1) or d == (-1, 1))  and
                       ((r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0))):
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif (d == (-1, 0) or d == (0, -1) or d == (1, 0) or d == (0, 1)):
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    def checkCapture(self, r, c):
        capture = []
        if self.xanhToMove:
            if (0 <= r - 1 and r + 1 < 5 and 0 <= c-1 and c+1 < 5 ):
                # up - down, left - right, ul - dr, ur - dl
                if (self.board[r - 1][c] == self.board[r + 1][c] == "1"):
                    capture.append(((r-1, c),(r+1, c)))
                if (self.board[r][c - 1] == self.board[r][c + 1] == "1"):
                    capture.append(((r, c-1),(r, c+1)))
                if (self.board[r - 1][c - 1] == self.board[r + 1][c + 1] == "1" and ((r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0))):
                    capture.append(((r-1, c-1),(r+1, c+1)))
                if (self.board[r - 1][c + 1] == self.board[r + 1][c - 1] == "1" and ((r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0))):
                    capture.append(((r-1, c+1),(r+1, c-1)))
            elif ((r + 1 < 0 or r + 1 > 4) and 0 <= c-1 and c+1 < 5):
                if (self.board[r][c - 1] == self.board[r][c + 1] == "1"):
                    capture.append(((r, c-1),(r, c+1)))
            elif ((c + 1 > 4 or c + 1 < 0) and 0 <= r - 1 and r + 1 < 5):
                if (self.board[r - 1][c] == self.board[r + 1][c] == "1"):
                    capture.append(((r-1, c),(r+1, c)))
        elif not self.xanhToMove:
            if (0 <= r - 1 and r + 1 < 5 and 0 <= c-1 and c+1 < 5 ):
                # up - down, left - right, ul - dr, ur - dl
                if (self.board[r - 1][c] == self.board[r + 1][c] == "-1"):
                    capture.append(((r-1, c),(r+1, c)))
                if (self.board[r][c - 1] == self.board[r][c + 1] == "-1"):
                    capture.append(((r, c-1),(r, c+1)))
                if (self.board[r - 1][c - 1] == self.board[r + 1][c + 1] == "-1" and ((r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0))):
                    capture.append(((r-1, c-1),(r+1, c+1)))
                if (self.board[r - 1][c + 1] == self.board[r + 1][c - 1] == "-1" and ((r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0))):
                    capture.append(((r-1, c+1),(r+1, c-1)))
            elif ((r + 1 < 0 or r + 1 > 4) and 0 <= c-1 and c+1 < 5):
                if (self.board[r][c - 1] == self.board[r][c + 1] == "-1"):
                    capture.append(((r, c-1),(r, c+1)))
            elif ((c + 1 > 4 or c + 1 < 0) and 0 <= r - 1 and r + 1 < 5):
                if (self.board[r - 1][c] == self.board[r + 1][c] == "-1"):
                    capture.append(((r-1, c),(r+1, c)))
        return capture

class Move():
    def __init__(self, startPc, endPc, board):
        self.startRow = startPc[0]
        self.startCol = startPc[1]
        self.endRow = endPc[0]
        self.endCol = endPc[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.piecePlaced = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)

    
    '''
    Overriding equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getNotation(self):
        result = "({}, {}) to ({}, {})".format(self.startRow, self.startCol, self.endRow, self.endCol)
        return result

