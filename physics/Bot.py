import pygame
import math
import random
pygame.init()

from CollisionBox import CollisionBox

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

class Bot:
    def __init__(self, x, y, face):
        self.structure = "bot"
        
        self.image = pygame.image.load("./assets/bot.png")

        self.x = x
        self.y = y

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.hit_box = CollisionBox(self.x, self.y, self.width, self.height)

        self.change_loc_hit_box = CollisionBox(self.x, self.y, 20, 20)

        self.target_x = 0
        self.target_y = 0

        self.vel_x = 0
        self.vel_y = 0

        self.rotated_image = None

    def rotate(self, image, targetx, targety):
	    self.targetx = targetx
	    self.targety = targety
	    self.angle = (180/math.pi) * -math.atan2((self.targety-self.y),(self.targetx-self.x))
	    img_copy = image
	    return pygame.transform.rotozoom(img_copy, int(self.angle-90), 1)

    def draw(self, screen):
        self.hit_box.x = self.x - (self.width / 2)
        self.hit_box.y = self.y - (self.height / 2)

        #if hit change_loc_hit_box change location
        if self.hit_box.check_hit(self.change_loc_hit_box.x, self.change_loc_hit_box.y, self.change_loc_hit_box.width, self.change_loc_hit_box.height) or self.vel_x == 0 and self.vel_y == 0:
            self.change_loc_hit_box.x = random.randrange(100, SCREEN_WIDTH - 100)
            self.change_loc_hit_box.y = random.randrange(100, SCREEN_HEIGHT - 100)

            run = (self.change_loc_hit_box.x - self.x)
            rise = (self.change_loc_hit_box.y - self.y)

            angle = math.atan2(run, rise)
            self.vel_x = math.sin(angle) * 1.2
            self.vel_y = math.cos(angle) * 1.2

            self.rotated_image = self.rotate(self.image, self.change_loc_hit_box.x, self.change_loc_hit_box.y)

        self.x += self.vel_x
        self.y += self.vel_y

        screen.blit(self.rotated_image, (self.x - (self.rotated_image.get_width() / 2), self.y - (self.rotated_image.get_height() / 2)))
        
