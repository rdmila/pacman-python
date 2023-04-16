from creature import Creature
import time
import random


class Ghost(Creature):
    def __init__(self, maze, config, pacman):
        super().__init__(maze, config)
        self.x = config.ghost_position_left_up[0] + random.randint(0, 0)
        self.y = config.ghost_position_left_up[1] + random.randint(0, 0)
        self.x *= config.cell_width
        self.y *= config.cell_width
        self.speed = config.ghost_speed
        self.pacman = pacman
        self.last_randomize_time = time.process_time()

    def choose_direction(self):
        if time.process_time() - self.last_randomize_time < 0.01:
            return self.direction
        else:
            self.last_randomize_time = time.process_time()
            res = random.choice(['U', 'R', 'L', 'D'])
            return self.Direction[res]

    def run(self):
        self.direction = self.choose_direction()
        super().run()

    def handle_collisions(self):
        pass
