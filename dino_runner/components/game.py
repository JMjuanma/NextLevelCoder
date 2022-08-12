import sys
import pygame, pygame.locals

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, RUNNING, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, HAMMER_TYPE
from .obstacles.manager import Manager as ObstacleManager
from .power_ups.manager import Manager as PowerUpManager

FONT_STYLE="freesansbold.ttf"
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.running = False
        self.playing = False
        self.game_speed = 20
        self.game_speed_in_use = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.death_count = 0
        self.points = 0
        self.points_record = 0

    def run(self):
        # Game loop: events - update - draw
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN :
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    pygame.quit()
                    sys.exit()
                else:
                    self.points = 0
                    self.run()

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_time()
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self.points, self.game_speed_in_use, self.player)
    
    def update_score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed +=1

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_score()
        self.player.check_invinsibility(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.update_time()
        self.x_pos_bg -= self.game_speed_in_use

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.points_record = max(self.points, self.points_record)
                self.game_speed = 20
                self.game_speed_on_use = 20
                self.show_menu()

        pygame.display.quit()
        pygame.quit() 
        
    def draw_score(self):
        self.show_message(f"Points {self.points}", 22, 1000, 50)

    def show_menu(self):
        self.screen.fill((200, 200, 250))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count:
            #mostrar numero de muertes y puntos, mensaje de reinicio
            self.show_message("You died", 60, half_screen_width, 50)
            self.show_message(f"Death number {self.death_count}", 20, half_screen_width, 130)
            self.show_message("Press key down to exit and any other to try again", 30, half_screen_width, half_screen_height)
            self.show_message(f"Final points : {self.points}", 30, half_screen_width, half_screen_height+50)
            self.show_message(f"Your points record: {self.points_record}", 20, half_screen_width, half_screen_height+100)
        else:
            self.show_message("Press any key to start", 30, half_screen_width, half_screen_height)
        self.screen.blit(RUNNING[0], (half_screen_width-20, half_screen_height-140))
        pygame.display.update()
        self.handle_events_on_menu()

    def show_message(self, message, characters_size, rect_x, rect_y):
        font = pygame.font.Font(FONT_STYLE, characters_size)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (rect_x, rect_y)
        self.screen.blit(text, text_rect)

    def update_time(self):
        if self.player.type == HAMMER_TYPE:
            self.game_speed_in_use = 20
        else:
            self.game_speed_in_use = self.game_speed