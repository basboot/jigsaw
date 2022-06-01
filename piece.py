import numpy as np
from dataclasses import dataclass

@dataclass
class Layout:
    blocks: list[tuple]


@dataclass
class Piece:
    layouts: list[Layout]
    representation: str


if __name__ == '__main__':
    peters_puzzel_pieces = [
        # 0
        Piece([Layout([(1, -1), (1, 0), (1, 1), (1, 2)])], 'A'),
        # 1
        Piece([Layout([(1, 0), (0, 1), (1, 1), (0, 2)])], 'B'),
        # 2
        Piece([Layout([(1, 0), (1, -1), (2, -1)])], 'C'),
        # 3
        Piece([Layout([(0, 1), (0, 2), (1, 2), (2, 2)])], 'D'),
        # 4
        Piece([Layout([(1, 0), (1, -1), (1, 1), (2, 0)])], 'E'),
        # 5
        Piece([Layout([(1, 0), (1, 1), (1, 2), (0, 2)])], 'F'),
        # 6
        Piece([Layout([(1, 0), (1, -1), (2, -1), (0, 1)])], 'G'),
        # 7
        Piece([Layout([(1, 0), (1, -1), (1, 1)])], 'H'),
        # 8
        Piece([Layout([(0, 1), (1, 1), (2, 1)])], 'I'),
        # 9
        Piece([Layout([(1, 0), (1, -1), (2, 0), (2, 1)])], 'J')
    ]

    for piece in peters_puzzel_pieces:
        print(piece)
        block_matrix = np.zeros((len(piece.layouts[0].blocks) + 1, 2), dtype=np.int32)
        for i in range(len(piece.layouts[0].blocks)):
            print(piece.layouts[0].blocks[i])
            block_matrix[i+1, :] = piece.layouts[0].blocks[i]
        print(block_matrix)
        rotate90 = np.array(((0, -1), (1, 0)))
        print(block_matrix @ rotate90)
        mirror_x = np.array(((-1, 0), (0, 1)))
        print(block_matrix @ mirror_x)

        # find smallest x
        print("---")
        matrix = block_matrix @ mirror_x

        print(np.amin(matrix, axis=0))
        result = np.where(matrix == np.amin(matrix))
        print(result)

        # now find the smallest y in the results
        smalllest_x_pos = result[0]
        print(smalllest_x_pos)
        y_s = matrix[smalllest_x_pos, 1]
        print(y_s)
        smallest_y = np.min(y_s)
        print(smallest_y)
        smallest_x = matrix[smalllest_x_pos[0], 0]
        print(smallest_x)

        print(matrix - np.array([smallest_x, smallest_y]))

        new_matrix = matrix - np.array([smallest_x, smallest_y])

        points = []
        for row in new_matrix:
            point = tuple(row)
            if point != (0, 0):
                print(tuple(row))
                points.append(tuple(row))
        print(f"Layout({points})")

        # TODO: use offset to calc new layout (done)
        # TODO: don't forget to cast to int (done ;-)
        # TODO: print layouts (and remove 0,0)