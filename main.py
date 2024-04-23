import pygame
import menu
import shared_data as sd

SCREEN = pygame.display.set_mode(sd.WINDOW_SIZE, pygame.RESIZABLE)
pygame.init()
pygame.display.set_caption('Game')
menu.main_menu(SCREEN, sd.back_image)
