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



## ---------------------------------------------- probably should be a new .py file but fuck it we ball

def main():
    win = Window(800, 600)
    point1 = Point(100,20)
    point2 = Point(300,78)
    line1 = Line(point1, point2)
    win.draw_line(line1, "black")
    win.wait_for_close()

if __name__ == "__main__":
    main()
