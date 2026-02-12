import pygame
import random
import math
import threading

from points import PointsManager
from card_manager import CardManager, Card
from player import Player
import copy
from music import MusicManager

# pygame setup
pygame.init()
screen = pygame.display.set_mode((900, 800))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption('Seven cards - seven squares')
icon = pygame.image.load('images//icon.png')
pygame.display.set_icon(icon)



# Constants to nawet nie jest stala, trzeba zrobic jakies miejsce do deklaracji tych zmiennych bo sa w 10 roznych miejsach
FONT = pygame.font.Font(None, size=30)


# Variables
players_list = []
players_effects_list = [] #troche psuje c
players_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)] # temporal list
for i in range(4):
    p = Player("Gracz " + str(i+1), i, players_colors[i])
    players_list.append(p)
    players_effects_list.append("")

number_of_players = len(players_list)
current_player = players_list[0]

card_manager = CardManager(players_list)
card_manager.initialise_cards()
card_manager.shuffle_cards()
for i in range(number_of_players):
    card_manager.refill_deck(players_list[i])

points_manager = PointsManager(players_list, card_manager)



#tu se wcisne obiekty
music_manager = MusicManager('temp')





#temp for debug
 # end chwile mi zajelo znalezienie tego co mi modyfikuje card_menager.board


HEADLINE_HEIGHT = 30
GAME_NAME = "Seven Cards / 7C"
HEADLINE_COLOR = (255, 255, 255)
HEADLINE_R_L_MARGIN = 10


headline_text_info = "Although all hope is lost, let the battle begin..."

def headline_draw():
    '''
    Draw completely overdesigned headline
    '''
    rect = pygame.Rect(0, 0, screen.get_width(), HEADLINE_HEIGHT)
    pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    # font for the writing data
    number_of_letters = len(GAME_NAME) + len(headline_text_info)
    just_good_font_size = int(screen.get_width() / (number_of_letters / 2)) # the font size that makes the texts don't overlap in most common cases
    if just_good_font_size < HEADLINE_HEIGHT:
        # the texts too big
        writing_font = pygame.font.Font(None, size=just_good_font_size)
    else:
        # the texts in ideal size
        writing_font = pygame.font.Font(None, size=HEADLINE_HEIGHT)

    # game name
    name = writing_font.render(GAME_NAME, True, HEADLINE_COLOR)
    screen.blit(name, name.get_rect(midleft=rect.midleft, left=HEADLINE_R_L_MARGIN))

    # more infos, maybe about the last move
    info = writing_font.render(headline_text_info, True, HEADLINE_COLOR)
    screen.blit(info, info.get_rect(midright=rect.midright, right=screen.get_width()-HEADLINE_R_L_MARGIN))



BOARD_DESTINATION = (10, 50); '''Position when the board will be drawn'''
TILE_SIZE = 80; '''Real size of tile is {TILE_SIZE} - {TILE_MARGIN}'''
TILE_MARGIN = 2
TILE_IMAGE_MARGIN = 4
TILE_ORDINAL_NUMBER_MARGIN = 30
TILE_ORDINAL_NUMBER_TEXT_COLOR = (0, 0, 0)
TILE_COLOR_DARK = (100, 100, 100)
TILE_COLOR_LIGHT = (200, 200, 200)
TILE_COLOR_MOUSE_COLLIDE = (255, 255, 255)
BACKGROUND_COLOR = (255, 238, 177); '''Background color of the game window'''
BOARD_BACKGROUND_COLOR = (255, 223, 108); '''Background color of the board'''
BOARD_SIZE = TILE_SIZE * 7 + TILE_ORDINAL_NUMBER_MARGIN
CURRENTLY_SELECTED_CARD = None   #ważne w chuj, wszystko na tym stoi
CURRENTLY_SELECTED_CARD_DECK_INDEX = -1
VALID_CARD_SELECTED = False
CARD_HAS_BEEN_PLACED = False
another_usless_variable = -1
coords = [-1, -1]

global DESTRUCTION
DESTRUCTION = 0
drawing_mode = False
killing_mode = False

def board_draw():
    '''
    Draw board on the screen
    '''
    board = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
    board.fill(BOARD_BACKGROUND_COLOR)

    global drawing_mode
    global coords
    global killing_mode

    x, y = TILE_ORDINAL_NUMBER_MARGIN - TILE_SIZE, TILE_ORDINAL_NUMBER_MARGIN - TILE_SIZE
    color = (0,0,0)
    for i in range(7):
        x += TILE_SIZE
        y = TILE_ORDINAL_NUMBER_MARGIN - TILE_SIZE
        for j in range(7):
            y += TILE_SIZE
            if (j%2==0 and i%2==0) or (i%2==1 and j%2==1): color = TILE_COLOR_DARK
            else: color = TILE_COLOR_LIGHT
            if not card_manager.is_tile_free(i, j): #to powinna byc chyba osobna funkcja ale zostawiam jak jest
                # on the tile is any card use the player color for tile co?
                color = card_manager.board[i][j].player.color #ja chcialem zrobic inne grafiki dla roznych graczy
                #pass



            tile_rect = pygame.Rect(x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN)
            normalized_mouse_position = (pygame.mouse.get_pos()[0] - BOARD_DESTINATION[0], pygame.mouse.get_pos()[1] - BOARD_DESTINATION[1]) # it is required because when I use new surface it use different coordinate system than mouse
            if tile_rect.collidepoint(normalized_mouse_position):
                global DESTRUCTION
                global is_mouse_pressed
                global another_usless_variable
                # the mouse is colliding with the tile
                if card_manager.is_tile_free(i, j):
                    color = TILE_COLOR_MOUSE_COLLIDE
                    global VALID_CARD_SELECTED
                    global CURRENTLY_SELECTED_CARD
                    global CURRENTLY_SELECTED_CARD_DECK_INDEX
                    global CARD_HAS_BEEN_PLACED

                    if pygame.mouse.get_pressed()[0] and not is_mouse_pressed and VALID_CARD_SELECTED and is_valid(i,j, current_player) and not CARD_HAS_BEEN_PLACED:
                        is_mouse_pressed = True                                      #tutaj kladziona jest karta
                        card_manager.board[i][j] = CURRENTLY_SELECTED_CARD
                        CURRENTLY_SELECTED_CARD.is_selected = False
                        card_manager.decks[current_player.index].pop(CURRENTLY_SELECTED_CARD_DECK_INDEX)
                        card_manager.board[i][j].player = current_player #asigment playera bo potrzebne do kolorów, tymaczoswe
                        CARD_HAS_BEEN_PLACED = True
                        if CURRENTLY_SELECTED_CARD.card_class == 0:
                            DESTRUCTION = 1
                        if CURRENTLY_SELECTED_CARD.card_class == 2:
                            DESTRUCTION = 3
                        if CURRENTLY_SELECTED_CARD.card_class == 5:
                            DESTRUCTION = 1
                        if CURRENTLY_SELECTED_CARD.card_class in [0, 2, 5]:
                            coords = [i, j]
                            another_usless_variable = CURRENTLY_SELECTED_CARD.card_class
                            killing_mode = True

                        print(card_manager.board[i][j].player.index)
                        if CURRENTLY_SELECTED_CARD.card_class == 6: CARD_HAS_BEEN_PLACED = False  #jezeli koń to możemy postawic jeszcze jdna kartę
                        CURRENTLY_SELECTED_CARD = None
                        CURRENTLY_SELECTED_CARD_DECK_INDEX = -1
                        VALID_CARD_SELECTED = False
                        drawing_mode = False
                        music_manager.play_effect(0)

                    if not pygame.mouse.get_pressed()[0]:
                        is_mouse_pressed = False  #mega zawaliste rozwiązanie z tym is_mouse_pressed, super
                    #klikamy nie zeby postawic ale zeby zniszczyc
                else:
                    if pygame.mouse.get_pressed()[0] and DESTRUCTION > 0 and not is_mouse_pressed and destroable(i, j, coords):
                        if card_manager.board[i][j].player == current_player: continue  # jezeli zostala wybrana karta tego samego gracza to nie moze zostac zniszczona.
                        is_mouse_pressed = True
                        card_manager.board[i][j] = None
                        DESTRUCTION -=1
                        if DESTRUCTION == 0: killing_mode = False

                        if another_usless_variable == 0:
                            music_manager.play_effect(2)
                        elif another_usless_variable == 2:
                            music_manager.play_effect(3)
                        elif another_usless_variable == 5:
                            music_manager.play_effect(4)
                    if not pygame.mouse.get_pressed()[0]:
                        is_mouse_pressed = False


            if drawing_mode and is_valid(i, j, current_player) and card_manager.is_tile_free(i, j):
                color = (255, 0, 123)

            # draw tile
            pygame.draw.rect(board, color, tile_rect)

            # draw card if it should
            if not card_manager.is_tile_free(i, j):

                # on the tile is any card
                card_image = pygame.image.load(card_manager.board[i][j].image_name)
                card_image = pygame.transform.scale(card_image, (TILE_SIZE - TILE_MARGIN - 2 * TILE_IMAGE_MARGIN, TILE_SIZE - TILE_MARGIN - 2 * TILE_IMAGE_MARGIN))
                board.blit(card_image, (x + TILE_IMAGE_MARGIN, y + TILE_IMAGE_MARGIN))


    # show ordinal numbers of tiles aka draw numery boczne
    for i in range(2):
        for j in range(7):
            ordinal_number_font = pygame.font.Font(None, TILE_ORDINAL_NUMBER_MARGIN)
            if i == 0:
                # vertical numbers
                text = ordinal_number_font.render(str(j + 1), True, TILE_ORDINAL_NUMBER_TEXT_COLOR)
                text_rect = pygame.Rect(0, TILE_ORDINAL_NUMBER_MARGIN + TILE_SIZE * j, TILE_ORDINAL_NUMBER_MARGIN, TILE_SIZE)
            else:
                # horizontal numbers
                text = ordinal_number_font.render(chr(j+65), True, TILE_ORDINAL_NUMBER_TEXT_COLOR)
                text_rect = pygame.Rect(TILE_ORDINAL_NUMBER_MARGIN + TILE_SIZE * j, 0, TILE_SIZE, TILE_ORDINAL_NUMBER_MARGIN)
            board.blit(text, text.get_rect(center=text_rect.center))

    screen.blit(board, BOARD_DESTINATION)


STAT_DESTINATION = (620, 80)
STAT_BACKGROUND_COLOR = (60,110,200)
STAT_BACKGROUND_COLOR_OF_CURRENT_PLAYER = (200, 200, 200)
STAT_CELL_SIZE = (200, 60); '''It is real size'''
STAT_CELL_MARGIN = 30
STAT_PLAYER_NAME_MARGIN = 10

STAT_EFFECT_PLUS_COLOR = (0, 255, 0)
STAT_EFFECT_MINUS_COLOR = (255, 0, 0)
STAT_EFFECT_NEUTRAL_COLOR = (123, 123, 123)


players_effects_list = ["-1", "+5", "0", "grfv"]; '''The list with extra text info which is displayed near the player statistics. It has three states: if the text for player start with {+}, {-}, or others it will be shown in different color'''

def stat_draw():
    '''
    Draw statistics of players
    '''
    stat = pygame.Surface((STAT_CELL_SIZE[0], number_of_players * STAT_CELL_SIZE[1] + (number_of_players - 1) * STAT_CELL_MARGIN), pygame.SRCALPHA)
    x = 0
    y = 0
    for i in range(number_of_players):
        color = STAT_BACKGROUND_COLOR
        if current_player.index == i:
            # iteration step on player whose turn is
            color = STAT_BACKGROUND_COLOR_OF_CURRENT_PLAYER

        # current player cell rect
        rect = pygame.Rect(x, y, STAT_CELL_SIZE[0], STAT_CELL_SIZE[1])
        pygame.draw.rect(stat, color, rect)

        # player name text
        player_name = FONT.render(f"{players_list[i].name}: {players_list[i].get_all_points()}", True, players_list[i].color)
        stat.blit(player_name, player_name.get_rect(midleft=rect.midleft, left=STAT_PLAYER_NAME_MARGIN))

        # effect text
        if players_effects_list[i][0] == '+':
            color = STAT_EFFECT_PLUS_COLOR
        elif players_effects_list[i][0] == '-':
            color = STAT_EFFECT_MINUS_COLOR
        else:
            color = STAT_EFFECT_NEUTRAL_COLOR

        effect = FONT.render(players_effects_list[i], True, color)
        stat.blit(effect, effect.get_rect(center=rect.center, right=rect.right-STAT_PLAYER_NAME_MARGIN))

        # increment counter
        y += STAT_CELL_MARGIN + STAT_CELL_SIZE[1]

        screen.blit(stat, STAT_DESTINATION)


is_mouse_pressed = False

descriptions = []
f = open('descriptions.txt', 'r')
for i in f:
    descriptions.append(i.rstrip())
print(descriptions)
f.close()

def description_draw():
    font = pygame.font.Font(None, size=30)
    text1 = font.render(f"Name: {CURRENTLY_SELECTED_CARD.reversed_class_names_dict[CURRENTLY_SELECTED_CARD.card_class]}", True, (0, 0, 0))
    text2 = font.render(f"Description: {descriptions[CURRENTLY_SELECTED_CARD.card_class]}", True, (0,0,0))
 #trzeba napisac funkcje sprawdzjaca dlugosc tekstu, zrobic nowy syrface, podzielic desc na slowa i sprawdzac dlugosc tekstu  czy wychodzi za boksa
    screen.blit(text1, (620, 450))
    screen.blit(text2, (620, 470))

def end_turn_draw():
    '''
    Draw end turn  button
    '''
    rect = pygame.Rect(640, 680, 210, 80)  #zrobiłem na szybko i na oko i jest brzydko, trzeba będzie sie zajac pod koniec wyglądem
    font = pygame.font.Font(None, size=40)
    text = font.render("[ END TURN ]", True, (0,0,0))


    global is_mouse_pressed
    if rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] and not is_mouse_pressed:
        end_turn()
        is_mouse_pressed = True
    if not pygame.mouse.get_pressed()[0]:
        is_mouse_pressed = False

    ...
    pygame.draw.rect(screen, (100,50,0), rect)
    screen.blit(text, (660, 700))

def end_turn():
    global current_player
    global DESTRUCTION
    DESTRUCTION = 0
    global killing_mode
    killing_mode = False
    #istonty segment potrzebny do działania players effect list
    old_score = [x.current_points for x in players_list]
    points_manager.recount_points()
    new_score = [x.current_points for x in players_list]
    for i in range(len(players_list)):
        x = ""
        if new_score[i]-old_score[i] > 0: x="+"
        players_effects_list[i] = x + str(new_score[i]-old_score[i])


    card_manager.refill_deck(current_player)
    current_player_index = current_player.index #?
    current_player_index += 1
    if current_player_index == number_of_players:
        current_player_index = 0
    current_player = players_list[current_player_index]

    card_manager.board = rotate(card_manager.board)
    music_manager.play_effect(1)
    global CARD_HAS_BEEN_PLACED
    CARD_HAS_BEEN_PLACED = False

    card_manager.number_of_turns +=1
    global headline_text_info
    headline_text_info = f"The turn number {(card_manager.number_of_turns//4)+1}"

def rotate(n):
    unnecessary_copy = [[None] * 7 for _ in range(7)] #dupa sraka znalazlem w necie nwm czemu mi none samo nie dzialalo
    for i in range(7):
        for j in range(7):
            unnecessary_copy[6-j][i] = card_manager.board[i][j]
    return unnecessary_copy

DECK_DESTINATION = (50, 670)
DECK_CARD_SIZE = 100 # this is real size
DECK_MARGIN = 10
CURRENTLY_SELECTED_CARD: Card = None
CURRENTLY_SELECTED_CARD_DECK_INDEX = 0
VALID_CARD_SELECTED = False

def cards_draw():
    hand = pygame.Surface((DECK_CARD_SIZE * 5 + DECK_MARGIN * 5, DECK_CARD_SIZE + DECK_MARGIN))
    hand.fill(BACKGROUND_COLOR)

    for i in range(len(card_manager.decks[current_player.index])):
        global CURRENTLY_SELECTED_CARD
        global CURRENTLY_SELECTED_CARD_DECK_INDEX
        global VALID_CARD_SELECTED
        global drawing_mode

        rect = pygame.Rect(i * DECK_CARD_SIZE + i * DECK_MARGIN + DECK_MARGIN/2, DECK_MARGIN/2, DECK_CARD_SIZE, DECK_CARD_SIZE + DECK_MARGIN)
        image = pygame.image.load(card_manager.decks[current_player.index][i].image_name)
        normalized_mouse_position = (pygame.mouse.get_pos()[0] - DECK_DESTINATION[0], pygame.mouse.get_pos()[1] - DECK_DESTINATION[1])
        if rect.collidepoint(normalized_mouse_position) or (VALID_CARD_SELECTED and CURRENTLY_SELECTED_CARD_DECK_INDEX == i):
            image = pygame.transform.scale(image, (DECK_CARD_SIZE + DECK_MARGIN, DECK_CARD_SIZE + DECK_MARGIN))
            rect.x -= DECK_MARGIN / 2
            rect.y -= DECK_MARGIN / 2

            if pygame.mouse.get_pressed()[0] and not card_manager.decks[current_player.index][i].is_selected:
                image = pygame.transform.scale(image, (DECK_CARD_SIZE + DECK_MARGIN, DECK_CARD_SIZE + DECK_MARGIN))
                card_manager.decks[current_player.index][i].is_selected = True
                CURRENTLY_SELECTED_CARD = card_manager.decks[current_player.index][i]
                CURRENTLY_SELECTED_CARD_DECK_INDEX = i
                VALID_CARD_SELECTED = True
                drawing_mode = True
            elif pygame.mouse.get_pressed()[0] and card_manager.decks[current_player.index][i].is_selected:
                card_manager.decks[current_player.index][i].is_selected = False

        else:
            image = pygame.transform.scale(image, (DECK_CARD_SIZE, DECK_CARD_SIZE))
        hand.blit(image, (rect.x, rect.y))
    screen.blit(hand, DECK_DESTINATION)

def is_valid(i: int, j: int, current_player: Player):
    if (i==3 and j==6): return True
    if j!=6:
        if (type(card_manager.board[i][j+1]) == Card) and (card_manager.board[i][j+1].player == current_player): return True
    if j!=0:
        if (type(card_manager.board[i][j-1]) == Card) and (card_manager.board[i][j-1].player == current_player): return True
    if i!=0:
        if (type(card_manager.board[i-1][j]) == Card) and (card_manager.board[i-1][j].player == current_player): return True
    if i!=6:
        if (type(card_manager.board[i+1][j]) == Card) and (card_manager.board[i+1][j].player == current_player): return True
    if CURRENTLY_SELECTED_CARD != None:
        if CURRENTLY_SELECTED_CARD.card_class == 4: return True
    return False

def destroable(i, j, coords):
    if another_usless_variable == 5:
        try:
            if ([i, j+2] == coords or [i, j+3] == coords or
                [i, j-2] == coords or [i, j-3] == coords or
                [i+2, j] == coords or [i+3, j] == coords or
                [i-2, j] == coords or [i-3, j] == coords):
                return True
        except IndexError: pass
        return False
    else:
        if j!=6:
            if [i, j+1] == coords: return True
        if j!=0:
            if [i, j-1] == coords: return True
        if i!=0:
            if [i-1, j] == coords: return True
        if i!=6:
            if [i+1, j] == coords: return True
        return False

def game_end():
    screen.fill((0,0,0))
    font = pygame.font.Font(None, size=30)
    text = font.render("Wygrała Hiszpańska Inkwizycja - tego nikt sie nie spodziewał", True, (255,255,255))
    screen.blit(text, (100, 300))



'''
#wgrywanie obrazków
card_img = pygame.image.load("images/temp.jpg").convert_alpha() # dla img z transparencją
card_img = pygame.transform.scale(card_img, (128,128))
card_img.set_colorkey((0,0,0))
card_img.set_alpha(40) # przeźroczystość

#można równiez tworzyć wlasne surface i póżniej te powierzchnie .blit na surface jaką jest screen eg.

cards = pygame.Surface((400,400), pygame.SRCALPHA)
cards.blit(card_img, (0, 20))
cards.blit(card_img, (10, 30))

#ważny temat, rect-y
kwadrat1 = pygame.Rect(0,0,50,50) #pozycjja, wymiary
kwadrat2 = pygame.Rect(300,300,300,300) #pozycjja, wymiary
kolizja = kwadrat1.colliderect(kwadrat2) #zwraca true or false
pygame.draw.rect(screen,(100,100,100), kwadrat2) #surface, color, what rectangle to draw
'''
#threading.Thread(target=music_manager.play_background_music, daemon=True).start()

while running:
    print(drawing_mode)
    if card_manager.number_of_turns // 4 == 20: game_end()
    else:
        screen.fill((255, 238, 177))  # miejsce na board_draw()

        headline_draw()
        board_draw()
        stat_draw()
        cards_draw()
        end_turn_draw()
        if VALID_CARD_SELECTED: description_draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # print(card_manager.board)
    # flip() przeniesienie modyfikacji powierzchni screen na display
    pygame.display.flip()

    clock.tick(60) # to jest nasze ograniczenie klatek
pygame.quit()