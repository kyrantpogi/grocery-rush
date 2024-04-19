import pygame
import math
import random
pygame.init()

from CollisionBox import CollisionBox

VIRTUAL_SCREEN_WIDTH = 1200
VIRTUAL_SCREEN_HEIGHT = 700

class Mosquito:
    def __init__(self, x, y):
        self.structure = "mosquito"
        
        self.images = [
            pygame.image.load("./assets/mosquito/1.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/2.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/3.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/4.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/5.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/6.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/7.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/8.png").convert_alpha(),
            pygame.image.load("./assets/mosquito/9.png").convert_alpha()
        ]
        
        self.image_index = 0

        self.x = x
        self.y = y

        self.hit_box = CollisionBox(self.x, self.y, 44,38)

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
        if self.image_index == len(self.images):
            self.image_index = 0

        #if hit change_loc_hit_box change location
        if self.hit_box.check_hit(self.change_loc_hit_box.x, self.change_loc_hit_box.y, self.change_loc_hit_box.width, self.change_loc_hit_box.height) or self.vel_x == 0 and self.vel_y == 0:
            self.change_loc_hit_box.x = random.randrange(10, VIRTUAL_SCREEN_WIDTH - 50)
            self.change_loc_hit_box.y = random.randrange(10, VIRTUAL_SCREEN_HEIGHT - 50)

            run = (self.change_loc_hit_box.x - self.x)
            rise = (self.change_loc_hit_box.y - self.y)

            angle = math.atan2(run, rise)
            self.vel_x = math.sin(angle) * 5
            self.vel_y = math.cos(angle) * 5
            self.rotated_image = self.rotate(self.images[self.image_index], self.change_loc_hit_box.x, self.change_loc_hit_box.y)
        else:
            self.rotated_image = self.rotate(self.images[self.image_index], self.change_loc_hit_box.x, self.change_loc_hit_box.y)
           

        self.x += self.vel_x
        self.y += self.vel_y

        self.hit_box.x = self.x - (self.rotated_image.get_width() / 2)
        self.hit_box.y = self.y - (self.rotated_image.get_height() / 2)
        screen.blit(self.rotated_image, (self.x - (self.rotated_image.get_width() / 2), self.y - (self.rotated_image.get_height() / 2)))

        self.image_index += 1

