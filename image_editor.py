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

        self._matrix = [['0' for _ in range(width)] for _ in range(height)]

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
                self.matrix[col][row] = '0'

    def color_dot(self, coordinate: tuple, color: str):
        """
        Colors a pixel at the coordinate (x, y) with color
        L command
        :param coordinate: the coordinate of the dot
        :param color: the color to paint the color with
        :return:
        """
        self._verify_coordinate(coordinate=coordinate)
        self._verify_color(color=color)
        self._matrix[coordinate[1]][coordinate[0]] = color

    def draw_line(self, direction: str, a_dot_coordinate: tuple, b_dot_coordinate: tuple, color: str):
        """
        Draws a line in the :param direction: connecting :param a_dot: to :param b_dot with :param color
        V & H commands
        :param direction: ['v'|'h']]
        :param a_dot_coordinate: (Xa, Ya)
        :param b_dot_coordinate: (Xb, Yb)
        :param color: the character to draw the line with
        :return:
        """
        def draw_horizontal():
            if a_dot_coordinate[1] != b_dot_coordinate[1]:
                raise ValueError('The Y axis of both coordinates must be the same for a horizontal line')

            if a_dot_coordinate[0] > b_dot_coordinate[0]:
                right_most_dot = a_dot_coordinate
                left_most_dot = b_dot_coordinate
            else:
                right_most_dot = b_dot_coordinate
                left_most_dot = a_dot_coordinate

            for x in range(left_most_dot[0], right_most_dot[0] + 1):
                self.color_dot((x, a_dot_coordinate[1]), color=color)

        def draw_vertical():
            if a_dot_coordinate[0] != b_dot_coordinate[0]:
                raise ValueError('The X axis of both coordinates must be the same for a vertical line')

            if a_dot_coordinate[1] > b_dot_coordinate[1]:
                higher_dot = a_dot_coordinate
                lesser_dot = b_dot_coordinate
            else:
                higher_dot = b_dot_coordinate
                lesser_dot = a_dot_coordinate

            for y in range(lesser_dot[1], higher_dot[1] + 1):
                self.color_dot((a_dot_coordinate[0], y), color=color)

        if direction not in ('v', 'h'):
            raise ValueError('Direction must be either "v" (vertical) or "h" (horizontal)')

        self._verify_coordinate(a_dot_coordinate)
        self._verify_coordinate(b_dot_coordinate)
        self._verify_color(color=color)

        if direction == 'v':
            draw_vertical()
        else:
            draw_horizontal()

    def draw_rect(self, upper_left_corner_coordinate: tuple, lower_right_corner_coordinate: tuple, color: str):
        """
        Draws a rectangle, with the upper-left corner to the lower-right corner of the matrix with color
        K command
        :param upper_left_corner_coordinate: upper-left corner coordinate of the rectangle
        :param lower_right_corner_coordinate: lower-right corner coordinate of the rectangle
        :param color: the character to draw the rectangle with
        :return:
        """
        upper_right_corner_coordinate = (lower_right_corner_coordinate[0], upper_left_corner_coordinate[1])
        lower_left_corner_coordinate = (upper_left_corner_coordinate[0], lower_right_corner_coordinate[1])

        self._verify_coordinate(upper_left_corner_coordinate)
        self._verify_coordinate(lower_right_corner_coordinate)
        self._verify_coordinate(upper_right_corner_coordinate)
        self._verify_coordinate(lower_left_corner_coordinate)

        # upper row
        self.draw_line(direction='h',
                       a_dot_coordinate=upper_left_corner_coordinate,
                       b_dot_coordinate=upper_right_corner_coordinate,
                       color=color)
        # right column
        self.draw_line(direction='v',
                       a_dot_coordinate=upper_right_corner_coordinate,
                       b_dot_coordinate=lower_right_corner_coordinate,
                       color=color)
        # bottom row
        self.draw_line(direction='h',
                       a_dot_coordinate=lower_right_corner_coordinate,
                       b_dot_coordinate=lower_left_corner_coordinate,
                       color=color)
        # left column
        self.draw_line(direction='v',
                       a_dot_coordinate=lower_left_corner_coordinate,
                       b_dot_coordinate=upper_left_corner_coordinate,
                       color=color)

    def color_region(self, dot_within_coordinate: tuple, color: str):
        """
        Colors a region around the dot with color
        F command
        :param dot_within_coordinate: Coordinate to the dot with the region
        :param color: the color to paint with
        :return:
        """
        def spread_ink(pixel_coordinate: tuple):
            for x in range(pixel_coordinate[0] - 1, pixel_coordinate[0] + 2):
                for y in range(pixel_coordinate[1] - 1, pixel_coordinate[1] + 2):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        if self.matrix[y][x] == previous_color:
                            self.matrix[y][x] = color
                            pixels_to_visit.append((x, y))

        self._verify_coordinate(dot_within_coordinate)
        self._verify_color(color)

        pixels_to_visit = [dot_within_coordinate]
        previous_color = self.matrix[dot_within_coordinate[1]][dot_within_coordinate[0]]

        while len(pixels_to_visit) > 0:
            spread_ink(pixels_to_visit.pop(0))

    def save_to_file(self, file_path: str):
        """
        Saves the matrix in a file
        :param file_path: the file path to save the matrix in
        :return:
        """
        try:
            with open(file_path, 'w'):
                pass
        except OSError as err:
            print('Couldnt write file at {}. OSError: {}'.format(file_path, str(err)))

        content = []
        for line_idx in range(self.height):
            content.append(''.join(self.matrix[line_idx]))
        content = '\n'.join(content)

        with open(file_path, 'w') as file:
            file.write(content)

    def _verify_coordinate(self, coordinate: tuple):
        """
        Verifies the coordinate. Raises any necessary Exception
        :param coordinate: the coordinate to be verified
        :return:
        """
        def is_valid_coordinate(x: int, y: int) -> bool:
            """
            Checks if the coordinate is valid within the current matrix
            :param x: the X coordinate of the point
            :param y: the Y coordinate of the point
            :return: True if valid, False otherwise
            """
            return self.width >= x and self.height >= y

        if len(coordinate) != 2:
            raise ValueError('Coordinates must be a 2-sized tuple')
        if not is_valid_coordinate(*coordinate):
            raise IndexError('Coordinate out of bounds')

    @staticmethod
    def _verify_color(color: str):
        if not len(color) == 1:
            raise ValueError('Color param must be a single character')


def command_decoder(editor: MatrixEditor, command: tuple, *args):
    """
    Decodes command and execute it
    :param editor:
    :param command:
    :param args: the arguments of the command
    :return: None if command wasnt executed OK
    """
    def i_handler(m, n):
        return MatrixEditor(width=int(m), height=int(n))

    def s_handler(name):
        editor.save_to_file(file_path=name)

    def c_handler():
        editor.clear_matrix()

    def l_handler(x, y, c):
        editor.color_dot(coordinate=(int(x) - 1, int(y) - 1), color=c)

    def v_handler(x, y1, y2, c):
        editor.draw_line(direction='v',
                         a_dot_coordinate=(int(x) - 1, int(y1) - 1),
                         b_dot_coordinate=(int(x) - 1, int(y2) - 1),
                         color=c)

    def h_handler(x1, x2, y, c):
        editor.draw_line(direction='h',
                         a_dot_coordinate=(int(x1) - 1, int(y) - 1),
                         b_dot_coordinate=(int(x2) -1, int(y) - 1), color=c)

    def k_handler(x1, y1, x2, y2, c):
        editor.draw_rect(upper_left_corner_coordinate=(int(x1) - 1, int(y1) - 1),
                         lower_right_corner_coordinate=(int(x2) - 1, int(y2) - 1),
                         color=c)

    def f_handler(x, y, c):
        editor.color_region(dot_within_coordinate=(int(x) - 1, int(y) - 1), color=c)

    try:
        if str(command[0]).upper() == 'I':
            return i_handler(*args)
        elif str(command[0]).upper() == 'C':
            c_handler()
            return True
        elif str(command[0]).upper() == 'L':
            l_handler(*args)
            return True
        elif str(command[0]).upper() == 'V':
            v_handler(*args)
            return True
        elif str(command[0]).upper() == 'H':
            h_handler(*args)
            return True
        elif str(command[0]).upper() == 'K':
            k_handler(*args)
            return True
        elif str(command[0]).upper() == 'F':
            f_handler(*args)
            return True
        elif str(command[0]).upper() == 'S':
            s_handler(*args)
            return True
        elif str(command[0]).upper() == 'X':
            return True
        else:
            return None
    except Exception as err:
        return str(err)


def main():
    """
    Main function to read and handle commands via stdin
    :return:
    """
    editor = object()
    command = ''
    while command != 'X':
        command = str(input('Insert command: '))
        split_command = command.split(' ')
        command_result = command_decoder(editor, *split_command)
        if command_result is None:
            print('Unrecognized command')
        elif type(command_result) is str:
            print(command_result)
        elif split_command[0].upper() == 'I':
            editor = command_result


if __name__ == '__main__':
    main()
