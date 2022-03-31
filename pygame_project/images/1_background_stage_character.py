import pygame
import os
pygame.init()
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pygame_project")
clock = pygame.time.Clock()
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
# 배경 만들기
background = pygame.image.load(os.path.join(current_path, "background.png"))
stage = pygame.image.load(os.path.join(current_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 캐릭터를 스테이지 위에 놓기 위해 사용
# 캐릭터 만들기
character = pygame.image.load(os.path.join(current_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height - stage_height

weapon = pygame.image.load(os.path.join(current_path, "weapon.png"))


running = True

while running:
    dt = clock.tick(30)
    print(f"FPS : {clock.get_fps()}")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background, (0,0))
    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()

pygame.quit()