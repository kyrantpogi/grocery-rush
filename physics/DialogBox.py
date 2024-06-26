import pygame
pygame.init()

from DisplayText import DisplayText

class DialogBox:
	def __init__(self, text, x, y, width, height, size=20):
		self.text_image = DisplayText(text, x+10, y+10, 15)

		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self, screen):
		pygame.draw.rect(screen, "#000000", (self.x, self.y, self.width, self.height))

		self.text_image.x = self.x + 10
		self.text_image.y = self.y + 10

		self.text_image.draw_text(screen)
