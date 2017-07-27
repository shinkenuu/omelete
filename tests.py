import unittest
from image_editor import MatrixEditor

"""
Testes
------

Entrada 01:

I 5 6
L 2 3 A
S one.bmp
G 2 3 J
V 2 3 4 W
H 3 4 2 Z
F 3 3 J
S two.bmp
X

Saida 01:

one.bmp
OOOOO
OOOOO
OAOOO
OOOOO
OOOOO
OOOOO

two.bmp
JJJJJ
JJZZJ
JWJJJ
JWJJJ
JJJJJ
JJJJJ

Entrada 02:

I 10 9
L 5 3 A
G 2 3 J
V 2 3 4 W
H 1 10 5 Z
F 3 3 J
K 2 7 8 8 E
F 9 9 R
S one.bmp
X

Saida 02:

one.bmp
JJJJJJJJJJ
JJJJJJJJJJ
JWJJAJJJJJ
JWJJJJJJJJ
ZZZZZZZZZZ
RRRRRRRRRR
REEEEEEERR
REEEEEEERR
RRRRRRRRRR
"""


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
        def check_dot():
            for h in range(height):
                for w in range(width):
                    if w == dot_x and h == dot_y:
                        self.assertTrue(editor.matrix[h][w] == '1')
                    else:
                        self.assertTrue(editor.matrix[h][w] == '0')

        width = 5
        height = 8
        editor = MatrixEditor(width=width, height=height)

        dot_x = 3
        dot_y = 2
        editor.color_point(x=dot_x, y=dot_y, color='1')
        check_dot()

        with self.assertRaises(IndexError) as exc:
            editor.color_point(x=dot_x, y=dot_y + height, color='F')
        self.assertTrue('Coordinate out of bounds' == str(exc.exception))

        with self.assertRaises(ValueError) as exc:
            editor.color_point(x=dot_x, y=dot_y, color='')
        self.assertTrue('Color param must be a single character' == str(exc.exception))

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
