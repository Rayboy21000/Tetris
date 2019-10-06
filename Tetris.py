import random

christian = False

if christian:
    def user_input_array():
        x = []
        for i in range(15):
            x.append([-1*int(i) for i in input()])
        return x


class StraightTetronimo:
    def __init__(self):
        self.array = [
            [1],
            [1],
            [1],
            [1]
        ]


class SquareTetronimo:
    def __init__(self):
        self.array = [
            [2, 2],
            [2, 2]
        ]


class TTetronimo:
    def __init__(self):
        self.array = [
            [0, 3, 0],
            [3, 3, 3]
        ]


class LTetronimo:
    def __init__(self):
        self.array = [
            [0, 0, 4],
            [4, 4, 4]
        ]


class JTetronimo:
    def __init__(self):
        self.array = [
            [5, 0, 0],
            [5, 5, 5]
        ]


class STetronimo:
    def __init__(self):
        self.array = [
            [0, 6, 6],
            [6, 6, 0]
        ]


class ZTetronimo:
    def __init__(self):
        self.array = [
            [7, 7, 0],
            [0, 7, 7]
        ]


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


create_choices = [
    StraightTetronimo,
    SquareTetronimo,
    TTetronimo,
    LTetronimo,
    JTetronimo,
    STetronimo,
    ZTetronimo
]


def create_tetris_array(width, height):
    return [[0 for i in range(width)] for j in range(height)]


def create_shape(array, block_choices, designated_shape):
    game_running = True
    if designated_shape == 'SQ':
        shape_type = SquareTetronimo
    elif designated_shape == 'ST':
        shape_type = StraightTetronimo
    else:
        shape_type = random.choice(block_choices)
    shape = shape_type()

    array_row = array[0]
    shape_row = shape.array[0]
    array_width = len(array_row)
    shape_width = len(shape_row)
    shift_x = array_width//2 - shape_width//2

    for column_num in range(len(shape.array)):
        for row_num in range(len(shape.array[column_num])):
            if array[column_num][row_num + shift_x] != 0:
                game_running = False
            array[column_num][row_num + shift_x] = shape.array[column_num][row_num]
    return array, shape, game_running


def print_screen(array, score):
    print_borders = ''
    for x in range(len(array[0]) + 2):
        print_borders += '[ ]'
    print(print_borders)
    for row in array:
        print_row = '[ ]'
        for item in row:
            if item != 0:
                if item > 0:
                    print_row += ' ' + str(item) + ' '
                else:
                    print_row += ' ' + str(-1*item) + ' '

            else:
                print_row += '   '
        print_row += '[ ]'
        print(print_row)
    print(print_borders)
    print("Your score is: " + str(score))


def find_tetronimo_block_coordinates(array):
    blocks_found = 0
    block = list(range(4))
    for row in range(len(array)):
        for item in range(len(array[row])):
            if array[row][item] > 0:
                if blocks_found == 0:
                    tetronimo = array[row][item]
                    block[0] = Coordinate(item, row)
                    blocks_found += 1
                elif blocks_found == 1:
                    block[1] = Coordinate(item, row)
                    blocks_found += 1
                elif blocks_found == 2:
                    block[2] = Coordinate(item, row)
                    blocks_found += 1
                elif blocks_found == 3:
                    block[3] = Coordinate(item, row)
                    blocks_found += 1
    return block, tetronimo


def check_block_below(block, array, tetronimo, height):
    can_move_down = not (block[0].y + 1 == height or block[1].y + 1 == height or block[2].y + 1 == height or block[3].y + 1 == height)
    for i in range(4):
        can_move_down = can_move_down and not (array[block[i].y + 1][block[i].x] != 0 and array[block[i].y + 1][block[i].x] != tetronimo)
    return can_move_down


def check_block_right(block, array, tetronimo, width):
    can_move_right = not (block[0].x + 1 == width or block[1].x + 1 == width or block[2].x + 1 == width or block[3].x + 1 == width)
    for i in range(4):
        can_move_right = can_move_right and not (array[block[i].y][block[i].x + 1] != 0 and array[block[i].y][block[i].x + 1] != tetronimo)
    return can_move_right


def check_block_left(block, array, tetronimo):
    can_move_left = not (block[0].x == 0 or block[1].x == 0 or block[2].x == 0 or block[3].x == 0)
    for i in range(4):
        can_move_left = can_move_left and not (array[block[i].y][block[i].x - 1] != 0 and array[block[i].y][block[i].x - 1] != tetronimo)
    return can_move_left


def move_tetronimo_down(tetronimo, block, array, array_height):
    if check_block_below(block, array, tetronimo, array_height):
        for a in range(4):
            array[block[a].y][block[a].x] = 0
        for b in range(4):
            array[block[b].y + 1][block[b].x] = tetronimo
        for c in range(4):
            block[c].y += 1
        return array, True, block
    else:
        for a in range(4):
            array[block[a].y][block[a].x] = -1*tetronimo
        return array, False, block# This means that the tetronomino cannot move down


def move_tetronimo_right(tetronimo, block, array, array_width):
    if check_block_right(block, array, tetronimo, array_width):
        for a in range(4):
            array[block[a].y][block[a].x] = 0
        for b in range(4):
            array[block[b].y][block[b].x + 1] = tetronimo
        for c in range(4):
            block[c].x += 1
    return array, True, block


def move_tetronimo_left(tetronimo, block, array):
    if check_block_left(block, array, tetronimo):
        for a in range(4):
            array[block[a].y][block[a].x] = 0
        for b in range(4):
            array[block[b].y][block[b].x - 1] = tetronimo
        for c in range(4):
            block[c].x -= 1
    return array, True, block


def trade_full_rows_for_points(array, points):
    rows_to_delete = []
    for index, row in enumerate(array):
        if all(row):
            rows_to_delete.append(index)

    for row_index in rows_to_delete:
        del array[row_index]

    points += len(rows_to_delete)
    for i in range(len(rows_to_delete)):
        row = []
        for _ in range(len(array[-1])):
            row.append(0)
        array.insert(0, row)
    return array, points

TETRIS_ARRAY_HEIGHT = 15
TETRIS_ARRAY_WIDTH = 9

while True:
    score = 0
    player_control = input('Press enter to start').upper()
    game_running = True
    tetris_array = create_tetris_array(TETRIS_ARRAY_WIDTH, TETRIS_ARRAY_HEIGHT)
    tetris_array, tetronimo, game_running = create_shape(tetris_array, create_choices, player_control)
    block = [1, 2, 3, 4]
    block, tetronimo_number = find_tetronimo_block_coordinates(tetris_array)
    tetronimo_moving = True
    while game_running:
        print_screen(tetris_array, score)
        player_control = input().upper()
        if player_control == 'S':
            tetris_array, tetronimo_moving, block = move_tetronimo_down(tetronimo_number, block, tetris_array, TETRIS_ARRAY_HEIGHT)
        elif player_control == 'A':
            tetris_array, tetronimo_moving, block = move_tetronimo_left(tetronimo_number, block, tetris_array)
        elif player_control == 'D':
            tetris_array, tetronimo_moving, block = move_tetronimo_right(tetronimo_number, block, tetris_array, TETRIS_ARRAY_WIDTH)
        if not tetronimo_moving:
            tetris_array, score = trade_full_rows_for_points(tetris_array, score)
            tetris_array, tetronimo, game_running = create_shape(tetris_array, create_choices, player_control)
            block, tetronimo_number = find_tetronimo_block_coordinates(tetris_array)
            tetronimo_moving = True
    print('GAME OVER')
