import pygame
from enemy import *

class Stage():
    def __init__(self, num, limits):
        self.num = num

        self.enemies = []
        self.currEnemies = []

        self.shots = []
        self.shootSpeed = 0.2

        self.limits = [[0, limits[0]], [0, limits[1]]]

        self.boss = None


    def updateEnemies(self, surf, dt):
        if len(self.currEnemies) == 0 and len(self.enemies) != 0:
            self.currEnemies = (self.enemies.pop(0))

        for c in self.currEnemies:
            c.draw(surf)
            c.updateMov(dt)

            #Handling the shots
            sht = c.shoot(dt)
            if sht != -1:                
                self.shots.append(sht)

        #Update shot's y and drawing
        for c in self.shots:
            c[2] += self.shootSpeed * dt                

            #Removing if off limits
            if c[2] > self.limits[1][1]:
                self.shots.remove(c)

            surf.blit(c[0], (c[1], c[2]))

    def updateBoss(self, surf, dt):
        self.boss.update(surf, dt)
        atk = self.boss.attack(surf, dt)
        if atk != 'pilar' and atk != 'none':
            for c in range(atk[1]):
                self.currEnemies.append(Enemy(30 * c, 0, "images/enemy2.png", [self.limits[0][1], self.limits[1][1]]))

    def isClear(self):
        if len(self.enemies) == 0 and len(self.currEnemies) == 0 and self.boss == None:
            return 1
        return -1
            


            