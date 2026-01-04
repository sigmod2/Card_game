import pygame
from player import Player

class PointsManager:
    def __init__(self, players: list[Player], turn: int, cards_left: int):
        self.turn = turn
        self.cards_left = cards_left

    ("to na pozniej jak juz bedzie stawianie normalnie dzialac")