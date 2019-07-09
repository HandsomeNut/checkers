import tkinter as tk
from tkinter import messagebox as msg, CENTER
from math import floor

root = tk.Tk()
root.title(" Test Dame Feld ")
root.resizable(False, False)
checkersBoard = tk.Canvas(root, width=800, height=800, bg="beige")
checkersBoard.grid(column=0, row=0)

class Token():
    id = None
    player = None
    king = False
    coordBoard = []
    coordGui = []


# Drawing the game board in GUI

# Even rows
for y in range(0, 801, 200):
    for x in range(0, 801, 200):
        checkersBoard.create_rectangle(x, y, x +100, y+100, fill="brown")
# Odd rows
for y in range(100, 701, 200):
    for x in range(100, 701, 200):
        checkersBoard.create_rectangle(x, y, x +100, y+100, fill="brown")

# Creating a game board array
def newField():
    field = [["O" if j%2!=1 else "X" for j in range(8)] if i%2!=1 else ["O" if j%2!=0 else "X" for j in range(8)] for i in range(8)]
    return field

print(checkersBoard.find_all())

tokens = []
preMark = None
markedID = None
field = newField()

for row in field:
    print(row)


tokens.append([checkersBoard.create_oval(10,10,90, 90, fill="red"), "p1", False])
tokens.append([checkersBoard.create_oval(210,210,290, 290, fill="white"), "p2", False])

# Check for selected Fields in GUI

def tokenOnField(x, y):
    global markedID
    for piece in checkersBoard.find_overlapping(x, y, x+100, y+100):
        for token in tokens:
            if piece == token[0]:
                if preMark is None:
                    markedID = token
                return True

    return False

# Is selected field already marked
def isPremark(x, y, mark):

    for piece in checkersBoard.find_overlapping(x+2, y+2, x+98, y+98):
        if piece == mark:
            return True
    return False

#
def noLegalMove(x, y, mark):
    if checkersBoard.coords(mark[0])[1] > y and mark[2] == False:
        return True
    elif y > checkersBoard.coords(mark[0])[1] + 100:
        return True
    elif checkersBoard.coords(mark[0])[0] - 100 < x > checkersBoard.coords(mark[0])[0] + 100:
        return True
    elif checkersBoard.coords(mark[0])[0] == x + 10:
        return True

def checkForEnemy(x , y, mark):
    field = newField()
    if field[y/100][x/100] != "O":
        for token in tokens:
            pass


def boardAnalysis():
    field = newField()
    for token in tokens:
        x = floor(checkersBoard.coords(token[0])[0]/100)
        y = floor(checkersBoard.coords(token[0])[1]/100)
        field[y][x] = token[0]

    for row in field:
        print(row)

def winCondition():
    for token in tokens:
        if token[1] == "p2":
            return
    msg.showinfo("Gewonnen", " Spieler 1 hat das Spiel gewonnen")
# Moving and removing playing pieces
def makemove(event):
    global preMark
    global markedID
    # Getting exact field coords
    x = floor(event.x/100)*100
    y = floor(event.y/100)*100
    if preMark is None:
        # Happens when first clicked
        if tokenOnField(x, y) and markedID[1] !="p2":
            preMark = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
        else:
            msg.showwarning("Achtung!", "Kein legaler Spielstein auf diesem Feld!")

    # Happens when clicking the second time
    elif isPremark(x, y,preMark):
        msg.showwarning("Achtung!", "Feld ist bereits gewählt!")

    # If token is man
    elif markedID[2] == False:
        if tokenOnField(x, y) or noLegalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        else:
            # resets times clicked
            new = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
            checkersBoard.delete(preMark)
            checkersBoard.coords(markedID[0], x + 10, y + 10, x + 90, y + 90)
            if checkersBoard.coords(tokens[0][0])[1] > 700:
                msg.showinfo("Dame!", "Der Spielstein ist zur Dame geworden")
                tokens[0][2] = True

            markedID = None
            preMark = None
            checkersBoard.delete(new)
    # If token is king
    else:
        if tokenOnField(x, y) or noLegalMove(x, y, markedID):
            msg.showwarning("Achtung", "Kann Stein nicht auf dieses Feld bewegen")
        else:
            # resets times clicked
            new = checkersBoard.create_rectangle(x + 2, y + 2, x + 98, y + 98, width=4, outline="yellow")
            checkersBoard.delete(preMark)
            checkersBoard.coords(markedID[0], x + 10, y + 10, x + 90, y + 90)
            markedID = None
            preMark = None
            checkersBoard.delete(new)

    winCondition()
    boardAnalysis()
    print(markedID)
    print(preMark)


checkersBoard.bind("<Button-1>", makemove)

root.mainloop()

