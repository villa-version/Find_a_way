import pygame, sys
from random import randint as rand

CELL_NUMBER, CELL_SIZE = 20, 30


class Cell:

    def __init__(self, x, y, occupied, screen, wrong):
        self.x = x
        self.y = y
        self.occupied = occupied
        self.wrong = wrong
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


class FinishPoint:

    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def draw(self):
        obj = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE - 5, CELL_SIZE - 5)
        pygame.draw.rect(self.screen, (255, 0, 255), obj)


class PathWay:

    def __init__(self, x, y, screen, direction):
        self.x = x
        self.y = y
        self.direction = direction
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
        self.finish_point = None
        self.way = []
        self.direction = [0, 1, 2, 3]
        self.allow_to_spawn_first_pathway = True
        self.way_out_of_a_trap_state = True
        self.progress = 'SP'
        self.last_dir = -1

    def update(self):
        self.draw_elem()
        self.choose_dir()
        self.chek_collision_with_finish_point()

    def draw_elem(self):
        for row in self.grid:
            for cell in row:
                cell.draw()
        for pw in self.way:
            pw.draw()

        try:
            self.start_point.draw()
            self.finish_point.draw()
        except AttributeError:
            pass

    def spawn_points(self, mx, my):
        if self.progress == 'SP':
            self.progress = 'FP'
            x = mx//CELL_SIZE
            y = my//CELL_SIZE
            self.start_point = StartPoint(x, y, self.screen)
        elif self.progress == 'FP':
            self.progress = 'SP'
            x = mx // CELL_SIZE
            y = my // CELL_SIZE
            self.finish_point = FinishPoint(x, y, self.screen)

    def spawn_grid(self):
        r = range(CELL_NUMBER)
        for _ in r:
            self.grid.append([])
        for y in r:
            for x in r:
                self.grid[y].append(Cell(x, y, False, self.screen, False))

    def way_out_of_a_trap(self, dir):
        counter = 0
        if self.way_out_of_a_trap_state:
            if self.way[-1].y - 1 < 0:
                counter += 1
            else:
                if self.grid[self.way[-1].y - 1][self.way[-1].x].occupied:
                    counter += 1
            if self.way[-1].y + 1 > CELL_NUMBER - 1:
                counter += 1
            else:
                if self.grid[self.way[-1].y + 1][self.way[-1].x].occupied:
                    counter += 1
            if self.way[-1].x - 1 < 0:
                counter += 1
            else:
                if self.grid[self.way[-1].y][self.way[-1].x - 1].occupied:
                    counter += 1
            if self.way[-1].x + 1 > CELL_NUMBER - 1:
                counter += 1
            else:
                if self.grid[self.way[-1].y][self.way[-1].x + 1].occupied:
                    counter += 1

            self.last_dir = self.way[-1].direction

            if counter == 4:
                self.grid[self.way[-1].y][self.way[-1].x].occupied = False
                self.grid[self.way[-1].y][self.way[-1].x].wrong = True
                self.direction.remove(self.last_dir)
                self.way.remove(self.way[-1])
                self.way_out_of_a_trap_state = False
        else:
            if self.way[-1].y - 1 < 0:
                counter += 1
            else:
                if self.grid[self.way[-1].y - 1][self.way[-1].x].occupied:
                    counter += 1
                elif self.grid[self.way[-1].y - 1][self.way[-1].x].wrong:
                    counter += 1
            if self.way[-1].y + 1 > CELL_NUMBER - 1:
                counter += 1
            else:
                if self.grid[self.way[-1].y + 1][self.way[-1].x].occupied:
                    counter += 1
                elif self.grid[self.way[-1].y + 1][self.way[-1].x].wrong:
                    counter += 1
            if self.way[-1].x - 1 < 0:
                counter += 1
            else:
                if self.grid[self.way[-1].y][self.way[-1].x - 1].occupied:
                    counter += 1
                elif self.grid[self.way[-1].y][self.way[-1].x - 1].wrong:
                    counter += 1
            if self.way[-1].x + 1 > CELL_NUMBER - 1:
                counter += 1
            else:
                if self.grid[self.way[-1].y][self.way[-1].x + 1].occupied:
                    counter += 1
                elif self.grid[self.way[-1].y][self.way[-1].x + 1].wrong:
                    counter += 1

            self.last_dir = self.way[-1].direction

            if counter < 4:
                self.way_out_of_a_trap_state = True
                self.last_dir = -1
            else:
                self.grid[self.way[-1].y][self.way[-1].x].wrong = True
                self.grid[self.way[-1].y][self.way[-1].x].occupied = False
                self.way.remove(self.way[-1])
                if self.last_dir in self.direction:
                    self.direction.remove(self.last_dir)

    def choose_dir(self):
        new_direction = rand(self.direction[0], self.direction[-1])
        if self.allow_to_spawn_first_pathway:
            try:
                self.way.append(PathWay(self.start_point.x, self.start_point.y + 1, self.screen, new_direction))
                self.grid[self.start_point.y + 1][self.start_point.x].occupied = True
                self.grid[self.start_point.y][self.start_point.x].occupied = True
                self.allow_to_spawn_first_pathway = False
            except AttributeError:
                pass
        else:
            if new_direction == 0 and self.direction != [1, 2, 3]:
                if self.way[-1].y - 1 < 0:
                    self.direction = [2, 3]
                else:
                    if not self.grid[self.way[-1].y - 1][self.way[-1].x].occupied:
                        self.way.append(PathWay(self.way[-1].x, self.way[-1].y - 1, self.screen, new_direction))
                        self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                        self.direction = [0, 2, 3]
                    else:
                        self.direction = [1, 2, 3]
            elif new_direction == 1 and self.direction != [0, 2, 3]:
                if self.way[-1].y == CELL_NUMBER - 1:
                    self.direction = [2, 3]
                else:
                    if not self.grid[self.way[-1].y + 1][self.way[-1].x].occupied:
                        self.way.append(PathWay(self.way[-1].x, self.way[-1].y + 1, self.screen, new_direction))
                        self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                        self.direction = [1, 2, 3]
                    else:
                        self.direction = [0, 2, 3]
            elif new_direction == 2 and self.direction != [0, 1, 3]:
                if self.way[-1].x - 1 < 0:
                    self.direction = [0, 1]
                else:
                    if not self.grid[self.way[-1].y][self.way[-1].x - 1].occupied:
                        self.way.append(PathWay(self.way[-1].x - 1, self.way[-1].y, self.screen, new_direction))
                        self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                        self.direction = [0, 1, 2]
                    else:
                        self.direction = [0, 1, 3]
            elif new_direction == 3 and self.direction != [0, 1, 2]:
                if self.way[-1].x + 1 > CELL_NUMBER - 1:
                    self.direction = [0, 1]
                else:
                    if not self.grid[self.way[-1].y][self.way[-1].x + 1].occupied:
                        self.way.append(PathWay(self.way[-1].x + 1, self.way[-1].y, self.screen, new_direction))
                        self.grid[self.way[-1].y][self.way[-1].x].occupied = True
                        self.direction = [0, 1, 3]
                    else:
                        self.direction = [0, 1, 2]
            self.way_out_of_a_trap(new_direction)

    def chek_collision_with_finish_point(self):
        try:
            dx = abs(self.finish_point.x - self.way[-1].x)
            dy = abs(self.finish_point.y - self.way[-1].y)
            if dx == 1 and dy == 1:
                print('THE PROGRAM HAS FOUND A WAY TO FINISH POINT, YOU WON')
                pygame.quit()
                sys.exit()
        except AttributeError:
            pass


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
                main_controller.spawn_points(mouse_x, mouse_y)

        screen.fill((255, 255, 255))
        main_controller.update()
        pygame.display.update()
        fpsClock.tick(10)


if __name__ == '__main__':
    main()

