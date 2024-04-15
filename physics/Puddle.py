import pygame
import math
pygame.init()

from CollisionBox import CollisionBox

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

class Puddle:
    def __init__(self, x, y):
        self.structure = "puddle"
        
        self.image = pygame.image.load("./assets/puddle.png")

        self.x = x
        self.y = y

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hit_box = CollisionBox(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.hit_box.x = self.x
        self.hit_box.y = self.y

        screen.blit(self.image, (self.x, self.y))

