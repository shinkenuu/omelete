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
            self._height = height
            self._width = width
        else:
            raise ValueError(
                'Width and Height must be positive integers. Received height: {} width: {}'.format(height, width))

        self._matrix = [['0' for _ in range(height)] for _ in range(width)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def matrix(self):
        return self._matrix

    def clear_matrix(self):
        """
        Clears the matrix filling it with 0s
        C command
        :return:
        """
        for row in range(self.width):
            for col in range(self.height):
                self.matrix[row][col] = '0'

    def color_point(self, x: int, y: int, color: str):
        """
        Colors a pixel at the coordinate (x, y) with color
        L command
        :param x: the X coordinate of the point
        :param y: the Y coordinate of the point
        :param color: the color to paint the color with
        :return:
        """
        if not self.is_valid_coordinate(x, y):
            raise ValueError('Invalid coordinate')
        if not len(color) == 1:
            raise ValueError('color param must be a single character')
        self._matrix[x][y] = color

    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """
        Checks if the coordinate is valid within the current matrix
        :param x: the X coordinate of the point
        :param y: the Y coordinate of the point
        :return: True if valid, False otherwise
        """
        return self.width >= x and self.height >= y


def main():
    pass


if __name__ == '__main__':
    main()
