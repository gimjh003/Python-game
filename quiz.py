import pygame
import random
import os
pygame.init()
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("AVOID YELLOW SQUARE")
current_path = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(current_path, "background.png"))
character = pygame.image.load(os.path.join(current_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_speed = 0.6
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height
to_x = 0
enemy = pygame.image.load(os.path.join(current_path, "enemy.png"))
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0, screen_width-enemy_width)
enemy_y_pos = 0
enemy_speed = 0.6
clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(30)
    print(f"FPS : {clock.get_fps()}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    character_x_pos += to_x*dt
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    enemy_y_pos += enemy_speed*dt
    if enemy_y_pos > screen_height:
        enemy_x_pos = random.randint(0, screen_width-enemy_width)
        enemy_y_pos = 0

    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        print("GAME OVER")
        running = False

    pygame.display.update()

pygame.quit()