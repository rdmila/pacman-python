from enum import Enum
import random


class CellType(Enum):
    PASS = 0
    WALL = 1


class Candy:
    """"Usual candy"""

    def __init__(self, cell, points=5):
        self.cell = cell
        self.points = points

    def on_eaten(self):
        self.cell.candy = None


class ExtraCandy(Candy):
    """Expensive candy"""

    def __init__(self, cell, points=100):
        super().__init__(cell, points)

    def on_eaten(self):
        super().on_eaten()


class Cell:
    def __init__(self, type_):
        self.type = type_
        self.candy = None
        if self.type == CellType.PASS:
            if random.randint(1, 10) == 1:
                self.candy = ExtraCandy(self)
            else:
                self.candy = Candy(self)


class Maze:
    def __init__(self, config):
        self.grid = []
        self.cell_width = config.cell_width
        self.candy_cnt = 0
        with open(config.maze) as maze_file:
            for line in maze_file:
                line = line[:-1]
                self.grid.append([Cell(CellType.WALL if i == '1' else CellType.PASS) for i in line])
                for cell in self.grid[-1]:
                    if cell.type == CellType.PASS:
                        self.candy_cnt += 1
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def get_cell(self, x: int, y: int) -> Cell:
        """Returns the cell from maze by coordinates of a point.
        Note: each cell contains (self.cell_width)x(self.cell_width) points."""
        x_cell_id = x // self.cell_width
        y_cell_id = y // self.cell_width
        return self.grid[y_cell_id][x_cell_id]

    def pos_is_legal(self, x: int, y: int) -> bool:
        """Given coords of a center of a creature, checks if a creature can stand at point.
        It is assumed that any creature's diameter equals the width of a passage."""
        cell_type = self.get_cell(x, y).type
        cell_center = (self.cell_width // 2)
        is_centered_by_x = x % self.cell_width == cell_center
        is_centered_by_y = y % self.cell_width == cell_center
        return cell_type == CellType.PASS and (is_centered_by_x or is_centered_by_y)
