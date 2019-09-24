import random


points = 0
tetronimo_number = 0
tetris_array_height = 15
tetris_array_width = 9
current_shape = ''  # 8
tetris_array = []
tetronimo_moving = False
tetronimo = ''
player_control = ''
game_running = False
block1 = [0, 0]
block2 = [0, 0]
block3 = [0, 0]
block4 = [0, 0]




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


def create_tetris_array(array, height, width):
    array = []
    for x in range(height):  # the top 4 spaces will not be shown
        array.append([])
        for y in range(width):
            array[x].append(0)
    return array


def create_shape(array, block_choices):
    game_running = True
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


def print_screen(array):
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


def find_tetronimo_block_coordinates(array):
    blocks_found = 0
    for row in range(len(array)):
        for item in range(len(array[row])):
            if array[row][item] != 0:
                if blocks_found == 0:
                    tetronimo = array[row][item]
                    block1 = Coordinate(item, row)
                    blocks_found += 1
                elif blocks_found == 1:
                    block2 = Coordinate(item, row)
                    blocks_found += 1
                elif blocks_found == 2:
                    block3 = Coordinate(item, row)
                    blocks_found += 1
                elif blocks_found == 3:
                    block4 = Coordinate(item, row)
                    blocks_found += 1
    return block1, block2, block3, block4, tetronimo


def check_block_right_single(block, array, tetronimo, all_true):
    if all_true:
        if array[block.y][block.x + 1] != 0 and array[block.y][block.x + 1] != tetronimo:
            return False
        else:
            return True
    else:
        return False


def check_block_left_single(block, array, tetronimo, all_true):
    if all_true:
        if array[block.y][block.x - 1] != 0 and array[block.y][block.x - 1] != tetronimo:
            return False
        else:
            return True
    else:
        return False


def check_block_below_single(block, array, tetronimo, all_true):
    if all_true:
        if array[block.y + 1][block.x] != 0 and array[block.y + 1][block.x] != tetronimo:
            return False
        else:
            return True
    else:
        return False



def check_block_below(block1, block2, block3, block4, array, tetronimo, height):
    all_true = True
    if block1.y + 1 == height or block2.y + 1 == height or block3.y + 1 == height or block4.y + 1 == height:
        all_true = False
    all_true = check_block_below_single(block1, array, tetronimo, all_true)
    all_true = check_block_below_single(block2, array, tetronimo, all_true)
    all_true = check_block_below_single(block3, array, tetronimo, all_true)
    all_true = check_block_below_single(block4, array, tetronimo, all_true)
    if all_true:
        return True
    else:
        return False


def check_block_right(block1, block2, block3, block4, array, tetronimo, width):
    can_move_right = True
    if block1.x + 1 == width or block2.x + 1 == width or block3.x + 1 == width or block4.x + 1 == width:
        can_move_right = False
    can_move_right = check_block_right_single(block1, array, tetronimo, can_move_right)
    can_move_right = check_block_right_single(block2, array, tetronimo, can_move_right)
    can_move_right = check_block_right_single(block3, array, tetronimo, can_move_right)
    can_move_right = check_block_right_single(block4, array, tetronimo, can_move_right)
    return can_move_right


def check_block_left(block1, block2, block3, block4, array, tetronimo):
    can_move_left = True
    if block1.x == 0 or block2.x == 0 or block3.x == 0 or block4.x == 0:
        can_move_left = False
    can_move_left = check_block_left_single(block1, array, tetronimo, can_move_left)
    can_move_left = check_block_left_single(block2, array, tetronimo, can_move_left)
    can_move_left = check_block_left_single(block3, array, tetronimo, can_move_left)
    can_move_left = check_block_left_single(block4, array, tetronimo, can_move_left)
    if can_move_left:
        return True
    else:
        return False


def move_tetronimo_down(tetronimo, block1, block2, block3, block4, array, array_height, array_width):
    new_array = []
    for height in range(array_height):
        new_array.append([])
        for width in range(array_width):
            new_array[height].append(array[height][width])
    if check_block_below(block1, block2, block3, block4, array, tetronimo, array_height):
        new_array[block1.y][block1.x] = 0
        new_array[block2.y][block2.x] = 0
        new_array[block3.y][block3.x] = 0
        new_array[block4.y][block4.x] = 0
        new_array[block1.y + 1][block1.x] = tetronimo
        new_array[block2.y + 1][block2.x] = tetronimo
        new_array[block3.y + 1][block3.x] = tetronimo
        new_array[block4.y + 1][block4.x] = tetronimo
        block1.y += 1
        block2.y += 1
        block3.y += 1
        block4.y += 1
        return new_array, True, block1, block2, block3, block4
    else:
        new_array[block1.y][block1.x] = -1*tetronimo
        new_array[block2.y][block2.x] = -1*tetronimo
        new_array[block3.y][block3.x] = -1*tetronimo
        new_array[block4.y][block4.x] = -1*tetronimo
        return new_array, False, block1, block2, block3, block4# This means that the tetronomino cannot move down


def move_tetronimo_right(tetronimo, block1, block2, block3, block4, array, array_height, array_width):
    new_array = []
    for height in range(array_height):
        new_array.append([])
        for width in range(array_width):
            new_array[height].append(array[height][width])
    if check_block_right(block1, block2, block3, block4, array, tetronimo, array_width):
        new_array[block1.y][block1.x] = 0
        new_array[block2.y][block2.x] = 0
        new_array[block3.y][block3.x] = 0
        new_array[block4.y][block4.x] = 0
        new_array[block1.y][block1.x + 1] = tetronimo
        new_array[block2.y][block2.x + 1] = tetronimo
        new_array[block3.y][block3.x + 1] = tetronimo
        new_array[block4.y][block4.x + 1] = tetronimo
        block1.x += 1
        block2.x += 1
        block3.x += 1
        block4.x += 1
    return new_array, True, block1, block2, block3, block4


def move_tetronimo_left(tetronimo, block1, block2, block3, block4, array, array_height, array_width):
    new_array = []
    for height in range(array_height):
        new_array.append([])
        for width in range(array_width):
            new_array[height].append(array[height][width])
    if check_block_left(block1, block2, block3, block4, array, tetronimo):
        new_array[block1.y][block1.x] = 0
        new_array[block2.y][block2.x] = 0
        new_array[block3.y][block3.x] = 0
        new_array[block4.y][block4.x] = 0
        new_array[block1.y][block1.x - 1] = tetronimo
        new_array[block2.y][block2.x - 1] = tetronimo
        new_array[block3.y][block3.x - 1] = tetronimo
        new_array[block4.y][block4.x - 1] = tetronimo
        block1.x -= 1
        block2.x -= 1
        block3.x -= 1
        block4.x -= 1
    return new_array, True, block1, block2, block3, block4


def score_points(array, points):
    all_filled = true


while 1:
    input('Press enter to start')
    game_running = True
    tetris_array = create_tetris_array(tetris_array, tetris_array_height, tetris_array_width)
    tetris_array, tetronimo, game_running = create_shape(tetris_array, create_choices)
    block1, block2, block3, block4, tetronimo_number = find_tetronimo_block_coordinates(tetris_array)
    tetronimo_moving = True
    while game_running:
        print_screen(tetris_array)
        player_control = input().upper()
        if player_control == 'S':
            tetris_array, tetronimo_moving, block1, block2, block3, block4 = move_tetronimo_down(tetronimo_number, block1, block2, block3, block4, tetris_array, tetris_array_height, tetris_array_width)
        elif player_control == 'A':
            tetris_array, tetronimo_moving, block1, block2, block3, block4 = move_tetronimo_left(tetronimo_number, block1, block2, block3, block4, tetris_array, tetris_array_height, tetris_array_width)
        elif player_control == 'D':
            tetris_array, tetronimo_moving, block1, block2, block3, block4 = move_tetronimo_right(tetronimo_number, block1, block2, block3, block4, tetris_array, tetris_array_height, tetris_array_width)
        if not tetronimo_moving:
            tetris_array, tetronimo, game_running = create_shape(tetris_array, create_choices)
            block1, block2, block3, block4, tetronimo_number = find_tetronimo_block_coordinates(tetris_array)
            tetronimo_moving = True
    print('GAME OVER')

