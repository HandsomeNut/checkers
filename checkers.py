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

mainWindow = GameWindow()
mainWindow.root.mainloop()