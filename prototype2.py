import tkinter as tk
from math import floor
from tkinter import messagebox as msg


# Main window creation
root = tk.Tk()
root.title(" Test Dame Feld ")
root.resizable(False, False)
# canvas element 800w * 800h
checkersBoard = tk.Canvas(root, width=800, height=800, bg="beige")
checkersBoard.grid(column=0, row=0)


# for player tokens
class Token():
    def __init__(self, player, board, gui):
        self.player = player
        self.king = False
        self.jumped = False
        self.coordBoard = board
        self.coordGui = gui
        self.moveable = True



# Drawing the game board in GUI

# Even rows
for y in range(0, 801, 200):
    for x in range(0, 801, 200):
        checkersBoard.create_rectangle(x, y, x +100, y+100, fill="brown")
# Odd rows
for y in range(100, 701, 200):
    for x in range(100, 701, 200):
        checkersBoard.create_rectangle(x, y, x +100, y+100, fill="brown")


# creating a game board 2D array, for later AI interfacing
def newField():
    field = [["O" if j%2!=1 else "X" for j in range(8)] if i%2!=1 else ["O" if j%2!=0 else "X" for j in range(8)] for i in range(8)]
    return field

print(checkersBoard.find_all())

# Essential game variables
tokens = {}
preMark = None
markedID = None
field = newField()
turn = 0    # 0 => Player 1; 1 => Player 2

# Creating tokens; Player 1
for y in range(0, 301, 100):
    for x in range(0, 701, 100):
        # even numbered row
        if (y == 0 or (y/100)%2 != 1) and (x/100 % 2) == 0:
            id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="red")
            tokens[id] = Token(0, [floor((x + 10) / 100), floor((y+10)/100)], [x+10, y+10])
        # odd numbered row
        elif y == 100 and (x/100 % 2) == 1:
            id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="red")
            tokens[id] = Token(0, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])

# Creating tokens; Player 2
x = 300
y = 300
id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
tokens[id] = Token(1, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])

x = 500
y = 500
id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
tokens[id] = Token(1, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])


print(tokens)

# Writing present tokens on board into array
for id in tokens:
    x = tokens[id].coordBoard[0]
    y = tokens[id].coordBoard[1]
    field[y][x] = id

for row in field:
    print(row)

# to check if field is free and to select token for move
def tokenOnField(x, y):
    global markedID
    for piece in checkersBoard.find_overlapping(x, y, x+100, y+100):
        for id in tokens:
            if piece == id:
                if preMark is None and markedID is None:
                    markedID = id
                    print(markedID)
                return True

    return False

# Is selected field already marked?
def isPremark(x, y, mark):

    for piece in checkersBoard.find_overlapping(x, y, x+100, y+100):
        if piece == mark:
            return True
    return False

# Movement rules for tokens
def legalMove(x, y, id):
    print("mark.x", tokens[id].coordGui[0])
    print("mark.y", tokens[id].coordGui[1])
    print("x", x)
    print("y", y)
    # Rules for player 1
    if turn == 0:
        # token is inbetween 2 fields to jump over forward
        if y > tokens[id].coordGui[1] + 100 and canjump(x, y, id):
            return True
        # can only move diagonal towards the enemy
        elif tokens[id].coordGui[1] + 100 == y + 10 and (tokens[id].coordGui[0] - 100 == x + 10 \
                or x + 10 == tokens[id].coordGui[0] + 100) and not tokens[id].king:
            return True
    # Rules for player 2/ same as player 1 in reverse
    else:
        if y < tokens[id].coordGui[1] - 100 and canjump(x, y, id):
            return True
        elif tokens[id].coordGui[1] - 100 == y + 10 and (tokens[id].coordGui[0] - 100 == x + 10 \
                or x + 10 == tokens[id].coordGui[0] + 100) and not tokens[id].king:
            return True

def canjump(x, y, id):
    global tokens
    # is the target field free?
    if not tokenOnField(x,y):
        # getting the coordinates for the field between
        if tokens[id].coordGui[0] > x:
            dx = tokens[id].coordGui[0] - x
            dx = floor(((dx/2) + x)/100)*100
        else:
            dx = x - tokens[id].coordGui[0]
            dx = floor(((dx/2) + tokens[id].coordGui[0]) / 100) * 100

        if tokens[id].coordGui[1] > y:
            dy = tokens[id].coordGui[1] - y
            dy = floor(((dy/2) + y)/100)*100
        else:
            dy = y - tokens[id].coordGui[1]
            dy = floor(((dy/2) + tokens[id].coordGui[1]) / 100) * 100

        print(dx, dy)
        # checking if a token is on the field inbetween and if its an enemy
        if tokenOnField(dx,dy) and isEnemyToken(dx, dy):
            for piece in checkersBoard.find_overlapping(dx, dy, dx + 100, dy + 100):
                for id in tokens:
                    if piece == id:
                        # setting token for being deleted
                        tokens[id].jumped = True
            print("Jop, hier isn Stein!")
            return True
    return False

# gives back the enemy player id for the turn
def enemyPlayer():
    if turn == 0:
        return 1
    else:
        return 0


def isEnemyToken(x, y):
    for piece in checkersBoard.find_overlapping(x, y, x+100, y+100):
        for id in tokens:
            if piece == id and tokens[id].player == enemyPlayer():
                return True
    return False

# checks the board for tokens to delete and writes the present board into the array
def boardAnalysis():
    field = newField()
    for id in tokens:
        if tokens[id].jumped:
            checkersBoard.delete(id)
            del tokens[id]
            break
    for id in tokens:
        x = floor(checkersBoard.coords(id)[0] / 100)
        y = floor(checkersBoard.coords(id)[1] / 100)
        field[y][x] = id


    for row in field:
        print(row)

def switchTurn():
    global turn
    if turn == 0:
        turn = 1
        print("Spieler 2 ist am Zug!")
    else:
        turn = 0
        print("Spieler 1 ist am Zug!")

# can the present token jump over more tokens
def noMoreJumps():
    return True

# def turnPossible():
#     global tokens
#     for id in tokens:
#         if tokens[id].player == turn:
#             x2 = tokens[id].coordGui[0] - 10
#             y2 = tokens[id].coordGui[1] - 10
#             if not tokenOnField(x2 + 100, y2 + 100) or isEnemyToken(x2 + 100, y2 + 100):
#                 tokens[id].moveable = True
#                 print(id, x2, y2, "YEAH" ,tokens[id].coordGui[0],tokens[id].coordGui[1])
#             elif not tokenOnField(x2 - 100, y2 + 100) or isEnemyToken(x2 - 100, y2 + 100):
#                 tokens[id].moveable = True
#                 print(id, x2, y2, "YEAH!!!")
#             else:
#                 print(id, x2, y2, "Nein!")
#                 tokens[id].moveable = False

def winCondition():
    for id in tokens:
        if tokens[id].player == enemyPlayer():
            return
        if tokens[id].moveable:
            return
    msg.showinfo("Gewonnen", " Spieler 1 hat das Spiel gewonnen")

# Moving and removing playing pieces
def makemove(event):
    global preMark
    global markedID
    global tokens

    # turnPossible()

    # Getting exact field coords
    x = floor(event.x/100)*100
    y = floor(event.y/100)*100
    # Happens when first clicked
    if preMark is None:
        # drawing marker and selecting token
        if tokenOnField(x, y) and tokens[markedID].player != enemyPlayer(): #and tokens[markedID].moveable:
            preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
        else:
            msg.showwarning("Achtung!", "Kein legaler Spielstein auf diesem Feld!")
            markedID = None

    # Happens when clicking the second time
    elif isPremark(x, y,preMark):
        msg.showwarning("Achtung!", "Feld ist bereits gewählt!")

    # If token is man
    elif tokens[markedID].king == False:
        if tokenOnField(x, y) or not legalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        # if move is possible, resets marker to new position, updates token on board and coordinates in token object
        else:
            checkersBoard.delete(preMark)
            preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
            checkersBoard.coords(markedID, x + 10, y + 10, x + 90, y + 90)
            tokens[markedID].coordGui = [x + 10, y + 10]
            tokens[markedID].coordBoard = [floor(x/100), floor(y/100)]
            if tokens[markedID].coordGui[1] > 700:
                msg.showinfo("Dame!", "Der Spielstein ist zur Dame geworden")
                tokens[markedID].king = True
            # if moved or jumped and no more jumps available
            if noMoreJumps():
                checkersBoard.delete(preMark)
                markedID = None
                preMark = None
                switchTurn()


    # If token is king
    else:
        if tokenOnField(x, y) or not legalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        else:
            # resets times clicked
            new = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
            checkersBoard.delete(preMark)
            checkersBoard.coords(markedID, x + 10, y + 10, x + 90, y + 90)
            tokens[markedID].coordGui = [x + 10, y + 10]
            tokens[markedID].coordBoard = [floor(x / 100), floor(y / 100)]
            markedID = None
            preMark = None
            checkersBoard.delete(new)
    # checking for win and analysing and finally updating the board in GUI and Array
    winCondition()
    boardAnalysis()
    print(markedID)
    print(preMark)

# if left clicking on Canvas
checkersBoard.bind("<Button-1>", makemove)


# start main eventloop
root.mainloop()