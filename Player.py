import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float | int, float | int]):
        super().__init__()
        self._walk_frames = [
            pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha(),
            pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        ]
        self._jump_frame = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self._index = 0

        self.image = self._walk_frames[self._index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.gravity = 0

        self._jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self._jump_sound.set_volume(0.1)

    def _handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self._jump_sound.play()
    
    def _apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def _animate(self):
        if self.rect.bottom < 300:
            self.image = self._jump_frame
        else:
            self._index += 0.1
            if self._index >= len(self._walk_frames):
                self._index = 0
            self.image = self._walk_frames[int(self._index)]
    
    def update(self):
        self._handle_input()
        self._apply_gravity()
        self._animate()
