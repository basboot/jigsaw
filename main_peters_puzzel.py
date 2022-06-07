# Solve Peters puzzel https://www.peterspuzzels.nl

from piece import *
from puzzle_animation import PuzzleAnimation
from puzzle import Puzzle
import time

if __name__ == '__main__':
    # Create the 10 pieces for the puzzle
    peters_puzzel_pieces = [
        # 0
        create_piece([(0, 0), (1, -1), (1, 0), (1, 1), (1, 2)], 'A'),
        # 1
        create_piece([(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)], 'B'),
        # 2
        create_piece([(0, 0), (1, 0), (1, -1), (2, -1)], 'C'),
        # 3
        create_piece([(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)], 'D'),
        # 4
        create_piece([(0, 0), (1, 0), (1, -1), (1, 1), (2, 0)], 'E'),
        # 5
        create_piece([(0, 0), (1, 0), (1, 1), (1, 2), (0, 2)], 'F'),
        # 6
        create_piece([(0, 0), (1, 0), (1, -1), (2, -1), (0, 1)], 'G'),
        # 7
        create_piece([(0, 0), (1, 0), (1, -1), (1, 1)], 'H'),
        # 8
        create_piece([(0, 0), (0, 1), (1, 1), (2, 1)], 'I'),
        # 9
        create_piece([(0, 0), (1, 0), (1, -1), (2, 0), (2, 1)], 'J')
    ]

    # Text for the tiles of the puzzle
    peters_puzzel_text = [
        ["ma", "di", "wo", "do", "1", "2", "3", "4", "5", "6"],
        ["vr", "za", "zo", "7", "8", "9", "10", "11", "12", "13"],
        ["14", "15", "16", "17", "18", "19", "20", "jan", "feb", "mrt"],
        ["21", "22", "23", "24", "25", "26", "apr", "mei", "jun", "jul"],
        ["27", "28", "29", "30", "31", "aug", "sep", "okt", "nov", "dec"]
    ]

    peters_puzzel = Puzzle(10, 5, peters_puzzel_pieces)

    # Create dictionary to find tiles
    peters_puzzel_lookup = {}
    for x in range(peters_puzzel.m):
        for y in range(peters_puzzel.n):
            peters_puzzel_lookup[peters_puzzel_text[y][x]] = (x, y)

    # Invalidate a weekday, day and month
    peters_puzzel.invalidate(peters_puzzel_lookup["di"])
    peters_puzzel.invalidate(peters_puzzel_lookup["7"])
    peters_puzzel.invalidate(peters_puzzel_lookup["jun"])

    # Solve the puzzle
    animation = PuzzleAnimation(peters_puzzel, peters_puzzel_text)
    start_time = time.time()
    peters_solutions = peters_puzzel.solve((0, 0), animation, False)
    running_time = time.time() - start_time

    # Show results
    for i in range(len(peters_solutions)):
        print(f"solution #{i}")
        print(peters_solutions[i])
        peters_puzzel.solution = peters_solutions[i]
        print(peters_puzzel)

    print(f"Found {len(peters_solutions)} solutions in {running_time} seconds")

    animation.finish()