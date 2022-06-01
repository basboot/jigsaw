from piece import *

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

    def has_next_tile(self, tile):
        return tile[0] < self.m and tile[1] < self.n

    def next_tile(self, tile):
        assert self.has_next_tile(tile), "There is no next tile."
        x = tile[0]
        y = tile[1]

        x += 1
        if x == self.m:
            y = y + 1
            x = 0

        return x, y

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
        for block in self.pieces[piece_id].layouts[layout_id].blocks:
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
        for block in self.pieces[piece_id].layouts[layout_id].blocks:
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
        grid = [['.'] * self.m for _ in range(self.n)]

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


# TODO: laatste stuk niet meer doorgeven, maar na 'solve' opruimen
# TODO; check is dan niet meer nodig, voorkomt overslaat van layouts en maakt yield mogelijk
def solve(current_tile, puzzle):
    print(f"try tile {current_tile}")
    # No tiles left, so return solution, even if there isn't any
    if not puzzle.has_next_tile(current_tile):
        return puzzle.is_solved(), puzzle.solution
    else:
        # curent tile is already occupied, so try next
        if puzzle.is_occupied(current_tile):
            return solve(puzzle.next_tile(current_tile), puzzle)
        else:
            # this tile is not occupied, so we try all pieces in all layouts
            for piece_id in range(len(puzzle.pieces)):
                # skip pieces already used in the solution
                if piece_id in puzzle.solution:
                    continue
                for layout_id in range(len(puzzle.pieces[piece_id].layouts)):
                    print(f"try piece - layout {piece_id} - {layout_id}")
                    if puzzle.layout_fits(puzzle.pieces[piece_id].layouts[layout_id], current_tile):
                        print("FIT")
                        # piece fits, so use it
                        puzzle.add_piece(piece_id, layout_id, current_tile)
                        # and solve next
                        solution = solve(puzzle.next_tile(current_tile), puzzle)

                        if solution[0]:
                            # only return this solution if the puzzle has been solved
                            return solution
                        else:
                            # remove this piece/layout and try next (backtrack)
                            puzzle.remove_piece(piece_id, layout_id, current_tile)
                        print(f"after solve piece - layout {piece_id} - {layout_id}")
            # None of the pieces fits, so we cannot return a solution
            return False, None

if __name__ == '__main__':
    # puzzle_pieces = [
    #     Piece([Layout([])], 'A'),
    #     Piece([Layout([(0, 1)]), Layout([(1, 0)])], 'B')
    # ]

    puzzle_pieces = [
        Piece([Layout([])], 'A'),
        Piece([Layout([(1, 0), (1, 1)]), Layout([(1, -1), (1, 0)]), Layout([(0, 1), (1, 1)]),
               Layout([(1, 0), (0, 1)])], 'B'),
        Piece([Layout([(0, 1), (0, 2), (-1, 2)]), Layout([(0, 1), (1, 1), (2, 1)]), Layout([(1, 0), (0, 1), (0, 2)]),
               Layout([(1, 0), (2, 0), (2, -1)]), Layout([(0, 1), (0, 2), (1, 2)]), Layout([(1, 0), (2, 0), (2, -1)]),
               Layout([(1, 0), (1, 1), (1, 2)]), Layout([(0, 1), (1, 1), (2, 1)])], 'C')
    ]

    p = Puzzle(3, 3, puzzle_pieces)

    p.invalidate((2, 2))

    print(solve((0, 0), p))
    print(p)

