from tkinter import Tk, BOTH, Canvas
import time
import random

class Window:
    def __init__(self, width, height):
        self.__root = Tk()  # makes the window
        self.__root.geometry(f"{width}x{height}")  
        self.__root.title("Maze Solver")  # Set the title
        self.__canvas = Canvas(self.__root, bg="white")  # root as master
        self.__canvas.pack(fill=BOTH, expand=1)  # Create and pack the canvas
        self.__running = False  # running state
        self.__root.protocol("WM_DELETE_WINDOW", self.close)  # Handle window close
            
    
    def redraw(self): # handles updating the maze each frame(?) i think.
        self.__root.update_idletasks()
        self.__root.update()

    def draw_line(self, line, fill_colour):
        line.draw(self.__canvas, fill_colour)
    
    def wait_for_close(self):
        self.__running = True

        while self.__running == True: # loops the redraw method to update it
            self.redraw()
        
        
    
    def close(self):
        self.__running = False
        

class Point:
    def __init__(self, x_coord, y_coord):
        self.x = x_coord
        self.y = y_coord    


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def draw(self, canvas, colour):
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y , fill= colour, width=2)

class Cell:
    def __init__(self,x1, y1, x2, y2, win):
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.has_right_wall = True
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = win
        self.visited = False

    def draw(self, colour):
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x2, self._y1)
        wall_color = colour if self.has_top_wall else "white"
        self._win.draw_line(Line(p1, p2), wall_color)
        
        
        p1 = Point(self._x1, self._y2)
        p2 = Point(self._x2, self._y2)
        wall_color = colour if self.has_bottom_wall else "white"
        self._win.draw_line(Line(p1, p2), wall_color)

        
        p1 = Point(self._x1, self._y1)
        p2 = Point(self._x1, self._y2)
        wall_color = colour if self.has_left_wall else "white"
        self._win.draw_line(Line(p1, p2), wall_color)

        
        p1 = Point(self._x2, self._y1)
        p2 = Point(self._x2, self._y2)
        wall_color = colour if self.has_right_wall else "white"
        self._win.draw_line(Line(p1, p2), wall_color)


    def _draw_wall(self, p1, p2, has_wall, colour):
        wall_colour = colour if has_wall else "white"
        line = Line(p1, p2)
        self._win.draw_line(line, wall_colour)

    def draw_move(self, to_cell, undo=False):
        colour = "red"
        if undo:
            colour = "gray"

        # Midpoint of self (this cell)
        mid_x = (self._x1 + self._x2) / 2
        mid_y = (self._y1 + self._y2) / 2
        mid = Point(mid_x, mid_y)

        # Midpoint of target cell
        target_mid_x = (to_cell._x1 + to_cell._x2) / 2
        target_mid_y = (to_cell._y1 + to_cell._y2) / 2
        target_mid = Point(target_mid_x, target_mid_y)

        line1 = Line(mid, target_mid)
        self._win.draw_line(line1, colour)

        
class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed != None:
            self.seed = seed
        else:
            self.seed = None

        if self.num_rows == 0 or self.num_cols == 0 or self.cell_size_x == 0 or self.cell_size_y == 0:
            raise ValueError("Maze dimensions and cell sizes must be greater than zero")

        self._create_cells() # creates the grid of cells

    def _create_cells(self):
        self._cells = []
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                cell = Cell(
                self.x1 + (i * self.cell_size_x),
                self.y1 + (j * self.cell_size_y),
                self.x1 + ((i+1) * self.cell_size_x),
                self.y1 + ((j+1) * self.cell_size_y),
                self.win)
                column.append(cell)     
            self._cells.append(column)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        if self.win is not None:
            cell.draw("black")
            self._animate()
    
    def _animate(self):
        if self.win is not None:
            self.win.redraw()
            time.sleep(0.01)

    def _break_entrance_and_exit(self):
        if self._cells[0][0]:
            self._cells[0][0].has_top_wall = False
            self._draw_cell(0,0)


        end_cell = self._cells[self.num_cols - 1][self.num_rows - 1]
        if end_cell:
            end_cell.has_bottom_wall = False
            self._draw_cell(self.num_cols - 1,self.num_rows - 1)
            

## ---------------------------------------------- probably should be a new .py file but fuck it we ball

def main():
    win = Window(800, 600)

    maze = Maze(100,100,5,5,50,50,win) # 10,10,19,26,30,30,win
    maze._break_entrance_and_exit()
    

    win.wait_for_close()

if __name__ == "__main__":
    main()
