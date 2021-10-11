import pygame
import random

from stage import Stage

class Boss():
    def __init__(self):
        #Positional attributes
        self.x = 40
        self.y = 40
        self.img = pygame.image.load("images/enemy1.png")   
        self.width = self.img.get_rect()[2]
        self.height = self.img.get_rect()[3]

        self.health = 200
        self.lifebarIMG = None

        #Speed attributes
        self.vx = 0
        self.vy = 0
        self.speedRange = [-0.3, 0, 0.3]
        self.updateMovCD = 0              

        #Attack attributes
        self.attacks = ['pilar', 'summon']
        self.attackCD = 14000
        self.attackDelay = 14000
        self.currAtk = None

        self.laser = 0

        self.shootCD = 1600
        self.shootDelay = 1600

    def attack(self, surf, dt):
        self.attackCD -= dt

        surf_rect = surf.get_rect()
        width = surf_rect[2]
        height = surf_rect[3]

        if self.laser >= 1:
            #Draw first laser
            pygame.draw.rect(surf, (255, 255, 255), (0, 0, 100, 100))
        if self.laser >= 2:
            #Draw second laser
            pygame.draw.rect(surf, (255, 255, 255), (width-100, 0, 100, 100))


        if self.attackCD <= 0:         

            if self.currAtk == None:
                self.currAtk = random.choice(self.attacks)

            if self.currAtk == 'summon':
                self.currAtk = None
                self.attackCD = self.attackDelay
                return [self.currAtk, random.randrange(3, 6)]
            
            elif self.currAtk == 'pilar':
                #Move the boss to the top left side of the screen
                #Make it deploy a laser beam, then move it to the top right side of the screen
                #And make it deploy another laser beam
                #When both of the laser beams are positioned, fire a blast                

                self.vy = -0.3
                if self.laser == 0:
                    self.vx = -0.3 
                elif self.laser == 1:
                    self.vx = 0.3                    
                
                if self.x == 0 and self.y == 0:
                    self.laser = 1
                elif self.x == width - self.width and self.y == 0:
                    self.laser = 2

                if self.laser == 2:
                    #Shoot the laser beam
                    #IDEA: Append a different shot to the stage's shots array
                    #Several large shots, one on top of the other
                    #So they cover the entire screen, let the stage treat the collision

                    self.laser = 0
                    self.currAtk = None
                    self.attackCD = self.attackDelay

                return 'pilar'

        return 'none'

    def shoot(self, dt):
        self.shootCD -= dt
        if self.shootCD <= 0:
            self.shootCD = self.shootDelay

            x = self.x + self.width/2 - 2
            y = self.y + self.height

            return [pygame.image.load(self.shootImg), x, y]

        return -1        

    def update(self, surf, dt):
        surf.blit(self.img, (self.x, self.y))

        #Updating movement
        self.updateMovCD += 1/dt
        if self.updateMovCD >= 5:
            self.updateMovCD = 0

            if self.currAtk == None:
                self.vx = random.choice(self.speedRange)
                self.vy = random.choice(self.speedRange)
            

        self.x += self.vx * dt
        self.y += self.vy * dt

        #Boundaries
        surf_rect = surf.get_rect()
        x_limit = surf_rect[2]
        y_limit = surf_rect[3]
        
        if 0 > self.x and self.vx < 0:
            self.vx = 0
            self.x = 0
        elif self.x + self.width > x_limit and self.vx > 0:
            self.vx = 0
            self.x = x_limit - self.width

        if 0 > self.y and self.vy < 0 :
            self.vy = 0
            self.y = 0
        elif self.y + self.height > y_limit and self.vy > 0:
            self.vy = 0
            self.y = y_limit - self.height


pygame.init()

clock = pygame.time.Clock()

disw = 900
dish = 700

screen = pygame.display.set_mode((disw, dish))

def main_loop():
    running = True

    stg = Stage(1, (disw, dish))
    stg.boss = Boss()

    while running:
        dt = clock.tick(60)

        screen.fill((0, 0, 0))

        stg.updateEnemies(screen, dt)
        stg.updateBoss(screen, dt)      
        

        pygame.display.update()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

main_loop()