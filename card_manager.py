'''
The file contain the whole card management and data containers for cards.
'''

import pygame
from player import Player


class Card:
    def __init__(self):
        self.player: Player = None
        self.card_class = -1

        self.positionX = -1 # number between 0-7 mean the board field, the -1 is out of the board
        self.positionY = -1






class CardManager:
    def __init__(self, players):
        '''
        :param players_names: list of players names
        '''
        self.board = [[None for i in range(7)] for j in range(7)]
        self.decks = [[] for i in range(len(players))]
        self.other_cards = []


        self.card_classes = ["Pikeman", "Miner", "Mage", "Archer", "Cannon", "Cavalery", "Healer"]

    def shuffle_cards(self, card_list):
        '''
        Shuffle the given list of cards.
        :return:
        '''
        ...


    def initialise_cards(self):
        '''
        Create all card and put them in the self.other_cards list.
        :return:
        '''
        ...


    def get_player_cards_on_board(self, player: Player):
        '''
        Iterate through the board and return a list of all given player's cards.
        :return: the list of player cards
        '''

        temp = []
        for i in self.board:
            for j in i:
                if j is not None and j.player == player:
                    temp.append(j)
        return temp


    def get_neighboring_cards_of_position(self, positionX: int, positionY: int):
        '''
        Get all cards from board neighboring of the given position. It dont get card of given position.
        :param positionX: the x position
        :param positionY: the y position
        :return: list of cards
        '''
        temp = []

        positions_to_check = [
            (positionX - 1, positionY),
            (positionX + 1, positionY),
            (positionX, positionY + 1),
            (positionX, positionY - 1),
        ]

        for p in positions_to_check:
            if p[0] < 0 or p[1] < 0 or p[0] >= 7 or p[1] >= 7:
                continue
            temp.append(self.board[p[0]][p[1]])
        return temp




if __name__ == "__main__":
    players_list = []
    for i in range(4):
        p = Player("Gracz " + str(i), i, (0, i * 50, 0))
        players_list.append(p)



    aaa = CardManager(players_list)

    aaa.board[0][0] = Card()
    aaa.board[0][0].player = players_list[0]
    aaa.board[0][1] = Card()
    aaa.board[0][2] = Card()

    print("fff ", aaa.get_player_cards_on_board(players_list[0]))


    print(aaa.board)