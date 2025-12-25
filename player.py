'''
The file contain the player class, in which you can store all player data but not cards.
'''

import pygame

class Player:
    def __init__(self, name: str, index: int, color: (int, int, int)):
        '''
        :param name: name of the player
        :param index: index of player's deck or sth similar. Must be different for each player.
        :param color: displayed color of player in the board
        '''
        self.name = name
        self.index = index
        self.current_points = 10
        self.extra_points = 0

        self.color = color


    def get_all_points(self):
        return self.current_points + self.extra_points



    def __eq__(self, other):
        if other is not None:
            return self.index == other.index
        else:
            return False


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name