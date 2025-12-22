import pygame
import random
import math

# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 720))
clock = pygame.time.Clock()
running = True

#miejsce na funkcje w kodzie
def board_draw():
    x, y = 0, 0
    color = (0,0,0)
    for i in range(7):
        x=i*80
        for j in range(7):
            y=j*80
            if (j%2==0 and i%2==0) or (i%2==1 and j%2==1): color = (200,200,200)
            else: color = (100,100,100)
            pygame.draw.rect(screen, color, (x , y, 78, 78))

def stat_draw():
    x = 580
    y = 20
    for i in range(NumberOfPlayers):
        pygame.draw.rect(screen, (60,110,200), (x, y, 200, 60))
        text = font.render(f"Gracz {str(i+1)}: {punkty[i]}", True, (255, 255, 255))
        screen.blit(text, (x+10, y+20))
        y+=80

def end_turn_draw():
    pygame.draw.rect(screen, (200,50,0), (640, 480, 80, 80))
def end_turn():
    pass

def cards_draw():
    pass

#plansza gry
board = [["","","","","","",""],
         ["","","","","","",""],
         ["","","","","","",""],
         ["","","","","","",""],
         ["","","","","","",""],
         ["","","","","","",""],
         ["","","","","","",""]]

#dostępny karty
classes = ["Pikeman", "Miner", "Mage", "Archer", "Cannon", "Cavalery", "Healer"]

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

#miejsce za potrzebne zmienne
NumberOfPlayers = 4
punkty = [0,0,0,0]
font = pygame.font.Font(None, size=30)
decks = []

for i in range(NumberOfPlayers):
    deck = []
    for j in range(15):
        deck.append(classes[random.randint(1, 100)%7])
    decks.append(deck)


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