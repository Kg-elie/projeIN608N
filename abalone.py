import pygame, sys



WINDOW_SIZE = (1280, 720)
CELL_SIZE = 60
GRID_SIZE = 9

GRID_WIDTH = GRID_SIZE * CELL_SIZE
MARGIN_X = (WINDOW_SIZE[0] - GRID_WIDTH) // 2
MARGIN_Y = (WINDOW_SIZE[1] - GRID_WIDTH) // 2


WHITE = (255, 255, 255)
VIDE = (101, 67, 32)
BROWN = (139,69,19)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
BG = pygame.image.load('bg.png')

class Plateau:
    """ 
    Classe Plateau qui permet de creer un plateau de jeu, c'est la class main de la gestion du jeu
    """
    def __init__(self):
        """ 
        Constructeur de la classe Plateau
        """
        self.plateau = []
        self.rang = [5,6,7,8,9,8,7,6,5]
        self.init_plateau()
    
    def init_plateau(self):
        """
        Methode qui permet d'initialiser le plateau de jeu, elle permet de creer les billes et de les positionner sur le plateau.
        """
        pygame.draw.circle(screen, BROWN, (WINDOW_SIZE[0]//2 ,WINDOW_SIZE[1]//2 ), MARGIN_X);"creer un cercle marron au centre de l'ecran"
        schema = [[0,0,1,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,0,0],
                [0,1,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1,0],
                [1,1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,1,0],
                [0,1,1,1,1,1,1,0,0],
                [0,0,1,1,1,1,1,0,0]]; " matrice qui represente le plateau de jeu permet de savoir ou placer les billes sur le plateau"
        " position est la liste qui detient le departs des billes sur le plateau"
        position =[-1, -1,-1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        cpt = 0
        "c'est les main de la methode qui permet de creer les billes et de les positionner sur le plateau on ne cree une bille que si la valeur de la matrice est 1 et on choisi la couleur de la bille en fonction de la valeur de la liste position"
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if schema[row][col] == 1:
                    if row % 2 == 1:
                        x = MARGIN_X + col * CELL_SIZE + CELL_SIZE // 2 +30
                    else:
                        x = MARGIN_X + col * CELL_SIZE + CELL_SIZE // 2 
                    y = MARGIN_Y + row * CELL_SIZE + CELL_SIZE // 2
                    if position[cpt] == -1:
                        self.plateau.append(Bille(WHITE,x,y))
                    elif position[cpt] == 0:
                        self.plateau.append(Bille(VIDE,x,y))
                    else:
                        self.plateau.append(Bille(BLACK,x,y))
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



class Bille :
    """
    Classe Bille qui permet de creer une bille
    """
    def __init__(self,couleur,x,y):
        self.id =  pygame.draw.circle(screen, couleur, (x, y), CELL_SIZE // 4)
        self.couleur = couleur

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
    
    def set_id(self,id):
        """
        permet de modifier l'id de la bille
        """
        self.id = id
    
    def set_couleur(self,couleur):
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


screen = pygame.display.set_mode(WINDOW_SIZE)
screen.blit(BG, (0,0))
pygame.display.set_caption("Matrice de Ronds")








def game():
    """
    Fonction qui permet de lancer le jeu, elle permet de creer le plateau de jeu et de l'afficher 
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            


        screen.fill(WHITE)


        positions = Plateau()


        pygame.display.flip()

    print(positions)
    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    pygame.init()
    game()
