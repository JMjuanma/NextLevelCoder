import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import FONT_STYLE, DEFAULT_TYPE, JUMPING, RUNNING, DUCKING, RUNNING_SHIELD, SHIELD_TYPE, JUMPING_SHIELD, DUCKING_SHIELD, HAMMER_TYPE, DUCKING_HAMMER, RUNNING_HAMMER, JUMPING_HAMMER 

RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE:RUNNING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE:JUMPING_HAMMER}
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE:DUCKING_HAMMER}
class Dinosaur(Sprite):
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 9

    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.setup_state()

    def setup_state(self):
        self.has_power_up = False
        self.show_text = False
        self.power_time_up = False

    def update(self, user_input):

        if self.dino_run:
            self.step_index %= 10
            self.run()
        elif self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()

        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_duck = False
            self.dino_run = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_jump = False
            self.dino_duck = True
            self.dino_run = False
        elif not self.dino_jump:
            self.dino_jump = False
            self.dino_duck = False
            self.dino_run = True

        if self.step_index == 9:
            self.step_index = 0

    def run(self):
        self.image = RUN_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index +=1

    def jump(self):
        self.image = JUMP_IMG[self.type]
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 1

        if self.jump_vel < -self.JUMP_VEL:
            self.dino_rect.y = self.Y_POS
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS+30
        self.step_index +=1
    
    def check_invinsibility(self, screen):
        if self.type == SHIELD_TYPE:
            time_to_show = round((self.power_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0 and self.show_text:
                self.show_message(f"shield enable for {time_to_show}", 18, 500, 40, screen)
            else:
                self.type = DEFAULT_TYPE
        elif self.type == HAMMER_TYPE:
            time_to_show = round((self.power_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0 and self.show_text:
                self.show_message(f"The temporal hammer is enable for {time_to_show}", 18, 500, 40, screen)
            else:
                self.type = DEFAULT_TYPE
    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def show_message(self, message, characters_size, rect_x, rect_y, screen):
        font = pygame.font.Font(FONT_STYLE, characters_size)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (rect_x, rect_y)
        screen.blit(text, text_rect)