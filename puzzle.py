from dataclasses import dataclass

# A puzzle is a square bord with m x n tiles, which can be empty or occupied
# A piece of the puzzle is a shape of blocks. Each block can occupy a tile
# Because a piece kan be rotated and flipped it has multiple layouts, which
# do not have to be unique because of symmetry. Which results in 1 to 8 unique
# layouts per piece.

# The target is to occupy all tiles of the board but some. By invalidating
# (occupy!) the q tiles that cannot be used, and using pieces with a total
# number of blocks of m x n - q the problem reduces to putting all pieces
# of the puzzle on the board without overlapping.

# If we choose the origin (0, 0) of a layout to have no blocks above or left
# from it, we can solve the puzzle by trying all pieces to fill the puzzle
# from top left, to bottom right

# (0, 0) is top left, + is right/down
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

    def is_occupied(self, tile):
        return tile in self.occupied

    def next_tile(self, tile):
        x = tile[0]
        y = tile[1]

        x += 1
        if x == self.m:
            y = y + 1
        if y == self.n:
            return None

        return (x, y)

    def layout_fits(self, layout, tile):
        # redundant
        if self.is_occupied((tile[0], tile[1])):
            return False

        for block in layout.blocks:
            x = tile[0] + block[0]
            y = tile[1] + block[1]

            # check puzzle boundaries
            if x < 0 or x >= self.m:
                return False
            if y < 0 or y >= self.n:
                return False
            if self.is_occupied((x, y)):
                return False

        return True

    def add_piece(self, piece_id, layout_id, tile_origin):

        # add origin
        self.occupied.add((tile_origin[0], tile_origin[1]))
        for block in pieces[piece_id].layouts[layout_id].blocks:
            x = tile_origin[0] + block[0]
            y = tile_origin[1] + block[1]

            # TODO: add asserts
            # add to occupied
            self.occupied.add((x, y))

        # pieces on the board
        # piece id => (layout id, position)
        self.solution[piece_id] = (layout_id, tile_origin)

    def remove_piece(self, piece_id, layout_id, tile_origin):

        # remove origin
        self.occupied.remove((tile_origin[0], tile_origin[1]))
        for block in pieces[piece_id].layouts[layout_id].blocks:
            x = tile_origin[0] + block[0]
            y = tile_origin[1] + block[1]

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
        for tile in self.occupied:
            grid[tile[1]][tile[0]] = 'X'

        # mark pieces used in solution
        for piece_id, layout_position in self.solution.items():
            grid[layout_position[1][1]][layout_position[1][0]] = self.pieces[piece_id].representation
            for tile in self.pieces[piece_id].layouts[layout_position[0]].blocks:
                grid[tile[1] + layout_position[1][1]][tile[0] + layout_position[1][0]] = \
                    self.pieces[piece_id].representation

        # create string from grid
        repres = ""
        for row in grid:
            for tile in row:
                repres = f"{repres}{tile}"
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
