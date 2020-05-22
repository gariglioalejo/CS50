"""
Tic Tac Toe Player
"""

import math
import copy


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

# return [[EMPTY, X, O],
#             [O, X, X],
#             [X, EMPTY, O]]

    # return [[O, X, EMPTY],
    #             [EMPTY, X, EMPTY],
    #             [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    celdasOcupadas = 0

    for y in range(3): 
        celdasOcupadas += sum(x is not None for x in board[y])
        
    #print("Celdas Ocupadas: ",celdasOcupadas)
    if celdasOcupadas == 9:
        #print ("Turno de None")
        return "Nadie"

    elif celdasOcupadas % 2 == 0:
        # print ("Turno de X")
        return "X"
    else:
        # print ("Turno de O")
        return "O"



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    acciones =[]

    for i in range(3):
        for j in range (3):
            if board[i][j] == EMPTY:
                #print ("La Celda [%s][%s] está disponible" % (i,j))
                accion = i,j
                acciones.append(accion)

    return acciones


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    auxBoard = copy.deepcopy(board)


    if auxBoard[action[0]][action[1]] != EMPTY:
        # print("Casillero Ocupado")
        return board
    # print("se ocupo un casillero")
    actingPlayer = player(auxBoard)
    auxBoard[action[0]][action[1]] = actingPlayer


    return auxBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    ganador = "Nadie"
    winning_positions = [[(0,0),(0,1),(0,2)],
                         [(1,0),(1,1),(1,2)],
                         [(2,0),(2,1),(2,2)],
                         [(0,0),(1,0),(2,0)],
                         [(0,1),(1,1),(2,1)],
                         [(2,0),(2,1),(2,2)],
                         [(0,0),(1,1),(2,2)],
                         [(0,2),(1,1),(2,0)]]


    for i in range(len(winning_positions)):
        ganador = ganadorFilaColumna(winning_positions[i],board)
        if ganador != "Nadie":
            return ganador
    #print(ganador)
    return ganador



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != "Nadie":
        #print("terminal 1")
        return True

    else:
        if player(board) == "Nadie":
            #print("terminal 2")
            return True
        else:
            #print("terminal 3")
            return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    ganador = winner(board)
    if ganador == "X":
        return 1
    
    if ganador == "O":
        return -1
    

    return 0

def ganadorFilaColumna(FilaComlumna,board):
    """
    Returns the winner of an specified line/column
    """

    if board[FilaComlumna[0][0]][FilaComlumna[0][1]] == board[FilaComlumna[1][0]][FilaComlumna[1][1]] == board[FilaComlumna[2][0]][FilaComlumna[2][1]] != EMPTY:
        return board[FilaComlumna[0][0]][FilaComlumna[0][1]]

    else:
        return "Nadie"

def minimax(board):

    """
    Returns the optimal action for the current player on the board.
    """
    auxBoard = copy.deepcopy(board)
    if terminal(board):
        return None

    if player(board) == "X":


        vtobeat = float('-inf')
        acciones = actions(board)

        for accion in acciones:
            if winning_move(auxBoard,accion):
                return accion


        for accion in acciones:

            score = minvalue(auxBoard,accion)

            if score > vtobeat:
                bestaction = accion
                vtobeat = score

        
        return bestaction
    
    if player(board) == "O":


        vtobeat = float('inf')
        acciones = actions(board)

        for accion in acciones:
            if winning_move(auxBoard,accion):
                return accion

        for accion in acciones:

            score = maxvalue(auxBoard,accion)

            if score < vtobeat:
                bestaction = accion
                vtobeat = score

        
        return bestaction



def minvalue(board,action):


    auxBoard = result(board,action)

    if terminal(auxBoard):
        return utility(auxBoard)
    else:
        v = float('inf')
        acciones = actions(auxBoard)
        for action in acciones:

            v = min(v,maxvalue(auxBoard,action))

        return v


def maxvalue(board,action):
    
    auxBoard = result(board,action)

    if terminal(auxBoard):
        return utility(auxBoard)
    
    else:
        v = float('-inf')
        acciones = actions(auxBoard)
        for action in acciones:
            valorMinimoO = minvalue(auxBoard,action)
            v = max(v,valorMinimoO)

        return v

def winning_move(board,action):

    auxBoard = result(board,action)

    if not(terminal(auxBoard)):
        return False
        
    elif winner(auxBoard) == "Nadie":
        return False
            
    else:
        return True





def takeSecond(elem):
    return elem[1]

board = initial_state()
