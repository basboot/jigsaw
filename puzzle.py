from dataclasses import dataclass

# (0, 0) is top left, + is right/down


# origin (0, 0) of a layout must have no block above or left from it
# the origin does not have to be specified in the list of blocks
@dataclass
class Layout:
    blocks: list[tuple]

@dataclass
class Piece:
    layouts: list[Layout]

class Puzzle:
    def __init__(self, m, n, pieces):
        self.m = m
        self.n = n
        self.pieces = pieces

        # set with occupied blocks of the puzzle
        self.occupied = set()

        # pieces on the board
        # piece id => (layout id, position)
        self.solution = {}

    def is_occupied(self, point):
        return point in self.occupied


if __name__ == '__main__':
    pieces = [Piece([Layout([(0, 1)]), Layout([(0, 1), (1, 1)])])]
    p = Puzzle(3, 3, pieces)

    print(p.is_occupied((0, 0)))
