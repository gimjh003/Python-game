import pygame
pygame.init()
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hello, World!")
background = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\background.png")
character = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height

to_x = 0 # 이동할 좌표
to_y = 0 # 이동할 좌표

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: # 캐릭터를 왼쪽으로
                to_x -= 0.3
            elif event.key == pygame.K_RIGHT: # 캐릭터를 오른쪽으로
                to_x += 0.3
            elif event.key == pygame.K_UP: # 캐릭터를 위로
                to_y -= 0.3
            elif event.key == pygame.K_DOWN: # 캐릭터를 아래로
                to_y += 0.3
        if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
    character_x_pos += to_x # 좌표가 바뀌는 것을 이동한다고 느끼는 것일 뿐이다
    character_y_pos += to_y

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width

    # 세로 경계값 처리
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height-character_height:
        character_y_pos = screen_height-character_height

    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()

pygame.quit()

"""
주기적으로 화면을 새로고침하면서 수집한 이벤트에 따라 화면 속 요소들의 값을 변경해 주는 것이 핵심이구나.
움직이는게 아니라 바뀌는 거였어.
"""