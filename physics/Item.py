import pygame
import random
pygame.init()

from Button import Button

def random_hex():
	acceptable_code = "abcdefABCDEF0123456789"
	output = "#"

	for x in range(0, 6):
		output += acceptable_code[random.randrange(0, len(acceptable_code) - 1)]

	return output

class Item:
	def __init__(self, brand, price, image_destination):
		
		self.brand = brand
		self.price = price

		self.uuid = random_hex()

		self.image_destination = image_destination
		self.raw_image = pygame.image.load(self.image_destination).convert_alpha()
		self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * 1), int(self.raw_image.get_height() * 1)))

		self.raw_x_image = pygame.image.load("./assets/Bag.png").convert_alpha()
		self.x_image = pygame.transform.scale(self.raw_x_image, (int(self.raw_image.get_width() * 0.3), int(self.raw_image.get_height() * 0.3)))

		self.is_equipped = False #CHECK if equiped on player's inventory
		self.btn = Button(100, 100, self.image, 1)

	def click(self, screen, pos):
		self.btn.rect.topleft = pos

		if self.btn.click(screen):
			return True

		if self.is_equipped:
			screen.blit(self.x_image, (self.btn.rect.x, self.btn.rect.y))