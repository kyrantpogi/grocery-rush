import pygame
import math
pygame.init()

from CollisionBox import CollisionBox

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

class Player:
	def __init__(self, x, y, health_bar_color="#1BE830"):
		self.x = x
		self.y = y
		self.money = 100
		self.health = 100
		self.health_bar_color = health_bar_color
		self.show_hit_box = False
		self.inventory = []
		

		self.images = [pygame.image.load("./assets/playerv2/sprite_00.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_01.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_02.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_03.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_04.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_05.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_06.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_07.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_08.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_09.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_10.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_11.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_12.png").convert_alpha(),
						pygame.image.load("./assets/playerv2/sprite_13.png").convert_alpha(),
		]

		self.hit_box = CollisionBox(self.x, self.y, 75, 47)

		self.fps_counter = 0
		self.walking_animation_fps = 0

		self.last_x = 0
		self.last_y = 0

		self.vel_x = 0
		self.vel_y = 0

		self.is_moving = False

		self.angle = 0

	def rotate(self, image, targetx, targety):
		self.targetx = targetx
		self.targety = targety
		self.angle = (180/math.pi) * -math.atan2((self.targety-self.y),(self.targetx-self.x))
		img_copy = image
		return pygame.transform.rotozoom(img_copy, int(self.angle-90), 1)

	def move(self, vel_x, vel_y):
		self.vel_x = vel_x
		self.vel_y = vel_y

		self.x += self.vel_x
		self.y += self.vel_y

	def draw(self, screen, targetx, targety):
		self.fps_counter += 1
		self.walking_animation_fps += 1

		if self.fps_counter % 60 == 0:
			self.health -= 1
			self.fps_counter = 0

		if self.walking_animation_fps == len(self.images):
			self.walking_animation_fps = 0

		mouse_x, mouse_y = pygame.mouse.get_pos()

		#check if idle or walking to show / stop animation
		if self.last_x == self.x and self.last_y == self.y:
			rotated_image = self.rotate(self.images[0], mouse_x, mouse_y)
			screen.blit(rotated_image, (self.x - (rotated_image.get_width() / 2), self.y - (rotated_image.get_height() / 2)))
		else:
			if self.is_moving:
				rotated_image = self.rotate(self.images[self.walking_animation_fps], targetx, targety)
				screen.blit(rotated_image, (self.x - (rotated_image.get_width() / 2), self.y - (rotated_image.get_height() / 2)))
			else:
				rotated_image = self.rotate(self.images[0], mouse_x, mouse_y)
				screen.blit(rotated_image, (self.x - (rotated_image.get_width() / 2), self.y - (rotated_image.get_height() / 2)))

		self.last_x = self.x
		self.last_y = self.y
    
		#change hitbox pos and dimensions according to mouse angle(rotation)
		if self.angle > 45 and self.angle < 135:
			self.hit_box.x = self.x - 25
			self.hit_box.y = self.y - 35
			self.hit_box.width = 53
			self.hit_box.height = 85

		if self.angle < 45 and self.angle > -45:
			self.hit_box.x = self.x - 40
			self.hit_box.y = self.y - 23
			self.hit_box.width = 75
			self.hit_box.height = 47

		if self.angle < -45 and self.angle > -135:
			self.hit_box.x = self.x - 25
			self.hit_box.y = self.y - 50
			self.hit_box.width = 53
			self.hit_box.height = 85

		if self.angle < -135 or self.angle > 135:
			self.hit_box.x = self.x - 30
			self.hit_box.y = self.y - 23
			self.hit_box.width = 75
			self.hit_box.height = 47

		if self.show_hit_box:
			self.hit_box.draw(screen)