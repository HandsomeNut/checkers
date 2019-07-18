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
        self.king = True
        self.dead = False
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
fieldX = 0
fieldY = 0

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
for y in range(500, 701, 100):
    for x in range(0, 701, 100):
        # even odd row
        if (y == 500 or (y/100)%2 != 0) and (x/100 % 2) == 1:
            id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
            tokens[id] = Token(1, [floor((x + 10) / 100), floor((y+10)/100)], [x+10, y+10])
        # even numbered row
        elif y == 600 and (x/100 % 2) == 0:
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
                if preMark is None:
                    markedID = id
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
    # Rules for player 1
    if tokens[id].king:
        dx, dy = getDelta(x, y, id)
        print(dx, dy)
        # If Jump possible
        if dx/dy == 1 and canJump(x, y, id) and not tokens[id].jumped:
            makeJump(id)
            return True
        # If can make regular move
        elif dx/dy == 1 and not tokens[id].jumped:
            return True
        # If already jump and can jumpAgain only if next to token
        elif dx/dy == 1 and canJump(x, y, id) and tokens[id].coordGui[1] + 201 <= y >= tokens[id].coordGui[1] - 211:
            return True

        print("shit happened")
    elif turn == 0:
        # token is inbetween 2 fields to jump over forward
        if y > tokens[id].coordGui[1] + 100 and canJump(x, y, id):
            makeJump(id)
            return True
        # can only move diagonal towards the enemy
        elif tokens[id].coordGui[1] + 100 == y + 10 and (tokens[id].coordGui[0] - 100 == x + 10 \
                or x + 10 == tokens[id].coordGui[0] + 100) and not tokens[id].jumped:
            return True
    # Rules for player 2/ same as player 1 in reverse
    else:
        if y < tokens[id].coordGui[1] - 100 and canJump(x, y, id):
            makeJump(id)
            return True
        elif tokens[id].coordGui[1] - 100 == y + 10 and (tokens[id].coordGui[0] - 100 == x + 10 \
                or x + 10 == tokens[id].coordGui[0] + 100) and not tokens[id].jumped:
            return True

def canJump(x, y, id):
    # is the target field free?
    if not tokenOnField(x,y):
        # getting the coordinates for the field in between
        prevX, prevY = previousField(x, y, id)
        # checking if a token is on the field inbetween and if its an enemy
        if tokenOnField(prevX,prevY) and isEnemyToken(prevX, prevY):
            print("Jop, hier isn Stein!", prevX, prevY)
            return True
    return False

def previousField(x, y, id):
    global fieldX, fieldY
    # Coordinates of the previous field
    if tokens[id].coordGui[0] > x:
        fieldX = x + 100
    else:
        fieldX = x - 100

    if tokens[id].coordGui[1] > y:
        fieldY = y + 100
    else:
        fieldY = y - 100

    return fieldX, fieldY

def getDelta(x, y, id):
    # neutral Delta move values for x and y
        if tokens[id].coordGui[0] > x:
            dx = floor(tokens[id].coordGui[0]/100)*100 - x
        else:
            dx = x - floor(tokens[id].coordGui[0]/100)*100

        if tokens[id].coordGui[1] > y:
            dy = floor(tokens[id].coordGui[1]/100)*100 - y
        else:
            dy = y - floor(tokens[id].coordGui[1]/100)*100

        return dx, dy

# Jump over a token
def makeJump(markedID):
    global tokens
    for piece in checkersBoard.find_overlapping(fieldX, fieldY, fieldX + 100, fieldY + 100):
        for id in tokens:
            if piece == id and preMark is not None:
                # setting token for being deleted
                tokens[id].dead = True
                tokens[markedID].jumped = True


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
        if tokens[id].dead:
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
    global turn, markedID, preMark

    checkersBoard.delete(preMark)
    markedID = None
    preMark = None

    # switching turn over
    if turn == 0:
        turn = 1
        print("Spieler 2 ist am Zug!")
    else:
        turn = 0
        print("Spieler 1 ist am Zug!")

    winCondition()


def turnPossible():
    global tokens

    # setting the values with respect to player side
    if turn == 0:
        nmove = 100
        jmove = 200

    else:
        nmove = -100
        jmove = -200
    for id in tokens:
        if tokens[id].player == turn:
            x = tokens[id].coordGui[0] - 10
            y = tokens[id].coordGui[1] - 10
            # False if at the right side an no way to jump
            if x > 699 and (tokenOnField(x - 100, y + nmove) and not canJump(x - 200, y + jmove, id)):
                tokens[id].moveable = False
            # False if at the left side and no way to jump over enemy
            elif x < 100 and (tokenOnField(x + 100, y + nmove) and not canJump(x + 200, y + jmove, id)):
                tokens[id].moveable = False
            # True if field to the right is free or enemy token to jump over
            elif not tokenOnField(x + 100, y + nmove) or isEnemyToken(x + 100, y + nmove) \
                    and (not x > 599 and canJump(x + 200, y + jmove, id)):
                tokens[id].moveable = True
            # Same for the left side
            elif not tokenOnField(x - 100, y + nmove) or isEnemyToken(x - 100, y + nmove) \
                    and (not x < 200 and canJump(x - 200, y + jmove, id)):
                tokens[id].moveable = True
            else:
                tokens[id].moveable = False

def jumpAgain(id):

    x = tokens[id].coordGui[0]
    y = tokens[id].coordGui[1]
    if turn == 0:
        # make check for Player 1
        if ((x < 600 and canJump(x + 200, y + 200, id)) or (x > 200 and canJump(x - 200, y + 200, id))) and y < 600:
           return True
        return False
        # check for Player 2
    else:
        if ((x < 600 and canJump(x + 200, y - 200, id)) or (x > 200 and canJump(x - 200, y - 200, id))) and y > 200:
           return True
        return False

def winCondition():
    print(turn)
    # turncheck when changing Turns
    turnPossible()
    for id in tokens:
        if tokens[id].player == turn:
            if tokens[id].moveable:
                return
    msg.showinfo("Gewonnen", "Spieler " + str(enemyPlayer() + 1) + " hat das Spiel gewonnen")

# happens at the end of every move
def moveMade(x, y):
    global preMark, tokens
    checkersBoard.delete(preMark)
    preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
    checkersBoard.coords(markedID, x + 10, y + 10, x + 90, y + 90)
    tokens[markedID].coordGui = [x + 10, y + 10]
    tokens[markedID].coordBoard = [floor(x / 100), floor(y / 100)]
    boardAnalysis()

# Moving and removing playing pieces
def makemove(event):
    global preMark, tokens, markedID

    # Getting exact field coords
    x = floor(event.x/100)*100
    y = floor(event.y/100)*100
    # Happens on first click
    if preMark is None:
        # drawing marker and marking ID of token in that field
        if tokenOnField(x, y) and tokens[markedID].player != enemyPlayer() and tokens[markedID].moveable:
            preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
        else:
            msg.showwarning("Achtung!", "Zug nicht möglich!")
            markedID = None

    # Happens when clicking the second time
    elif isPremark(x, y, preMark):
        deselectField = msg.askyesno("Achtung!", "Stein ist bereits gewählt!\nStein abwählen?")
        if deselectField:
            checkersBoard.delete(preMark)
            preMark = None

    # If token is man
    elif not tokens[markedID].king:
        if tokenOnField(x, y) or not legalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        # if token has jumped
        elif tokens[markedID].jumped:
            moveMade(x, y)
            if not jumpAgain(markedID):
                if (turn == 0 and tokens[markedID].coordGui[1] > 700) or (turn == 1 and tokens[markedID].coordGui[1] < 100):
                    msg.showinfo("Dame!", "Der Spielstein ist zur Dame geworden")
                    tokens[markedID].king = True
                tokens[markedID].jumped=False
                switchTurn()
            else:
                msg.showinfo("Weiterspringen!", "Spring weiter!")

        # if move is possible, resets marker to new position, updates token on board and coordinates in token object
        else:
            moveMade(x, y)
            if (turn == 0 and tokens[markedID].coordGui[1] > 700) or (turn == 1 and tokens[markedID].coordGui[1] < 100):
                msg.showinfo("Dame!", "Der Spielstein ist zur Dame geworden")
                tokens[markedID].king = True

            switchTurn()
    # If token is king
    else:
        if tokenOnField(x, y) or not legalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        elif tokens[markedID].jumped:
            moveMade(x, y)
            if not jumpAgain(markedID):
                tokens[markedID].jumped = False
                switchTurn()
            else:
                msg.showinfo("Weiterspringen!", "Spring weiter!")
        else:
            # resets times clicked # if moved
            moveMade(x, y)

            switchTurn()

    # checking for win and analysing and finally updating the board in GUI and Array
    print(markedID)
    print(preMark)

# if left clicking on Canvas
checkersBoard.bind("<Button-1>", makemove)

# Initial Boardcheck
turnPossible()

# start main eventloop
root.mainloop()