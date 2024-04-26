import pygame
import sys
import toolbox
import shared_data as sd
import menu



cercles = []
turn = 0
player = [sd.BLUE, sd.RED]

def game(SCREEN):
    """
    Fonction qui permet de lancer le jeu, elle permet de creer le plateau de jeu et de l'afficher 
    """
    global turn
    pointsBlue = 0
    bleft = 0
    pointsRed = 0
    rleft = 0
    billes_select = []
    alignement = ""
    running = True
    SCREEN.fill("#171614")
    toolbox.draw_regular_polygon(SCREEN, sd.BROWN, 6, sd.WINDOW_SIZE[1]//2 + 50,
                                (sd.WINDOW_SIZE[0]//2, sd.WINDOW_SIZE[1]//2), 0)

    plateau = toolbox.Plateau(
        SCREEN, sd.WINDOW_SIZE, sd.CELL_SIZE, sd.GRID_LENGTH, sd.RAYON)
    
    
    while running:

        GAME_POS = pygame.mouse.get_pos()

        MENU_BACK = toolbox.Button(image=None, pos=(
            sd.WINDOW_SIZE[0]//1.10, sd.WINDOW_SIZE[1]//1.10), text_input="Menu", font=toolbox.get_font(
            sd.FONT_SIZE*1.7), base_color="Grey", hovering_color="Grey")
    
        MENU_BACK.changeColor(GAME_POS)
        MENU_BACK.update(SCREEN)

        for bille in plateau.plateau.values():
            if bille.get_couleur() == (0, 0, 255):
                bleft += 1
            elif bille.get_couleur() == (255, 0, 0):
                rleft += 1
                
        pointsRed = 14 - bleft
        pointsBlue = 14 - rleft
        bleft, rleft = 0, 0

        points_f = toolbox.get_font(sd.FONT_SIZE*2.2).render(
                f"{pointsBlue} : {pointsRed}", True, "White")
        pygame.draw.rect(SCREEN, "#171614", (sd.WINDOW_SIZE[0]//1.30, sd.WINDOW_SIZE[1]//14.4, sd.WINDOW_SIZE[0]//5, sd.WINDOW_SIZE[1]//7.2))
        points_rect = points_f.get_rect(center=(sd.WINDOW_SIZE[0]//1.163, sd.WINDOW_SIZE[1]//7.2))
        SCREEN.blit(points_f, points_rect)

        if winner := plateau.verif_victoire():
            game_over_screen_fade = pygame.Surface((sd.WINDOW_SIZE[0], sd.WINDOW_SIZE[1]))
            game_over_screen_fade.set_alpha(50)
            SCREEN.blit(game_over_screen_fade, (0, 0))
            ENDGAME_TEXT = toolbox.get_font(sd.FONT_SIZE).render(
            f"{winner} won !", True, "White")
            ENDGAME_RECT = ENDGAME_TEXT.get_rect(    
                center=(sd.WINDOW_SIZE[0]//2, sd.WINDOW_SIZE[1]//2.7))
            SCREEN.blit(ENDGAME_TEXT, ENDGAME_RECT)

        if turn == 0:
            player_turn = toolbox.get_font(sd.FONT_SIZE*1.35).render(
                "blue's turn", True, "BLACK")
            pygame.draw.rect(SCREEN, sd.BLUE, (sd.WINDOW_SIZE[0]//25.6, sd.WINDOW_SIZE[1]//14.4, sd.WINDOW_SIZE[0]//4.27, sd.WINDOW_SIZE[1]//7.2))
            player_rect = player_turn.get_rect(center=(sd.WINDOW_SIZE[0]//6.4, sd.WINDOW_SIZE[1]//7.2))
            SCREEN.blit(player_turn, player_rect)
        else:
            player_turn = toolbox.get_font(sd.FONT_SIZE*1.35).render(
                "red's turn", True, "BLACK")
            pygame.draw.rect(SCREEN, sd.RED, (sd.WINDOW_SIZE[0]//25.6, sd.WINDOW_SIZE[1]//14.4, sd.WINDOW_SIZE[0]//4.27, sd.WINDOW_SIZE[1]//7.2))
            player_rect = player_turn.get_rect(center=(sd.WINDOW_SIZE[0]//6.4, sd.WINDOW_SIZE[1]//7.2))
            SCREEN.blit(player_turn, player_rect)

        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BACK.checkForInput(GAME_POS):
                    cercles.clear()
                    turn = 0
                    menu.main_menu(SCREEN, sd.back_image)
                for place, bille in plateau.get_plateau().items():
                    if toolbox.distance(GAME_POS, (bille.get_x(), bille.get_y())) <= sd.RAYON and len(billes_select) <= 3:
                        """ gestion du deplacement des billes selectionnées """
                        if bille.get_couleur() == sd.VIDE:
                            print("deplacement bille vide")
                            if len(billes_select) > 0:
                                if toolbox.deplacement(
                                        plateau, billes_select, place, cercles):
                                    turn = (turn + 1) % 2
                                billes_select = []
                                break
                            elif len(billes_select) == 0:
                                break
                            
                        elif bille.get_couleur() != player[turn] and len(billes_select) > 0:
                            print("bille adverse")
                            if toolbox.deplacement(
                                    plateau, billes_select, place, cercles):
                                turn = (turn + 1) % 2
                            billes_select = []
                            break

                        elif place in billes_select:
                            """ bille selectionnée supprimer """
                            print("suppression bille")
                            billes_select.remove(place)
                            cercles.remove(
                                (x := bille.get_x(), y := bille.get_y(), sd.RAYON + 2))
                            pygame.draw.circle(
                                plateau.SCREEN, (139, 69, 19), (x, y), plateau.RAYON + 2, 5)
                            break

                        elif len(billes_select) == 0:
                            """ premiere bille a ajouter """
                            print("ajout de la premiere bille")
                            if bille.get_couleur() == player[turn]:
                                billes_select.append(place)
                                cercles.append(
                                    (bille.get_x(), bille.get_y(), sd.RAYON + 2))
                                break

                        elif len(billes_select) < 3:
                            """ plusieurs billes selectionnée  """
                            if bille.get_couleur() == player[turn]:
                                """ verification de la couleur"""
                                if len(billes_select) == 1:
                                    alignement = toolbox.alignement(
                                        billes_select[-1], place)
                                    if not alignement:
                                        continue
                                elif toolbox.alignement(billes_select[-1], place) != alignement:
                                    """ verification de l'alignement"""
                                    print(toolbox.alignement(
                                        billes_select[-1], place))
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

        sd.clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    BG = pygame.image.load('bg.png')
    pygame.init()
    SCREEN = pygame.display.set_mode(sd.WINDOW_SIZE)
    SCREEN.blit(BG, (0, 0))
    pygame.display.set_caption("Matrice de Ronds")
    game(SCREEN)
