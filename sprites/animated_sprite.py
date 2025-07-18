import pygame

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_images):
        super().__init__()
        self.images = sprite_images
        self.image_index = 0
        self.animation_fps = 30
        print(sprite_images)
        self.image = sprite_images[self.image_index]
        self.rect = self.image.get_rect()
        self.time_since_last_change = 0
        self.flip_x = False
        self.flip_y = False

    def change_image(self, dt):
        if self.time_since_last_change > (1 / self.animation_fps):
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            if self.flip_x:
                self.image = pygame.transform.flip(self.image, True, False)
            self.time_since_last_change = 0
        else:
            self.time_since_last_change += dt
