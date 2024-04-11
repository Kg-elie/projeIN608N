import pygame
import sys
import abalone
import toolbox


def main_menu(SCREEN, BG):
    pygame.display.set_caption('Main Menu')

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = toolbox.get_font(
            100).render('Main Menu', 1, (255, 255, 255))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_Button = toolbox.Button(image=None, pos=(640, 300), text_input="PLAY", font=toolbox.get_font(
            75), base_color="#d7fcd4", hovering_color="Green")
        QUIT_Button = toolbox.Button(image=None, pos=(640, 500), text_input="QUIT", font=toolbox.get_font(
            75), base_color="#d7fcd4", hovering_color="Green")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for Button in [PLAY_Button, QUIT_Button]:
            Button.changeColor(MENU_MOUSE_POS)
            Button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_Button.checkForInput(MENU_MOUSE_POS):
                    play(SCREEN)
                if QUIT_Button.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play(SCREEN):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = toolbox.get_font(45).render(
            "This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        GAME_Button = toolbox.Button(image=None, pos=(640, 360), text_input="PLAY GAME", font=toolbox.get_font(
            75), base_color="WHITE", hovering_color="Green")
        PLAY_BACK = toolbox.Button(image=None, pos=(640, 460), text_input="BACK", font=toolbox.get_font(
            75), base_color="White", hovering_color="Green")

        GAME_Button.changeColor(PLAY_MOUSE_POS)
        GAME_Button.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if GAME_Button.checkForInput(PLAY_MOUSE_POS):
                    abalone.game(SCREEN)
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    BG = pygame.image.load('bg.png')
    pygame.display.set_caption('Game')
    main_menu(SCREEN, BG)
