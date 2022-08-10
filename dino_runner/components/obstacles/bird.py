from random import choice

from dino_runner.components.obstacles.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self, image):
        self.family="bird"
        self.type = 0
        self.heights=[50, 0, -50, -100]
        self.height=choice(self.heights)
        super().__init__(image, self.type)
        self.rect.y = 125