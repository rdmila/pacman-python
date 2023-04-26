from creature import Creature
import time
import random


class Ghost(Creature):
    def __init__(self, game, maze, config, pacman):
        super().__init__(game, maze, config)
        x = config.ghost_position_left_up[0] + random.randint(0, 0)
        y = config.ghost_position_left_up[1] + random.randint(0, 0)
        self.set_place_and_direction(x, y)
        self.pacman = pacman
        self.speed = config.ghost_speed
        self.last_randomize_time = time.process_time()

    def choose_direction(self):
        if time.process_time() - self.last_randomize_time < 0.2:
            return self.direction
        else:
            self.last_randomize_time = time.process_time()
            res = random.choice(['U', 'R', 'L', 'D'])
            self.old_dir = self.direction
            return self.Direction[res]

    def run(self, continue_old_dir=False):
        self.direction = self.choose_direction()
        super().run(continue_old_dir)

    def handle_collisions(self):
        if abs(self.pacman.x - self.x) <= self.radius and abs(self.pacman.y - self.y) <= self.radius:
            self.game.over(False)
