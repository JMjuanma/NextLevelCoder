import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import SHIELD_TYPE

class Manager:
    def __init__(self):
        self.power_ups=[]
        self.when_appears = 0
        self.options = [Shield(), Hammer()]

    def update(self, points, game_speed, player):
        self.generate_power_ups(points)
        for power_up in self.power_ups :
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.show_text = True #a
                player.type = power_up.type
                time_random = random.randint(5, 8)
                player.power_time_up = power_up.start_time + (time_random * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)
    
    def generate_power_ups(self, points):
        if len(self.power_ups) == 0 and self.when_appears == points :
            self.when_appears = random.randint( 200 + self.when_appears, self.when_appears + 300)
            self.power_ups.append(random.choice(self.options))

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)
