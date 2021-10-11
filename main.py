import pygame
from player import *
import pickle
from enemy import *
from stage import *

pygame.init()
pygame.font.init()

disw = 900
dish = 700

screen = pygame.display.set_mode((disw, dish))

black = 0, 0, 0
white = 255, 255, 255

clock = pygame.time.Clock()

currSave = None

clickSound = pygame.mixer.Sound("sounds/click.wav")

def collided(rectA, rectB):
    x1 = rectA[0]
    y1 = rectA[1]
    w1 = rectA[2]
    h1 = rectA[3]

    x2 = rectB[0]
    y2 = rectB[1]
    w2 = rectB[2]
    h2 = rectB[3]

    if x2 + w2 > x1 > x2 and y2 + h2 > y1 > y2:
        return 1

    return 0

def drawText(msg, size, color):
    font = pygame.font.SysFont("vgafix.ttf", size)
    textSurf = font.render(msg, False, color)
    textRect = textSurf.get_rect()

    return textSurf, textRect

def drawButton(x, y, w, h, color, text, textSz, textClr):
    mouse = pygame.mouse.get_pos()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (150, 0, 0), (x-5, y-5, w+10, h+10))

        if pygame.mouse.get_pressed()[0]:
            clickSound.play()            
            return 1
    
    pygame.draw.rect(screen, color, (x, y, w, h))
    
    txt, rect = drawText(text, textSz, textClr)

    txtX = x + w/2 - rect[2]/2
    txtY = y + h/2 - rect[3]/2

    screen.blit(txt, (txtX, txtY))

def updateWindow(dt, player, stg):
    screen.fill(black)
    player.draw(screen)
    player.move(dt)
    player.shoot(dt)

    stg.updateEnemies(screen, dt)

    pygame.display.update()

def loadPlayer(save):
    try:
        f = open("save" + str(save), "rb")
        player = pickle.load(f)
        f.close()
        player.image = pygame.image.load("images/player.png")
    except:
        player = Player("images/player.png", [disw, dish])

    return player

def saveGame(player):
    print("Saving game...")

    player.image = None
    player.shots = []

    f = open("save" + str(currSave), "wb")
    pickle.dump(player, f)
    f.close()

    print("Game Saved!")  
    

def menuScreen():
    global currSave

    running = True  

    selSaves = False

    title = pygame.image.load("images/title.png")

    while running:
        screen.fill(black)

        screen.blit(title, (disw/2 - 300, 20))

        if selSaves:
            if drawButton(disw/4 - 100 - 10, 300, 200, 100, white, "Save 1", 50, black):
                player = loadPlayer(1)
                currSave = 1
                running = False

            elif drawButton(disw/4 - 100 + 10 + disw/2, 300, 200, 100, white, "Save 2", 50, black):
                player = loadPlayer(2)
                currSave = 2
                running = False

            elif drawButton(disw/4 - 100 - 10, 450, 200, 100, white, "Save 3", 50, black):
                player = loadPlayer(3)
                currSave = 3
                running = False
                
            elif drawButton(disw/4 - 100 + 10 + disw/2, 450, 200, 100, white, "Save 4", 50, black):
                player = loadPlayer(4)
                currSave = 4
                running = False

            elif drawButton(disw/2 - 80, 500, 160, 100, white, "Voltar", 50, black):
                selSaves = False            
        else:
            if drawButton(disw/2 - 100, 150, 200, 100, white, "Jogar", 50, black):
                selSaves = True

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    
    selectStageScreen(player)

def pauseScreen():
    running = True
    while running:
        screen.fill(black)

        title, titleRct = drawText("Jogo Pausado", 80, white)

        screen.blit(title, (disw/2 - titleRct[2]/2, 20))

        if drawButton(disw/2 - 100, 150, 200, 100, white, "Continuar", 30, black):
            running = False

        if drawButton(disw/2 - 100, 300, 200, 100, white, "Abandonar Fase", 30, black):
            running = False
            return 1

        if drawButton(disw/2 - 100, 450, 200, 100, white, "Voltar para o Menu", 30, black):
            running = False
            return -1

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def selectStageScreen(player):
    running = True
    
    while running:
        screen.fill(black)

        title, titleRct = drawText("Selecione uma fase", 80, white)
        screen.blit(title, (disw/2 - titleRct[2]/2, 20))

        for c in range(1, 11):
            line = c // 6 + 1     

            if c > player.stage:
                drawButton(100 * (c%6) + 20 + 150, 100 * (line+1), 80, 80, white, "XXX", 30, black)
            else:
                if drawButton(100 * (c%6) + 20 + 150, 100 * (line+1), 80, 80, white, "Fase " + str(c), 30, black):
                    currStage = c
                    running = False


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    main_loop(player, currStage)

def main_loop(player, currStage):
    running = True

    print(currStage)

    #Sound Effects
    bckgMusic = pygame.mixer.music.load("sounds/bckgMusic.mp3")
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(-1, 0.0)

    #Generating level
    hitSound = pygame.mixer.Sound("sounds/hit.wav")

    en = []
    stg = Stage(currStage, [disw, dish])

    for c in range(2):
        en.append(Enemy(20 * c + 80, 20, "images/enemy1.png", [disw, dish]))

    for c in range(2):
        en.append(Enemy(20 * c + 80, 80, "images/enemy2.png", [disw, dish]))

    stg.enemies.append(en)

    paused = False

    while running:
        dt = clock.tick(60)    

        updateWindow(dt, player, stg)

        for c in stg.currEnemies:
            #Checking player's shot hit
            for d in player.shots:
                rect1 = [d[1], d[2], 4, 8]
                rect2 = [c.x, c.y, c.width, c.height]
                if collided(rect1, rect2):
                    #If its a hit, remove the enemy and remove the shot
                    stg.currEnemies.remove(c)
                    player.shots.remove(d)
            #Checking enemie's shot hit
            for d in stg.shots:
                rect1 = [d[1], d[2], 4, 8]
                rect2 = [player.x, player.y, player.width, player.height]
                if collided(rect1, rect2):
                    #If its a hit, decrease player's health
                    print("TOMOU TIRO AI AMIGAO")
                    stg.shots.remove(d)
                    hitSound.play()
                    player.health -= 1
                    for c in player.lifeBars:
                        if c[1] == 1:
                            c[0] = pygame.image.load("images/lifebarEmpty.png")
                            c[1] = 0
                            break

        if player.health <= 0:
            print("GAME OVER!")
            running = False
            menuScreen()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                #PAUSE DOES NOT WORK PROPERLY --------------------------------------------------------------------------------------------------
                if event.key == pygame.K_ESCAPE:
                    running = False                    
                    opt = pauseScreen()
                    if opt == -1:
                        #Vai para o menu
                        running = False
                        menuScreen()
                    elif opt == 1:
                        #Vai para a tela de seleçao de fases
                        running = False
                        selectStageScreen(player)  
                    else:
                        running = True         

menuScreen()