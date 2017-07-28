import unittest
from image_editor import MatrixEditor


class TestMatrixEditor(unittest.TestCase):
    def setUp(self):
        pass

    @staticmethod
    def _verify_white_matrix(editor: MatrixEditor):
        """
        Verifies if all pixels of matrix is white ('0')
        Made so we DRY in the tests
        :param editor: the matrix editor to be verified
        :return:
        """
        for h in range(editor.height):
            for w in range(editor.width):
                if editor.matrix[h][w] != '0':
                    return False
        return True

    @staticmethod
    def _check_dot(matrix: [[]], matrix_height: int, matrix_width: int, dot_coordinate: tuple, color: str) -> bool:
        for h in range(matrix_height):
            for w in range(matrix_width):
                if w == dot_coordinate[0] and h == dot_coordinate[1]:
                    return matrix[h][w] == color

    def test_command_i(self):
        """
        Tests the I command - Initializing a matrix
        :return:
        """
        height = 0
        width = 0

        with self.assertRaises(ValueError) as exc:
            MatrixEditor(height=height, width=width)
        self.assertTrue('Width and Height must be positive integers' in str(exc.exception))

        height = 6
        width = 5

        editor = MatrixEditor(width=width, height=height)
        self.assertTrue(self._verify_white_matrix(editor))

    def test_command_c(self):
        """
        Tests the C command - Clear the matrix
        :return:
        """
        height = 3
        width = 3

        editor = MatrixEditor(width=width, height=height)
        self.assertTrue(self._verify_white_matrix(editor))

    def test_command_l(self):
        """
        Tests the L command - Writes a char within the matrix
        :return:
        """
        width = 5
        height = 8
        editor = MatrixEditor(width=width, height=height)

        dot_coordinate = (3, 2)
        editor.color_dot(coordinate=dot_coordinate, color='1')
        self._check_dot(matrix=editor.matrix, matrix_height=height, matrix_width=width,
                        dot_coordinate=dot_coordinate, color='1')

        with self.assertRaises(IndexError) as exc:
            editor.color_dot(coordinate=(dot_coordinate[0] + width, dot_coordinate[1]), color='F')
        self.assertTrue('Coordinate out of bounds' == str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.color_dot(coordinate=dot_coordinate, color='')
        self.assertTrue('Color param must be a single character' == str(exc.exception))

    def test_command_v(self):
        """
        Tests the V command - Draws a vertical line
        :return:
        """
        height = 10
        width = 5
        editor = MatrixEditor(width=width, height=height)

        a_dot = (1, 2)
        b_dot = (1, 7)
        color = 'V'
        editor.draw_line(direction='v', a_dot_coordinate=a_dot, b_dot_coordinate=b_dot, color=color)

        for y in range(a_dot[1], b_dot[1] + 1):
            self.assertTrue(self._check_dot(matrix=editor.matrix, matrix_height=height, matrix_width=width,
                                            dot_coordinate=(b_dot[0], y), color=color))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='f', a_dot_coordinate=a_dot, b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Direction must be' in str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='v', a_dot_coordinate=a_dot, b_dot_coordinate=(0, 1, 2), color=color)
        self.assertTrue('Coordinates must be a 2-sized tuple' == str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='v', a_dot_coordinate=(0, 1, 1), b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Coordinates must be a 2-sized tuple' == str(exc.exception))

        with self.assertRaises(IndexError) as exc:
            editor.draw_line(direction='v', a_dot_coordinate=(a_dot[0], a_dot[1] + height),
                             b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Coordinate out of bounds' in str(exc.exception))

        with self.assertRaises(IndexError) as exc:
            editor.draw_line(direction='v', a_dot_coordinate=a_dot,
                             b_dot_coordinate=(b_dot[0] + width, b_dot[1]), color=color)
        self.assertTrue('Coordinate out of bounds' in str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='v', a_dot_coordinate=a_dot,
                             b_dot_coordinate=b_dot, color='red')
        self.assertTrue('single character' in str(exc.exception))

    def test_command_h(self):
        """
        Tests the H command - Draws a horizontal line
        :return:
        """
        height = 13
        width = 6
        editor = MatrixEditor(width=width, height=height)

        a_dot = (3, 8)
        b_dot = (5, 8)
        color = 'H'
        editor.draw_line(direction='h', a_dot_coordinate=a_dot, b_dot_coordinate=b_dot, color=color)

        for x in range(a_dot[0], b_dot[0] + 1):
            self.assertTrue(self._check_dot(matrix=editor.matrix, matrix_height=height, matrix_width=width,
                                            dot_coordinate=(x, b_dot[1]), color=color))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='b', a_dot_coordinate=a_dot, b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Direction must be' in str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='h', a_dot_coordinate=(0, ), b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Coordinates must be a 2-sized tuple' == str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='h', a_dot_coordinate=a_dot, b_dot_coordinate=(1, 2, 0), color=color)
        self.assertTrue('Coordinates must be a 2-sized tuple' == str(exc.exception))

        with self.assertRaises(IndexError) as exc:
            editor.draw_line(direction='h', a_dot_coordinate=a_dot,
                             b_dot_coordinate=(b_dot[0], b_dot[1] + height), color=color)
        self.assertTrue('Coordinate out of bounds' in str(exc.exception))

        with self.assertRaises(IndexError) as exc:
            editor.draw_line(direction='h', a_dot_coordinate=(a_dot[0] + width, a_dot[1]),
                             b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Coordinate out of bounds' in str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='h', a_dot_coordinate=a_dot,
                             b_dot_coordinate=b_dot, color='')
        self.assertTrue('single character' in str(exc.exception))

    def test_command_k(self):
        """
        Tests the K command - Draws a rectangle
        :return:
        """
        height = 8
        width = 10
        editor = MatrixEditor(width=width, height=height)

        a_dot = (1, 1)
        b_dot = (7, 7)
        color = '.'
        editor.draw_rect(upper_left_corner_coordinate=a_dot, lower_right_corner_coordinate=b_dot, color=color)

        for x in range(width):
            for y in range(height):
                if x in (a_dot[0], b_dot[0]) and y in (a_dot[1], b_dot[1]):
                    self.assertTrue(self._check_dot(matrix=editor.matrix, matrix_height=height, matrix_width=width,
                                                    dot_coordinate=(x, y), color=color))

        with self.assertRaises(ValueError) as exc:
            editor.draw_line(direction='b', a_dot_coordinate=a_dot, b_dot_coordinate=b_dot, color=color)
        self.assertTrue('Direction must be' in str(exc.exception))

    def test_command_f(self):
        """
        Tests the F command - Paints a region
        :return:
        """
        height = 6
        width = 5
        editor = MatrixEditor(width=width, height=height)
        editor._matrix = [
            ['0', '0', '1', '0', '1'],
            ['1', '1', '1', '1', '1'],
            ['0', '1', '1', '1', '1'],
            ['1', '1', '1', '0', '1'],
            ['0', '0', '1', '0', '0'],
            ['1', '1', '1', '0', '1'],
        ]
        
        expected_matrix = [
            ['0', '0', '.', '0', '.'],
            ['.', '.', '.', '.', '.'],
            ['0', '.', '.', '.', '.'],
            ['.', '.', '.', '0', '.'],
            ['0', '0', '.', '0', '0'],
            ['.', '.', '.', '0', '1'],
        ] 

        a_dot = (2, 3)
        color = '.'
        editor.color_region(dot_within_coordinate=a_dot, color=color)

        self.assertEqual(editor.matrix, expected_matrix)

    def test_command_s(self):
        """
        Tests the S command - Saves the matrix content to a file
        :return
        """
        height = 13
        width = 20
        file_path = 's_command_result.txt'
        editor = MatrixEditor(width=width, height=height)

        editor.save_to_file(file_path=file_path)

        with open(file_path, 'r') as file:
            lines_amount = sum(1 for line in file)

        line_content = ''.join(['0' for _ in range(width)])

        with open(file_path, 'r') as file:
            cur_line_idx = 0
            for line in file:
                cur_line_idx += 1
                if cur_line_idx == lines_amount:
                    self.assertTrue(line == line_content)
                else:
                    self.assertTrue(line[:-1] == line_content)  # dont consider the \n char
        self.assertTrue(height == lines_amount)


if __name__ == '__main__':
    unittest.main()
