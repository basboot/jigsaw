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
    representation: str

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
        # redundant
        if self.is_occupied((position[0], position[1])):
            return False

        for block in layout.blocks:
            x = position[0] + block[0]
            y = position[1] + block[1]

            # check puzzle boundaries
            if x < 0 or x >= self.m:
                return False
            if y < 0 or y >= self.n:
                return False
            if self.is_occupied((x, y)):
                return False

        return True

    def add_piece(self, piece_id, layout_id, position):

        # add origin
        self.occupied.add((position[0], position[1]))
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

        # remove origin
        self.occupied.remove((position[0], position[1]))
        for block in pieces[piece_id].layouts[layout_id].blocks:
            x = position[0] + block[0]
            y = position[1] + block[1]

            # TODO: add asserts
            # add to occupied
            self.occupied.remove((x, y))

        # pieces on the board
        # piece id => (layout id, position)
        del self.solution[piece_id]

    def __str__(self):
        # init empty grid
        grid = [ ['.'] * self.m for i in range(self.n)]

        # set occupied blocks
        for cell in self.occupied:
            grid[cell[1]][cell[0]] = 'X'

        # mark pieces used in solution
        for piece_id, layout_position in self.solution.items():
            grid[layout_position[1][1]][layout_position[1][0]] = self.pieces[piece_id].representation
            for cell in self.pieces[piece_id].layouts[layout_position[0]].blocks:
                grid[cell[1] + layout_position[1][1]][cell[0] + layout_position[1][0]] = \
                    self.pieces[piece_id].representation

        # create string from grid
        repres = ""
        for row in grid:
            for cell in row:
                repres = f"{repres}{cell}"
            repres = f"{repres}\n"
        return repres

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
    pieces = [Piece([Layout([])], 'A'), Piece([Layout([(0, 1)]), Layout([(0, 1), (1, 1)])], 'B')]
    p = Puzzle(3, 3, pieces)

    p.add_piece(0, 0, (2, 1))
    print(p.layout_fits(p.pieces[1].layouts[1], (1, 1)))
    p.add_piece(1, 1, (1, 1))
    print(p.is_occupied((0, 0)))

    print(p)
