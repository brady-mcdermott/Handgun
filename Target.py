import pygame, os
from random import randint

# Target Instance (no longer using sprite group but I'd rather not break it at this point)
class Target(pygame.sprite.Sprite):
    def __init__(self, pos, group, time):
        super().__init__(group)

        # You get the jist
        self.image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'target.png')).convert_alpha(), (50,50))
        self.rect = self.image.get_rect(topleft = pos)
        self.spawned_at = time