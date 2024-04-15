import pygame
pygame.init()

from CollisionBox import CollisionBox

class Cashier:
    def __init__(self, x, y):
        self.structure = "cashier"

        self.x = x
        self.y = y

        self.raw_image = pygame.image.load("./assets/cashier.png")
        self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * 0.7), int(self.raw_image.get_height() * 0.7)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hit_box = CollisionBox(self.x, self.y, self.width, self.height)


    def draw(self, screen):
        self.hit_box.x = self.x
        self.hit_box.y = self.y
        screen.blit(self.image, (self.x, self.y))