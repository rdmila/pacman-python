from creature import Creature


class Pacman(Creature):
    def __init__(self, game, maze, config):
        super().__init__(game, maze, config)
        self.x = config.pacman_position[0]
        self.y = config.pacman_position[1]
        self.x *= config.cell_width
        self.y *= config.cell_width
        self.speed = config.pacman_speed

    def handle_collisions(self):
        candy = self.maze.get_cell(self.x, self.y).candy
        if candy is not None:
            candy.on_eaten()
            self.game.candy_cnt -= 1

    def set_direction(self, direction):
        self.direction = Creature.Direction[direction]
