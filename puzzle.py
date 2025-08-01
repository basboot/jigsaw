# Puzzle: class to store a puzzle, the pieces and helper function to move
# pieces on the board and solve the puzzle

# A puzzle is a square board with m x n tiles, which can be empty or occupied.
# A piece of the puzzle is a shape of blocks. Each block can occupy a tile.
# Because a piece kan be rotated and flipped it has multiple layouts, which
# do not have to be unique because of symmetry, which results in 1 to 8 unique
# layouts per piece.

# The target is to keep a few specified tiles open an occupy all others. By
# invalidating (occupy) the q tiles that cannot be used beforehand, and using
# pieces with a total number of blocks of m x n - q the problem reduces to placing
# all pieces of the puzzle on the board without overlapping.

# If we choose the origin (0, 0) of a piece to be the most left block on the top
# row, we can solve the puzzle by trying all pieces from top left, to bottom right
# to fill the puzzle.

# Convention: (0, 0) is top left, + is right/down
# the origin does not have to be specified in the list of blocks

from piece import *
from puzzle_animation import PuzzleAnimation


class Puzzle:
    def __init__(self, m, n, pieces):
        self.m = m
        self.n = n
        self.pieces = pieces

        # set with occupied blocks of the puzzle
        self.occupied = set()

        # set with illegal tiles to use
        self.invalidated = set()

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

            assert (x, y) not in self.occupied, f"Cannot put tile on ({x},{y}) because it is already occupied"
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

            assert (x, y) in self.occupied, f"Cannot remove tile from ({x},{y}) because it is not occupied"
            # add to occupied
            self.occupied.remove((x, y))

        # pieces on the board
        # piece id => (layout id, position)
        del self.solution[piece_id]

    # invalidate illegal tiles
    def invalidate(self, tile):
        self.invalidated.add(tile)
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
        representation = ""
        for puzzle_row in grid:
            for tile in puzzle_row:
                representation = f"{representation}{tile}"
            representation = f"{representation}\n"
        return representation

    def solve(self, animation=None, all_solutions=False, current_tile=(0, 0)):
        # No tiles left, so return a copy of the solution, or an empty list if there isn't any
        if not self.has_next_tile(current_tile):
            return [self.solution.copy()] if self.is_solved() else []
        else:
            # current tile is already occupied, so skip and return solution for next tile
            if self.is_occupied(current_tile):
                return self.solve(animation, all_solutions, self.next_tile(current_tile))
            else:
                # this tile is not occupied, so we try all pieces in all layouts
                # store all solutions found for this piece (empty list =  no solutions possible)
                solutions = []
                for piece_id in range(len(self.pieces)):
                    # skip pieces already used in the solution
                    if piece_id in self.solution:
                        continue
                    for layout_id in range(len(self.pieces[piece_id].layouts)):
                        if self.layout_fits(self.pieces[piece_id].layouts[layout_id], current_tile):
                            # piece fits, so use it
                            self.add_piece(piece_id, layout_id, current_tile)
                            if animation is not None:
                                animation.update()

                            # and solve next
                            solution = self.solve(animation, all_solutions, self.next_tile(current_tile))

                            # if we are only interested in one solution, just return the first that is found
                            if not all_solutions:
                                if len(solution) > 0:
                                    return [solution[0]]

                            # Add new solutions to solutions already found
                            solutions += solution

                            # remove this piece/layout and try next (backtrack)
                            self.remove_piece(piece_id, layout_id, current_tile)
                            if animation is not None:
                                animation.update()

                # Return all solutions found (could be zero)
                return solutions


if __name__ == '__main__':
    # 3 x 3 puzzle, to debug algorithm
    puzzle_pieces = [
        create_piece([(0, 0)], 'A'),
        create_piece([(0, 0), (1, 0), (1, 1)], 'B'),
        create_piece([(0, 0), (0, 1), (0, 2), (-1, 2)], 'C')
    ]

    p = Puzzle(3, 3, puzzle_pieces)

    p.invalidate((0, 0))

    a = PuzzleAnimation(p)
    s = p.solve((0, 0), a, True)
    print(s)
    for i in range(len(s)):
        print(f"Solution #{i}")
        p.solution = s[i]
        print(p)
    a.finish()