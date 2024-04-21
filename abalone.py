import pygame
import sys
import toolbox
import shared_data as sd


cercles = []

turn = 0
player = [sd.BLUE, sd.RED]
def game(SCREEN):
    """
    Fonction qui permet de lancer le jeu, elle permet de creer le plateau de jeu et de l'afficher 
    """
    global turn
    billes_select = []
    alignement = ""
    running = True
    SCREEN.fill(sd.WHITE)
    toolbox.draw_regular_polygon(SCREEN, sd.BROWN, 6, sd.WINDOW_SIZE[1]//2 + 50,
                                     (sd.WINDOW_SIZE[0]//2, sd.WINDOW_SIZE[1]//2), 0)

    plateau = toolbox.Plateau(
            SCREEN, sd.WINDOW_SIZE, sd.CELL_SIZE, sd.GRID_LENGTH, sd.RAYON)
    while running:

        
        if gagnant := plateau.verif_victoire() :
            running = False
            print(f"victoire de {gagnant} ")
            continue
        if turn == 0:
            player_turn = toolbox.get_font(45).render(
                "blue's turn", True, "BLACK")
            pygame.draw.rect(SCREEN, sd.BLUE, (50, 50, 300, 100))
            player_rect = player_turn.get_rect(center=(200, 100))
            SCREEN.blit(player_turn, player_rect)
        else:
            player_turn = toolbox.get_font(45).render(
                "red's turn", True, "BLACK")
            pygame.draw.rect(SCREEN, sd.RED, (50, 50, 300, 100))
            player_rect = player_turn.get_rect(center=(200, 100))
            SCREEN.blit(player_turn, player_rect)

        GAME_POS = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                
            if event.type == pygame.MOUSEBUTTONDOWN:
                for place, bille in plateau.get_plateau().items():
                    if toolbox.distance(GAME_POS, (bille.get_x(), bille.get_y())) <= sd.RAYON and len(billes_select) <= 3:
                        """ gestion du deplacement des billes selectionnées """
                        if bille.get_couleur() == sd.VIDE  :
                            print("deplacement bille vide")
                            if len(billes_select) > 0:
                                if toolbox.deplacement(
                                plateau, billes_select, place, cercles) :
                                    turn = (turn + 1) % 2
                                billes_select = []
                                break
                            elif len(billes_select) == 0:
                                break
                        elif  bille.get_couleur() !=  player[turn] and len(billes_select) > 0 :
                            print("bille adverse")
                            if toolbox.deplacement(
                                plateau, billes_select, place, cercles) :
                                turn = (turn + 1) % 2
                            billes_select = []
                            break
                         
                        elif place in billes_select:
                            """ bille selectionnée supprimer """
                            print("suppression bille")
                            billes_select.remove(place)
                            cercles.remove(
                                (bille.get_x(), bille.get_y(), sd.RAYON + 2))
                            pygame.draw.circle(plateau.SCREEN, (139, 69, 19), (bille.get_x(), bille.get_y()), plateau.RAYON + 2,5)
                            break

                        elif len(billes_select) == 0:
                            """ premiere bille a ajouter """
                            print("ajout de la premiere bille")
                            if bille.get_couleur() == player[turn]:
                                billes_select.append(place)
                                cercles.append(
                                    (bille.get_x(), bille.get_y(), sd.RAYON + 2))
                                break

                        elif  len(billes_select) < 3:
                            """ plusieurs billes selectionnée  """
                            if bille.get_couleur() == player[turn]:
                                """ verification de la couleur"""
                                if len(billes_select) == 1:
                                    alignement = toolbox.alignement(
                                        billes_select[-1], place)
                                    if not alignement:
                                        continue
                                elif toolbox.alignement(billes_select[-1], place) != alignement :
                                    """ verification de l'alignement"""
                                    print(toolbox.alignement(billes_select[-1], place))
                                    print(alignement)
                                    print("alignement pas ok")
                                    continue
                                print(alignement)
                                print("ajout bille")
                                billes_select.append(place)
                                cercles.append(
                                    (bille.get_x(), bille.get_y(), sd.RAYON + 2))

                            
                print(f" liste des billes selectionner{billes_select}")
                                    
            

        for x, y, rayon in cercles:
            pygame.draw.circle(SCREEN, (0, 0, 0), (x, y), rayon, 5)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    BG = pygame.image.load('bg.png')
    pygame.init()
    SCREEN = pygame.display.set_mode(sd.WINDOW_SIZE)
    SCREEN.blit(BG, (0, 0))
    pygame.display.set_caption("Matrice de Ronds")
    game(SCREEN)
