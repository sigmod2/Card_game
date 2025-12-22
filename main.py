import pygame

# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((720, 720))
clock = pygame.time.Clock()
running = True

#miejsce na funkcje w kodzie
def board_draw():
    x, y = 0, 0
    color = (0,0,0)
    for i in range(7):
        x=i*64
        for j in range(7):
            y=j*64
            if i%2==0:
                if j%2==0: color = (200,200,200)
                else: color = (100,100,100)
            else:
                if j%2==0: color = (100,100,100)
                else: color = (200,200,200)
            pygame.draw.rect(screen, color, (x , y, 64, 64))


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

#wgrywanie obrazków
card_img = pygame.image.load("images/temp.jpg").convert_alpha() # dla img z transparencją
card_img = pygame.transform.scale(card_img, (128,128))
card_img.set_colorkey((0,0,0))
card_img.set_alpha(40) # przeźroczystość

#można równiez tworzyć wlasne surface i póżniej te powierzchnie .blit na surface jaką jest screen eg.
cards = pygame.Surface((400,400), pygame.SRCALPHA)
cards.blit(card_img, (0, 20))
cards.blit(card_img, (10, 30))

#można rónież pisać jeśli byloby to potrzebne
font = pygame.font.Font(None, size=30)
"""
text = font.render("Hello world ", True, (0,0,0))
screen.blit(text,(50,300))   wyświetlajie tekstu, to oczywiscie w loopie
    """

#ważny temat, rect-y
kwadrat1 = pygame.Rect(0,0,50,50) #pozycjja, wymiary
kwadrat2 = pygame.Rect(300,300,300,300) #pozycjja, wymiary
kolizja = kwadrat1.colliderect(kwadrat2) #zwraca true or false
pygame.draw.rect(screen,(100,100,100), kwadrat2) #surface, color, what rectangle to draw

while running:
    screen.fill((255,255,255))  # miejsce na board_draw()
    #słynne event_loop
    board_draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #pygame.draw.rect(screen,(255,100,100), kwadrat2)
    #screen.blit(cards, (0,0))

    # flip() przeniesienie modyfikacji powierzchni screen na display
    pygame.display.flip()

    clock.tick(60) # to jest nasze ograniczenie klatek
pygame.quit()