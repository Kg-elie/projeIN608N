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

    def __init__(self, SCREEN, WINDOW_SIZE, CELL_SIZE, GRID_LENGTH, RAYON, copie = False):
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
        self.copie = copie
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
        if not self.copie:
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
    
    def copy(self):
        """
        permet de copier le plateau de jeu
        """
        copy = Plateau(self.SCREEN, self.WINDOW_SIZE, self.CELL_SIZE, self.GRID_LENGTH, self.RAYON, True)
        copy.plateau = self.plateau.copy()
        return copy

    def verif_victoire(self):
        """
        permet de verifier si un joueur a gagner la partie
        """
        red = 0
        blue = 0
        for bille in self.plateau.values():
            if bille.get_couleur() == (0, 0, 255):
                blue += 1
            elif bille.get_couleur() == (255, 0, 0):
                red += 1
        if red == 8:
            return "blue"
        elif blue == 8:
            return "red"
        else:
            return ""


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
    lettre,num = ord(pos_bille[0]),int(pos_bille[1]); #separes les coordonnes de la bille
    boussole = {"NE":(-1,0),"NW":(-1,-1),"SE":(1,1),"SW":(1,0),"E":(0,1),"W":(0,-1)}; #dictionnaire qui permet de trouver la nouvelle position de la bille
    new_pos = (chr(lettre+boussole[direction][0]),str(num+boussole[direction][1])) ; #trouve la nouvelle position de la bille
    return new_pos[0]+new_pos[1]

def verification_mouvement(plateau,pos_bille, direction,billes_select):
    """
    Fonction qui permet de verifier si le mouvement est possible
    """
    lettre,num = ord(pos_bille[0]),int(pos_bille[1]); #separes les coordonnes de la bille
    boussole = {"NE":(-1,0),"NW":(-1,-1),"SE":(1,1),"SW":(1,0),"E":(0,1),"W":(0,-1)}; #dictionnaire qui permet de trouver la nouvelle position de la bille
    try:
        key = chr(lettre+boussole[direction][0])+str(num+boussole[direction][1]); #trouve la nouvelle position de la bille
    except :
        print(f"mouvement impossible de {pos_bille} "); #affiche un message d'erreur si le mouvement est impossible car la position n'existe pas
        return False
    if key in plateau.plateau and (plateau.get_bille(key).get_couleur() == (101, 67, 32) or key in billes_select):
        return True; #retourne vrai si le mouvement est possible c.a.d si la bille est vide ou si la bille est selectionnee
    elif key in plateau.plateau and plateau.get_bille(key).get_couleur() != plateau.get_bille(pos_bille).get_couleur():
        return verification_sumito(plateau,billes_select,direction)[0];
    print(f"mouvement impossible de {pos_bille} vers {chr(lettre+boussole[direction][0])+str(num+boussole[direction][1])}")
    return False; #retourne faux si le mouvement est impossible 

def front_sumito(billes_select,direction) :
    """ donne quel bille est en face de la bille adverse si il y a sumito"""
    pos = billes_select[0]
    for bille in billes_select:
        lettre,num = ord(bille[0]),int(bille[1]); #separes les coordonnes de la bille
        match direction:
            case "NE": 
                if ord(bille[0]) < ord(pos[0]) and int(bille[1]) == int(pos[1]):
                    pos = bille
            case "NW":
                if ord(bille[0]) < ord(pos[0]) and int(bille[1]) < int(pos[1]):
                    pos = bille
            case "SE":
                if ord(bille[0]) > ord(pos[0]) and int(bille[1]) > int(pos[1]):
                    pos = bille
            case "SW":
                if ord(bille[0]) > ord(pos[0]) and int(bille[1]) == int(pos[1]):
                    pos = bille
            case "E":
                if ord(bille[0]) == ord(pos[0]) and int(bille[1]) > int(pos[1]):
                    pos = bille
            case "W":
                if ord(bille[0]) == ord(pos[0]) and int(bille[1]) < int(pos[1]):
                    pos = bille
    return pos



def verification_sumito(plateau,billes_select, direction):
    force = len(billes_select) # combien de bille font le sumito sumito
    front = front_sumito(billes_select,direction) #bille en face de la bille adverse
    couleur_joueur = plateau.get_bille(front).get_couleur() #couleur du joueur
    bille_adverse = [] #liste des billes adverses a deplacer
    possibilite = True 
    for i in range(force):
        try:   
            pos_adverse = trouver_position(front,direction)
        except:
            return False, bille_adverse
        try:
            couleur_pos = plateau.get_bille(pos_adverse).get_couleur() 
        except:
            return True, bille_adverse
        if i == 0 and couleur_pos == (101, 67, 32):
                return False, bille_adverse # si la premiere bille est vide
        if couleur_pos == (101, 67, 32):
                return True, bille_adverse # si il y a bille est vide 
        if couleur_pos != couleur_joueur:
            if i == force - 1:
                return False, bille_adverse # si il y le meme nombre de bille adverse que de bille du joueur
            possibilite *= True 
            front = pos_adverse
            bille_adverse.append(pos_adverse)
        else:
            possibilite *= False # si il y a une bille du joueur
            break
    return possibilite, bille_adverse
        



def deplacement(plateau, billes_select, bille, cercles):
    """
    Fonction qui permet de receuillirtoutes les inormations pour le deplacement 
    d'une bille sur le plateau de jeu
    """
    
    """coordonnes de la bille selectionner pour le deplacement"""
    new_x, new_y = plateau.get_bille(bille).get_x(), plateau.get_bille(bille).get_y()
    x,y = plateau.get_bille(billes_select[-1]).get_x(),plateau.get_bille(billes_select[-1]).get_y()
    
    """analyse de la direstion du dplacement"""
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
    
    """verification de la validite du mouvement"""
    verif = True
    for bille in billes_select:
        verif*=verification_mouvement(plateau,bille,trouver_direction(mouvement),billes_select)
    """ verification de la validite du sumito si il y a sumito"""
    verif_sumito = verification_sumito(plateau,billes_select,trouver_direction(mouvement))
    print(f"sumito ?  {verif_sumito[0]}")

    if verif:
        if verif_sumito[0]:
            print(f" sumito possible en poussant {verif_sumito[1]}")
            billes_select.extend(verif_sumito[1]) #ajoute les billes adverses a deplacer
            
        donnee_deplacement = [] #stocke les nouvelles position position des billes a deplacer
        for bille_select in billes_select:
            actual= plateau.get_bille(bille_select)
            x, y = actual.get_x(), actual.get_y() #coordonnes de la bille selectionner pour le deplacement
            if  (x, y, plateau.RAYON + 2)  in cercles:
                cercles.remove((x, y, plateau.RAYON + 2))
                pygame.draw.circle(plateau.SCREEN, (139, 69, 19), (x, y), plateau.RAYON + 2,5) #dessine un cercle vide pour effacer le cercle de selection
             
            try :
                new_pos = trouver_position(bille_select,trouver_direction(mouvement)) #trouve la nouvelle position de la bille en fonction de la direction
                new_x, new_y = plateau.get_bille(new_pos).get_x(), plateau.get_bille(new_pos).get_y() #coordonnes de la nouvelle position de la bille
                donnee_deplacement.append((new_pos,new_x,new_y,actual.get_id(),actual.get_couleur())) #ajoute les nouvelles position  de la bille  
            except:
                continue
            effacer_bille(plateau, bille_select, x, y ,plateau.get_bille(new_pos).get_id()) #efface la bille
        for donnee in donnee_deplacement:
            deplacer_bille(plateau,donnee[0],donnee[1],donnee[2],donnee[3],donnee[4]) #deplace les billes
        return True
    else: 
        print("mouvement impossible") #affiche un message d'erreur si le mouvement est impossible
        for _ in range(len(cercles)):
            #nettoie le plateau de jeu
            x,y,r = cercles[-1]
            pygame.draw.circle(plateau.SCREEN,(139, 69, 19), (x, y), r,6)
            cercles.remove((x, y, r)) 
        return False

def effacer_bille(plateau, bille,x,y,t_cpt):
    """
    Fonction qui permet d'effacer une bille sur le plateau de jeu. on renplace la bille par une case vide
    """
    plateau.plateau[bille] = Bille(plateau.SCREEN, (101, 67, 32), x, y, t_cpt, plateau.RAYON)
    pass


def deplacer_bille(plateau, target,new_x,new_y, cpt, color):
    """
    Fonction qui permet de deplacer une bille sur le plateau de jeu. on remplace la bille par une autre bille a une nouvelle position
    """
    plateau.plateau[target] = Bille(plateau.SCREEN, color, new_x, new_y, cpt, plateau.RAYON)
    
    
def alignement(billes_select, bille):
    """
    Fonction qui permet de verifier si les billes selectionnees sont alignees
    """
    if billes_select[0] == bille[0] and int(billes_select[1]) - int(bille[1]) in [-1,1] : 
        """ ex : A1 A2 """
        return "horizontale"
    elif billes_select[1] == bille[1] and ord(billes_select[0]) - ord(bille[0]) in [-1,1]:
        """ ex : A1 B1 """
        return "DiagonaleMemeNumero"
    elif ord(billes_select[0]) - ord(bille[0]) in [-1,1] and int(billes_select[1]) - int(bille[1]) in [-1,1]:
        """ ex : A1 B2 """
        return "diagonale"
    else: 
        return "" #si billes non alignees
    


def rencontre_bille(billes_select, bille):
    """
    Fonction qui deplace une bille en confrontant celles de l'adversaire
    """
    pass

def confrontation(plateau,bille,mouvement):
    """
    Fonction qui permet de gerer la confrontation entre deux billes
    """
    bille 


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
    return pygame.font.Font("font.ttf", int(size))

def simulate_click(position):
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': position, 'button': 1}))


def billes_jouables_IA(plateau):
    """
    Fonction qui retourne les billes jouables par l'IA
    """
    billes = []
    for pos, bille in plateau.get_plateau().items():
        if bille.get_couleur() == (255, 0, 0):
            if move := voisins_jouables(plateau, pos):
                billes.append((pos, bille))
    return billes

def direction_IA(plateau, bille, destination):

    new_x, new_y = plateau.get_bille(destination).get_x(), plateau.get_bille(destination).get_y()
    x,y = plateau.get_bille(bille).get_x(),plateau.get_bille(bille).get_y()
    
    """analyse de la direstion du deplacement"""
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
    return trouver_direction(mouvement)

def coequipier_voisins(plateau, bille,direction):
    """
    Fonction qui permet de trouver les voisins alliés d'une bille
    """
    lettre,num = ord(bille[0]),int(bille[1]) #separes les coordonnes de la bille
    boussole = {"NE":(1,0),"NW":(1,1),"SE":(-1,-1),"SW":(-1,0),"E":(0,-1),"W":(0,1)} #dictionnaire qui permet de trouver l'allié
    voisins = []
    sens = boussole[direction]
    for _ in range(2):
        try:
            key = chr(lettre+sens[0])+str(num+sens[1]) #trouve la nouvelle position de la bille
            if plateau.get_bille(key).get_couleur() == (255, 0, 0):
                lettre,num = ord(key[0]),int(key[1])
                
                voisins.append(key)
        except:
            continue
    return voisins

def voisins_jouables(plateau, bille):
    """
    Fonction qui permet de trouver les voisins libres d'une bille
    """
    lettre,num = ord(bille[0]),int(bille[1]) #separes les coordonnes de la bille
    boussole = {"NE":(-1,0),"NW":(-1,-1),"SE":(1,1),"SW":(1,0),"E":(0,1),"W":(0,-1)} #dictionnaire qui permet de trouver la nouvelle position de la bille
    voisins = []
    allie = []
    for direction in boussole.keys():
        try:
            key = chr(lettre+boussole[direction][0])+str(num+boussole[direction][1]) #trouve la nouvelle position de la bille
            alliance = []
            alliance.extend(coequipier_voisins(plateau, bille,direction))
            aligne = bille
            
            if plateau.get_bille(key).get_couleur() == (101, 67, 32) :
                voisins.append(key)
                for aide in alliance:
                    if not alignement(aligne,aide):
                        alliance.remove(aide)
                    aligne = aide
                allie.append(alliance)
            
            elif plateau.get_bille(key).get_couleur() == (0, 0, 255) and verification_sumito(plateau,[bille] + alliance,direction)[0] :
                voisins.append(key)
                for aide in alliance:
                    if not alignement(aligne,aide):
                        alliance.remove(aide)
                    aligne = aide
                allie.append(alliance)
            print(f"fn : voisins de {bille} jouables{voisins} - alliance {allie} POUR direction {direction}")    
        except:
            continue
    
    return voisins,allie