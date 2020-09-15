import random
import time
import colorama
import curses

# TODO
# comments
# unit tests
# restucturing
# const instead of magic numbers
# exceptions
# user interaction
# terminal UI -> curses


def dead_board(width, height):
    """
    Returns a board of size height x width, all cells dead
    :return: 2d array representing a board
    """
    return [[0 for _ in range(width)] for _ in range(height)]


def random_state(aliveness):
    """
    Returns 0 (dead) or 1 (alive)
    :param aliveness: probability that the cell is alive
    """
    rng = random.random()
    if rng >= aliveness:
        return 0
    else:
        return 1


def random_board(width, height, aliveness=0.5):
    return [[random_state(aliveness) for _ in range(width)] for _ in range(height)]


def get_board_width(board):
    return len(board[0])


def get_board_height(board):
    return len(board)


def render(board):
    """
    Board rendering using colorama for colors in terminal
    """
    border = '#'
    alive = u"\u2588"
    dead = ' '

    width = get_board_width(board)

    for x in range(0, width + 2):
        print(border, end=" ")

    print()

    for line in board:
        print(border, end=" ")
        for elem in line:
            if elem == 1:
                char = alive
                print(f'{colorama.Fore.GREEN}{char}{colorama.Style.RESET_ALL}', end=" ")
            else:
                char = dead
                print(f'{char}', end=" ")
        print(border)

    for x in range(0, width + 2):
        print(border, end=" ")
    print()


def next_cell_state(x, y, board):
    """
    Calculates the next state of board[y][x] according to Conway's Game of Life rules
    :param x: place on x-axis (0 is leftmost)
    :param y: place on y-axis (0 is top)
    :return: 0 (dead), 1 (alive)
    """
    current = board[y][x]
    population = -current
    is_alive = board[y][x] == 1

    width = get_board_width(board)
    height = get_board_height(board)

    row_start = max(x - 1, 0)
    row_end = min(x + 1, width - 1)
    col_start = max(y - 1, 0)
    col_end = min(y + 1, height - 1)

    for x in range(col_start, col_end + 1):
        for y in range(row_start, row_end + 1):
            population += board[x][y]

    if is_alive:
        if population < 2 or population > 3:
            return 0
        else:
            return 1
    else:
        if population == 3:
            return 1
        else:
            return 0


def next_board_state(board):
    """
    Calculates board state in next step using next_cell_state function
    :return: Board after calculating new state for every cell
    """
    width = get_board_width(board)
    height = get_board_height(board)
    new = dead_board(width, height)
    for y in range(0, height):
        for x in range(0, width):
            new[y][x] = next_cell_state(x, y, board)

    return new


def loop(board):
    """
    Infinite rendering loop, may use 'q' for user-demand exit
    :param board:
    """
    new = board
    while 0 < 1:
        render(new)
        new = next_board_state(new)
        time.sleep(1)
        # x = input()
        # if(x == 'q'):
        #    return


def read_state_from_file(filepath):
    """
    Reads a board state from plaintext file
    :param filepath: string - relative path to a file
    :return: board saved in a file
    """
    with open(filepath) as reader:
        lines = reader.readlines()
        reader.close()
    width = len(lines[0]) - 1
    height = len(lines)
    return [[int(lines[x][y]) for y in range(width)] for x in range(height)]


# randomb = random_board(5,5)
# render(randomb)
# render(next_board_state(randomb))

#loop(read_state_from_file('Conway/toad.txt'))  # runs board from file toad.txt

# loop(random_board(5,5))
loop([
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 1, 1, 1, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
 ])
#
# repeater = dead_board(15, 15)
# repeater[7][7] = repeater[6][7] = repeater[7][6] = repeater[7][8] = 1
# loop(repeater)
