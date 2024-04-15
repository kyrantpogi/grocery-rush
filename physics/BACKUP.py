import pygame
import sys
import random
import os
import math
import time
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("100")

def print_clear(text):
	os.system("cls")
	print(text)

def random_hex():
	acceptable_code = "abcdefABCDEF0123456789"
	output = "#"

	for x in range(0, 6):
		output += acceptable_code[random.randrange(0, len(acceptable_code) - 1)]

	return output

class DisplayText:
	def __init__(self, text, x=0, y=0, size=20, color="#ffffff"):
		self.text = text
		self.x = x
		self.y = y
		self.size = size
		self. color = color
		self.font = pygame.font.Font("./font/PirataOne-Regular.ttf", self.size)
		
		self.type_letter = 0
		self.type_fps = 0
		self.cutscene_text = ""

		self.multiline_index = 0

		self.global_lines = self.__get_lines(self.text)
		print(self.global_lines)

		self.final_lines = []

		self.is_done = False

	def draw_text(self, screen):
		text_prop = self.font.render(str(self.text), True, self.color)
		screen.blit(text_prop, (self.x, self.y))

	def draw_text_center(self, screen):
		text_prop = self.font.render(str(self.text), True, self.color)
		text_rect = text_prop.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) #get rect to center
		screen.blit(text_prop, text_rect)

	#DISPLAY MULTILINE TEXT
	def multiline_text(self, screen):
		words = self.text.split()
		line = ""
		lines = []

		#each line has 10 words, get the remainder to still add the missing words
		for i in range(0, len(words)):
			line += words[i] + " "
			if len(line.split()) == 10:
				lines.append(line)
				line = " "
		#reset
		line = ""

		#FOR THE REMAINDER
		remainder = len(words) % 10
		for i in range(len(words) - remainder, len(words)): # count backwards
			line += words[i] + " "

		lines.append(line)
		line = ""

			
			

		#render lines
		for i in range(0, len(lines)):
			text = self.font.render(lines[len(lines)-1-i], True, self.color)
			text_width, text_height = text.get_size()
			text_rect = text.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - (text_height * i))) #get rect to center

			screen.blit(text, text_rect)

	#=============================================================FUNCTIONS USED FOR MULTILINE CUTSCENE TEXT================================================
	#PRIVATE FUNCTION RETURN LIST ONLY
	def __get_lines(self, text):
		words = self.text.split()
		line = ""
		lines = []

		#each line has 10 words, get the remainder to still add the missing words
		for i in range(0, len(words)):
			line += words[i] + " "
			if len(line.split()) == 10:
				lines.append(line)
				line = " "
		#reset
		line = ""

		#FOR THE REMAINDER
		remainder = len(words) % 10
		for i in range(len(words) - remainder, len(words)): # count backwards
			line += words[i] + " "

		lines.append(line)
		line = ""

		return lines

	def multiline_text_for_typewriter(self, screen, lines):
		#render lines
		for i in range(0, len(lines)):
			text = self.font.render(lines[len(lines)-1-i], True, self.color)
			text_width, text_height = text.get_size()
			text_rect = text.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - (text_height * (i+1)))) #get rect to center

			screen.blit(text, text_rect)

	def typewriter(self, screen):

		try:
			line_is_done = self.__inner_cutscene(screen, self.global_lines[self.multiline_index], self.multiline_index)
		except:
			self.multiline_text_for_typewriter(screen, self.final_lines)
			return True
		
		if line_is_done:
			print(self.multiline_index)
			self.final_lines.append(self.global_lines[self.multiline_index])
			if self.multiline_index < len(self.global_lines):
				self.multiline_index += 1
				self.type_letter = 0
				self.cutscene_text = ""

		if len(self.final_lines) > 0:
			self.multiline_text_for_typewriter(screen, self.final_lines)
		
		

	def __inner_cutscene(self, screen, text, index):
		if self.type_fps % 6 == 0:
			if self.type_letter == len(text):
				text_prop = self.font.render(str(self.cutscene_text), True, self.color)
				text_width, text_height = text_prop.get_size()
				text_rect = text_prop.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT/2) - (text_height * index))) #get rect to center
				screen.blit(text_prop, text_rect)
				return True #do not overflow

			
			self.cutscene_text += text[self.type_letter]
			self.type_letter += 1
			self.type_fps = 0

		text_prop = self.font.render(str(self.cutscene_text), True, self.color)
		text_rect = text_prop.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) #get rect to center
		screen.blit(text_prop, text_rect)

		self.type_fps += 1

	#=============================================================FUNCTIONS USED FOR MULTILINE CUTSCENE TEXT================================================

	def cutscene_text_draw(self, screen):
		if self.type_fps % 4 == 0:
			if self.type_letter == len(self.text):
				text_prop = self.font.render(str(self.cutscene_text), True, self.color)
				text_rect = text_prop.get_rect(center=(SCREEN_WIDTH/2, self.y)) #get rect to center
				screen.blit(text_prop, text_rect)
				return #do not overflow

			
			self.cutscene_text += self.text[self.type_letter]
			self.type_letter += 1
			self.type_fps = 0

		text_prop = self.font.render(str(self.cutscene_text), True, self.color)
		text_rect = text_prop.get_rect(center=(SCREEN_WIDTH/2, self.y)) #get rect to center
		screen.blit(text_prop, text_rect)

		self.type_fps += 1
		
class GameStateManager:
	def __init__(self, first_state):

		self.start = StartScreen()
		self.game = GamePrototype()
		

		self.states = {
			"start-menu": self.start,
			"game": self.game
		}

		self.current_state = first_state

	def set_game_state(self, state):
		self.current_state = state

	def get_game_state(self):
		return self.current_state

class Button:
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def click(self, screen):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action

class StartScreen:
	def __init__(self):
		self.bg = "#000000"
		self.welcome_text = DisplayText("PesoRush: Juan's Hundred-Second Shopping Spree",y=200, size=55, color="#ffffff")

		self.play_btn = Button(348, 400, pygame.image.load("./assets/Buttons/play.png"), 1)
		self.mechanics_btn = Button(552, 400, pygame.image.load("./assets/Buttons/mechanics.png"), 1)
		self.exit_btn = Button(756, 400, pygame.image.load("./assets/Buttons/exit.png"), 1)

	def run(self, screen, game_state):
		screen.fill(self.bg)
		keys = pygame.key.get_pressed()

		self.welcome_text.cutscene_text_draw(screen)

		if self.play_btn.click(screen):
			game_state.set_game_state("game")
		if self.mechanics_btn.click(screen):
			game_state.set_game_state("mechanics")
		if self.exit_btn.click(screen):
			pygame.quit()
			sys.exit()
		
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

class DialogBox:
	def __init__(self, text, x, y, width, height):
		self.text_image = DisplayText(text, x+10, y+10, 20)

		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def draw(self, screen):
		pygame.draw.rect(screen, "#000000", (self.x, self.y, self.width, self.height))
		self.text_image.draw_text(screen)

	def page(self):
		pass

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

		self.hit_box = CollisionBox(0, 0, 75, 47)

		self.fps_counter = 0
		self.walking_animation_fps = 0

		self.last_x = 0
		self.last_y = 0

	def rotate(self, image, targetx, targety):
		self.targetx = targetx
		self.targety = targety
		self.angle = (180/math.pi) * -math.atan2((self.targety-self.y),(self.targetx-self.x))
		img_copy = image
		return pygame.transform.rotozoom(img_copy, int(self.angle-90), 1)

	def draw(self, screen, targetx, targety):
		self.fps_counter += 1
		self.walking_animation_fps += 1

		if self.fps_counter % 60 == 0:
			self.health -= 1
			self.fps_counter = 0

		if self.walking_animation_fps == len(self.images):
			self.walking_animation_fps = 0

		#check if idle or walking to show / stop animation
		if self.last_x == self.x and self.last_y == self.y:
			rotated_image = self.rotate(self.images[0], targetx, targety)
			screen.blit(rotated_image, (self.x - (rotated_image.get_width() / 2), self.y - (rotated_image.get_height() / 2)))
		else:
			rotated_image = self.rotate(self.images[self.walking_animation_fps], targetx, targety)
			screen.blit(rotated_image, (self.x - (rotated_image.get_width() / 2), self.y - (rotated_image.get_height() / 2)))


		self.last_x = self.x
		self.last_y = self.y

		pygame.draw.rect(screen, self.health_bar_color, (SCREEN_WIDTH - 110, 10, self.health, 10)) #health bar
		pygame.draw.rect(screen, "#ffffff", (SCREEN_WIDTH - 110, 9, 101, 10+1), 3) #BACKGROUND
  
  
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

class Item:
	def __init__(self, brand, type_, price, image_destination,):
		
		self.brand = brand
		self.type = type_
		self.price = price

		self.image_destination = image_destination
		self.raw_image = pygame.image.load(self.image_destination).convert_alpha()
		self.image = pygame.transform.scale(self.raw_image, (int(self.raw_image.get_width() * 1), int(self.raw_image.get_height() * 1)))

		self.is_equipped = False #CHECK if equiped on player's inventory
		self.btn = Button(100, 100, self.image, 1)

	def click(self, screen, pos):
		self.btn.rect.topleft = pos
		if self.btn.click(screen):
			return True

class Shelf:
	def __init__(self, type_, x, y, items=[]):

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
		self.hit_box.draw(screen)

		self.hit_box_inner.x = self.x + ((self.types[self.type]["width"] - self.types[self.type]["inner-width"]) / 2)
		self.hit_box_inner.y = self.y + ((self.types[self.type]["height"] - self.types[self.type]["inner-height"]) / 2)

		if self.index == len(self.types[self.type]["images"]):
			self.index = 0

		screen.blit(self.types[self.type]["images"][self.index], (self.x, self.y))
		self.index += 1
		
class Cashier:
	def __init__(self):
		pass

	def check_status(self):
		pass

	def draw(self, screen):
		pass

class GamePrototype:
	def __init__(self):
		self.shelf1_items = [
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
			Item("A", "milk", 29, "./assets/milk.png"),
		]

		self.shelf2_items = [
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
			Item("A", "coffee", 29, "./assets/coffee.png"),
		]

		self.shelf1 = Shelf("basic", 394, 270, self.shelf1_items)
		self.shelf2 = Shelf("basic", 637, 270, self.shelf2_items)
		self.shelf3 = Shelf("basic", 900, 270)

		self.shelf4 = Shelf("vegetable", 403, 0)
		self.shelf5 = Shelf("vegetable", 637, 0)
		self.shelf6 = Shelf("vegetable", 871, 0)

		self.shelf7 = Shelf("freezer", 322, 595)
		self.shelf8 = Shelf("freezer", 627, 595)
		self.shelf9 = Shelf("freezer", 957, 595)

		self.player = Player(0, 0, "#D2042D")
		self.player_velocity = 3

		self.camera = Camera(self.player, (SCREEN_WIDTH/2) - 150, (SCREEN_HEIGHT/2) - 150, 300, 300, 3)
		self.camera.sprite_list = [self.shelf1, self.shelf2, self.shelf3, self.shelf4, self.shelf5, self.shelf6, self.shelf7, self.shelf8, self.shelf9]


		self.background = pygame.image.load("./assets/bg-1440-2.png").convert()
		self.background_x = 0
		self.background_y = 0
		self.background_width = self.background.get_width()
		self.background_height = self.background.get_height()

		self.touch_other_objects = False

		self.fps_counter = 0

		
		self.player_inventory = DialogBox("?", 0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50)
		self.shelf_items_text = DialogBox("Shelf Items: ", 0, 0, SCREEN_WIDTH, 50)
		self.list_to_display_pos_inventory = [
			(237, 645),
			(326, 645),
			(415, 645),
			(504, 645),
			(593, 645),
			(682, 645),
			(771, 645),
			(860, 645),
			(949, 645)
		]
		self.list_to_display_pos = [
			(237, 0),
			(326, 0),
			(415, 0),
			(504, 0),
			(593, 0),
			(682, 0),
			(771, 0),
			(860, 0),
			(949, 0)
		]
		self.list_to_display = []
		self.show_item_dialog = False
		
		self.cutscene = False
		self.cutscene_text = DisplayText("Your mother told you to buy her some eggs and tomatoes.========================= ==========================Sinabi ng nanay mo na bumili ka ng mga itlog at kamatis.                            ", color="#ffffff")

		self.current_shelf = ""

	def run(self, screen, game_state):
		if self.cutscene:
			screen.fill("#000000")
			is_done = self.cutscene_text.typewriter(screen)
			
			if is_done:
				self.cutscene = False

		else: #start game

			screen.blit(self.background, (self.background_x,self.background_y)) #draw background
			
			keys = pygame.key.get_pressed()
			if keys[pygame.K_w]:
				if not self.background_y >= 0:
					self.background_y += self.player_velocity
					self.camera.update_pos("up")	
				if not self.player.y <= 0:
					self.player.y -= self.player_velocity
			if keys[pygame.K_s]:
				if not self.background_y + self.background_height <= SCREEN_HEIGHT - 50:
					self.background_y -= self.player_velocity
					self.camera.update_pos("down")	
				if not self.player.y >= SCREEN_HEIGHT - 50:
					self.player.y += self.player_velocity
			if keys[pygame.K_a]:
				if not self.background_x >= 0:
					self.background_x += self.player_velocity
					self.camera.update_pos("left")			
				if not self.player.x <= 0:
					self.player.x -= self.player_velocity
			if keys[pygame.K_d]:
				if not self.background_x + self.background_width <= SCREEN_WIDTH:
					self.background_x -= self.player_velocity
					self.camera.update_pos("right")			
				if not self.player.x >= SCREEN_WIDTH:
					self.player.x += self.player_velocity

			#EQUIP DEQUIP KEYS




			mouseX, mouseY = pygame.mouse.get_pos()

			self.player.draw(screen, mouseX, mouseY)

			#for collissions
			for shelf in self.camera.sprite_list:
				phb = self.player.hit_box
				shb = shelf.hit_box_inner
				hhb = shelf.hit_box

				if phb.check_hit(shb.x, shb.y, shb.width, shb.height):
					self.player_velocity = 0.05
					self.camera.vel = 0.05
					break
				else:
					self.player_velocity = 3
					self.camera.vel = 3

				#SHOW ITEMS IN DIALOG BOX
				if phb.check_hit(hhb.x, hhb.y, hhb.width, hhb.height):
					self.list_to_display = shelf.items
					self.show_item_dialog = True
					self.current_shelf = shelf
					break
				else:
					self.current_shelf = shelf
					self.show_item_dialog = False
				

			for shelf in self.camera.sprite_list:
				shelf.draw(screen)


			self.player_inventory.text_image.text = "INVENTORY: "
			self.player_inventory.draw(screen)
			for i in range(0, len(self.player.inventory)):
				item = self.player.inventory[i]
				if item.click(screen, self.list_to_display_pos_inventory[i]):
					if item.is_equipped:
						self.player.inventory.pop(i)
						print(self.player.inventory)
						break
				

			
			if self.show_item_dialog:
				self.shelf_items_text.draw(screen)
				for i in range(0, len(self.list_to_display)):
					item = self.list_to_display[i]
				
					if item.click(screen, self.list_to_display_pos[i]):
						if not item.is_equipped:
							item.is_equipped = True
							self.player.inventory.append(item)
							break;
						
							
		


#==========================================MAIN LOOP===========================================

if __name__ == "__main__":
	

	fps_text = DisplayText("?", 10, 10, 20, random_hex())
	show_fps = False

	game_state_manager = GameStateManager("game")

	
	

	clock = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			
		game_state_manager.states[game_state_manager.get_game_state()].run(screen, game_state_manager)
		if show_fps:
			fps = int(clock.get_fps())
			fps_text.text = "FPS- " + str(fps)
			fps_text.color = random_hex()
			fps_text.draw_text(screen)

		
		clock.tick(60)
		pygame.display.flip()


	pygame.quit()
	sys.exit()






