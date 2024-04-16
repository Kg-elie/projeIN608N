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
        self.SCREEN = SCREEN
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
        return "Bille id : " + str(self.id) + " Bille couleur : " + str(self.couleur)

    def __repr__(self):
        """
        permet d'afficher la bille
        """
        return " Bille couleur : " + str(self.couleur)

def trouver_direction(mouvement):
    if mouvement == "++":
        return "SE"
    elif mouvement == "-+":
        return "SW"
    elif mouvement == "--":
        return "NW"
    elif mouvement == "+-": 
        return "NE"
    elif mouvement == "+/": 
        return "E"
    elif mouvement == "-/":
        return "W"

def trouver_position(pos_bille,direction):
    """
    donne la nouvelle position de la bille en fonction de la direction
    """
    lettre,num = ord(pos_bille[0]),int(pos_bille[1])
    boussole = {"NE":(-1,0),"NW":(-1,-1),"SE":(1,1),"SW":(1,0),"E":(0,1),"W":(0,-1)}
    new_pos = (chr(lettre+boussole[direction][0]),str(num+boussole[direction][1]))
    print(f"position {pos_bille} vers {new_pos[0]+new_pos[1]} avec un mouvement : {direction}")
    return new_pos[0]+new_pos[1]

def verification_mouvement(plateau,pos_bille, direction,billes_select):
    """
    Fonction qui permet de verifier si le mouvement est possible
    """
    lettre,num = ord(pos_bille[0]),int(pos_bille[1])
    boussole = {"NE":(-1,0),"NW":(-1,-1),"SE":(1,1),"SW":(1,0),"E":(0,1),"W":(0,-1)}
    if plateau.get_bille(chr(lettre+boussole[direction][0])+
        str(num+boussole[direction][1])).get_couleur() == (101, 67, 32) or chr(
        lettre+boussole[direction][0])+str(num+boussole[direction][1]) in billes_select:
        return True
    print(f"mouvement impossible de {pos_bille} vers {chr(lettre+boussole[direction][0])+str(num+boussole[direction][1])}")
    return False

def deplacement(plateau, billes_select, bille, cercles):
    """
    Fonction qui permet de receuillirtoutes les inormations pour le deplacement 
    d'une bille sur le plateau de jeu Utilisation de récursivité ? 
    """
    print(f" liste des billes selectionner{billes_select}")
    new_x, new_y = plateau.get_bille(bille).get_x(), plateau.get_bille(bille).get_y()
    x,y = plateau.get_bille(billes_select[-1]).get_x(),plateau.get_bille(billes_select[-1]).get_y()
    mouvement = ""
    if new_x == x:
        mouvement +="/"
    elif new_x >= x:
        mouvement += "+"
    else:
        mouvement += "-"
    if new_y == y:
        mouvement +="/"
    elif new_y >= y:
        mouvement += "+"
    else:
        mouvement += "-"
    verif = True
    for bille in billes_select:
        verif*=verification_mouvement(plateau,bille,trouver_direction(mouvement),billes_select)
    if verif:
        donnee_deplacement = []
        for bille_select in billes_select:
            actual= plateau.get_bille(bille_select)
            x, y = actual.get_x(), actual.get_y()
            cercles.remove((x, y, plateau.RAYON + 2))
            pygame.draw.circle(plateau.SCREEN, (139, 69, 19), (x, y), plateau.RAYON + 2,5)
            new_pos = trouver_position(bille_select,trouver_direction(mouvement))
            new_x, new_y = plateau.get_bille(new_pos).get_x(), plateau.get_bille(new_pos).get_y()
            donnee_deplacement.append((new_pos,new_x,new_y,actual.get_id(),actual.get_couleur()))
            effacer_bille(plateau, bille_select, x, y ,plateau.get_bille(new_pos).get_id())
            actual= plateau.get_bille(bille_select)
        for donnee in donnee_deplacement:
            deplacer_bille(plateau,donnee[0],donnee[1],donnee[2],donnee[3],donnee[4])
    else: print("mouvement impossible")

def effacer_bille(plateau, bille,x,y,t_cpt):
    """
    Fonction qui permet d'effacer une bille sur le plateau de jeu
    """
    plateau.plateau[bille] = Bille(plateau.SCREEN, (101, 67, 32), x, y, t_cpt, plateau.RAYON)


def netttoye(plateau,cercles):
    for cercle in cercles:
        x,y,r = cercle
        pygame.draw.circle(plateau.SCREEN,(139, 69, 19), (x, y), r + 3,5)
        cercles.remove((x, y, plateau.RAYON + 2))

def deplacer_bille(plateau, target,new_x,new_y, cpt, color):
    """
    Fonction qui permet de deplacer une bille sur le plateau de jeu
    """
    plateau.plateau[target] = Bille(plateau.SCREEN, color, new_x, new_y, cpt, plateau.RAYON)
    
    
def alignement(billes_select, bille):
    """
    Fonction qui permet de verifier si les billes selectionnees sont alignees
    """
    print(f"billes_select : {billes_select} bille : {bille}")
    if billes_select[0] == bille[0] and int(billes_select[1]) - int(bille[1]) in [-1,1]:
        return "horizontale"
    elif billes_select[1] == bille[1] and ord(billes_select[0]) - ord(bille[0]) in [-1,1]:
        return "DiagonaleMemeNumero"
    elif ord(billes_select[0]) - ord(bille[0]) in [-1,1] and int(billes_select[1]) - int(bille[1]) in [-1,1]:
        return "diagonale"
    else :
        print (f"billes_select : {billes_select} bille : {bille}")
    
    return ""
    


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
