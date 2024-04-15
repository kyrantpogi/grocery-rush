import pygame
pygame.init()

from CollisionBox import CollisionBox


class Shelf:
	def __init__(self, type_, x, y, items=[]):
		self.structure = "shelf"

		self.types = {
			"basic": {
				"width": 192,
				"height": 192,
				"inner-width": 104,
				"inner-height": 192,
				"images": [
					pygame.image.load("./assets/shelves/basic-shelf.png").convert_alpha()
				]
			},
			"vegetable": {
				"width": 216,
				"height": 160,
				"inner-width": 182,
				"inner-height": 73,
				"images": [
					pygame.image.load("./assets/shelves/vegetable-rack.png").convert_alpha()
				]
			},
			"freezer": {
				"width": 220,
				"height": 220,
				"inner-width": 192,
				"inner-height": 114,
				"images": [
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_00.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_01.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_02.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_03.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_04.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_05.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_06.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_07.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_08.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_09.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_10.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_11.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_12.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_13.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_14.png").convert_alpha(),
					pygame.image.load("./assets/shelves/Ice_Freezer/2xFrames_15.png").convert_alpha(),
				]
			}
		}

		self.x = x
		self.y = y
		

		self.type = type_

		self.items = items

		self.index = 0

		#item hover only
		self.hit_box = CollisionBox(self.x, self.y, self.types[self.type]["width"], self.types[self.type]["height"])

		#SLOW PLAYER WHEN HE HITS THE ACTUAL SHELF
		self.inner_x = self.x + ((self.types[self.type]["width"] - self.types[self.type]["inner-width"]) / 2)
		self.inner_y = self.y + ((self.types[self.type]["height"] - self.types[self.type]["inner-height"]) / 2)
		self.hit_box_inner = CollisionBox(self.inner_x, self.inner_y, self.types[self.type]["inner-width"], self.types[self.type]["inner-height"])		

	def draw(self, screen):
		self.hit_box.x = self.x
		self.hit_box.y = self.y

		self.hit_box_inner.x = self.x + ((self.types[self.type]["width"] - self.types[self.type]["inner-width"]) / 2)
		self.hit_box_inner.y = self.y + ((self.types[self.type]["height"] - self.types[self.type]["inner-height"]) / 2)

		if self.index == len(self.types[self.type]["images"]):
			self.index = 0

		screen.blit(self.types[self.type]["images"][self.index], (self.x, self.y))
		self.index += 1