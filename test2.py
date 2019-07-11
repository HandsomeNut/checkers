import tkinter as tk
from math import floor
from tkinter import messagebox as msg

root = tk.Tk()
root.title(" Test Dame Feld ")
root.resizable(False, False)
checkersBoard = tk.Canvas(root, width=800, height=800, bg="beige")
checkersBoard.grid(column=0, row=0)


# for player tokens
class Token():
    def __init__(self, id, player, board, gui):
        self.id = id
        self.player = player
        self.king = False
        self.jumped = False
        self.coordBoard = board
        self.coordGui = gui



# Drawing the game board in GUI

# Even rows
for y in range(0, 801, 200):
    for x in range(0, 801, 200):
        checkersBoard.create_rectangle(x, y, x +100, y+100, fill="brown")
# Odd rows
for y in range(100, 701, 200):
    for x in range(100, 701, 200):
        checkersBoard.create_rectangle(x, y, x +100, y+100, fill="brown")



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

# Creating player tokens; Player 1
for y in range(0, 301, 100):
    for x in range(0, 701, 100):
        if (y == 0 or (y/100)%2 != 1) and (x/100)%2 == 0:
            id = checkersBoard.create_oval(x +10,y + 10,x + 90, y + 90, fill="red")
            tokens[id] = Token(id, 0,[floor((x +10) / 100), floor((y+10)/100)],[x+10, y+10])
        elif y == 100 and (x/100%2)==1:
            id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="red")
            tokens[id] = Token(id, 0, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])


x = 300
y = 300
id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
tokens[id] = Token(id, 1, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])

x = 500
y = 500
id = checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
tokens[id] = Token(id, 1, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])


print(tokens)

for id in tokens:
    x = tokens[id].coordBoard[0]
    y = tokens[id].coordBoard[1]
    field[y][x] = id

for row in field:
    print(row)

# Check for selected Fields in GUI

def tokenOnField(x, y):
    global markedID
    for piece in checkersBoard.find_overlapping(x, y, x+100, y+100):
        for id in tokens:
            if piece == id:
                if preMark is None and markedID is None:
                    markedID = tokens[id]
                return True

    return False

# Is selected field already marked?
def isPremark(x, y, mark):

    for piece in checkersBoard.find_overlapping(x, y, x+100, y+100):
        if piece == mark:
            return True
    return False

#
def noLegalMove(x, y, mark):
    print("mark.x", mark.coordGui[0])
    print("mark.y",mark.coordGui[1])
    print("x", x)
    print("y", y)
    # Abfrage ob ein Sprung mit Stein dazwischen
    if turn == 0:
        if y > mark.coordGui[1] + 100 and canjump(x,y, mark):
            return False
        elif mark.coordGui[1] > y and mark.king == False:
            return True
        elif y > mark.coordGui[1] + 100:
            return True
        elif mark.coordGui[0] - 100 < x > mark.coordGui[0] + 100:
            return True
        elif mark.coordGui[0] == x + 10:
            return True
    else:
        if not y > mark.coordGui[1] - 100 and canjump(x,y, mark):
            return False
        elif mark.coordGui[1] < y and mark.king == False:
            return True
        elif y > mark.coordGui[1] - 100:
            return True
        elif mark.coordGui[0] - 100 < x > mark.coordGui[0] + 100:
            return True
        elif mark.coordGui[0] == x + 10:
            return True


def canjump(x, y, mark):
    global tokens
    if not tokenOnField(x,y):
        if mark.coordGui[0] > x:
            dx = mark.coordGui[0] - x
            dx = floor(((dx/2) + x)/100)*100
        else:
            dx = x - mark.coordGui[0]
            dx = floor(((dx/2) + mark.coordGui[0])/100)*100

        if mark.coordGui[1] > y:
            dy = mark.coordGui[1] - y
            dy = floor(((dy/2) + y)/100)*100
        else:
            dy = y - mark.coordGui[1]
            dy = floor(((dy/2) + mark.coordGui[1])/100)*100

        print(dx, dy)
        if tokenOnField(dx,dy) and isEnemyToken(dx, dy):
            for piece in checkersBoard.find_overlapping(dx, dy, dx + 100, dy + 100):
                for id in tokens:
                    if piece == id:
                        tokens[id].jumped = True
            print("Jop, hier isn Stein!")
            return True
    return False

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

def noMoreJumps():
    return True

def winCondition():
    for key in tokens:
        if tokens[key].player == enemyPlayer():
            return
    msg.showinfo("Gewonnen", " Spieler 1 hat das Spiel gewonnen")

# Moving and removing playing pieces
def makemove(event):
    global preMark
    global markedID
    global tokens

    # Getting exact field coords
    x = floor(event.x/100)*100
    y = floor(event.y/100)*100
    if preMark is None:
        # Happens when first clicked
        if tokenOnField(x, y) and markedID.player != enemyPlayer():
            preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
        else:
            msg.showwarning("Achtung!", "Kein legaler Spielstein auf diesem Feld!")
            markedID = None

    # Happens when clicking the second time
    elif isPremark(x, y,preMark):
        msg.showwarning("Achtung!", "Feld ist bereits gewählt!")

    # If token is man
    elif markedID.king == False:
        if tokenOnField(x, y) or noLegalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        else:
            # resets times clicked
            checkersBoard.delete(preMark)
            preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
            checkersBoard.coords(markedID.id, x + 10, y + 10, x + 90, y + 90)
            tokens[markedID.id].coordGui = [x + 10, y + 10]
            tokens[markedID.id].coordBoard = [floor(x/100), floor(y/100)]
            if tokens[markedID.id].coordGui[1] > 700:
                msg.showinfo("Dame!", "Der Spielstein ist zur Dame geworden")
                tokens[markedID.id].king = True

            if noMoreJumps():
                checkersBoard.delete(preMark)
                markedID = None
                preMark = None
                switchTurn()


    # If token is king
    else:
        if tokenOnField(x, y) or noLegalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        else:
            # resets times clicked
            new = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
            checkersBoard.delete(preMark)
            checkersBoard.coords(markedID.id, x + 10, y + 10, x + 90, y + 90)
            tokens[markedID.id].coordGui = [x + 10, y + 10]
            tokens[markedID.id].coordBoard = [floor(x / 100), floor(y / 100)]
            markedID = None
            preMark = None
            checkersBoard.delete(new)

    winCondition()
    boardAnalysis()
    print(markedID)
    print(preMark)


checkersBoard.bind("<Button-1>", makemove)

root.mainloop()