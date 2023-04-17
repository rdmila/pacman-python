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
        self.state = UsualState()
        self.finish = False
        self.config = GameConfig('config.json')
        self.score = 0
        self.candy_cnt = 0

        self.maze = Maze(self.config)
        for i in self.maze.maze:
            for j in i:
                if j.candy is not None:
                    self.candy_cnt += 1

        self.ghosts = []
        self.pacman = Pacman(self, self.maze, self.config)
        for _ in range(self.config.ghosts_count):
            self.ghosts.append(Ghost(self, self.maze, self.config, self.pacman))
        self.graphics = GraphicsManager(self.maze, self.pacman, self.ghosts, self.config)
        self.graphics.root.after(100, self.update_field)
        self.graphics.start()
        self.after = None

    def update_field(self):
        if self.finish:
            return
        self.graphics.draw()
        self.pacman.run()
        for ghost in self.ghosts:
            ghost.run()
        if self.candy_cnt == 0:
            self.over(True)
        self.after = self.graphics.root.after(100, self.update_field)

    def over(self, win):
        self.finish = True
        self.graphics.root.after_cancel(self.after)
        if win:
            self.graphics.win()
        else:
            self.graphics.lose()
