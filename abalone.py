import pygame
import sys


WINDOW_SIZE = (1280, 720)
CELL_SIZE = 70
GRID_SIZE = 9

GRID_WIDTH = GRID_SIZE * CELL_SIZE
MARGIN_X = (WINDOW_SIZE[0] - GRID_WIDTH) // 2
MARGIN_Y = (WINDOW_SIZE[1] - GRID_WIDTH) // 2
RAYON = CELL_SIZE // 4


WHITE = (255, 255, 255)
VIDE = (101, 67, 32)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BG = pygame.image.load('bg.png')


class Plateau:
    """ 
    Classe Plateau qui permet de creer un plateau de jeu, c'est la class main de la gestion du jeu
    """

    def __init__(self, SCREEN):
        """ 
        Constructeur de la classe Plateau
        """
        self.plateau = []
        self.rang = [5, 6, 7, 8, 9, 8, 7, 6, 5]
        self.init_plateau(SCREEN)

    def init_plateau(self, SCREEN):
        """
        Methode qui permet d'initialiser le plateau de jeu, elle permet de creer les billes et de les positionner sur le plateau.
        """

        schema = [[0, 0, 1, 1, 1, 1, 1, 0, 0],
                  [0, 1, 1, 1, 1, 1, 1, 0, 0],
                  [0, 1, 1, 1, 1, 1, 1, 1, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1, 0],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 0],
                  [0, 1, 1, 1, 1, 1, 1, 1, 0],
                  [0, 1, 1, 1, 1, 1, 1, 0, 0],
                  [0, 0, 1, 1, 1, 1, 1, 0, 0]]
        " matrice qui represente le plateau de jeu permet de savoir ou placer les billes sur le plateau"
        " position est la liste qui detient le departs des billes sur le plateau"
        position = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        cpt = 0
        "c'est les main de la methode qui permet de creer les billes et de les positionner sur le plateau on ne cree une bille que si la valeur de la matrice est 1 et on choisi la couleur de la bille en fonction de la valeur de la liste position"
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if schema[row][col] == 1:
                    if row % 2 == 1:
                        x = MARGIN_X + col * CELL_SIZE + CELL_SIZE // 2 + 30
                    else:
                        x = MARGIN_X + col * CELL_SIZE + CELL_SIZE // 2
                    y = MARGIN_Y + row * CELL_SIZE + CELL_SIZE // 2
                    if position[cpt] == -1:
                        self.plateau.append(Bille(SCREEN, WHITE, x, y))
                    elif position[cpt] == 0:
                        self.plateau.append(Bille(SCREEN, VIDE, x, y))
                    else:
                        self.plateau.append(Bille(SCREEN, BLACK, x, y))
                    cpt += 1

    def get_plateau(self):
        """
         retourne le plateau de jeu
        """
        return self.plateau

    def get_rang(self):
        """
        retourne la liste des rangées
        """
        return self.rang

    def __str__(self):
        """
        permet d'afficher le plateau de jeu
        """
        return "Plateau : " + str(self.plateau) + " Rang : " + str(self.rang)


class Bille:
    """
    Classe Bille qui permet de creer une bille
    """

    def __init__(self, SCREEN, couleur, x, y):
        self.id = pygame.draw.circle(SCREEN, couleur, (x, y), RAYON)
        self.couleur = couleur
        self.x = x
        self.y = y

    def get_id(self):
        """
        retourne l'id de la bille
        """
        return self.id

    def get_couleur(self):
        """
        retourne la couleur de la bille
        """
        return self.couleur

    def get_x(self):
        """
        retourne la position x de la bille
        """
        return self.x

    def get_y(self):
        """
        retourne la position y de la bille
        """
        return self.y

    def set_id(self, id):
        """
        permet de modifier l'id de la bille
        """
        self.id = id

    def set_couleur(self, couleur):
        """
        permet de modifier la couleur de la bille
        """
        self.couleur = couleur

    def __str__(self):
        """
        permet d'afficher la bille
        """
        return "Bille id : " + str(self.id) + " Bille couleur : " + self.couleur

    def __repr__(self):
        """
        permet d'afficher la bille
        """
        return " Bille couleur : " + str(self.couleur)


def deplacer_bille():
    """
    Fonction qui permet de deplacer une bille sur le plateau de jeu
    """
    pass


def distance(point1, point2):
    """
    Fonction qui permet de calculer la distance entre deux points, permet de reconnaitre si le curseur est dans la zoene d'une bille
    """
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def game(SCREEN):
    """
    Fonction qui permet de lancer le jeu, elle permet de creer le plateau de jeu et de l'afficher 
    """

    billes_select = []

    running = True
    while running:

        SCREEN.fill(WHITE)
        pygame.draw.circle(
            SCREEN, BROWN, (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2), WINDOW_SIZE[1]//2)
        "creer un cercle marron au centre de l'ecran"

        positions = Plateau(SCREEN)

        GAME_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bille in positions.get_plateau():
                    if distance(GAME_POS, (bille.get_x(), bille.get_y())) <= RAYON:
                        if bille.get_id() in billes_select:
                            billes_select.remove(bille.get_id())
                            print(billes_select)
                            break
                        elif len(billes_select) < 3:
                            billes_select.append(bille.get_id())
                            print(billes_select)
                            break
                        else:
                            print("Vous ne pouvez pas selectionner plus de 3 billes")
                            break

        pygame.display.flip()

    print(positions)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode(WINDOW_SIZE)
    SCREEN.blit(BG, (0, 0))
    pygame.display.set_caption("Matrice de Ronds")
    game(SCREEN)
