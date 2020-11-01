import pygame
import random
import math
from pygame import mixer
pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('back.png')


mixer.music.load('alien-spaceship_daniel_simion.wav')
mixer.music.play(-1)

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('space-ship.png')
playerX = 370
playerY = 480
playerx_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyx_change = []
enemyy_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('space-invaders.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyx_change.append(2)
    enemyy_change.append(20)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletx_change = 0
bullety_change = 5
bullet_state = 'ready'

score_val=0
font=pygame.font.Font('freesansbold.ttf',32)
fontt=pygame.font.Font('freesansbold.ttf',64)
textx=10
texty=10
def scoree(x,y):
    score=font.render('Score : '+str(score_val),True,(255,255,255))
    screen.blit(score,(x,y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(bulletX, bulletY, enemyY, enemyX):
    sqr = (((enemyX - bulletX) * (enemyX - bulletX)) + ((enemyY - bulletY) * (enemyY - bulletY)))
    dist = math.sqrt(sqr)
    if dist < 27:
        return True
    else:
        return False
def game_over():
    over = fontt.render('GAME OVER!', True, (255, 255, 255))
    screen.blit(over, (200, 250))


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -2
            if event.key == pygame.K_RIGHT:
                playerx_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
                    bulletsound=mixer.Sound('Missle_Launch-Kibblesbob-2118796725.wav')
                    bulletsound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    playerX += playerx_change

    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0
    for i in range(num_of_enemies):


        if enemyY[i]>300:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over()
            break
        enemyX[i] += enemyx_change[i]

        if enemyX[i] >= 736:
            enemyx_change[i] = -2
            enemyY[i] += enemyy_change[i]
        elif enemyX[i] <= 0:
            enemyx_change[i] = 2
            enemyY[i] += enemyy_change[i]
        collision = isCollision(bulletX, bulletY, enemyY[i], enemyX[i])
        if collision:
            colsound=mixer.Sound('Torpedo+Explosion.wav')
            colsound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_val += 1

            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i],i)
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bullety_change


    player(playerX, playerY)
    scoree(textx,texty)

    pygame.display.update()
