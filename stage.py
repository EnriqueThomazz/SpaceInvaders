import pygame
from enemy import *

class Stage():
    def __init__(self, num):
        self.num = num

        self.enemies = []
        self.currEnemies = []

        self.boss = None


    def updateEnemies(self, surf, dt):
        if len(self.currEnemies) == 0 and len(self.enemies) != 0:
            self.currEnemies = (self.enemies.pop(0))

        for c in self.currEnemies:
            c.draw(surf)
            c.shoot(dt)
            c.updateMov(dt)