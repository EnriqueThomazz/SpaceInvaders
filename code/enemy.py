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
        self.speedRange = [-0.3, 0, 0.3]
        self.updateMovTime = 4

        self.shootTime = 0
        self.shootDelay = 1600
        self.shootImg = "images/enemyShot.png"        

        self.limits = [[0, limits[0]], [0, limits[1]]]

    def draw(self, surf):
        surf.blit(self.img, (self.x, self.y))

    def shoot(self, dt):
        self.shootTime -= dt

        if self.shootTime <= 0:
            x = self.x + self.width/2 - 2
            y = self.y + self.height
            
            self.shootTime = self.shootDelay

            sht = [pygame.image.load(self.shootImg), x, y]

            return sht       

        return -1
        
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