import pygame
from sys import exit
from random import choice
from Player import *
from Obstacle import *
from BackgroundLayer import *

class Game:
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Pixel Runner')
        self._clock = pygame.time.Clock()

        self._game_active = False

        self._start_time = 0
        self._score = 0
        self._score_record = 0

        self._font = pygame.font.Font('font/Pixeltype.ttf', 50)

        self._bg_music = pygame.mixer.Sound('audio/music.wav')
        self._bg_music.set_volume(0.3)
        self._bg_music.play(loops=-1)

        self._player_group = pygame.sprite.GroupSingle()
        self._player_group.add(Player((80, 300)))
        self._obstacle_group = pygame.sprite.Group()

        self._sky = BackgroundLayer('graphics/sky.png', speed=0.5, y=0)
        self._ground = BackgroundLayer('graphics/ground.png', speed=1, y=300)

        self._player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
        self._player_stand = pygame.transform.rotozoom(self._player_stand, 0, 2)
        self._player_stand_rect = self._player_stand.get_rect(center=(400,200))
        self._title_surf = self._font.render('Pixel Runner', False, (111,196,169))
        self._title_rect = self._title_surf.get_rect(center=(400,80))
        self._instruction_surf = self._font.render('Press space to run', False, (111,196,169))
        self._instruction_rect = self._instruction_surf.get_rect(center=(400,320))

        self._OBSTACLE_TIMER = pygame.USEREVENT + 1
        pygame.time.set_timer(self._OBSTACLE_TIMER, 1500)
    
    def _display_score(self) -> int:
        self._score = (pygame.time.get_ticks() - self._start_time) // 1000
        score_surf = self._font.render(f'Score: {self._score}', False, (64,64,64))
        score_rect = score_surf.get_rect(center=(400,50))
        self._screen.blit(score_surf, score_rect)
        
        return self._score

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if self._game_active:
                if event.type == self._OBSTACLE_TIMER:
                    obstacle_type = choice(['fly', 'snail', 'snail', 'snail'])
                    self._obstacle_group.add(Obstacle(obstacle_type))
            
            else:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    self._game_active = True
                    self._start_time = pygame.time.get_ticks()
                    self._score_record =  self._score if self._score > self._score_record else self._score_record
                    self._obstacle_group.empty()
                    self._player_group.sprite.rect.midbottom = (80, 300)
                    self._sky.x = 0
                    self._ground.x = 0

    def _update_game(self):
        self._sky.update()
        self._ground.update()

        self._player_group.update()
        self._obstacle_group.update()

        if pygame.sprite.spritecollide(
            self._player_group.sprite,
            self._obstacle_group,
            False
        ):
            self._game_active = False

    def _draw_game(self):
        self._sky.draw(self._screen)
        self._ground.draw(self._screen)

        self._display_score()

        self._player_group.draw(self._screen)
        self._obstacle_group.draw(self._screen)

    def _draw_menu(self):
        self._screen.fill((94,129,162))
        self._screen.blit(self._player_stand, self._player_stand_rect)
        self._screen.blit(self._title_surf, self._title_rect)

        record_msg = self._font.render(f'Record: {self._score_record}', False, (111,196,169))
        record_msg_rect = record_msg.get_rect(midleft=(20,40))

        if self._score == 0:
            self._screen.blit(self._instruction_surf, self._instruction_rect)
            self._screen.blit(record_msg, record_msg_rect)

        elif self._score > self._score_record:
            new_record_msg = self._font.render(f'You got a new record: {self._score}!', False, (111, 196, 169))
            new_record_msg_rect = new_record_msg.get_rect(center=(400, 330))
            self._screen.blit(new_record_msg, new_record_msg_rect)
        
        else:
            score_msg = self._font.render(f'Your score: {self._score}', False, (111, 196, 169))
            score_msg_rect = score_msg.get_rect(center=(400, 330))
            self._screen.blit(score_msg, score_msg_rect)    
            self._screen.blit(record_msg, record_msg_rect)        
    
    def run(self):
        while True:
            self._handle_events()

            if self._game_active:
                self._update_game()
                self._draw_game()
            else:
                self._draw_menu()
            
            pygame.display.update()
            self._clock.tick(60)
