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

    def is_solved(self):
        return len(self.pieces) == len(self.solution)

    def next_tile(self, tile):
        x = tile[0]
        y = tile[1]

        x += 1
        if x == self.m:
            y = y + 1
            x = 0
        # not protected against wrong values, because the solver should handle it

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

    # invalidate illegal tiles
    def invalidate(self, tile):
        self.occupied.add(tile)

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
# TODO: rename to tile
def solve(current_position, puzzle, last_piece_id):
    if puzzle.is_solved():
        print("solved1")
        return puzzle.solution
    print(f"solve {current_position}")

    if puzzle.is_occupied(current_position):
        # this tile is already occupied, so we can move to the next
        solve(puzzle.next_tile(current_position), puzzle, last_piece_id)
        if puzzle.is_solved():
            print("solved4")
            return puzzle.solution
    else:
        # this tile is not occupied, so we try all pieces in all layouts
        for piece_id in range(len(puzzle.pieces)):
            print(f"try piece {piece_id}")
            # skip pieces already used in the solution
            if piece_id in puzzle.solution:
                continue
            for layout_id in range(len(puzzle.pieces[piece_id].layouts)):
                print(f"try layout {layout_id}")
                if puzzle.layout_fits(puzzle.pieces[piece_id].layouts[layout_id], current_position):
                    print("FIT")
                    # piece fits, so use it
                    puzzle.add_piece(piece_id, layout_id, current_position)

                    solve(puzzle.next_tile(current_position), puzzle, piece_id)

                if puzzle.is_solved():
                    print("solved2")
                    return puzzle.solution

        if puzzle.is_solved():
            print("solved3")
            return puzzle.solution


        # none of the pieces fit anywhere, backtrack
        # remove last piece from solution
        print(f"BACKTRACK, remove {last_piece_id}")
        puzzle.remove_piece(last_piece_id, puzzle.solution[last_piece_id][0], puzzle.solution[last_piece_id][1])

if __name__ == '__main__':
    pieces = [
        Piece([Layout([])], 'A'),
        Piece([Layout([(0, 1)]), Layout([(1, 0)])], 'B')
    ]

    p = Puzzle(2, 2, pieces)

    p.invalidate((0, 0))

    print(solve((0, 0), p, None))
    print(p)
