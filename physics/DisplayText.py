import pygame
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700


class DisplayText:
	def __init__(self, text, x=0, y=0, size=20, color="#ffffff"):
		self.text = text
		self.x = x
		self.y = y
		self.size = size
		self.color = color
		self.font = pygame.font.Font("./font/fff-forward.regular.ttf", self.size)
		
		self.type_letter = 0
		self.type_fps = 0
		self.cutscene_text = ""

		self.multiline_index = 0

		self.global_lines = self.__get_lines(self.text)
		# # # print(self.global_lines)

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
			# # # print(self.multiline_index)
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