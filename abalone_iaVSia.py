import pygame
import sys
import toolbox
import minmax
import shared_data as sd
import menu
import time
cercles = []
turn = 1
player = [sd.BLUE, sd.RED]


def game_IA(SCREEN):
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
            f"{pointsBlue} : {pointsRed}", True, "Grey")
        text_points = toolbox.get_font(sd.FONT_SIZE*1.3).render(
            "Blue  Red", True, "Grey")

        pygame.draw.rect(
            SCREEN, "#171614", (sd.WINDOW_SIZE[0]//1.30, sd.WINDOW_SIZE[1]//14.4, sd.WINDOW_SIZE[0]//5, sd.WINDOW_SIZE[1]//6))
        points_rect = points_f.get_rect(
            center=(sd.WINDOW_SIZE[0]//1.163, sd.WINDOW_SIZE[1]//6))
        text_rect = text_points.get_rect(
            center=(sd.WINDOW_SIZE[0]//1.163, sd.WINDOW_SIZE[1]//12))

        SCREEN.blit(points_f, points_rect)
        SCREEN.blit(text_points, text_rect)

        if winner := plateau.verif_victoire():
            menu.endgame(SCREEN, winner)

        if turn == 1:
            player_turn = toolbox.get_font(sd.FONT_SIZE*1.35).render(
                "Blue's turn", True, "BLACK")
            pygame.draw.rect(
                SCREEN, sd.BLUE, (sd.WINDOW_SIZE[0]//25.6, sd.WINDOW_SIZE[1]//14.4, sd.WINDOW_SIZE[0]//4.27, sd.WINDOW_SIZE[1]//7.2))
            player_rect = player_turn.get_rect(
                center=(sd.WINDOW_SIZE[0]//6.4, sd.WINDOW_SIZE[1]//7.2))
            SCREEN.blit(player_turn, player_rect)
        else:
            player_turn = toolbox.get_font(sd.FONT_SIZE*1.35).render(
                "Red's turn", True, "BLACK")
            pygame.draw.rect(
                SCREEN, sd.RED, (sd.WINDOW_SIZE[0]//25.6, sd.WINDOW_SIZE[1]//14.4, sd.WINDOW_SIZE[0]//4.27, sd.WINDOW_SIZE[1]//7.2))
            player_rect = player_turn.get_rect(
                center=(sd.WINDOW_SIZE[0]//6.4, sd.WINDOW_SIZE[1]//7.2))
            SCREEN.blit(player_turn, player_rect)
        time.sleep(1)
        if len(billes_select) == 0:
            print(f"tour de l'IA pour le joueur {player[turn]}")
            noeud = minmax.Node(plateau, depth=2, color=player[turn])
            meilleur_mouvement = noeud.minimax(noeud.depth, True)
            print(meilleur_mouvement)
            place_IA = meilleur_mouvement[1]
            billes_IA = [plateau.get_bille(i) for i in place_IA]
            billes_select = place_IA
            print(f"{place_IA} billes selectionner par l'IA")
            for bille_IA in billes_IA:
                pygame.mouse.set_pos(bille_IA.get_x(), bille_IA.get_y())
                GAME_POS = pygame.mouse.get_pos()
                toolbox.simulate_click((bille_IA.get_x(), bille_IA.get_y()))
                cercles.append(
                    (bille_IA.get_x(), bille_IA.get_y(), sd.RAYON + 2))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BACK.checkForInput(GAME_POS):
                    cercles.clear()
                    turn = 0
                    menu.main_menu(SCREEN, sd.back_image)
                if len(billes_select) > 0:
                    move = meilleur_mouvement[2]
                    bille = plateau.get_bille(move)
                    direction = toolbox.direction_IA(
                        plateau, billes_select[0], move)
                    print(f"direction du mouvement {direction}")

                    toolbox.simulate_click((bille.get_x(), bille.get_y()))
                    print(f"{billes_select} deplacer vers {move}")
                    GAME_POS = pygame.mouse.get_pos()
                    if bille.get_couleur() == sd.VIDE:
                        print("deplacement bille vide")
                        if len(billes_select) > 0:
                            if toolbox.deplacement(
                                    plateau, billes_select, move, cercles):
                                turn = (turn + 1) % 2
                            billes_select = []
                            break
                        elif len(billes_select) == 0:
                            break
                    elif bille.get_couleur() != player[turn] and len(billes_select) > 0:
                        print("bille adverse")
                        if toolbox.deplacement(
                                plateau, billes_select, move, cercles):
                            turn = (turn + 1) % 2
                        billes_select = []
                        break

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
                                (bille.get_x(), bille.get_y(), sd.RAYON + 2))
                            pygame.draw.circle(plateau.SCREEN, (139, 69, 19), (bille.get_x(
                            ), bille.get_y()), plateau.RAYON + 2, 5)
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

                # print(f" liste des billes selectionner{billes_select}")
                # print(f" le score du plateau pour l'ia est de {minmax.eval_score(plateau)}")

        for x, y, rayon in cercles:
            pygame.draw.circle(SCREEN, (0, 0, 0), (x, y), rayon, 5)

        pygame.display.flip()

        sd.clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    BG = pygame.image.load('assets/bg.png')
    pygame.init()
    SCREEN = pygame.display.set_mode(sd.WINDOW_SIZE)
    SCREEN.blit(BG, (0, 0))
    pygame.display.set_caption("Matrice de Ronds")
    game_IA(SCREEN)
