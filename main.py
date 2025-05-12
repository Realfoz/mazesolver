from tkinter import Tk, BOTH, Canvas

root = Tk() # makes a window
root.title("Maze Solver")
root.geometry("420x420") # sets window dimensions
root.mainloop() # places window on screen, listen for events

maze = Canvas(master=None,bg="white")

