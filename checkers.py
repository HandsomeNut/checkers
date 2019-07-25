import tkinter as tk
import math as floor
from tkinter import messagebox as msg

# token data type to store information for every token
class Token():
    def __init__(self, player, board, gui):
        self.player = player
        self.coordboard = board
        self.coordGui = gui
        self.king = False
        self.moveable = False
        self.jumped = False
        self.dead = False


# Main window class
class GameWindow():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Tk-Checkers ")
        self.root.resizable(False, False)
        self.checkersBoard = tk.Canvas(self.root, width=800, height=800, bg="beige")
        self.checkersBoard.grid(row=0, column= 0)
        self.boardObjects()

    def boardObjects(self):
        # Drawing the game board in GUI

        # Even rows
        for y in range(0, 801, 200):
            for x in range(0, 801, 200):
                self.checkersBoard.create_rectangle(x, y, x + 100, y + 100, fill="brown")
        # Odd rows
        for y in range(100, 701, 200):
            for x in range(100, 701, 200):
                self.checkersBoard.create_rectangle(x, y, x + 100, y + 100, fill="brown")

        # Essential game variables
        tokens = {}
        # preMark = None
        # markedID = None
        # enemyID = None
        # field = newField()
        # turn = 0  # 0 => Player 1; 1 => Player 2

        # Creating tokens; Player 1
        for y in range(0, 301, 100):
            for x in range(0, 701, 100):
                # even numbered row
                if (y == 0 or (y / 100) % 2 != 1) and (x / 100 % 2) == 0:
                    id = self.checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="red")
                    # tokens[id] = Token(0, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])
                # odd numbered row
                elif y == 100 and (x / 100 % 2) == 1:
                    id = self.checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="red")
                    # tokens[id] = Token(0, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])

        # Creating tokens; Player 2
        for y in range(500, 701, 100):
            for x in range(0, 701, 100):
                # even odd row
                if (y == 500 or (y / 100) % 2 != 0) and (x / 100 % 2) == 1:
                    id = self.checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
                    # tokens[id] = Token(1, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])
                # even numbered row
                elif y == 600 and (x / 100 % 2) == 0:
                    id = self.checkersBoard.create_oval(x + 10, y + 10, x + 90, y + 90, fill="white")
                    # tokens[id] = Token(1, [floor((x + 10) / 100), floor((y + 10) / 100)], [x + 10, y + 10])

        print(tokens)


mainWindow = GameWindow()
mainWindow.root.mainloop()