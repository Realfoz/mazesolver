import unittest
from main import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_rectangle_cells(self):
        num_cols = 15
        num_rows = 30
        m1 = Maze(0, 0, num_rows, num_cols, 6, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )


        ## to do, unit test for mazes with 0 dimensions for exception checking
        ## also add a few more quirky numbers 

if __name__ == "__main__":
    unittest.main()