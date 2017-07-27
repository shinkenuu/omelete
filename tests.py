import unittest
from image_editor import MatrixEditor

"""
* Utilize TDD de preferência;
* Só importe uma biblioteca se você realmente precisar;
* Utilize um versionamento git ou mercurial com todos os seus commits para que fique um registro histórico do seu desenvolvimento;

Seu código será avaliado nos seguintes quesitos:
* Completude da solução
* Legibilidade
* Simplicidade
* Cobertura dos testes
* PEP8



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
        self.matrix_editor = None

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

        self.matrix_editor = MatrixEditor(width=width, height=height)

        for h in range(height):
            for w in range(width):
                self.assertTrue(self.matrix_editor.matrix[h][w] == 0)



if __name__ == '__main__':
    unittest.main()
