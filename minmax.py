
import pygame
import sys
import toolbox


WHITE = (255, 255, 255)
VIDE = (101, 67, 32)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

COEF_CENTRE = 1.5
COEF_DENSITE = 1
COEF_ELIMINATION = 2.5
class node:
    def __init__(self, children= [], parent=None, depth=0, score=0, move = None):
        self.move = move
        self.parent = parent
        self.children = []
        self.score = 0
        self.depth = depth
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    def get_children(self):
        return self.children
    def __str__(self):
        return str(self.data)

def eval(plateau):
    pass

def distance_center(plateau,color):
    distance = 0
    cpt = 0
    lettre_c, num_c = ord("E"),4
    for pos, bille in plateau.get_plateau().items():
        lettre,num = ord(pos[0]),int(pos[1])
        if bille.get_couleur() == color:
            cpt += 1
            distance += max([abs(lettre-lettre_c),abs(num-num_c)])
    return 4- distance/cpt


def distance_allie(plateau,color):
    moyenne = 0
    cpt_moyenne = 0
    
    for pos_ref, bille_ref in plateau.get_plateau().items():
        distance = 0
        cpt = 0
        for pos, bille in plateau.get_plateau().items():
            if bille.get_couleur() == color and bille_ref.get_couleur() == color:
                cpt += 1
                distance += max([abs(ord(pos[0])-ord(pos_ref[0])),abs(int(pos[1])-int(pos_ref[1]))])
        if cpt > 0:
            cpt_moyenne += 1
            moyenne  += distance/cpt
    return 8 - moyenne/cpt_moyenne

def bille_elimine(plateau,color):
    """ retourne le nombre de bille elimine de l'adversaire"""
    cpt = 0
    for pos, bille in plateau.get_plateau().items():
        if bille.get_couleur() != color and bille.get_couleur() != VIDE:
            cpt += 1
    return 14 - cpt
    

    

def eval_score(plateau):
    densite_allie = distance_allie(plateau, RED)
    center_allie = distance_center(plateau, RED)
    elimination_allie = bille_elimine(plateau, RED)

    densite_ennemi = distance_allie(plateau, BLUE)
    center_ennemi = distance_center(plateau, BLUE)
    elimination_ennemi = bille_elimine(plateau, BLUE)
 
    
    score_allie = COEF_CENTRE * center_allie + COEF_DENSITE * densite_allie + COEF_ELIMINATION * elimination_allie
    score_ennemi = COEF_CENTRE * center_ennemi + COEF_DENSITE * densite_ennemi + COEF_ELIMINATION * elimination_ennemi

    score = score_allie - score_ennemi

            
    return  round(score,2)
def preview(plateau,billes, direction):
    plateau = plateau.copy()
    new_pos = []
    ancienne_pos = []
    bille_vide = None
    for bile in plateau.get_plateau().values():
        if bile.get_couleur() == VIDE:
            bille_vide = bile
            break

       
    for pos in billes:
        ancienne_pos.append(plateau.get_bille(pos))
        try: 
            new = toolbox.trouver_position( pos, direction)
            new_pos.append(new)
            if new in plateau.get_plateau().keys():
                if pos == billes[-1]:
                    plateau.get_plateau()[pos] = plateau.get_bille(new)
                else:
                    plateau.get_plateau()[pos] = bille_vide
                plateau.get_plateau()[new] =ancienne_pos[-1]
            else:
                plateau.get_plateau()[pos] = plateau.get_bille(bille_vide)
            
            
        except:
            return -1000
        
    return eval_score(plateau)


    pass

def choix_billes(plateau, billes_jouables):
    meilleur = None
    for bille in billes_jouables:
        bille =[ bille[0]]
        
        possibilite,alliance = toolbox.voisins_jouables(plateau, bille[0])
        
        for pos,allie in zip(possibilite,alliance):
            bille = [bille[0]]
            bille.extend(allie)
            direction = toolbox.direction_IA(plateau,bille[0],pos)
            score = preview(plateau,bille,direction)
            if meilleur == None or score > meilleur[0]:
                meilleur = (score,bille,pos)
    return meilleur
