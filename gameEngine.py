import json
from timeManager import TimeManager
from pacman import Pacman
from ghost import Ghost
from maze import Maze
from graphics import GraphicsManager

class State:
    def handle_collision(self, game, ghost):
        pass


class UsualState(State):
    def handle_collision(self, game, ghost):
        game.over()


class DopingState(State):
    def handle_collision(self, game, ghost):
        del ghost
        game.ghosts.append(Ghost(game.maze, game.config, game.pacman))


class GameConfig:
    def __init__(self, file_name):
        with open(file_name) as json_file:
            config_map = json.load(json_file)
        for param in config_map:
            setattr(self, param, config_map[param])


class Game:
    def __init__(self):
        self.timeManager = TimeManager()
        self.state = UsualState()
        self.config = GameConfig('config.json')
        self.score = 0

        self.maze = Maze(self.config)
        self.ghosts = []
        self.pacman = Pacman(self.maze, self.config)
        for _ in range(self.config.ghosts_count):
            self.ghosts.append(Ghost(self.maze, self.config, self.pacman))
        self.graphics = GraphicsManager(self.maze, self.pacman, self.ghosts, self.config)
        self.graphics.root.after(100, self.update_field)
        self.graphics.start()

    def update_field(self):
        self.pacman.run()
        for ghost in self.ghosts:
            ghost.run()
        self.graphics.draw()
        self.graphics.root.after(100, self.update_field)
