import pygame
import random
import math
from card_manager import CardManager, Card
from player import Player


# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 720))
clock = pygame.time.Clock()
running = True



# Constants
TILE_SIZE = 80
TILE_MARGIN = 2
TILE_IMAGE_MARGIN = 4
TILE_ORDINAL_NUMBER_MARGIN = 30
TILE_ORDINAL_NUMBER_TEXT_COLOR = (0, 0, 0)
TILE_COLOR_DARK = (100, 100, 100)
TILE_COLOR_LIGHT = (200, 200, 200)
TILE_COLOR_MOUSE_COLLIDE = (255, 255, 255)
BACKGROUND_COLOR = (255, 238, 177)
BOARD_BACKGROUND_COLOR = (255, 223, 108)
BOARD_SIZE = TILE_SIZE * 7 + TILE_ORDINAL_NUMBER_MARGIN

FONT = pygame.font.Font(None, size=30)



# Variables
players_list = []
players_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)] # temporal list
for i in range(4):
    p = Player("Gracz " + str(i+1), i, players_colors[i])
    players_list.append(p)

number_of_players = len(players_list)


card_manager = CardManager(players_list)
#temp for debug
card_manager.board[0][0] = Card(players_list[0], 'archer', 0, 0)
card_manager.board[1][0] = Card(players_list[0], 'healer', 1, 0)
card_manager.board[2][2] = Card(players_list[1], 'healer', 2, 2)
# end













#miejsce na funkcje w kodzie
def board_draw():
    board = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
    board.fill(BOARD_BACKGROUND_COLOR)

    x, y = TILE_ORDINAL_NUMBER_MARGIN - TILE_SIZE, TILE_ORDINAL_NUMBER_MARGIN - TILE_SIZE
    color = (0,0,0)
    for i in range(7):
        x += TILE_SIZE
        y = TILE_ORDINAL_NUMBER_MARGIN - TILE_SIZE
        for j in range(7):
            y += TILE_SIZE
            if (j%2==0 and i%2==0) or (i%2==1 and j%2==1): color = TILE_COLOR_DARK
            else: color = TILE_COLOR_LIGHT
            if not card_manager.is_tile_free(i, j):
                # if on the tile is any card use the player color for tile
                color = card_manager.board[i][j].player.color

            tile_rect = pygame.Rect(x, y, TILE_SIZE - TILE_MARGIN, TILE_SIZE - TILE_MARGIN)
            if tile_rect.collidepoint(pygame.mouse.get_pos()):
                # the mouse is colliding with the tile

                if card_manager.is_tile_free(i, j):
                    color = TILE_COLOR_MOUSE_COLLIDE

            pygame.draw.rect(board, color, tile_rect)

            if not card_manager.is_tile_free(i, j):
                # on the tile is any card
                card_image = pygame.image.load(card_manager.board[i][j].image_name)
                card_image = pygame.transform.scale(card_image, (TILE_SIZE - TILE_MARGIN - 2 * TILE_IMAGE_MARGIN, TILE_SIZE - TILE_MARGIN - 2 * TILE_IMAGE_MARGIN))
                board.blit(card_image, (x + TILE_IMAGE_MARGIN, y + TILE_IMAGE_MARGIN))


    # show ordinal numbers of tiles
    for i in range(2):
        for j in range(7):
            text = FONT.render(str(j + 1), True, TILE_ORDINAL_NUMBER_TEXT_COLOR)
            if i == 0:
                board.blit(text, (TILE_ORDINAL_NUMBER_MARGIN / 3, TILE_ORDINAL_NUMBER_MARGIN + (TILE_SIZE / 3) + (j * TILE_SIZE)))
            else:
                board.blit(text, (TILE_ORDINAL_NUMBER_MARGIN + (TILE_SIZE / 3) + (j * TILE_SIZE), TILE_ORDINAL_NUMBER_MARGIN / 3))

    screen.blit(board, (10, 10))










def stat_draw():
    x = 580
    y = 20
    for i in range(number_of_players):
        pygame.draw.rect(screen, (60,110,200), (x, y, 200, 60))
        text = FONT.render(f"{players_list[i].name}: {players_list[i].get_all_points()}", True, players_list[i].color)
        screen.blit(text, (x+10, y+20))
        y+=80

def end_turn_draw():
    pygame.draw.rect(screen, (200,50,0), (640, 480, 80, 80))
def end_turn():
    pass

def cards_draw():
    pass





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








while running:
    screen.fill((255, 238, 177))  # miejsce na board_draw()


    board_draw()
    stat_draw()
    end_turn_draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    # flip() przeniesienie modyfikacji powierzchni screen na display
    pygame.display.flip()

    clock.tick(60) # to jest nasze ograniczenie klatek
pygame.quit()