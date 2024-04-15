import pygame
import sys
import math
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player_x = 100
player_y = 100

target_x = 0
target_y = 0

vel_x = 0
vel_y = 0

move_player_x = False

def linear_equation(slope, x, b):
    return (slope * x) + b

def move(vel_x, vel_y):
    global player_x
    global player_y

    player_x += vel_x
    player_y += vel_y

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                target_x, target_y = pygame.mouse.get_pos()
                
                run = (target_x - player_x) 
                rise = (target_y - player_y)

                angle = math.atan2(run, rise)
                vel_x = math.sin(angle) * 3.5
                vel_y = math.cos(angle) * 3.5

            if event.button == 1:
                vel_x = 0
                vel_y = 0      


    screen.fill("#000000")

    player_x += vel_x 
    player_y += vel_y 
    
    pygame.draw.rect(screen, "#ffffff", (player_x, player_y, 50, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()