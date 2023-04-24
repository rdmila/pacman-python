import tkinter as tk
from maze import CellType
from config import GameConfig
import time


def points_to_pixels(x):
    return x * GameConfig.cell_in_pixels // GameConfig.cell_width


class GraphicsManager:

    def bind_controls(self):
        self.root.bind("<Left>", lambda event: self.pacman.set_direction('L'))
        self.root.bind("<Right>", lambda event: self.pacman.set_direction('R'))
        self.root.bind("<Up>", lambda event: self.pacman.set_direction('U'))
        self.root.bind("<Down>", lambda event: self.pacman.set_direction('D'))

    def draw_maze(self):
        """Initializes maze background."""
        width = GameConfig.cell_in_pixels
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, background='black')
        for i, row in enumerate(self.maze.grid):
            for j, cell in enumerate(row):
                if cell.type == CellType.WALL:
                    left_up = [j * width, i * width]
                    right_down = [(j + 1) * width, (i + 1) * width]
                    self.canvas.create_rectangle(*left_up, *right_down, fill='blue', outline='blue')
                elif cell.candy is not None:
                    radius = 0.05
                    shift = 0.5
                    left_up = [(j + shift - radius) * width, (i + shift - radius) * width]
                    right_down = [(j + shift + radius) * width, (i + shift + radius) * width]
                    self.candy_sprites[i][j] = \
                        self.canvas.create_oval(*left_up, *right_down, fill='pink', outline='pink')

    def draw_creatures(self):
        """Initializes creatures: ghosts and pacman."""
        x = points_to_pixels(self.pacman.x)
        y = points_to_pixels(self.pacman.y)
        sh = self.cell_in_pixels // 2
        self.pacman_sprite = self.canvas.create_oval(x - sh, y - sh, x + sh, y + sh, fill='yellow')

        self.ghost_sprites = []
        for ghost in self.ghosts:
            x = points_to_pixels(ghost.x)
            y = points_to_pixels(ghost.y)
            sprite = self.canvas.create_oval(x - sh, y - sh, x + sh, y + sh, fill='red')
            self.ghost_sprites.append(sprite)
        self.canvas.pack()

    def __init__(self, maze, pacman, ghosts):
        self.maze = maze
        self.pacman = pacman
        self.ghosts = ghosts

        self.root = tk.Tk()
        self.bind_controls()

        self.cell_in_pixels = GameConfig.cell_in_pixels
        cell_cnt_by_x = self.maze.width
        cell_cnt_by_y = self.maze.height
        self.canvas_width = self.cell_in_pixels * cell_cnt_by_x
        self.canvas_height = self.cell_in_pixels * cell_cnt_by_y

        self.candy_sprites = [[None] * cell_cnt_by_x for _ in range(cell_cnt_by_y)]
        self.canvas = None
        self.draw_maze()

        self.pacman_sprite = None
        self.ghost_sprites = None
        self.draw_creatures()

        self.canvas.pack()
        self.root.update()

    def start(self):
        self.root.mainloop()

    def update(self):
        """Changes positions of creatures on canvas."""
        sh = self.cell_in_pixels // 2
        x = points_to_pixels(self.pacman.x)
        y = points_to_pixels(self.pacman.y)
        self.canvas.coords(self.pacman_sprite, x - sh, y - sh, x + sh, y + sh)

        for num, ghost in enumerate(self.ghosts):
            x = points_to_pixels(ghost.x)
            y = points_to_pixels(ghost.y)
            self.canvas.coords(self.ghost_sprites[num], x - sh, y - sh, x + sh, y + sh)

        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.candy_sprites[i][j] is not None and self.maze.grid[i][j].candy is None:
                    self.canvas.delete(self.candy_sprites[i][j])
                    self.candy_sprites[i][j] = None

    def win(self):
        self.root.destroy()

    def lose(self):
        """Draws picture saying that player lost the game, waits one second and finishes."""
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="red", outline="red")
        self.canvas.pack()
        self.root.update()
        self.root.after(1000, self.root.destroy)
