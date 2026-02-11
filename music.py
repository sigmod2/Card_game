import pygame
import time

class MusicManager:
    def __init__(self, temp):
        self.temp = temp
        self.soundtracks_list = [
            "music\\Beer and Women.mp3",
            "music\\Evening in the Tavern.mp3",
            "music\\Tavern.mp3",
            "music\\Tavern at the End of World.mp3",
            "music\\The Heathen.mp3"]
        self.effectstracks_list = [
            "music\\card-placement.mp3",
            "music\\flipcard.mp3",
            "music\\arrow_hit.mp3",
            "music\\fireball.mp3",
            "music\\trebuchet.mp3"]
        self.soundtracks_lenghts = [
            110,
            57,
            77,
            85,
            188
        ]

    def play_music(self, track_number: int):
        tracks = {}
        for i in range(len(self.soundtracks_list)):
            tracks[i] = pygame.mixer.Sound(self.soundtracks_list[i])
        tracks[track_number].play()

    '''na razie tak, zmodyfikuje to wszystko tak, zeby jak skonczy sie grac jeden soundtrack to zaczynal nastepny'''
    def play_effect(self, effect_number: int):
        effects = {}
        for i in range(len(self.effectstracks_list)):
            effects[i] = pygame.mixer.Sound(self.effectstracks_list[i])
        effects[effect_number].play()

    def play_background_music(self):
        tracks = {}
        num = 0
        for i in range(len(self.soundtracks_list)):
            tracks[i] = pygame.mixer.Sound(self.soundtracks_list[i])

        while True:
            tracks[num].play()
            time.sleep(self.soundtracks_lenghts[num])
            num+=1
            if num == len(self.soundtracks_list): num = 0


    def paths(self):
        pass
