import pygame
import sys
import toolbox


WINDOW_SIZE = (1280, 720)
CELL_SIZE = 75
GRID_LENGTH = 9

RAYON = CELL_SIZE // 4

WHITE = (255, 255, 255)
VIDE = (101, 67, 32)
BROWN = (139, 69, 19)

player = 1

cercles = []


def game(SCREEN):
    """
    Fonction qui permet de lancer le jeu, elle permet de creer le plateau de jeu et de l'afficher 
    """
    global plateau
    billes_select = []

    running = True
    while running:

        SCREEN.fill(WHITE)
        toolbox.draw_regular_polygon(SCREEN, BROWN, 6, WINDOW_SIZE[1]//2 + 50,
                                     (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), 0)

        plateau = toolbox.Plateau(
            SCREEN, WINDOW_SIZE, CELL_SIZE, GRID_LENGTH, RAYON)

        GAME_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print(plateau.plateau)
            if event.type == pygame.MOUSEBUTTONDOWN:
                for place, bille in plateau.get_plateau().items():
                    if toolbox.distance(GAME_POS, (bille.get_x(), bille.get_y())) <= RAYON and len(billes_select) <= 3:
                        if bille.get_couleur() == VIDE:
                            print("0")
                            if len(billes_select) > 0:
                                toolbox.deplacer_bille(
                                    plateau, billes_select, place, cercles)
                                billes_select = []
                            elif len(billes_select) == 0:
                                break

                        elif place in billes_select:
                            print("1")
                            billes_select.remove(place)
                            cercles.remove(
                                (bille.get_x(), bille.get_y(), RAYON + 2))
                            break

                        elif len(billes_select) == 0:
                            print("2")
                            billes_select.append(place)
                            cercles.append(
                                (bille.get_x(), bille.get_y(), RAYON + 2))
                            print(billes_select)
                            break

                        elif len(billes_select) < 3:
                            print("3")
                            if bille.get_couleur() == plateau.get_bille(billes_select[-1]).get_couleur():
                                print("4")
                                billes_select.append(place)
                                cercles.append(
                                    (bille.get_x(), bille.get_y(), RAYON + 2))

                            elif bille.get_couleur != plateau.get_bille(billes_select[-1]).get_couleur():
                                print("5")
                                toolbox.deplacer_bille(billes_select, place)
                                billes_select = []
                print("billes:", billes_select)

        for x, y, rayon in cercles:
            pygame.draw.circle(SCREEN, (0, 0, 0), (x, y), rayon, 5)

        pygame.display.flip()

    print(plateau)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    BG = pygame.image.load('bg.png')
    WINDOW_SIZE = (1280, 720)
    CELL_SIZE = 75
    GRID_LENGTH = 9

    RAYON = CELL_SIZE // 4

    WHITE = (255, 255, 255)
    VIDE = (101, 67, 32)
    BROWN = (139, 69, 19)
    pygame.init()
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    SCREEN.blit(BG, (0, 0))
    pygame.display.set_caption("Matrice de Ronds")
    game(SCREEN)
