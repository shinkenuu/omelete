#!/usr/bin/python
# -*- coding: utf8 -*-

class MatrixEditor(object):
    """
    Creates, edits and saves a simple ASCII matrix
    """
    def __init__(self, width: int, height: int):
        """
        Initializes a matrix with width and height, filling it with 0s
        :param width: positive integer for matrix width
        :param height: positive integer for matrix height
        """
        if width > 0 and height > 0:
            self.height = height
            self.width = width
        else:
            raise ValueError(
                'Width and Height must be positive integers. Received height: {} width: {}'.format(height, width))

        self.matrix = [[0 for m in range(width)] for n in range(height)]

def main():
    pass

if __name__ == '__main__':
    main()
