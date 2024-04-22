import pygame
import menu
import shared_data as sd

pygame.init()
SCREEN = pygame.display.set_mode(sd.WINDOW_SIZE)
back_image = pygame.image.load("bg.png")
back_image = pygame.transform.scale(back_image, sd.WINDOW_SIZE)
pygame.display.set_caption('Game')
menu.main_menu(SCREEN, back_image)
