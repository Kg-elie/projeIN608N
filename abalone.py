import pygame, sys

pygame.init()

WINDOW_SIZE = (600, 600)
CELL_SIZE = 60
GRID_SIZE = 9

GRID_WIDTH = GRID_SIZE * CELL_SIZE
MARGIN_X = (WINDOW_SIZE[0] - GRID_WIDTH) // 2
MARGIN_Y = (WINDOW_SIZE[1] - GRID_WIDTH) // 2


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Matrice de Ronds")


def draw_matrix():
    schema = [[0,0,1,1,1,1,1,0,0],[0,1,1,1,1,1,1,0,0],[0,1,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1,0],[1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,0,0],[0,0,1,1,1,1,1,0,0]]
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if schema[row][col] :
                if row % 2 == 1:
                    x = MARGIN_X + col * CELL_SIZE + CELL_SIZE // 2 +30
                else:
                    x = MARGIN_X + col * CELL_SIZE + CELL_SIZE // 2  
                y = MARGIN_Y + row * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, BLACK, (x, y), CELL_SIZE // 4)




def game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            


        screen.fill(WHITE)


        positions = draw_matrix()


        pygame.display.flip()

 
    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    game()
