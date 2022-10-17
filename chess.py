import random
import time
import math
from IPython.display import clear_output

# you can add/change the input parameters for each function 
# you can change the function names and also add more functions if needed

ROWS = COLS = 8

def ChessBoardSetup():
    # initialize and return a chess board - create a 2D 8x8 array that has the value for each cell
    # USE the following characters for the chess pieces - lower-case for BLACK and upper-case for WHITE
    # . for empty board cell
    # p/P for pawn
    # r/R for rook
    # t/T for knight
    # b/B for bishop
    # q/Q for queen
    # k/K for king
    board = [[],[],[],[],[],[],[],[]]
    board[0] = ['r','t','b','q','k','b','t','r']
    board[1] = ['p','p','p','p','p','p','p','p']
    board[2] = ['.','.','.','.','.','.','.','.']
    board[3] = ['.','.','.','.','.','.','.','.']
    board[4] = ['.','.','.','.','.','.','.','.']
    board[5] = ['.','.','.','.','.','.','.','.']
    board[6] = ['P','P','P','P','P','P','P','P']
    board[7] = ['R','T','B','Q','K','B','T','R']
    return board

def DrawBoard(board):
    # write code to print the board - following is one print example
    # r t b q k b t r
    # p p p p p p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # . . . . . . . .
    # P P P P P P P P
    # R T B Q K B T R
    for r in range(ROWS):
        for c in range(COLS):
            print(board[r][c], end=' ')
        print()

def MovePiece(board, fromSquare, toSquare):
    # write code to move the one chess piece
    # you do not have to worry about the validity of the move - this will be done before calling this function
    # this function will at least take the move (from-piece and to-piece) as input and return the new board layout
    board[toSquare[0]][toSquare[1]] = board[fromSquare[0]][fromSquare[1]]
    board[fromSquare[0]][fromSquare[1]] = '.'

# return True if the input move (from-square and to-square) is legal, else False
# this is the KEY function which contains the rules for each piece type 
def IsMoveLegal(board,player,fromSquare,toSquare):
    fromSquare_r = fromSquare[0]
    fromSquare_c = fromSquare[1]
    toSquare_r = toSquare[0]
    toSquare_c = toSquare[1]
    fromPiece = board[fromSquare_r][fromSquare_c]
    toPiece = board[toSquare_r][toSquare_c]

    if fromSquare == toSquare:
        return False
    
    if fromPiece.lower() == 'k':
        hDistance = abs(toSquare_r - fromSquare_r)
        vDistance = abs(toSquare_c - fromSquare_c)
        if (toPiece == '.' or ((player == "black" and toPiece.isupper()) or (player == "white" and toPiece.islower()))):
            if hDistance <= 1 and vDistance <= 1:
                return True

    # else if the from-piece is a "rook"
    elif(fromPiece.lower() == 'r'):
        # if to-square is either in the same row or column as the from-square
        if (toSquare_r == fromSquare_r or toSquare_c == fromSquare_c):
            # if to-square is either empty or contains a piece that belongs to the enemy team
            if (toPiece == '.' or ((player == "black" and toPiece.isupper()) or (player == "white" and toPiece.islower()))):
                # if IsClearPath() - a clear path exists between from-square and to-square
                if IsClearPath(board,fromSquare,toSquare):
                    # return True
                    return True

    elif(fromPiece.lower() == 'b'):
        if abs(toSquare_r - fromSquare_r) == abs(toSquare_c - fromSquare_c):
            if (toPiece == '.' or ((player == "black" and toPiece.isupper()) or (player == "white" and toPiece.islower()))):
                if IsClearPath(board,fromSquare,toSquare):
                    return True

    elif fromPiece.lower() == 'q':
        if (toSquare_r == fromSquare_r or toSquare_c == fromSquare_c):
            if (toPiece == '.' or ((player == "black" and toPiece.isupper()) or (player == "white" and toPiece.islower()))):
                if IsClearPath(board,fromSquare,toSquare):
                    return True
        if abs(toSquare_r - fromSquare_r) == abs(toSquare_c - fromSquare_c):
            if (toPiece == '.' or ((player == "black" and toPiece.isupper()) or (player == "white" and toPiece.islower()))):
                if IsClearPath(board,fromSquare,toSquare):
                    return True
    
    elif fromPiece.lower() == 't':
        rowDiff = abs(toSquare_r - fromSquare_r)
        colDiff = abs(toSquare_c - fromSquare_c)
        if (toPiece == '.' or ((player == "black" and toPiece.isupper()) or (player == "white" and toPiece.islower()))):
            if (colDiff == 1 and rowDiff == -2) or (colDiff == 2 and rowDiff == -1) or (colDiff == 2 and rowDiff == 1) or (colDiff == 1 and rowDiff == 2) or (colDiff == -1 and rowDiff == -2) or (colDiff == -2 and rowDiff == -1) or (colDiff == -2 and rowDiff == 1) or (colDiff == -1 and rowDiff == 2):
                return True

    elif fromPiece.lower() == 'p':
        if player == "white":
            if toSquare_r == fromSquare_r - 1 and toSquare_c == fromSquare_c:
                if toPiece == '.':
                    return True
            elif toSquare_r == fromSquare_r - 2 and toSquare_c == fromSquare_c and fromSquare_r == 6:
                if toPiece == '.' and board[5][fromSquare_c] == '.':
                    return True
            elif toSquare_r == fromSquare_r - 1 and (toSquare_c == fromSquare_c - 1 or toSquare_c == fromSquare_c + 1):
                if toPiece != '.' and toPiece.isupper():
                    return True
        elif player == "black":
            if toSquare_r == fromSquare_r + 1 and toSquare_c == fromSquare_c:
                if toPiece == '.':
                    return True
            elif toSquare_r == fromSquare_r + 2 and toSquare_c == fromSquare_c and fromSquare_r == 1:
                if toPiece == '.' and board[2][fromSquare_c] == '.':
                    return True
            elif toSquare_r == fromSquare_r + 1 and (toSquare_c == fromSquare_c - 1 or toSquare_c == fromSquare_c + 1):
                if toPiece != '.' and toPiece.islower():
                    return True

    # if none of the other True's are hit above
    return False



# gets a list of legal moves for a given piece
# input = from-square
# output = list of to-square locations where the piece can move to
def GetListOfLegalMoves(board, player, fromSquare):
    legalMoves = []
    for r in range(ROWS):
        for c in range(COLS):
            if IsMoveLegal(board, player, fromSquare, (r,c)):
                if not DoesMovePutPlayerInCheck(board, player, fromSquare, (r,c)):
                    legalMoves.append((r,c))
    return legalMoves

# gets a list of all pieces for the current player that have legal moves
def GetPiecesWithLegalMoves(board, player):
    # initialize the list of pieces with legal moves to []
    # go through all squares on the board
    # for the selected square
        # if the square contains a piece that belongs to the current player's team
            # call GetListOfLegalMoves() to get a list of all legal moves for the selected piece / square 
            # if there are any legel moves
                # append this piece to the list of pieces with legal moves
    # return the final list of pieces with legal moves
    piecesWithLegalMoves = []
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != '.':
                if (player == "white" and board[r][c].isupper()) or (player == "black" and board[r][c].islower()):
                    if GetListOfLegalMoves(board, player, (r,c)) != []:
                        piecesWithLegalMoves.append((r,c)) # ! is this supposed to be coordinates or the piece?
    return piecesWithLegalMoves



# returns True if the current player is in checkmate, else False
def IsCheckmate(board, player):
    # call GetPiecesWithLegalMoves() to get all legal moves for the current player
    # if there is no piece with any valid move
        # return True
    # else
        # return False
    if GetPiecesWithLegalMoves(board, player) == []:
        return True
    return False



# returns True if the given player is in Check state
def IsInCheck(board, player):
    # find given player's King's location = king-square
    # go through all squares on the board
        # if there is a piece at that location and that piece is of the enemy team
            # call IsMoveLegal() for the enemy player from that square to the king-square
            # if the value returned is True
                # return True
            # else
                # do nothing and continue 
    # return False at the end
    kingSquare = ()
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == 'K' and player == "white":
                kingSquare = (r,c)
            elif board[r][c] == 'k' and player == "black":
                kingSquare = (r,c)
        
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != '.':
                if (player == "white" and board[r][c].islower()) or (player == "black" and board[r][c].isupper()): # ! double check the isupper islower stuff
                    if IsMoveLegal(board, player, (r,c), kingSquare):
                        return True
    
    return False



# helper function to figure out if a move is legal for straight-line moves (rooks, bishops, queens, pawns)
# returns True if the path is clear for a move (from-square and to-square), non-inclusive
def IsClearPath(board,fromSquare,toSquare):
    fromSquare_r = fromSquare[0]
    fromSquare_c = fromSquare[1]
    toSquare_r = toSquare[0]
    toSquare_c = toSquare[1]
    fromPiece = board[fromSquare_r][fromSquare_c]

    # if the from and to squares are only one square apart
    if abs(fromSquare_r - toSquare_r) <= 1 and abs(fromSquare_c - toSquare_c) <= 1:
        #The base case: just one square apart
        return True
    else:
        # if to-square is in the +ve vertical direction from from-square
        if toSquare_r > fromSquare_r and toSquare_c == fromSquare_c:
            # new-from-square = next square in the +ve vertical direction
            newSquare = (fromSquare_r+1,fromSquare_c)
        # else if to-square is in the -ve vertical direction from from-square
        elif toSquare_r < fromSquare_r and toSquare_c == fromSquare_c:
            # new-from-square = next square in the -ve vertical direction
            newSquare = (fromSquare_r-1,fromSquare_c)
        # else if to-square is in the +ve horizontal direction from from-square
        elif toSquare_r == fromSquare_r and toSquare_c > fromSquare_c:
            # new-from-square = next square in the +ve horizontal direction
            newSquare = (fromSquare_r,fromSquare_c+1)
        # else if to-square is in the -ve horizontal direction from from-square
        elif toSquare_r == fromSquare_r and toSquare_c < fromSquare_c:
            # new-from-square = next square in the -ve horizontal direction
            newSquare = (fromSquare_r,fromSquare_c-1)
        # else if to-square is in the SE diagonal direction from from-square
        elif toSquare_r > fromSquare_r and toSquare_c > fromSquare_c:
            # new-from-square = next square in the SE diagonal direction
            newSquare = (fromSquare_r+1,fromSquare_c+1)
        # else if to-square is in the SW diagonal direction from from-square
        elif toSquare_r > fromSquare_r and toSquare_c < fromSquare_c:
            # new-from-square = next square in the SW diagonal direction
            newSquare = (fromSquare_r+1,fromSquare_c-1)
        # else if to-square is in the NE diagonal direction from from-square
        elif toSquare_r < fromSquare_r and toSquare_c > fromSquare_c:
            # new-from-square = next square in the NE diagonal direction
            newSquare = (fromSquare_r-1,fromSquare_c+1)
        # else if to-square is in the NW diagonal direction from from-square
        elif toSquare_r < fromSquare_r and toSquare_c < fromSquare_c:
            # new-from-square = next square in the NW diagonal direction
            newSquare = (fromSquare_r-1,fromSquare_c-1)

    # if new-from-square is not empty
        # return False
    # else
        # return the result from the recursive call of IsClearPath() with the new-from-square and to-square
    if board[newSquare[0]][newSquare[1]] != '.':
        return False
    else:
        return IsClearPath(board, newSquare, toSquare)



# makes a hypothetical move (from-square and to-square)
# returns True if it puts current player into check
def DoesMovePutPlayerInCheck(board, player, fromSquare, toSquare):
    # given the move (from-square and to-square), find the 'from-piece' and 'to-piece'
    # make the move temporarily by changing the 'board'
    # Call the IsInCheck() function to see if the 'player' is in check - save the returned value
    # Undo the temporary move
    # return the value saved - True if it puts current player into check, False otherwise
    fromPiece = board[fromSquare[0]][fromSquare[1]]
    toPiece = board[toSquare[0]][toSquare[1]]
    board[toSquare[0]][toSquare[1]] = fromPiece
    board[fromSquare[0]][fromSquare[1]] = '.'
    isCheck = IsInCheck(board, player)
    board[toSquare[0]][toSquare[1]] = toPiece
    board[fromSquare[0]][fromSquare[1]] = fromPiece
    return isCheck



def GetRandomMove(board, player):
    # pick a random piece and a random legal move for that piece
    piecesWithLegalMoves = GetPiecesWithLegalMoves(board, player)
    piece = random.choice(piecesWithLegalMoves)
    moves = GetListOfLegalMoves(board, player, piece)
    return (piece, random.choice(moves))



def evl(player):
    # this function will calculate the score on the board, if a move is performed
    # give score for each of piece and calculate the score for the chess board
    whiteScore = 0
    blackScore = 0
    
    # ! not sure if this is the best way to do this
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'p':
                whiteScore += 1
            elif board[i][j] == 'P':
                blackScore += 1
            elif board[i][j] == 'b' or board[i][j] == 't':
                whiteScore += 3
            elif board[i][j] == 'B' or board[i][j] == 'T':
                blackScore += 3
            elif board[i][j] == 'r':
                whiteScore += 5
            elif board[i][j] == 'R':
                blackScore += 5
            elif board[i][j] == 'q':
                whiteScore += 9
            elif board[i][j] == 'Q':
                blackScore += 9
            elif board[i][j] == 'k':
                whiteScore += 100
            elif board[i][j] == 'K':
                blackScore += 100

    return whiteScore - blackScore


def GetMinMaxMove(board, player):
    # return the best move for the current player using the MinMax strategy
    # to get the allocated points, searching should be 2-ply (one Max and one Min)

    # Following is the setup for a 2-ply game

    # pieces = GetPiecesWithLegalMoves(curPlayer)
    # for each piece in pieces
        # moves = GetListOfLegalMoves(curPlayer, piece)
        # for move in moves
            # perform the move temporarily
            # enemyPieces = GetPiecesWithLegalMoves(enemyPlayer)
            # for enemyPiece in penemyPiecesieces
                # enemyMoves = GetListOfLegalMoves(enemyPlayer, enemyPiece)
                # for enemyMove in enemyMoves
                    # perform the enemyMove temporarily
                    # res = evl(curPlayer)
                    # update the bestEnemyMove -- this is the MIN player trying to minimize from the 'res' evaluation values
                    # undo the enemyMove
            # update the bestMove -- this is the MAX player trying to maximize from the 'bestEnemyMove' evaluation values
            # undo the move
    # if bestMove found without any doubt, pick that
    # if bestMove not found, pick randomly

    # OPTIONAL -- sometimes automated chess keeps on performing the moves again and again
    # e.g., move king left one square and then move king back - repeat
    # For this you will need to remember the previous move and see if the current best move is not the same and opposite as the previous move
    # If so, pick the second best move instead of the best move
    bestEnemyMove = None
    bestMove = None
    bMax = -math.inf
    bMin = math.inf
    pieces = GetPiecesWithLegalMoves(board, player)
    enemyPlayer = "black" if player == "white" else "white"
    for piece in pieces:
        moves = GetListOfLegalMoves(board, player, piece)
        for move in moves:
            tempPiece = board[move[0]][move[1]]
            MovePiece(board, piece, move)
            enemyPieces = GetPiecesWithLegalMoves(board, enemyPlayer)
            for enemyPiece in enemyPieces:
                enemyMoves = GetListOfLegalMoves(board, enemyPlayer, enemyPiece)
                for enemyMove in enemyMoves:
                    tempEPiece = board[enemyMove[0]][enemyMove[1]]
                    MovePiece(board, enemyPiece, enemyMove)
                    score = evl(player)
                    bMin = min(score, bMin)
                    board[enemyMove[0]][enemyMove[1]], tempEPiece = tempEPiece, board[enemyMove[0]][enemyMove[1]]
            bMax = ((piece, move), max(bMax, bMin))
            board[move[0]][move[1]], tempPiece = tempPiece, board[move[0]][move[1]]
    return bMax[0]

# initialize and setup the board
# player assignment and counter initializations
board = ChessBoardSetup()
player1Type = 'minmaxAI'
player1player = 'white'
player2Type = 'randomAI'
player2player = 'black'

currentPlayerIndex = 0
currentplayer = 'white'
turns = 0
N = 2

# main game loop - while a player is not in checkmate or stalemate (<N turns)
while not IsCheckmate(board,currentplayer) and turns < N:
    clear_output()
    DrawBoard(board)

    # code to take turns and move the pieces
    if currentplayer == 'black':
        move = GetRandomMove(board, currentplayer)
        print("\nBLACK / RandomAI plays!\n")
    else:
        turns = turns + 1
        move = GetMinMaxMove(board, currentplayer)
        print("\nWHITE / MinMaxAI plays!\n")
    
    board = MovePiece(board,move)
    currentPlayerIndex = (currentPlayerIndex+1)%2
    currentplayer = 'black' if currentplayer == 'white' else 'white'

    DrawBoard(board)
    time.sleep(0.5)

# check and print - Stalemate or Checkmate
if(IsCheckmate(board,currentplayer)):
    print("CHECKMATE!")
    winnerIndex = (currentPlayerIndex+1)%2
    if(winnerIndex == 0):
        print("MinMaxAI - WHITE - uppercase won the game in " + str(turns) + " turns!")
    else:
        print("RandomAI - BLACK - lowercase won the game in " + str(turns) + " turns!")
else:
    print("STALEMATE!")