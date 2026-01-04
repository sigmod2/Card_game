'''
The file contain the whole card management and data containers for cards.
'''

import pygame
from player import Player
import random

MAX_NUMBER_OF_CARDS_IN_DECK = 5


class Card:
    def __init__(
            self,
            player: Player = None,
            card_class: int | str = -1,
            row: int = -1,
            column: int = -1,
            is_selected: bool = False
    ):
        '''
        :param player: Player object to whom the card belongs
        :param card_class: int index of class or string name of class. Recommended value in string.
        :param row: number between 0-7 mean the board tile, the -1 is out of the board
        :param column: number between 0-7 mean the board tile, the -1 is out of the board
        param selected to czy wybrana mowi i jest mi potrzebny
        '''

        self.images_list = [
            "images\\Archer.png",
            "images\\Healer.png",
            "images\\Mage.png",
            "images\\Pikeman.png",
            "images\\SecretAgent.png",
            "images\\Trebuchet.png",
            "images\\Cavalry.png",
            "images\\temp.png"
        ]
        self.is_selected = False

        self.class_names_dict = {
            'archer' : 0,
            'healer' : 1,
            'mage' : 2,
            'pikeman' : 3,
            'secretagent': 4,
            'trebuchet': 5,
            'cavalry': 6,
            'temp': 7
        }

        self.reversed_class_names_dict = {
            -1: 'None',
            0: 'archer',
            1: 'healer',
            2: 'mage',
            3: 'pikeman',
            4: 'secretagent',
            5: 'trebuchet',
            6: 'cavalry',
            7: 'temp'
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


    def __repr__(self):
        '''
        It is for human-readable representation when printing this class
        '''
        return "Card: \"" + str(self.player) + "\" " + self.reversed_class_names_dict[self.card_class]


class CardManager:
    def __init__(self, players: list[Player]):
        '''
        :param players_names: list of players
        '''
        self.board = [[None for i in range(7)] for j in range(7)]
        self.decks = [[] for i in range(len(players))]
        self.other_cards = []
        self.card_classes = ["Pikeman", "SecretAgent", "Mage", "Archer", "Trebuchet", "Cavalry", "Healer", "temp"]

    def shuffle_cards(self):
        '''
        Shuffle the self.other_cards list of cards  takie o napisalem, lepszego nie potrzeba
        '''
        for i in range(random.randint(5,10)):
            for index in range(len(self.other_cards)):
                num = random.randint(0, len(self.other_cards )-1)
                memory = self.other_cards[index]
                self.other_cards[index] = self.other_cards[num]
                self.other_cards[num]  = memory


    def initialise_cards(self):
        '''
        Create all card and put them in the self.other_cards list.
        '''
        amount_of_specific_cards = {
            'archer': 8,
            'healer': 10,
            'mage': 4,
            'pikeman': 10,
            'secretagent': 6,
            'trebuchet': 8,
            'cavalry': 18
        }
        for card_class, amount in amount_of_specific_cards.items():
            for i in range(amount):
                self.other_cards.append(Card(card_class=card_class))


    def refill_deck(self, player: Player):
        while (len(self.decks[player.index]) < MAX_NUMBER_OF_CARDS_IN_DECK) or (len(self.other_cards) == 0):
            self.decks[player.index].append(self.other_cards[0])
            self.other_cards.pop(0)

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


'''
if __name__ == "__main__":
    players_list = []
    for i in range(4):
        p = Player("Gracz " + str(i), i, (0, i * 50, 0))
        players_list.append(p)



    aaa = CardManager(players_list)
    aaa.initialise_cards()
    aaa.decks[0].append(Card(players_list[0]))
    aaa.refill_deck(players_list[0])
    print(aaa.decks[0])

    aaa.board[0][0] = Card(players_list[0], 'mage', 0, 0)
    print(aaa.board[0][0].image_name)
    print(aaa.board[0][1])
    aaa.board[0][1] = Card()
    aaa.board[0][2] = Card()

    print("fff ", aaa.get_player_cards_on_board(players_list[0]))


    print(aaa.board)
'''