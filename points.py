import pygame


from player import Player
from card_manager import Card, CardManager


class PointsManager:
    def __init__(self, players: list[Player], card_manager: CardManager):
        self.turn = 1
        self.cards_left = 40
        self.players = players
        self.card_manager = card_manager
        self.hard_points = [0,0,0,0]

    def recount_points(self):

        self.players[0].current_points = self.hard_points[0]
        self.players[1].current_points = self.hard_points[1]
        self.players[2].current_points = self.hard_points[2]
        self.players[3].current_points = self.hard_points[3]
        for index in range(4):
            num_of_infant = 0
            test  = 0
            informants = 0

            mages = 0
            for i in range(7):
                for j in range(7):
                    if self.card_manager.board[i][j] != None and self.card_manager.board[i][j].player.index == index:
                        test+=1
                        if self.card_manager.board[i][j].card_class == 0:    #archer
                            self.players[index].current_points += 4

                        elif self.card_manager.board[i][j].card_class == 1:   #healer
                            print("debug")
                            if self.card_manager.number_of_turns%4 == index:
                                self.hard_points[index] += 1
                                self.players[index].current_points += 1

                        elif self.card_manager.board[i][j].card_class == 2:    #mage
                            self.players[index].current_points += self.get_max_of_board()
                        elif self.card_manager.board[i][j].card_class == 3:    #pikeman
                            num_of_infant +=1
                            print("Infantry spotted, current num:", num_of_infant)
                        elif self.card_manager.board[i][j].card_class == 4:    #secret agent
                            for x in range(-2, 3):
                                for y in range(-2, 3):
                                    try:
                                        if (i+x >= 0) and (j+y >= 0) and (abs(x)+abs(y) <=2):
                                            if (type(self.card_manager.board[i+x][j+y]) == Card) and self.card_manager.board[i+x][j+y].player.index != index:
                                                informants+=1
                                                print("informant on",i+x, j+y)
                                    except IndexError: pass

                        elif self.card_manager.board[i][j].card_class == 5:   #trebuchet
                            self.players[index].current_points += 8

                        elif self.card_manager.board[i][j].card_class == 6:    #cavlary
                            self.players[index].current_points += 7  #kawaleria daje 7 punktów i przyzywa swołocz

                        elif self.card_manager.board[i][j].card_class == 7:    #temporary placement
                            pass
            #koniec sprawdzania planszy dla danego gracza.


            self.players[index].current_points += (num_of_infant*num_of_infant)
            self.players[index].current_points += (informants*2)

            print("player", index + 1, "total num od cards:", test, "current points", self.players[index].current_points)
    def get_max_of_board(self):
        memory_thief = []
        for i in range(7):
            for j in range(7):
                # tutaj powinnismy sprawdzic wartosc kazdej karty i znalezc maksa
                pass
        return 0