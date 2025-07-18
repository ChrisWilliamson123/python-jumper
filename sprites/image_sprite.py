import pygame

class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_image):
        super().__init__()
        self.image = sprite_image
        self.rect = self.image.get_rect()
