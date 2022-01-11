import pygame
import os
from input_boxes import InputBox

# Game Initialization
pygame.init()
pygame.mixer.init()

click_sound = pygame.mixer.Sound('sound/clicksound.ogg')
click_sound.set_volume(1.0)

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width=900
screen_height=900
screen=pygame.display.set_mode((screen_width, screen_height))

# Text Renderer
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)

    return newText


# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

# Game Fonts
font = "Retro.ttf"


# Game Framerate
clock = pygame.time.Clock()
FPS=30

# Main Menu
def main_menu(level, comp_or_player, player1_name, player2_name):

    menu=True
    while menu:
        selected = ''
        # Main Menu UI
        screen.fill(white)
        title=text_format("Dungeon Dash", font, 90, gray)

        title_rect=title.get_rect()
        start_rect=pygame.Rect(375, 300, 150, 66)
        options_rect=pygame.Rect(352, 360, 196, 66)
        quit_rect=pygame.Rect(395, 420, 111, 66)
        # start_rect=pygame.Rect(0, 0, 150, 66)
        # options_rect=pygame.Rect(0, 0, 196, 66)
        # quit_rect=pygame.Rect(0, 0, 111, 66)

        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            selected = "start"
        if options_rect.collidepoint(mouse_pos):
            selected = "options"
        if quit_rect.collidepoint(mouse_pos):
            selected = "quit"

        if selected=="start":
            text_start=text_format("START", font, 75, blue)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="options":
            text_options=text_format("OPTIONS", font, 75, blue)
        else:
            text_options = text_format("OPTIONS", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, blue)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (start_rect.x, start_rect.y))
        screen.blit(text_options, (options_rect.x, options_rect.y))
        screen.blit(text_quit, (quit_rect.x, quit_rect.y))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if selected=="start":
                    menu = False
                if selected=="quit":
                    pygame.quit()
                    quit()
                if selected=="options":
                    level, comp_or_player, player1_name, player2_name = \
                        options_menu(level, comp_or_player, player1_name, player2_name)

            # if event.type==pygame.KEYDOWN:
            #     if event.key==pygame.K_UP:
            #         if selected == "quit":
            #             selected = "options"
            #         else:
            #             selected="start"
            #     elif event.key==pygame.K_DOWN:
            #         if selected == "start":
            #             selected = "options"
            #         else:
            #             selected="quit"
            #     if event.key==pygame.K_RETURN:
            #         if selected=="start":
            #             menu = False
            #         if selected=="quit":
            #             pygame.quit()
            #             quit()
            #         if selected=="options":
            #             options_menu()

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Dungeon Dash - Menu")
    return level, comp_or_player, player1_name, player2_name

#Initialize the Game
# main_menu()
# pygame.quit()
# quit()

def options_menu(level, comp_or_player, player1_name, player2_name):

    menu=True
    input_box1 = InputBox(100, 415, 200, 40, player1_name)
    input_box2 = InputBox(100, 535, 200, 40, player2_name)
    input_boxes = [input_box1, input_box2]
    # text_easy = text_format("EASY", font, 75, blue)
    # text_medium = text_format("MEDIUM", font, 75, blue)
    # text_hard = text_format("HARD", font, 75, blue)
    # text_computer = text_format("COMPUTER", font, 75, blue)
    # text_player = text_format("PLAYER", font, 75, blue)
    # text_opponent = text_format("OPPONENT", font, 75, blue)
    # text_level = text_format("LEVEL", font, 75, blue)
    # text_player1 = text_format("PLAYER 1", font, 75, blue)
    # text_player2 = text_format("PLAYER 2", font, 75, blue)
    # for r in [text_easy,text_medium,text_hard,text_computer,text_player,text_opponent,text_level,text_player1,text_player2]:
    #     print(r.get_rect())

    chosen_level = level
    chosen_player = comp_or_player
    while menu:
        selected = ''
        # Main Menu UI
        screen.fill(white)
        title=text_format("OPTIONS", font, 90, gray)

        title_rect=title.get_rect()
        easy_rect=pygame.Rect(375, 400, 120, 66)
        medium_rect=pygame.Rect(375, 460, 176, 66)
        hard_rect=pygame.Rect(375, 520, 120, 66)
        player_rect=pygame.Rect(600, 400, 180, 66)
        computer_rect=pygame.Rect(600, 460, 245, 66)
        back_rect=pygame.Rect(600, 600, 120, 66)
        # start_rect=pygame.Rect(0, 0, 150, 66)
        # options_rect=pygame.Rect(0, 0, 196, 66)
        # quit_rect=pygame.Rect(0, 0, 111, 66)

        mouse_pos = pygame.mouse.get_pos()
        if easy_rect.collidepoint(mouse_pos):
            selected = "easy"
        if medium_rect.collidepoint(mouse_pos):
            selected = "medium"
        if hard_rect.collidepoint(mouse_pos):
            selected = "hard"
        if computer_rect.collidepoint(mouse_pos):
            selected = "computer"
        if player_rect.collidepoint(mouse_pos):
            selected = "player"
        if back_rect.collidepoint(mouse_pos):
            selected = "back"

        if chosen_player == 'player':
            text_easy=text_format("EASY", font, 75, gray)
        elif selected=="easy" or chosen_level == 'easy':
            text_easy=text_format("EASY", font, 75, blue)
        else:
            text_easy = text_format("EASY", font, 75, black)
        if chosen_player == 'player':
            text_medium = text_format("MEDIUM", font, 75, gray)
        elif selected=="medium" or chosen_level == 'medium':
            text_medium=text_format("MEDIUM", font, 75, blue)
        else:
            text_medium = text_format("MEDIUM", font, 75, black)
        if chosen_player == 'player':
            text_hard = text_format("HARD", font, 75, gray)
        elif selected=="hard" or chosen_level == 'hard':
            text_hard=text_format("HARD", font, 75, blue)
        else:
            text_hard = text_format("HARD", font, 75, black)
        if selected=="player" or chosen_player == 'player':
            text_player=text_format("PLAYER", font, 75, blue)
        else:
            text_player = text_format("PLAYER", font, 75, black)
        if selected=="computer" or chosen_player == 'computer':
            text_computer=text_format("COMPUTER", font, 75, blue)
        else:
            text_computer = text_format("COMPUTER", font, 75, black)
        if selected=="back":
            text_back=text_format("BACK", font, 75, blue)
        else:
            text_back = text_format("BACK", font, 75, black)

        text_level_header = text_format("LEVEL", font, 75, green)
        text_player_header = text_format("OPPONENT", font, 75, green)
        text_player1_header = text_format("PLAYER 1", font, 75, green)
        text_player2_header = text_format(f'{"PLAYER 2" if chosen_player == "player" else "COMPUTER"}', font, 75, green)

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_easy, (easy_rect.x, easy_rect.y))
        screen.blit(text_medium, (medium_rect.x, medium_rect.y))
        screen.blit(text_hard, (hard_rect.x, hard_rect.y))
        screen.blit(text_player, (player_rect.x, player_rect.y))
        screen.blit(text_computer, (computer_rect.x, computer_rect.y))
        screen.blit(text_level_header, (easy_rect.x, easy_rect.y - 60))
        screen.blit(text_player_header, (player_rect.x, player_rect.y - 60))
        screen.blit(text_player1_header, (100, easy_rect.y - 60))
        screen.blit(text_player2_header, (100, medium_rect.y))
        screen.blit(text_back, (back_rect.x, back_rect.y))

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_click = True
                if selected=="easy":
                    if chosen_player == 'player':
                        play_click = False
                    chosen_level = 'easy'
                if selected=="medium":
                    if chosen_player == 'player':
                        play_click = False
                    chosen_level = 'medium'
                if selected=="hard":
                    if chosen_player == 'player':
                        play_click = False
                    chosen_level = 'hard'
                if selected=="player":
                    chosen_player = 'player'
                if selected=="computer":
                    chosen_player = 'computer'
                if selected=="back":
                    menu=False
                if play_click:
                    click_sound.play()
            for box in input_boxes:
                box.handle_event(event)

            # if event.type==pygame.KEYDOWN:
            #     if event.key==pygame.K_UP:
            #         if selected == "quit":
            #             selected = "options"
            #         else:
            #             selected="start"
            #     elif event.key==pygame.K_DOWN:
            #         if selected == "start":
            #             selected = "options"
            #         else:
            #             selected="quit"
            #     if event.key==pygame.K_RETURN:
            #         if selected=="start":
            #             menu = False
            #         if selected=="quit":
            #             pygame.quit()
            #             quit()
            #         if selected=="options":
            #             options_menu()

        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Dungeon Dash - Menu")

    return chosen_level, chosen_player, input_box1.text, input_box2.text
