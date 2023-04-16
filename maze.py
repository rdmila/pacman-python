from enum import Enum


class CellType(Enum):
    PASS = 0
    WALL = 1


class Candy:
    def __init__(self, cell, points=5):
        self.cell = cell
        self.points = points

    def on_eaten(self, game):
        self.cell.candy = None
        game.add_score(self.points)


class ExtraCandy(Candy):
    def __init__(self, cell, points=100):
        super().__init__(cell, points)

    def on_eaten(self, game):
        super().on_eaten(game)
        game.turbo_state_on()


class Cell:
    def __init__(self, maze, type):
        self.maze = maze
        self.type = type
        self.candy = None


class Maze:
    def __init__(self, config):
        self.maze = []
        self.cell_width = config.cell_width
        with open(config.maze) as maze_file:
            for line in maze_file:
                line = line[:-1]
                self.maze.append([Cell(self, CellType.WALL if i == '1' else CellType.PASS) for i in line])
        self.width = len(self.maze[0])
        self.height = len(self.maze)


    def get_cell(self, x, y):
        return self.maze[int(y / self.cell_width)][int(x / self.cell_width)]

    def pos_is_legal(self, x, y):
        return self.get_cell(x, y).type == CellType.PASS
