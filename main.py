import pygame
import menu
import shared_data as sd

pygame.init()
SCREEN = pygame.display.set_mode(sd.WINDOW_SIZE)
BG = pygame.image.load('bg.png')
pygame.display.set_caption('Game')
menu.main_menu(SCREEN, BG)
