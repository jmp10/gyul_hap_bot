from GHPuzzles import *
from PIL import Image


def build_image(board, save_q):  # save_q = True will save to computer, save_q = False won't
    grid_bckgd = Image.open("background with 12 table.png")
    grid_labels = Image.open("number labels.png")
    grid_bckgd_copy = grid_bckgd.copy()
    i = 0
    for top in [95, 345, 595]:
        for left in [97, 347, 597]:
            grid_bckgd_copy.paste(Image.open(board[i].link), (left, top))
            i += 1
    grid_bckgd_copy.paste(grid_labels, (70, 70), grid_labels)
    if save_q:
        grid_bckgd_copy.save("test.png", "PNG")
    return grid_bckgd_copy


def main():
    tiles = generate_tiles()

    board = generate_board(tiles)  # list of 9 Tile objects for the board
    board_text = [tile.code for tile in board]
    print(board_text)

    solution = solve_board(board)
    solution_text = [[tile.code for tile in hap] for hap in solution]
    print(solution_text)

    build_image(board, True)


if __name__ == "__main__":
    main()
