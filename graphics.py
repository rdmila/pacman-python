import tkinter as tk
from maze import CellType
import time

class GraphicsManager:
    def points_to_pixels(self, x):
        return x * self.config.cell_in_pixels / self.config.cell_width

    def bind_controls(self):
        self.root.bind("<Left>", lambda event: self.pacman.set_direction('L'))
        self.root.bind("<Right>", lambda event: self.pacman.set_direction('R'))
        self.root.bind("<Up>", lambda event: self.pacman.set_direction('U'))
        self.root.bind("<Down>", lambda event: self.pacman.set_direction('D'))

    def __init__(self, maze, pacman, ghosts, config):
        self.config = config
        self.maze = maze
        self.pacman = pacman
        self.ghosts = ghosts

        self.root = tk.Tk()
        self.bind_controls()

        cell_in_pixels = self.config.cell_in_pixels

        maze_width = len(maze.maze[0])
        maze_height = len(maze.maze)

        self.candy_sprites = [[None] * maze_width for _ in range(maze_height)]
        self.canvas_width = cell_in_pixels * maze_width
        self.canvas_height = cell_in_pixels * maze_height
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, background='black')
        for i, row in enumerate(maze.maze):
            for j, cell in enumerate(row):
                if cell.type == CellType.WALL:
                    self.canvas.create_rectangle(j * cell_in_pixels, i * cell_in_pixels,
                                            (j + 1) * cell_in_pixels, (i + 1) * cell_in_pixels,
                                            fill='blue', outline='blue')
                elif cell.candy is not None:
                    self.candy_sprites[i][j] = self.canvas.create_oval((j + 0.45) * cell_in_pixels, (i + 0.45) * cell_in_pixels,
                                            (j + 0.55) * cell_in_pixels, (i + 0.55) * cell_in_pixels,
                                            fill='pink', outline='pink')

        x = self.points_to_pixels(pacman.x)
        y = self.points_to_pixels(pacman.y)
        sh = cell_in_pixels // 2
        self.pacman_sprite = self.canvas.create_oval(x, y, x + sh, y + sh, fill='yellow')
        self.ghost_sprites = []
        self.canvas.pack()

        for ghost in self.ghosts:
            x = self.points_to_pixels(ghost.x)
            y = self.points_to_pixels(ghost.y)
            sprite = self.canvas.create_oval(x, y, x + sh, y + sh, fill='red')
            self.ghost_sprites.append(sprite)
        self.canvas.pack()

    def start(self):
        self.root.mainloop()

    def draw(self):
        cell_in_pixels = self.config.cell_in_pixels
        sh = cell_in_pixels // 2
        x = self.points_to_pixels(self.pacman.x)
        y = self.points_to_pixels(self.pacman.y)
        self.canvas.coords(self.pacman_sprite, x, y, x + sh, y + sh)

        for num, ghost in enumerate(self.ghosts):
            x = self.points_to_pixels(ghost.x)
            y = self.points_to_pixels(ghost.y)
            self.canvas.coords(self.ghost_sprites[num], x, y, x + sh, y + sh)
        self.canvas.pack()

        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.candy_sprites[i][j] is not None and self.maze.maze[i][j].candy is None:
                    self.canvas.delete(self.candy_sprites[i][j])
                    self.candy_sprites[i][j] = None

    def win(self):
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill='green')
        time.sleep(1)
        self.root.quit()

    def lose(self):
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill='red')
        time.sleep(1)
        self.root.quit()
