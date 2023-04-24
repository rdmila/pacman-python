from pacman import Pacman
from ghost import Ghost
from maze import Maze
from graphics import GraphicsManager
from config import GameConfig


class Game:
    def __init__(self):
        self.finish = False
        self.config = GameConfig
        self.score = 0

        self.maze = Maze(self.config)
        self.ghosts = []
        self.pacman = Pacman(self, self.maze, self.config)
        for _ in range(self.config.ghosts_count):
            self.ghosts.append(Ghost(self, self.maze, self.config, self.pacman))
        self.graphics = GraphicsManager(self.maze, self.pacman, self.ghosts)
        self.graphics.root.after(10, self.update_field)
        self.graphics.start()
        self.after = None

    def update_field(self):
        if self.finish:
            return
        self.graphics.update()
        self.pacman.run()
        for ghost in self.ghosts:
            ghost.run()
        if self.maze.candy_cnt == 0:
            self.over(True)
        self.after = self.graphics.root.after(10, self.update_field)

    def over(self, win):
        self.finish = True
        func = self.graphics.win if win else self.graphics.lose
        self.graphics.root.after(10, func)
