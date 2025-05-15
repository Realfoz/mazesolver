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

    def test_maze_zero_cells(self):
        with self.assertRaises(ValueError) as context:
            m1 = Maze(0, 0, 0, 0, 6, 10)
        self.assertEqual(str(context.exception), "Maze dimensions and cell sizes must be greater than zero")

        

if __name__ == "__main__":
    unittest.main()