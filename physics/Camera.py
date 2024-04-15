import pygame
pygame.init()

class Camera:
	def __init__(self, player, x, y, width, height, vel, sprite_list=[]):
		self.player = player

		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.vel = vel

		self.sprite_list = sprite_list

	def draw_camera(self, screen):
		pygame.draw.rect(screen, "#000000", (self.x, self.y, self.width, self.height), 2)

	def update_pos(self, face):
		for sprite in self.sprite_list:
			if face == "up":
				sprite.y += self.vel
			elif face == "down":
				sprite.y -= self.vel
			elif face == "left":
				sprite.x += self.vel
			elif face == "right":
				sprite.x -= self.vel
