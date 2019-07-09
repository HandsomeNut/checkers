import tkinter as tk
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


def newField():
    field = [["O" if j%2!=1 else "X" for j in range(8)] if i%2!=1 else ["O" if j%2!=0 else "X" for j in range(8)] for i in range(8)]
    return field

print(checkersBoard.find_all())

tokens = {}
preMark = None
markedID = None
field = newField()

token = Token()
token.id = checkersBoard.create_oval(10,10,90, 90, fill="red")
token.player = "p1"
token.coordGui = [checkersBoard.coords(token.id)[0] - 10, checkersBoard.coords(token.id)[1] - 10]
token.coordBoard = [floor(token.coordGui[0]/100), floor(token.coordGui[1]/100)]

tokens[token.id] = token

token = Token()
token.id = checkersBoard.create_oval(210, 210, 290, 290, fill="white")
token.player = "p2"
token.coordGui = [checkersBoard.coords(token.id)[0] - 10, checkersBoard.coords(token.id)[1] - 10]
token.coordBoard = [floor(token.coordGui[0] / 100), floor(token.coordGui[1] / 100)]

tokens[token.id] = token

print(tokens)

for key in tokens:
    x = tokens[key].coordBoard[0]
    y = tokens[key].coordBoard[1]
    field[y][x] = tokens[key].id

for row in field:
    print(row)

root.mainloop()