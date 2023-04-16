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

    def place(self, x, y):
        self.x = x
        self.y = y
        self.direction = self.Direction['R']

    def run(self):
        old_pos = [self.x, self.y]
        match self.direction:
            case self.Direction.R:
                self.x += self.speed
            case self.Direction.D:
                self.y += self.speed
            case self.Direction.L:
                self.x -= self.speed
            case self.Direction.U:
                self.y -= self.speed
        if self.y < 0:
            self.y += self.config.cell_in_pixels * self.maze.height
        if self.x < 0:
            self.x += self.config.cell_in_pixels * self.maze.width

        self.y %= self.config.cell_in_pixels * self.maze.height
        self.x %= self.config.cell_in_pixels * self.maze.width

        if not self.maze.pos_is_legal(self.x, self.y):
            self.x, self.y = old_pos
        self.handle_collisions()
