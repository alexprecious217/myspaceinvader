# Space Invader Game source codes
# 05-01-2020
# by Alex Precious
# IG: @dahfirstborn

import pygame
import random
import math

from pygame import mixer

# Initialize the game
pygame.init()

# Create the screen game-window
screen_window = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load("space-bg.jpg")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
win_name = pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("space-ship.png")
playerX = 370
playerY = 480
playerX_change = 0

enemy1Img = []
enemy1X = []
enemy1Y = []
enemy1X_change = []
enemy1Y_change = []
no_of_enemies = 4

# Enemy1
for i in range(no_of_enemies):
    enemy1Img.append(pygame.image.load("enemy.png"))
    enemy1X.append(random.randint(0, 736))
    enemy1Y.append(random.randint(0, 150))
    enemy1X_change.append(4)
    enemy1Y_change.append(100)

# # Enemy2
# enemy2Img = pygame.image.load("enemy.png")
# enemy2X = random.randint(0, 736)
# enemy2Y = random.randint(0, 150)
# enemy2X_change = 4
# enemy2Y_change = 40

# Ready - The bullet is hidden off the screen
# Fire - Bullet is made visible in decreasing order
# Bullet
bulletImg = pygame.image.load("bullet1.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

# Score Font
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game over text Font
over_font = pygame.font.Font("freesansbold.ttf", 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen_window.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 9, 12))
    screen_window.blit(over_text, (200, 250))


def player(x, y):
    screen_window.blit(playerImg, (x, y))


def enemy1(x, y, i):
    screen_window.blit(enemy1Img[i], (x, y))


# def enemy2(x, y):
#     screen_window.blit(enemy2Img, (enemy2X, enemy2Y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen_window.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # change the display bgcolor
    screen_window.fill((0, 0, 0))

    # Persistent background image
    screen_window.blit(background, (0, 0))

    # Create the quit function to quit the game-window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key stroke is pressed down check whether it's left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -8
            if event.key == pygame.K_RIGHT:
                playerX_change = 8
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current x-coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Key removal or key up method
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Control out of boundary movement for player
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Control out of boundary movement for enemy1(Enemy Movement)
    for i in range(no_of_enemies):
        # Game over
        if enemy1Y[i] > 440:
            for j in range(no_of_enemies):
                enemy1Y[j] = 2000
            game_over_text()
            # break

        enemy1X[i] += enemy1X_change[i]
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 4
            enemy1Y[i] += enemy1Y_change[i]
        elif enemy1X[i] >= 736:
            enemy1X_change[i] = -4
            enemy1Y[i] += enemy1Y_change[i]

        # Collision
        collision1 = isCollision(enemy1X[i], enemy1Y[i], bulletX, bulletY)
        if collision1:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemy1X[i] = random.randint(0, 736)
            enemy1Y[i] = random.randint(0, 150)

        # collision2 = isCollision(enemy2X, enemy2Y, bulletX, bulletY)
        # if collision2:
        #     bulletY = 480
        #     bullet_state = "ready"
        #     score += 1
        #     print(score)
        #     enemy2X = random.randint(0, 736)
        #     enemy2Y = random.randint(0, 150)

        enemy1(enemy1X[i], enemy1Y[i], i)
        # pygame.display.flip()

        # Control out of boundary movement for enemy2
        # enemy2X += enemy2X_change
        #
        # if enemy2X <= 0:
        #     enemy2X_change = 4
        #     enemy2Y += enemy2Y_change
        # elif enemy2X >= 736:
        #     enemy2X_change = -4
        #     enemy2Y += enemy2Y_change

        # Control movement for bullet
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        # enemy2(enemy2X, enemy2Y)
        show_score(textX, textY)
        pygame.display.update()
