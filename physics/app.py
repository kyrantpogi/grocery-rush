import pygame
import sys
import random
import os
import math
import time
import json

from DisplayText import DisplayText
from Button import Button
from CollisionBox import CollisionBox
from DialogBox import DialogBox
from Camera import Camera
from Player import Player
from Item import Item
from Shelf import Shelf
from Cashier import Cashier
from Bot import Bot
from Puddle import Puddle

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("100")

running = True

def print_clear(text):
	os.system("cls")
	print(text)

def random_hex():
	acceptable_code = "abcdefABCDEF0123456789"
	output = "#"

	for x in range(0, 6):
		output += acceptable_code[random.randrange(0, len(acceptable_code) - 1)]

	return output

def load_JSON(file):
	file = open(f"""./saves/{file}""", "r")
	return json.loads(file.read())
		
class GameStateManager:
	def __init__(self, first_state):

		self.start = StartScreen()
		self.game = GamePrototype()
		self.decider_screen = DeciderScreen()
		

		self.states = {
			"start-menu": self.start,
			"game": self.game,
			"decider-screen": self.decider_screen
		}

		self.current_state = first_state

	def set_game_state(self, state):
		self.current_state = state

	def get_game_state(self):
		return self.current_state

	def win_or_lose(self, winner=False):
		self.decider_screen.win = winner 

	def reset_level(self):
		self.game.__init__()

class StartScreen:
	def __init__(self):
		self.bg = "#000000"
		self.welcome_text = DisplayText("Grocery Rush",y=200, size=30, color="#ffffff")

		self.play_btn = Button(348, 400, pygame.image.load("./assets/Buttons/play.png"), 1)
		self.mechanics_btn = Button(552, 400, pygame.image.load("./assets/Buttons/mechanics.png"), 1)
		self.exit_btn = Button(756, 400, pygame.image.load("./assets/Buttons/exit.png"), 1)

	def run(self, screen, game_state):
		global running
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 3:
					print("clicked")

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
		
class DeciderScreen:
	def __init__(self, win=False):
		self.win = False

		self.text = DisplayText("?", 0, 0, 35)

		self.winner_sound = pygame.mixer.Sound("./music/winner.mp3")
		self.loser_sound = pygame.mixer.Sound("./music/bsod.mp3")

		self.play_music = True

	def run(self, screen, game_state):
		global running
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 3:
					print("clicked")

		screen.fill("#000000")

		keys = pygame.key.get_pressed()

		if keys[pygame.K_p]:
			game_state.reset_level()
			game_state.set_game_state("game")
			return

		if self.win:
			if self.play_music:
				# self.winner_sound.play()
				self.play_music = False
			self.text.text = "CONGRATULATIONS!"
			self.text.draw_text_center(screen)

		else:
			if self.play_music:
				# self.loser_sound.play()
				self.play_music = False
			self.text.text = "TRY AGAIN!"
			self.text.draw_text_center(screen)

class GamePrototype:
	def __init__(self):
		self.typing_sound = pygame.mixer.Sound("./music/typingsound.mp3")
		#load level
		self.vegetable_items = load_JSON("vegetable.json")
		self.frozen_items = load_JSON("frozen.json")
		self.shelf_items = load_JSON("shelf.json")

		self.levels = load_JSON("levels.json")

		self.level = None

		for level in self.levels:
			if level["done"] == "no":
				self.level = level
				break

		self.requirements_to_win = self.level["requirements"]

		#player
		self.player = Player(300, 131, "#D2042D")
		self.player_velocity = 3

		#cashier 
		self.cashier = Cashier(-7, 131)

		#FIXED VARIABLES
		self.camera = Camera(self.player, (SCREEN_WIDTH/2) - 150, (SCREEN_HEIGHT/2) - 150, 300, 300, 3)
		self.camera.sprite_list = [self.cashier]

		self.background = pygame.image.load("./assets/bg-1440-2.png").convert()
		self.background_x = 0
		self.background_y = 0
		self.background_width = self.background.get_width()
		self.background_height = self.background.get_height()

		#load bots
		for bot in self.level["bots"]:
			faces = ["up", "down", "left", "right"]
			b = Bot(bot["x"], bot["y"], faces[random.randrange(0, len(faces))])
			self.camera.sprite_list.append(b)

		self.shelf_list = []

		#load shelves
		for prop in self.level["shelves"]:
			shelf_items = []

			if prop["type"] == "freezer":
				for i in range(0, 18):
					item = self.frozen_items["items"][random.randrange(0, len(self.frozen_items["items"]))]
					product = Item(item["name"], item["price"], item["image"])
					shelf_items.append(product)

			if prop["type"] == "vegetable":
				for i in range(0, 18):
					item = self.vegetable_items["items"][random.randrange(0, len(self.vegetable_items["items"]))]
					product = Item(item["name"], item["price"], item["image"])
					shelf_items.append(product)
			
			if prop["type"] == "basic":
				for i in range(0, 18):
					item = self.shelf_items["items"][random.randrange(0, len(self.shelf_items["items"]))]
					product = Item(item["name"], item["price"], item["image"])
					shelf_items.append(product)

			shelf = Shelf(prop["type"], prop["x"], prop["y"], shelf_items)
			self.shelf_list.append(shelf)
			self.camera.sprite_list.append(shelf)

		#load puddles
		for puddle in self.level["puddles"]:
			p = Puddle(puddle["x"], puddle["y"])
			self.camera.sprite_list.append(p)

		self.player_inventory = DialogBox("?", 0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50, 20)
		self.shelf_items_text = DialogBox("Shelf Items: ", 299.5, 174.5, 600, 350, 20)
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
			(334, 249),
			(431, 249),
			(528, 249),
			(625, 249),
			(722, 249),
			(819, 249),
			(334, 339),
			(431, 339),
			(528, 339),
			(625, 339),
			(722, 339),
			(819, 339),
			(334, 429),
			(431, 429),
			(528, 429),
			(625, 429),
			(722, 429),
			(819, 429)
		]
		self.list_to_display = []
		self.show_item_dialog = False
		
		self.cutscene = True
		self.cutscene_text = DisplayText(self.level["cutscene-text"], size=14,color="#ffffff")

		self.current_shelf = ""

		self.index_to_remove = 0
		self.remove_item_from_inventory = False

		self.vel_x = 0
		self.vel_y = 0

		self.target_x = 0
		self.target_y = 0

		self.mouse_rect = CollisionBox(0, 0, 10, 10)

		self.show_item_dialog_2 = False
	
	def show_timer(self):
		pygame.draw.rect(screen, self.player.health_bar_color, (SCREEN_WIDTH - 110, 10, self.player.health, 10)) #health bar
		pygame.draw.rect(screen, "#ffffff", (SCREEN_WIDTH - 110, 9, 101, 10+1), 3) #BACKGROUND
	

	def run(self, screen, game_state):
		global running
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 3:
					if not self.show_item_dialog_2:
						self.target_x, self.target_y = pygame.mouse.get_pos()


						run = (self.target_x - self.player.x)
						rise = (self.target_y - self.player.y)

						angle = math.atan2(run, rise)

						self.vel_x = math.sin(angle) * 3.4
						self.vel_y = math.cos(angle) * 3.4

						self.mouse_rect.x = self.target_x
						self.mouse_rect.y = self.target_y

						self.player.is_moving = True

				if event.button == 1:
					print("LEFT CLICK")
					self.player.is_moving = False
					self.vel_x = 0
					self.vel_y = 0

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_e:
					print(self.show_item_dialog)
					if self.show_item_dialog:
						self.show_item_dialog_2 = not self.show_item_dialog_2
						print("go")
						

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					#search through bots
					for structure in self.camera.sprite_list:
						if structure.structure == "bot":
							structure.vel_x = 0
							structure.vel_y = 0
				if event.key == pygame.K_s:
					for structure in self.camera.sprite_list:
						if structure.structure == "bot":
							structure.vel_x = 0
							structure.vel_y = 0
				if event.key == pygame.K_a:
					#search through bots
					for structure in self.camera.sprite_list:
						if structure.structure == "bot":
							structure.vel_x = 0
							structure.vel_y = 0
				if event.key == pygame.K_d:
					for structure in self.camera.sprite_list:
						if structure.structure == "bot":
							structure.vel_x = 0
							structure.vel_y = 0
	
		if self.cutscene:
			screen.fill("#000000")
			# self.typing_sound.play()
			is_done = self.cutscene_text.typewriter(screen)
			
			
			if is_done:
				print("done")
				self.cutscene = False

		else: #start game

			screen.blit(self.background, (self.background_x,self.background_y)) #draw background
			
			keys = pygame.key.get_pressed()

			if not self.show_item_dialog_2:
				if keys[pygame.K_w]:
					if not self.background_y >= 0:
						self.background_y += self.player_velocity

						self.vel_x = 0
						self.vel_y = 0
						self.player.y += self.player_velocity
						self.player.is_moving = False
						self.camera.update_pos("up")	
				if keys[pygame.K_s]:
					if not self.background_y + self.background_height <= SCREEN_HEIGHT - 50:
						self.background_y -= self.player_velocity

						self.vel_x = 0
						self.vel_y = 0
						self.player.y -= self.player_velocity
						self.player.is_moving = False
						self.camera.update_pos("down")	
				if keys[pygame.K_a]:
					if not self.background_x >= 0:
						self.background_x += self.player_velocity

						self.vel_x = 0
						self.vel_y = 0
						self.player.x += self.player_velocity
						self.player.is_moving = False
						self.camera.update_pos("left")			
				if keys[pygame.K_d]:
					if not self.background_x + self.background_width <= SCREEN_WIDTH:
						self.background_x -= self.player_velocity

						self.vel_x = 0
						self.vel_y = 0
						self.player.x -= self.player_velocity
						self.player.is_moving = False
						self.camera.update_pos("right")		
				

			for structure in self.camera.sprite_list:
				phb = self.player.hit_box
				if structure.structure == "puddle":
					puddle_hb = structure.hit_box
					if phb.check_hit(puddle_hb.x, puddle_hb.y, puddle_hb.width, puddle_hb.height):
						self.player_velocity += 15
						break
					else:
						self.player_velocity = 3

			if self.player.hit_box.check_hit(self.mouse_rect.x, self.mouse_rect.y, self.mouse_rect.width, self.mouse_rect.height):
				self.vel_x = 0
				self.vel_y = 0

			self.player.move(self.vel_x, self.vel_y)
			self.player.draw(screen, self.target_x, self.target_y)

			#collision loop for shelf, bots, and puddle
			for structure in self.camera.sprite_list: # FOR THE DIALOG BOX ONLY
				phb = self.player.hit_box
				if structure.structure == "shelf":
					hhb = structure.hit_box
					if phb.check_hit(hhb.x, hhb.y, hhb.width, hhb.height):
						self.show_item_dialog = True
						self.list_to_display = structure.items
						self.current_shelf = structure
						break
					else:
						self.current_shelf = structure
						self.show_item_dialog = False

			for structure in self.camera.sprite_list:
				phb = self.player.hit_box
				#check if shelf
				if structure.structure == "shelf":
					shb = structure.hit_box_inner
					hhb = structure.hit_box

					if phb.check_hit(shb.x, shb.y, shb.width, shb.height):
						self.vel_x = 0
						self.vel_y = 0
						break

					structure.is_player_in_hover(self.player)
					
											
				if structure.structure == "bot":
					bhb = structure.hit_box
					if phb.check_hit(bhb.x, bhb.y, bhb.width, bhb.height):
						self.player.health -= 1

					#check if it hit a shelf
					for building in self.camera.sprite_list:
						if building.structure == "shelf":
							shelf_hit_box = building.hit_box_inner
							if shelf_hit_box.check_hit(structure.hit_box.x, structure.hit_box.y, structure.hit_box.width, structure.hit_box.height):
								structure.vel_x = 0 # RESET
								structure.vel_y = 0 # RESET
								break

				#THIS WILL DETERMINE THE WINNER
				if structure.structure == "cashier":
					chb = self.cashier.hit_box
					if phb.check_hit(chb.x, chb.y, chb.width, chb.height):
						score_to_beat = len(self.requirements_to_win)
						player_score = 0

						for item_requirement in self.requirements_to_win:
							for item in self.player.inventory:
								if item_requirement["name"] == item.brand:
									player_score += 1
									break
								
						if player_score == score_to_beat:
							game_state.win_or_lose(True)
							game_state.set_game_state("decider-screen")
						else:
							game_state.win_or_lose(False)
							game_state.set_game_state("decider-screen")
						
				
			#draw everything on camera list
			for sprite in self.camera.sprite_list:
				sprite.draw(screen)

			self.show_timer()

			#create checker
			if self.remove_item_from_inventory:
				del self.player.inventory[self.index_to_remove]
				self.index_to_remove = 0
				self.remove_item_from_inventory = False

			self.player_inventory.text_image.text = "Inventory: "
			self.player_inventory.draw(screen)
			for i in range(0, len(self.player.inventory)):
				item = self.player.inventory[i]
				if item.click(screen, self.list_to_display_pos_inventory[i]):
					if item.is_equipped:
						self.index_to_remove = i
						self.remove_item_from_inventory = True
						time.sleep(0.150)
						break
							
			
			if self.show_item_dialog_2:
				self.shelf_items_text.draw(screen)
				for i in range(0, len(self.list_to_display)):
					item = self.list_to_display[i]
					if item.click(screen, self.list_to_display_pos[i]):
						if len(self.player.inventory) < 9:
							if not item.is_equipped:
								item.is_equipped = True
								self.player.inventory.append(item)
								break;
						
							
		


#==========================================MAIN LOOP===========================================

if __name__ == "__main__":
	

	fps_text = DisplayText("?", 10, 10, 20, random_hex())
	show_fps = False

	game_state_manager = GameStateManager("game")

	event_ = None

	clock = pygame.time.Clock()
	
	while running:
			
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






