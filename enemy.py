import pygame
import random

class Enemy():
    def __init__(self, x, y, img, limits):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.width = self.img.get_rect()[2]
        self.height = self.img.get_rect()[3]

        self.vx = 0
        self.vy = 0
        self.speedRange = [-0.2, 0, 0.2]
        self.updateMovTime = 0


        self.shootTime = 0
        self.shootDelay = 1600
        self.shots = []
        self.shootImg = "images/enemyShot.png"
        self.shootSpeed = 0.2

        self.limits = [[0, limits[0]], [0, limits[1]]]

    def draw(self, surf):
        surf.blit(self.img, (self.x, self.y))
        
        for c in self.shots:
            surf.blit(c[0], (c[1], c[2]))

    def shoot(self, dt):
        if self.shootTime <= 0:
            x = self.x + self.width/2 - 2
            y = self.y + self.height

            self.shots.append([pygame.image.load(self.shootImg), x, y])

            self.shootTime = self.shootDelay

        for c in self.shots:
            c[2] += 0.2 * dt

            if c[2] > self.limits[0][1]:
                self.shots.remove(c) 

        self.shootTime -= dt
        
    def chooseMov(self):
        return random.choice(self.speedRange), random.choice(self.speedRange)
    
    def updateMov(self, dt):
        self.updateMovTime += 1/dt

        if self.updateMovTime >= 5:
            self.vx, self.vy = self.chooseMov()
            self.updateMovTime = 0

        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.limits[0][0] > self.x and self.vx < 0 :
            self.vx *= -1
        elif self.x + self.width > self.limits[0][1] and self.vx > 0:
            self.vx *= -1

        if self.limits[1][0] > self.y and self.vy < 0 :
            self.vy *= -1
        elif self.y + self.height > self.limits[1][1] and self.vy > 0:
            self.vy *= -1