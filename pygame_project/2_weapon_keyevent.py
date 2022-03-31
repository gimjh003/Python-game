import pygame
import os
pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pygame_project")
clock = pygame.time.Clock()
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
img_path = os.path.join(current_path, "images")
# 배경 만들기
background = pygame.image.load(os.path.join(img_path, "background.png"))
stage = pygame.image.load(os.path.join(img_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 캐릭터를 스테이지 위에 놓기 위해 사용
# 캐릭터 만들기
character = pygame.image.load(os.path.join(img_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height - stage_height
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(img_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
weapon_height = weapon_size[1]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

running = True

while running:
    dt = clock.tick(30)
    print(f"FPS : {clock.get_fps()}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos+character_width/2-weapon_width/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width
    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로
    # weapons에 원래 들어있는 값은 [weapon_x_pos, weapon_y_pos]
    # 그 좌표값을 w에 불러와서 y값을 내리고(위로 이동) 다시 업데이트(하나씩 집어넣고 초기화(=))한다.
    # w[0] = weapon_x_pos, w[1] = weapon_y_pos

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]
    # y 좌표가 0보다 큰(천장에 안닿은) 공격들만 존재하게 하는 것.

    screen.blit(background, (0,0))
    screen.blit(stage, (0, screen_height-stage_height))
    for weapon_x_pos, weapon_y_pos in weapons: # 결과적으로 매 초마다 y의 좌표가 업데이트 되는 천장에 안닿은 공격들만 리스트에 존재하게 됨.
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) # 공격이 올라가는 게 아니라, 올라가는 공격이 하나씩 다시 들어가고 아래에 있는 것들이 사라지는 것.
    screen.blit(character, (character_x_pos, character_y_pos))

    pygame.display.update()

pygame.quit()