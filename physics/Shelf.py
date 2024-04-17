import pygame
pygame.init()

from CollisionBox import CollisionBox
from DialogBox import DialogBox


class Shelf:
	def __init__(self, type_, x, y, items=[]):
		self.structure = "shelf"

		self.types = {
			"basic": {
				"width": 200,
				"height": 300,
				"inner-width": 104,
				"inner-height": 220,
				"images": [
					pygame.image.load("./assets/shelves/basic-shelf.png").convert_alpha()
				]
			},
			"vegetable": {
				"width": 200,
				"height": 150,
				"inner-width": 150,
				"inner-height": 73,
				"images": [
					pygame.image.load("./assets/shelves/vegetable-rack.png").convert_alpha()
				]
			},
			"freezer": {
				"width": 260,
				"height": 270,
				"inner-width": 192,
				"inner-height": 150,
				"images": [
					pygame.image.load("./assets/shelves/ice-freezer.png").convert_alpha()
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

		self.open_text = DialogBox("E", self.hit_box_inner.x, self.hit_box_inner.y, 33, 40, size=16)
		self.open_text.text_image.color = "#ffffff"
		self.open_text_is_open = False

		self.shelf_items_text = DialogBox("Shelf Items: ", 299.5, 174.5, 600, 350, 20)
		self.list_to_display = []
		self.show_item_dialog = False

	def is_player_in_hover(self, player):
		if player.hit_box.check_hit(self.hit_box.x, self.hit_box.y, self.hit_box.width, self.hit_box.height):
			self.open_text_is_open = True
			return True

		self.open_text_is_open = False
		return False

	def draw(self, screen):
		self.hit_box.x = self.x
		self.hit_box.y = self.y
		# self.hit_box.draw(screen)

		self.hit_box_inner.x = self.x + ((self.types[self.type]["width"] - self.types[self.type]["inner-width"]) / 2)
		self.hit_box_inner.y = self.y + ((self.types[self.type]["height"] - self.types[self.type]["inner-height"]) / 2)

		self.open_text.x = self.hit_box_inner.x
		self.open_text.y = self.hit_box_inner.y

		if self.index == len(self.types[self.type]["images"]):
			self.index = 0

		screen.blit(self.types[self.type]["images"][self.index], (self.x, self.y))
		if self.open_text_is_open:
			self.open_text.draw(screen)


		self.index += 1

		