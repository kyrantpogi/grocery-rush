import pygame
pygame.init()

from CollisionBox import CollisionBox


class Wall:
    def __init__(self, x, y, width, height):
        self.structure = "wall"

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hit_box = CollisionBox(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        self.hit_box.x = self.x
        self.hit_box.y = self.y

