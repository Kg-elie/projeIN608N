import pygame
from math import cos, sin, pi


class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(
                self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(
                self.text_input, True, self.base_color)


class Plateau:
    """ 
    Classe Plateau qui permet de creer un plateau de jeu, c'est la class main de la gestion du jeu
    """

    def __init__(self, SCREEN, WINDOW_SIZE, CELL_SIZE, GRID_LENGTH, RAYON):
        """ 
        Constructeur de la classe Plateau
        """
        self.plateau = dict()
        self.WINDOW_SIZE = WINDOW_SIZE
        self.CELL_SIZE = CELL_SIZE
        self.GRID_LENGTH = GRID_LENGTH
        self.GRID_WIDTH = CELL_SIZE * GRID_LENGTH
        self.MARGIN_X = (WINDOW_SIZE[0] - self.GRID_WIDTH) // 2
        self.MARGIN_Y = (WINDOW_SIZE[1] - self.GRID_WIDTH) // 2
        self.RAYON = RAYON
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
        for row in range(self.GRID_LENGTH):
            difference = 0
            for col in range(self.GRID_LENGTH):
                if schema[row][col] == 1:
                    if row % 2 == 1:
                        x = self.MARGIN_X + col * self.CELL_SIZE + self.CELL_SIZE // 2 + 30
                    else:
                        x = self.MARGIN_X + col * self.CELL_SIZE + self.CELL_SIZE // 2
                    y = self.MARGIN_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
                    if row > 4:
                        decalage = row - 4
                        "permet de gerer les colonnes en diagonale"
                    else:
                        decalage = 0
                    if position[cpt] == -1:
                        self.plateau[chr(
                            row+65) + str(col-difference + decalage)] = Bille(SCREEN, (255, 0, 0), x, y, cpt, self.RAYON)
                    elif position[cpt] == 0:
                        self.plateau[chr(
                            row+65) + str(col-difference + decalage)] = Bille(SCREEN, (101, 67, 32), x, y, cpt, self.RAYON)
                    else:
                        self.plateau[chr(
                            row+65) + str(col-difference + decalage)] = Bille(SCREEN, (0, 0, 255), x, y, cpt, self.RAYON)
                    cpt += 1
                else:
                    difference += 1

    def get_plateau(self):
        """
         retourne le plateau de jeu
        """
        return self.plateau

    def get_bille(self, cle):
        """
        retourne la bille a la position cle
        """
        return self.plateau[cle]

    def __str__(self):
        """
        permet d'afficher le plateau de jeu
        """
        return "Plateau : " + str(self.plateau)


class Bille:
    """
    Classe Bille qui permet de creer une bille
    """

    def __init__(self, SCREEN, couleur, x, y, id, RAYON):
        self.circle = pygame.draw.circle(SCREEN, couleur, (x, y), RAYON)
        self.couleur = couleur
        self.x = x
        self.y = y
        self.id = id

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


def deplacer_bille(plateau, billes_select, bille, cercles):
    """
    Fonction qui permet de deplacer une bille sur le plateau de jeu
    Utilisation de récursivité ? 
    """

    for bille_select in billes_select:
        x, y = plateau.get_bille(bille_select).get_x(
        ), plateau.get_bille(bille_select).get_y()
        cercles.remove((x, y, plateau.RAYON + 2))

    print(f"deplacement{billes_select} vers {bille} ")


def rencontre_bille(billes_select, bille):
    """
    Fonction qui deplace une bille en confrontant celles de l'adversaire
    """
    pass


def draw_regular_polygon(surface, couleur, nb_cote,
                         rayon, position, epaisseur=0):
    """
    Fonction qui permet de dessiner un polygone a n cotes (on peut garder juste le draw)
    """
    n, r = nb_cote, rayon
    x, y = position
    pygame.draw.polygon(surface, couleur, [
        (x + r * cos(2 * pi * i / n),
         y + r * sin(2 * pi * i / n))
        for i in range(n)
    ], epaisseur)


def distance(point1, point2):
    """
    Fonction qui permet de calculer la distance euclidienne entre deux points, permet de reconnaitre si le curseur est dans la zoene d'une bille
    """
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def get_font(size):
    return pygame.font.Font("font.ttf", size)
