import pygame


class BackgroundLayer:
    def __init__(self, image_path: str, speed : float, y: int = 0):
        self.image = pygame.image.load(image_path).convert()
        self._speed = speed
        self._y = y
        self._x = 0
        self._width = self.image.get_width()
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x: int):
        self._x = x
    
    def update(self):
        self._x -= self._speed
        if self._x <= -self._width:
            self._x = 0
    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self._x, self._y))
        surface.blit(self.image, (self._x + self._width, self._y))
    
    
