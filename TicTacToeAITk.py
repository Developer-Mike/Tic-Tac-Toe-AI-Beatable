import tkinter as tk
from numpy import transpose
import random

random.seed()

size = {'x':3, 'y':3}
isHumanX = True if random.randint(0, 1) == 1 else False
turnX = True

def CreateMatrix(size):
    matrix = []
    for y in range(size['y']):
        matrix.append([])
        for _ in range(size['x']):
            matrix[y].append(None)
    return matrix

def RemoveMatrix(matrix):
    tmpList = []
    for element in matrix:
        if type(element) == list:
            for innerElement in element:
                tmpList.append(innerElement)
        else:
            tmpList.append(element)
    return tmpList

root = tk.Tk()
root.title('Tic Tac Toe')

noneSprite = tk.PhotoImage(file='None.png')
xSprite = tk.PhotoImage(file='X.png')
oSprite = tk.PhotoImage(file='O.png')

def Create2DTicTacToe():
    global fields
    field2D = CreateMatrix(size)
    for y in range(size['y']):
        for x in range(size['x']):
            if fields[x][y]["image"] == str(xSprite):
                field2D[x][y] = 'X'
            elif fields[x][y]["image"] == str(oSprite):
                field2D[x][y] = 'O'
            else:
                field2D[x][y] = None
    return field2D

def CheckForWin(board):
    #Check row and column (rotate)
    for newBoard in [board, transpose(board)]:
        #Check rows
        for row in newBoard:
            if len(set(row)) == 1 and row[0] != None:
                return row[0]
    
    #Check 
    #0 - -
    #- 0 -
    #- - 0
    if len(set([board[0][0], board[1][1], board[2][2]])) == 1 and board[0][0] != None:
        return board[0][0]
    
    #Check 
    #- - 0
    #- 0 -
    #0 - -
    if len(set([board[0][2], board[1][1], board[2][0]])) == 1 and board[0][2] != None:
        return board[0][2]

def UpdateCursor():
    global fields
    for button in RemoveMatrix(fields):
        if turnX:
            button['cursor'] = 'X_cursor'
        else:
            button['cursor'] = 'circle'

def DisableButtons(disable=True):
    global fields
    for button in RemoveMatrix(fields):
        if disable:
            button["state"] = tk.DISABLED
        else:
            button["state"] = tk.ACTIVE

def ResetFields():
    global fields, turnX, winner, isHumanX
    
    try:
        global popup
        popup.destroy()
    except:
        pass
    
    DisableButtons(False)
    for button in RemoveMatrix(fields):
        button['image'] = noneSprite
    
    turnX = True
    UpdateCursor()
    
    winner = None

    isHumanX = True if random.randint(0, 1) == 1 else False
    print(isHumanX)
    if not isHumanX:
        AITurn()

def AIBrain(board):
    global isHumanX, fields, size

    #Weight own more
    chars = ['O', 'X'] if isHumanX else ['X', 'O']
    for char in chars:
        #Check row and column (rotate)
        for boardNum, newBoard in enumerate([board, transpose(board)]):
            newBoard = list(newBoard)
            #Check rows
            for rowNum, row in enumerate(newBoard):
                row = list(row)
                if len(set(row)) == 2 and row.count(None) == 1 and char in set(row):
                    if boardNum == 1:
                        return list(newBoard[rowNum]).index(None), rowNum
                    else:
                        return rowNum, list(newBoard[rowNum]).index(None)

    #Weight own more
    diagonales = [[board[0][0], board[1][1], board[2][2]], [board[0][2], board[1][1], board[2][0]]]
    diagonaleAxes = [  [[0, 0],      [1, 1],      [2, 2]],      [[0, 2],      [1, 1],      [2, 0]]]
    for char in chars:
        #Check Diagonales
        for diagonaleNum, diagonale in enumerate(diagonales):
            if len(set(diagonale)) == 2 and diagonale.count(None) == 1 and char in diagonale:
                return diagonaleAxes[diagonaleNum][diagonale.index(None)]

    randomMove = [random.randint(0, size['x']-1), random.randint(0, size['y']-1)]
    while fields[randomMove[0]][randomMove[1]]["image"] != str(noneSprite):
        randomMove = [random.randint(0, size['x']-1), random.randint(0, size['y']-1)]

    return randomMove

def AITurn():
    global isHumanX

    if not isHumanX and turnX or isHumanX and not turnX:
        x, y = AIBrain(Create2DTicTacToe())
        Place(x, y, False)

def Place(X, Y, fromHuman):
    global turnX, fields, isHumanX

    EvaluateCheckForWin()

    #Check, if human at row
    if fromHuman and (isHumanX and not turnX or not isHumanX and turnX):
        return None

    if turnX:
        fields[X][Y]["image"]  = xSprite
        turnX = False
    else:
        fields[X][Y]["image"] = oSprite
        turnX = True
    fields[X][Y]["state"] = tk.DISABLED
    UpdateCursor()
    
    isWin = EvaluateCheckForWin()
    if not isWin:
        if fromHuman:
            AITurn()

def EvaluateCheckForWin():
    field2D = Create2DTicTacToe()
    global winner
    winner = CheckForWin(field2D)
    if winner != None:
        DisableButtons()
        WinnerScreen()
        return True
    elif not None in set(RemoveMatrix(field2D)):
        winner = 'Draw'
        DisableButtons()
        WinnerScreen()
        return True
    else:
        return False

def WinnerScreen():
    global winner, popup
    
    popup = tk.Toplevel(root)
    popup.title("Game Finished")
    
    def Quit():
        popup.destroy()
        root.destroy()
    
    tk.Label(popup, text='The Winner Is: '+winner).grid(row=0, column=0, columnspan=2)
    tk.Button(popup, text='Replay', relief='groove', command=lambda:ResetFields()).grid(row=1, column=0)
    tk.Button(popup, text='Quit', relief='groove', command=lambda:Quit()).grid(row=1, column=1)
    
    popup.resizable(0, 0)
    popup.protocol("WM_DELETE_WINDOW", Quit)

fields = CreateMatrix(size)
for y in range(size['y']):
    for x in range(size['x']):
        fields[x][y] = tk.Button(root, 
              width=100, height=100, 
              image=noneSprite, cursor='X_cursor',
              relief='groove', 
              command=lambda x=x, y=y: Place(x, y, True))
        fields[x][y].grid(row=x, column=y)

if not isHumanX:
    AITurn()

root.resizable(0, 0)
root.mainloop()