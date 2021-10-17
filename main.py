import pygame, sys
from random import randint as rand

CELL_NUMBER, CELL_SIZE = 30, 30


class Cell:

    def __init__(self, x, y, occupied, screen):
        self.x = x
        self.y = y
        self.occupied = occupied
        self.screen = screen

    def draw(self):
        for i in range(2):
            obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE - 5 * i,
                                CELL_SIZE - 5 * i)
            pygame.draw.rect(self.screen, (255 * i, 255 * i, 255 * i), obj)


class StartPoint:

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE - 5, CELL_SIZE - 5)
        pygame.draw.rect(self.screen, (0, 255, 0), obj)


class PathWay:

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE - 5, CELL_SIZE - 5)
        pygame.draw.rect(self.screen, (255, 0, 0), obj)


class MainController:

    def __init__(self, screen):
        self.screen = screen
        self.grid = []
        self.spawn_grid()
        self.start_point = None
        self.way = []
        self.direction = [0, 1, 2, 3]
        self.allow_to_spawn_first_pathway = True

    def update(self):
        self.draw_elem()
        self.choose_dir()

    def draw_elem(self):
        for row in self.grid:
            for cell in row:
                cell.draw()
        for pw in self.way:
            pw.draw()

        try:
            self.start_point.draw()
        except AttributeError:
            pass

    def spawn_start_point(self, mx, my):
        x = mx//CELL_NUMBER
        y = my//CELL_NUMBER
        self.start_point = StartPoint(x, y, self.screen)

    def spawn_grid(self):
        r = range(CELL_NUMBER)
        for _ in r:
            self.grid.append([])
        for y in r:
            for x in r:
                self.grid[y].append(Cell(x, y, False, self.screen))

    def choose_dir(self):
        new_direction = rand(self.direction[0], self.direction[-1])
        if self.allow_to_spawn_first_pathway:
            try:
                self.way.append(PathWay(self.start_point.x, self.start_point.y - 1, self.screen))
                self.grid[self.start_point.y - 1][self.start_point.x].occupied = True
                self.allow_to_spawn_first_pathway = False
            except AttributeError:
                pass
        else:
            if new_direction == 0 and self.direction != [1, 2, 3]:
                if not self.grid[self.way[-1].y - 1][self.way[-1].x].occupied:
                    self.way.append(PathWay(self.way[-1].x, self.way[-1].y - 1, self.screen))
                    self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                    self.direction = [0, 2, 3]
                else:
                    self.direction = [1, 2, 3]
            elif new_direction == 1 and self.direction != [0, 2, 3]:
                if not self.grid[self.way[-1].y + 1][self.way[-1].x].occupied:
                    self.way.append(PathWay(self.way[-1].x, self.way[-1].y + 1, self.screen))
                    self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                    self.direction = [1, 2, 3]
                else:
                    self.direction = [0, 2, 3]
            elif new_direction == 2 and self.direction != [0, 1, 3]:
                if not self.grid[self.way[-1].y][self.way[-1].x - 1].occupied:
                    self.way.append(PathWay(self.way[-1].x - 1, self.way[-1].y, self.screen))
                    self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                    self.direction = [0, 1, 2]
                else:
                    self.direction = [0, 1, 3]
            elif new_direction == 3 and self.direction != [0, 1, 2]:
                if not self.grid[self.way[-1].y][self.way[-1].x + 1].occupied:
                    self.way.append(PathWay(self.way[-1].x + 1, self.way[-1].y, self.screen))
                    self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                    self.direction = [0, 1, 3]
                else:
                    self.direction = [0, 1, 2]


def main():
    screen = pygame.display.set_mode((CELL_SIZE * CELL_NUMBER, CELL_SIZE * CELL_NUMBER))
    fpsClock = pygame.time.Clock()
    main_controller = MainController(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                main_controller.spawn_start_point(mouse_x, mouse_y)

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()
        fpsClock.tick(10)


if __name__ == '__main__':
    main()

