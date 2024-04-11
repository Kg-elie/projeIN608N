import pygame
import menu

WINDOW_SIZE = (1280, 720)
CELL_SIZE = 75
GRID_LENGTH = 9

RAYON = CELL_SIZE // 4

WHITE = (255, 255, 255)
VIDE = (101, 67, 32)
BROWN = (139, 69, 19)

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load('bg.png')
pygame.display.set_caption('Game')
menu.main_menu(SCREEN, BG, WINDOW_SIZE, CELL_SIZE, GRID_LENGTH,
               RAYON, WHITE, VIDE, BROWN)
