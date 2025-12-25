'''
The file contain the whole card management and data containers for cards.
'''

import pygame
from player import Player





class Card:
    def __init__(
            self,
            player: Player = None,
            card_class: int | str = -1,
            row: int = -1,
            column: int = -1,
    ):
        '''
        :param player: Player object to whom the card belongs
        :param card_class: int index of class or string name of class. Recommended value in string.
        :param row: number between 0-7 mean the board tile, the -1 is out of the board
        :param column: number between 0-7 mean the board tile, the -1 is out of the board
        '''

        self.images_list = [
            "images\\Archer.png",
            "images\\Healer.png",
            "images\\Mage.png",
            "images\\Pikeman.png"
        ]

        self.class_names_dict = {
            'archer' : 0,
            'healer' : 1,
            'mage' : 2,
            'pikeman' : 3
        }

        self.player: Player = player

        if type(card_class) is int:
            self.card_class = card_class
        elif type(card_class) is str:
            self.card_class = self.class_names_dict[card_class]

        self.row = row
        self.column = column

        self.image_name = None
        self.set_class_by_index(self.card_class)


    def set_class_by_index(self, card_class: int):
        '''
        Set the class of card by a given integer index
        :param card_class: card_class of the card as int index
        '''
        if card_class == -1:
            return -1
        self.card_class = card_class
        self.image_name = self.images_list[card_class]


    def set_class_by_text(self, image_name: str):
        '''
        Set the class of card by a given string name
        :param image_name: card_class of the card as string name
        '''
        self.set_class_by_index(self.class_names_dict[image_name])






class CardManager:
    def __init__(self, players: list[Player]):
        '''
        :param players_names: list of players
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


    def get_neighboring_cards_of_position(self, row: int, column: int):
        '''
        Get all cards from board neighboring of the given position. It don't get card of given position.
        :param row: the x position
        :param column: the y position
        :return: list of cards
        '''
        temp = []

        positions_to_check = [
            (row - 1, column),
            (row + 1, column),
            (row, column + 1),
            (row, column - 1),
        ]

        for p in positions_to_check:
            if p[0] < 0 or p[1] < 0 or p[0] >= 7 or p[1] >= 7:
                continue
            temp.append(self.board[p[0]][p[1]])
        return temp


    def can_put_card_on_coordinates(self, row: int, column: int):
        ...


    def is_tile_free(self, row: int, column: int):
        '''
        Check if given position is free of cards.
        '''
        if self.board[row][column] is None:
            return True
        else:
            return False



if __name__ == "__main__":
    players_list = []
    for i in range(4):
        p = Player("Gracz " + str(i), i, (0, i * 50, 0))
        players_list.append(p)



    aaa = CardManager(players_list)

    aaa.board[0][0] = Card(players_list[0], 'mage', 0, 0)
    print(aaa.board[0][0].image_name)
    aaa.board[0][1] = Card()
    aaa.board[0][2] = Card()

    print("fff ", aaa.get_player_cards_on_board(players_list[0]))


    print(aaa.board)