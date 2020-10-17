import itertools
import random


class Tile:
    def __init__(self, color, background, shape):
        self.color = color
        self.background = background
        self.shape = shape
        self.code = str(self.color) + str(self.background) + str(self.shape)
        self.link = "Tiles/" + str(self.code) + ".png"


def generate_tiles():
    all_tiles = {}
    possible_colors, possible_backgrounds, possible_shapes = ["B", "R", "Y"], ["G", "K", "W"], ["C", "S", "T"]
    for bunch in itertools.product(possible_colors, possible_backgrounds, possible_shapes):
        string = "".join(bunch)
        all_tiles[string] = Tile(bunch[0], bunch[1], bunch[2])
    return all_tiles


def generate_board(all_tiles):
    board = random.sample(list(all_tiles.values()), 9)
    return board


def check_hap(trio):  # trio is list of three Tile objects
    trio_colors = [tile.color for tile in trio]
    trio_colors = list(dict.fromkeys(trio_colors))
    trio_backgrounds = [tile.background for tile in trio]
    trio_backgrounds = list(dict.fromkeys(trio_backgrounds))
    trio_shapes = [tile.shape for tile in trio]
    trio_shapes = list(dict.fromkeys(trio_shapes))
    if (len(trio_colors) in (1, 3)) and (len(trio_backgrounds) in (1, 3)) and (len(trio_shapes) in (1, 3)):
        return True
    else:
        return False


def solve_board(board):
    haps = []
    trios = itertools.combinations(board, 3)
    for possible_hap in trios:
        if check_hap(possible_hap):
            haps += [possible_hap]
    return haps


def solve_board_numbers(board):
    haps = []
    trios = itertools.combinations(board, 3)
    for possible_hap in trios:
        if check_hap(possible_hap):
            haps += ["".join([str(board.index(tile)+1) for tile in possible_hap])]
    return haps


def main():
    tiles = generate_tiles()

    board = generate_board(tiles)  # list of 9 Tile objects for the board
    board_text = [tile.code for tile in board]
    print(board_text)

    solution = solve_board(board)
    solution_text = [[tile.code for tile in hap] for hap in solution]
    print(solution_text)
    print(solve_board_numbers(board))


if __name__ == "__main__":
    main()
