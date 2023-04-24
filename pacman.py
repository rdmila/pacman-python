from creature import Creature


class Pacman(Creature):
    def __init__(self, game, maze, config):
        super().__init__(game, maze, config)
        self.set_place_and_direction(config.pacman_position[0], config.pacman_position[1])
        self.speed = config.pacman_speed

    def handle_collisions(self) -> bool:
        """Checks collisions with candies. Calls candy's on_eaten() method and returns True if collides."""
        candy = self.maze.get_cell(self.x, self.y).candy
        if candy is None:
            return False
        else:
            candy.on_eaten()
            return True

    def set_direction(self, direction):
        self.old_dir = self.direction
        self.direction = Creature.Direction[direction]
