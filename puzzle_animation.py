import sys
from time import sleep

import pygame as pygame

# game colors
BACKGROUND = (50, 50, 50)
BORDER = (150, 150, 150)
CELL = [(100, 100, 100), (0, 0, 200), (0, 200, 0), (0, 200, 200), (200, 0, 0), (200, 0, 200), (200, 200, 0), (200, 200, 200), (250, 250, 250), (100, 50, 200)]

# game size
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 250


# update speed
UPDATE_DELAY = 0.0

SHOW_ANIMATION = True

class PuzzleAnimation:
    def __init__(self, puzzle, text=None):
        self.puzzle = puzzle
        self.text = text

        self.cell_size_x = WINDOW_WIDTH / puzzle.m
        self.cell_size_y = WINDOW_HEIGHT / puzzle.n

        if SHOW_ANIMATION:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.clock = pygame.time.Clock()

    def update(self):
        if SHOW_ANIMATION:
            # draw puzzle
            font = pygame.font.Font('freesansbold.ttf', 32)


            self.screen.fill(BACKGROUND)
            for x in range(self.puzzle.m):
                for y in range(self.puzzle.n):
                    rect = pygame.Rect(x * self.cell_size_x, y * self.cell_size_y, self.cell_size_x, self.cell_size_y)
                    pygame.draw.rect(self.screen, BORDER, rect, 1)
                    if self.text is not None:
                        text = font.render(self.text[y][x], True, BORDER, BACKGROUND)
                        self.screen.blit(text, rect)

            for piece_id, layout_position in self.puzzle.solution.items():
                for block in self.puzzle.pieces[piece_id].layouts[layout_position[0]].blocks + [(0, 0)]:
                    #print(block)
                    x = layout_position[1][0] + block[0]
                    y = layout_position[1][1] + block[1]

                    rect = pygame.Rect(x * self.cell_size_x, y * self.cell_size_y, self.cell_size_x, self.cell_size_y)
                    pygame.draw.rect(self.screen, CELL[piece_id], rect, 0)

                    # else:
                    #     pygame.draw.rect(self.screen, BORDER, rect, 1)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            sleep(UPDATE_DELAY)
        #print(f"Update: {self.puzzle.solution}")
