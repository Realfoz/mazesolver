from tkinter import Tk, BOTH, Canvas

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

    def draw(self, colour):
        if self.has_top_wall:
            p1 = Point(self._x1, self._y1)
            p2 = Point(self._x2, self._y1)
            top_line = Line(p1,p2)
            self._win.draw_line(top_line, colour)  # Use the Window's draw_line method

        if self.has_bottom_wall:
            p1 = Point(self._x1, self._y2)
            p2 = Point(self._x2, self._y2)
            bot_line = Line(p1,p2)
            self._win.draw_line(bot_line, colour)

        if self.has_left_wall:
            p1 = Point(self._x1, self._y1)
            p2 = Point(self._x1, self._y2)
            left_line = Line(p1,p2)
            self._win.draw_line(left_line, colour)

        if self.has_right_wall:
            p1 = Point(self._x2, self._y1)
            p2 = Point(self._x2, self._y2)
            right_line = Line(p1,p2)
            self._win.draw_line(right_line, colour)

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
        win,
    ):
        self.x = x1
        self.y = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win

    def _create_cells(self):
        cells = []
        


## ---------------------------------------------- probably should be a new .py file but fuck it we ball

def main():
    win = Window(800, 600)

    cell1 = Cell(100,200,200,300, win)
    cell1.has_bottom_wall = False
    cell1.has_top_wall = False
    cell1.draw("black")

    cell2 = Cell(300, 200, 400, 300, win)
    cell2.has_right_wall = False  
    cell2.draw("red")

    cell3 = Cell(500, 200, 600, 300, win)
    cell3.has_left_wall = False  
    cell3.draw("blue")

    move_line = cell1.draw_move(cell3)

    win.wait_for_close()

if __name__ == "__main__":
    main()
