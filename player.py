import pygame

class Player():
    def __init__(self, img, limits):
        self.x = 0
        self.y = 0
        self.speed = 0.2
        self.image = pygame.image.load(img)
        self.width = 64
        self.height = 64

        self.health = 3

        self.shootImg = "images/shot.png"
        self.shots = []
        self.timeShot = 0
        self.shootDelay = 300

        self.limits = [[0, limits[0]], [0, limits[1]]]

        self.stage = 1

    def draw(self, surf):
        surf.blit(self.image, (self.x, self.y))

        for c in self.shots:
            surf.blit(c[0], (c[1], c[2]))

            if c[2] + 8 < 0:
                self.shots.remove(c)           


    def move(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.x += self.speed * dt
        if keys[pygame.K_w]:
            self.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.y += self.speed * dt

        if self.limits[0][0] > self.x:
            self.x = self.limits[0][0]

        elif self.x + self.width > self.limits[0][1]:
            self.x = self.limits[0][1] - self.width
        
        if self.limits[1][0] > self.y:
            self.y = self.limits[1][0]
        elif self.y + self.height > self.limits[1][1]:
            self.y = self.limits[1][1] - self.height

    def updateShots(self, dt):
        for c in self.shots:
            c[2] -= self.speed * 2 * dt           

    def shoot(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.timeShot <= 0:
            x = self.x + self.width/2 - 2
            y = self.y - 8

            self.shots.append([pygame.image.load(self.shootImg), x, y])

            self.timeShot = self.shootDelay

        self.timeShot -= dt
        self.updateShots(dt)
