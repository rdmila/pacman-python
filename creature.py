from enum import Enum


class Creature:
    class Direction(Enum):
        R = 0
        D = 1
        L = 2
        U = 3

    def handle_collisions(self):
        pass

    def __init__(self, game, maze, config):
        self.game = game
        self.maze = maze
        self.config = config
        self.x = None
        self.y = None
        self.speed = None
        self.sprite = None
        self.direction = self.Direction.R
        self.old_dir = self.direction
        self.radius = self.config.cell_width // 2

    def set_place_and_direction(self, x, y):
        sh = self.config.cell_width // 2
        self.x = x * self.config.cell_width + sh
        self.y = y * self.config.cell_width + sh
        self.direction = self.Direction['R']

    def get_shift(self, run_dir):
        dx, dy = 0, 0
        match run_dir:
            case self.Direction.R:
                dx = 1
            case self.Direction.D:
                dy = 1
            case self.Direction.L:
                dx = -1
            case self.Direction.U:
                dy = -1
        return [dx, dy]

    def run(self, continue_old_dir=False):
        run_dir = self.old_dir if continue_old_dir else self.direction
        dx, dy = self.get_shift(run_dir)

        border_x = self.x + dx * (self.speed + self.radius)
        border_y = self.y + dy * (self.speed + self.radius)

        if self.maze.pos_is_legal(border_x, border_y):
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            self.x, self.y = new_x, new_y
            if not continue_old_dir:
                self.old_dir = self.direction
        else:
            if not continue_old_dir:
                self.run(True)

        self.handle_collisions()
