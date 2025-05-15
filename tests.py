import unittest
from main import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_maze_rectangle_cells(self):
        num_cols = 15
        num_rows = 30
        m1 = Maze(0, 0, num_rows, num_cols, 10, 6)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_maze_zero_cells(self):
        with self.assertRaises(ValueError) as context:
            m1 = Maze(0, 0, 0, 0, 6, 10)
        self.assertEqual(str(context.exception), "Maze dimensions and cell sizes must be greater than zero")


    def test_reset_cells_visited(self):
        # Setup
        maze = Maze(10, 10, 10, 10, 10, 10, None)  # None for window to avoid drawing
        
        # Set some cells to visited
        middle_row = maze.num_rows // 2
        middle_col = maze.num_cols // 2
        maze._cells[middle_row][middle_col].visited = True
        maze._cells[0][0].visited = True
        maze._cells[maze.num_rows-1][maze.num_cols-1].visited = True
        
        # Call the method
        maze._reset_cells_visited()
        
        # Assert
        self.assertFalse(maze._cells[middle_row][middle_col].visited)
        self.assertFalse(maze._cells[0][0].visited)
        self.assertFalse(maze._cells[maze.num_rows-1][maze.num_cols-1].visited)


        

if __name__ == "__main__":
    unittest.main()