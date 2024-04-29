
import toolbox
import shared_data as sd

COEF_CENTRE = 1.5
COEF_DENSITE = 1
COEF_ELIMINATION = 4



class Node:
    def __init__(self,  plateau: toolbox.Plateau, parent=None, depth=0, score=0, move = None, new_pose = None, color = 0):
        self.plateau = plateau
        self.move = move
        self.new_pose = new_pose
        self.parent = parent
        self.children = []
        self.score = score
        self.depth = depth
        self.color = color
        self.enemi = sd.RED if self.color == sd.BLUE else sd.BLUE
        self.generate_children()
        print(f" noeud crée avec un score de {self.score} et une profondeur de {self.depth}")

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_children(self):
        return self.children

    def __str__(self):
        return f" mouvement : {str(self.move)} vers {self.new_pose} avec score : {self.score }"
    
    def __repr__(self):
        return f" mouvement : {str(self.move)} vers {self.new_pose} avec score : {self.score }  "
    
    def get_mouvement(self):
        return self.resultat
    
    def generate_children(self):
        """ fonction qui genere les enfants d'un noeud"""

        
        mouvement = toolbox.billes_jouables_IA(self.plateau, self.color)
        if self.depth == 0:
            self.score = eval_score(self.plateau, self.color)
            return 
        
        for bille in mouvement:
            possibilite, alliance = toolbox.voisins_jouables(self.plateau, bille[0],self.color)

            for pos, allie in zip(possibilite, alliance):
                bille = [bille[0]]
                bille.extend(allie)
                direction = toolbox.direction_IA(self.plateau, bille[0], pos)
                score = preview(self.plateau, bille, direction, self.color)
                child = Node(score[1], depth = self.depth - 1, move = bille, parent = self, new_pose = pos, color = self.enemi)
                self.add_child(child)
                
        
    def minimax(self, depth, max_player, alpha = -1000, beta = 1000):
        """" fonction de recherche minimax"""
        if depth == 0:
            return self.score,self.move, self.new_pose
            
        move = None
        pos = None
        if   max_player:
            value = -1000
            for child in self.children:
                
                eval = child.minimax( depth - 1, False, alpha, beta)
                if eval[0] > beta:
                    return eval
                if value < eval[0]:   
                    value = eval[0]
                    move = child.move
                    pos = child.new_pose
                    alpha =  value

        else: 
            value = 1000
            for child in self.children:
                
                eval = child.minimax( depth - 1, True)
                if eval[0] < alpha:
                    return eval
                if eval[0] < value:
                    value = eval[0] 
                    move = child.move
                    pos = child.new_pose
                    beta = value

        self.score = value
        if self.depth > 0:
            print(f" le meilleur score possible avec une recherche de profondeur {self.depth} est : {value} avec le pions  {move} vers {pos} pour le joueur {self.color}")
        return value, move,pos
        
        

def distance_center(plateau, color):
    distance = 0
    cpt = 0
    lettre_c, num_c = ord("E"), 4
    for pos, bille in plateau.get_plateau().items():
        lettre, num = ord(pos[0]), int(pos[1])
        if bille.get_couleur() == color:
            cpt += 1
            distance += max([abs(lettre-lettre_c), abs(num-num_c)])
    return 4 - distance/cpt


def distance_allie(plateau, color):
    moyenne = 0
    cpt_moyenne = 0

    for pos_ref, bille_ref in plateau.get_plateau().items():
        distance = 0
        cpt = 0
        for pos, bille in plateau.get_plateau().items():
            if bille.get_couleur() == color and bille_ref.get_couleur() == color:
                cpt += 1
                distance += max([abs(ord(pos[0])-ord(pos_ref[0])),
                                abs(int(pos[1])-int(pos_ref[1]))])
        if cpt > 0:
            cpt_moyenne += 1
            moyenne += distance/cpt
    return 8 - moyenne/cpt_moyenne


def bille_elimine(plateau, color):
    """ retourne le nombre de bille elimine de l'adversaire"""
    cpt = 0
    for pos, bille in plateau.get_plateau().items():
        if bille.get_couleur() != color and bille.get_couleur() != sd.VIDE:
            cpt += 1
    return 14 - cpt


def eval_score(plateau,color):
    """ fonction qui retourne le score d'un plateau pour un joueur donné"""
    player = color
    enemy = sd.RED if player == sd.BLUE else sd.BLUE


    densite_allie = distance_allie(plateau,player )
    center_allie = distance_center(plateau,player )
    elimination_allie = bille_elimine(plateau,player )

    densite_ennemi = distance_allie(plateau, enemy)
    center_ennemi = distance_center(plateau,enemy)
    elimination_ennemi = bille_elimine(plateau,enemy )

    score_allie = COEF_CENTRE * center_allie + COEF_DENSITE * \
        densite_allie + COEF_ELIMINATION * elimination_allie
    score_ennemi = COEF_CENTRE * center_ennemi + COEF_DENSITE * \
        densite_ennemi + COEF_ELIMINATION * elimination_ennemi

    score = score_allie - score_ennemi
    return round(score, 2)


def preview(plateau, billes, direction,color):
    """ fonction qui simule un deplacement de billes"""
    plateau = plateau.copy()
    new_pos = []
    ancienne_pos = []
    bille_vide = None
    for bile in plateau.get_plateau().values():
        if bile.get_couleur() == sd.VIDE:
            bille_vide = bile
            break

    for pos in billes:
        ancienne_pos.append(plateau.get_bille(pos))
        try:
            new = toolbox.trouver_position(pos, direction)
            new_pos.append(new)
            if new in plateau.get_plateau().keys():
                if pos == billes[-1]:
                    plateau.get_plateau()[pos] = plateau.get_bille(new)
                else:
                    plateau.get_plateau()[pos] = bille_vide
                plateau.get_plateau()[new] = ancienne_pos[-1]
            else:
                plateau.get_plateau()[pos] = plateau.get_bille(bille_vide)

        except:
            return -1000,plateau

    return eval_score(plateau, color),plateau

    


