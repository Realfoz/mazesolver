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
            colour = "#D3D3D3"

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
        for i in range(self.num_rows):
            row = []
            for j in range(self.num_cols):
                cell = Cell(
                self.x1 + (j * self.cell_size_x),  # column
                self.y1 + (i * self.cell_size_y),  # row
                self.x1 + ((j+1) * self.cell_size_x),
                self.y1 + ((i+1) * self.cell_size_y),
                self.win)
                row.append(cell)     
            self._cells.append(row)

        for i in range(self.num_rows):
            for j in range(self.num_cols):
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


        end_cell = self._cells[self.num_rows - 1][self.num_cols - 1]
        if end_cell:
            end_cell.has_bottom_wall = False
            self._draw_cell(self.num_rows - 1,self.num_cols - 1)
    
    def _break_walls_r(self,i,j):
        self._cells[i][j].visited = True

        while True:
            possible = []
            # Check the four adjacent cells
            adjacent_cells = [
                (i-1, j),  # up
                (i+1, j),  # down
                (i, j-1),  # left
                (i, j+1)   # right
            ]

            for next_i, next_j in adjacent_cells:
                if self._is_valid_unvisited(next_i, next_j):
                    possible.append((next_i, next_j))
            if len(possible) == 0:
                self._draw_cell(i,j)
                return
            next_i, next_j = random.choice(possible)
            self._break_wall_between(i,j,next_i,next_j)
            self._break_walls_r(next_i,next_j)    
        
            

    def _is_valid_unvisited(self, i, j):
        # Check if within bounds
        if i < 0 or i >= self.num_rows or j < 0 or j >= self.num_cols:
            return False
         
        # Check if not visited
        return not self._cells[i][j].visited
    
    def _break_wall_between(self, i, j, next_i, next_j):
        if next_i == i - 1:  # Moving up
            if not self._is_top_edge(i, j):
                self._cells[i][j].has_top_wall = False
            if not self._is_bottom_edge(next_i, next_j):
                self._cells[next_i][next_j].has_bottom_wall = False
        # Moving down
        elif next_i == i + 1:
            if not self._is_bottom_edge(i, j):
                self._cells[i][j].has_bottom_wall = False
            if not self._is_top_edge(next_i, next_j):
                self._cells[next_i][next_j].has_top_wall = False
        # Moving left
        elif next_j == j - 1:
            if not self._is_left_edge(i, j):
                self._cells[i][j].has_left_wall = False
            if not self._is_right_edge(next_i, next_j):
                self._cells[next_i][next_j].has_right_wall = False
        # Moving right
        elif next_j == j + 1:
            if not self._is_right_edge(i, j):
                self._cells[i][j].has_right_wall = False
            if not self._is_left_edge(next_i, next_j):
                self._cells[next_i][next_j].has_left_wall = False
        

    def _is_top_edge(self, i, j):
        return i == 0
    def _is_bottom_edge(self, i, j):
        return i == self.num_rows - 1
    def _is_left_edge(self, i, j):
        return j == 0
    def _is_right_edge(self, i, j):
        return j == self.num_cols - 1
    
    def _reset_cells_visited(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self._cells[i][j].visited = False

    def solve(self):
        result = self._solve_r(0,0)
        return result
    
    def _solve_r(self,i,j):
        self._animate()
        current = self._cells[i][j]
        current.visited = True
        if current == self._cells[self.num_rows - 1][self.num_cols - 1]:
            return True
        
        # Directions as coordinate changes: (row_change, col_change)
        directions = [(-1, 0),  # Up
                    (0, 1),   # Right
                    (1, 0),   # Down
                    (0, -1)]  # Left

        for di, dj in directions:
            new_i, new_j = i + di, j + dj
            
            if self._is_valid_unvisited(new_i,new_j):
                if not self._is_wall_between(i,j, new_i, new_j):
                    current_cell = self._cells[i][j]
                    next_cell = self._cells[new_i][new_j]
                    current_cell.draw_move(next_cell)
                    if self._solve_r(new_i,new_j):
                        return True
                    current_cell.draw_move(next_cell, True)
        return False



    def _is_wall_between(self, i1, j1, i2, j2):
        # Check which direction we're moving and return if there's a wall
        
        # Moving North
        if i2 == i1 - 1 and j2 == j1:
            return self._cells[i1][j1].has_top_wall
        
        # Moving South
        elif i2 == i1 + 1 and j2 == j1:
            return self._cells[i1][j1].has_bottom_wall
        
        # Moving West
        elif i2 == i1 and j2 == j1 - 1:
            return self._cells[i1][j1].has_left_wall
        
        # Moving East
        elif i2 == i1 and j2 == j1 + 1:
            return self._cells[i1][j1].has_right_wall
        
        # Not adjacent cells
        else:
            return True  # Consider it a wall if not adjacent



    
## ---------------------------------------------- probably should be a new .py file but fuck it we ball

def main():
    win = Window(800, 600)
    time.sleep(10.00)
    maze = Maze(10,10,19,26,30,30,win) # 10,10,19,26,30,30,win
    maze._break_entrance_and_exit()
    maze._break_walls_r(0,0)
    maze._reset_cells_visited()
    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()
