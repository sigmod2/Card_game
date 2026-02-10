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
            memory_thief = []
            mages = 0
            for i in range(7):
                for j in range(7):
                    if self.card_manager.board[i][j] != None and self.card_manager.board[i][j].player.index == index:
                        test+=1
                        if self.card_manager.board[i][j].card_class == 0:
                            self.players[index].current_points += 4
                            if 4 not in memory_thief: memory_thief.append(4)
                        elif self.card_manager.board[i][j].card_class == 1:
                            if self.card_manager.number_of_turns%4 == index:
                                self.hard_points[index] += 1
                            if 1 not in memory_thief: memory_thief.append(1)
                        elif self.card_manager.board[i][j].card_class == 2:
                            mages+=1
                        elif self.card_manager.board[i][j].card_class == 3:
                            num_of_infant +=1
                        elif self.card_manager.board[i][j].card_class == 4:
                            for x in range(-2, 3):
                                for y in range(-2, 3):
                                    try:
                                        if (i+x >= 0) and (j+y >= 0) and (abs(x)+abs(y) <=2):
                                            if (type(self.card_manager.board[i+x][j+y]) == Card) and self.card_manager.board[i+x][j+y].player.index != index:
                                                informants+=1
                                                print("informant on",i+x, j+y)
                                    except IndexError: pass
                            if informants*2 not in memory_thief: memory_thief.append(informants*2)
                        elif self.card_manager.board[i][j].card_class == 5:
                            self.players[index].current_points += 8
                            if 8 not in memory_thief: memory_thief.append(8)
                        elif self.card_manager.board[i][j].card_class == 6:
                            pass
                        elif self.card_manager.board[i][j].card_class == 7:
                            pass
            memory_thief.append(num_of_infant*num_of_infant)
            self.players[index].current_points+=num_of_infant*num_of_infant
            self.players[index].current_points += (informants*2)
            self.players[index].current_points += max(memory_thief)