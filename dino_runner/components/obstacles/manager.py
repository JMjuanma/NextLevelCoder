from random import choice
import pygame
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD

class Manager:
    def __init__(self):
        self.obstacles=[]
        self.list=[SMALL_CACTUS, LARGE_CACTUS, BIRD]
        self.bird_stage=0

    def update(self, game):
        if len(self.obstacles) == 0:
            self.family=choice(self.list)
            if self.family == BIRD:
                self.obstacles.append(Bird(self.family))
            elif self.family==LARGE_CACTUS:
                self.large_cactus_on_use = True
                self.obstacles.append(Cactus(self.family, "large"))
            else:
                self.large_cactus_on_use=False
                self.obstacles.append(Cactus(self.family, "small"))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                break
            if obstacle.family == "bird" and self.bird_stage<5:
                obstacle.type=0
                self.bird_stage += 1
            else:
                obstacle.type=1
                self.bird_stage = (self.bird_stage+1)%10
        

    def draw(self, screen):
        for obstacle in self.obstacles:
            if obstacle.family == "cactus":
                if obstacle.subfamily == "large":
                    obstacle.draw(screen, 15)
                else:
                    obstacle.draw(screen, 0)
            elif obstacle.family == "bird":
                obstacle.draw(screen, obstacle.height)