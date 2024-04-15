import pygame
pygame.init()

class CollisionBox:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self, screen):
		pygame.draw.rect(screen, "#ffffff", (self.x, self.y, self.width, self.height), 3)

	def check_hit(self, x2, y2, w2, h2):
		if (self.x + self.width >= x2
			and self.x <= x2 + w2
			and self.y + self.height >= y2
			and self.y <= y2 + h2):
			return True