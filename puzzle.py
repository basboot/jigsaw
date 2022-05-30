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

    def next_block(self, position):
        x = position[0]
        y = position[1]

        x += 1
        if x == self.m:
            y = y + 1
        if y == self.n:
            return None

        return (x, y)

    def layout_fits(self, layout, position):
        for block in layout.blocks:
            x = layout[0] + block[0]
            y = layout[1] + block[1]

            # check puzzle boundaries
            if x < 0 or x >= self.m:
                return False
            if y < 0 or y >= self.n:
                return False
            if self.is_occupied((x, y)):
                return False

        return True

    def add_piece(self, piece_id, layout_id, position):

        for block in pieces[piece_id].layouts[layout_id].blocks:
            x = position[0] + block[0]
            y = position[1] + block[1]

            # TODO: add asserts
            # add to occupied
            self.occupied.add((x, y))

        # pieces on the board
        # piece id => (layout id, position)
        self.solution[piece_id] = (layout_id, position)

    def remove_piece(self, piece_id, layout_id, position):

        for block in pieces[piece_id].layouts[layout_id].blocks:
            x = position[0] + block[0]
            y = position[1] + block[1]

            # TODO: add asserts
            # add to occupied
            self.occupied.remove((x, y))

        # pieces on the board
        # piece id => (layout id, position)
        del self.solution[piece_id]

# TODO: create copy, or cleanup intermediate solutions?
def solve(current_position, current_puzzle):
    if current_puzzle.is_occupied(current_position):
        # next pos
        pass
    else:
        # current pos
        # loop pieces * layouts
        # fit?
        # last piece => ready, else next position
        # all done? backtrack
        pass

if __name__ == '__main__':
    pieces = [Piece([Layout([(0, 1)]), Layout([(0, 1), (1, 1)])])]
    p = Puzzle(3, 3, pieces)

    print(p.is_occupied((0, 0)))
