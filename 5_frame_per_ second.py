import pygame
pygame.init()
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hello, World!")
clock = pygame.time.Clock() # FPS
background = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\background.png")
character = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width/2
character_y_pos = screen_height - character_height
to_x = 0
to_y = 0
character_speed = 0.6
running = True
while running:
    dt = clock.tick(65) # 게임 화면의 초당 프레임 수 설정
    print("fps : " + str(clock.get_fps())) # FPS 표시
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
            elif event.key == pygame.K_UP:
                to_y -= character_speed
            elif event.key == pygame.K_DOWN:
                to_y += character_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # 두 요인 전부 event.key ==를 붙여줘야 한다.
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
    character_x_pos += to_x * dt # 1초 동안 이동 할 수 있는 거리가 100일 때.
    character_y_pos += to_y * dt # 10FPS는 10만큼 이동해야하고, 20FPS는 5만큼 이동해야 함. (FPS에 따라 이동속도가 달라야 해서 곱한다.)

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width
    
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height-character_height:
        character_y_pos = screen_height-character_height

    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update() # 모든 계산 과정은 우리가 보기 위한 화면을 위한 것이다. 업데이트를 해주자.

pygame.quit()