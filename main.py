import pygame
import menu

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load('bg.png')
pygame.display.set_caption('Game')
menu.main_menu(SCREEN, BG)
