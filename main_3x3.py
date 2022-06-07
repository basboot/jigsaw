# Solve simple 3x3 puzzle

from piece import *
from puzzle import Puzzle

if __name__ == '__main__':
    # 3 x 3 puzzle
    puzzle_pieces = [
        create_piece([(0, 0)], 'A'),
        create_piece([(0, 0), (1, 0), (1, 1)], 'B'),
        create_piece([(0, 0), (0, 1), (0, 2), (-1, 2)], 'C')
    ]

    p = Puzzle(3, 3, puzzle_pieces)

    p.invalidate((0, 0))

    s = p.solve((0, 0))
    print(s)
    for i in range(len(s)):
        print(f"Solution #{i}")
        p.solution = s[i]
        print(p)
