import pygame
from random import randint


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type: str):
        super().__init__()
        
        if type == 'fly':
            self._frames = [
                pygame.image.load('graphics/Fly/Fly1.png').convert_alpha(),
                pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            ]
            self._y_pos = 210

        else:
            self._frames = [
                pygame.image.load('graphics/snail/snail1.png').convert_alpha(),
                pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            ]
            self._y_pos = 300
        
        self._index = 0
        self.image = self._frames[self._index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), self._y_pos))
    
    def _animate(self):
        self._index += 0.1
        if self._index >= len(self._frames):
            self._index = 0
        self.image = self._frames[int(self._index)]
    
    def update(self):
        self._animate()
        self.rect.x -= 6
        
        if self.rect.x <= -100:
            self.kill()