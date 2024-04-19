import pygame
import math
import random
pygame.init()

from CollisionBox import CollisionBox

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1100

class Bot:
    def __init__(self, x, y):
        self.structure = "bot"

        
        self.raw_image = pygame.image.load("./assets/bot.png")
        self.image = pygame.transform.rotate(self.raw_image, 0)

        self.x = x
        self.y = y

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hit_box = CollisionBox(self.x, self.y, self.width, self.height)

        self.rotated_image = None

    def draw(self, screen):

        screen.blit(self.image, (self.x, self.y))
