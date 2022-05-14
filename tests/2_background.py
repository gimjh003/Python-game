import pygame
pygame.init()
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption = "Hello, World!"
background = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\background.png") # 배경 이미지 불러오기
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #screen.fill((255, 255, 255)) = 화면을 rgb값으로 설정
    screen.blit(background, (0,0)) # 배경 이미지 좌표 설정 (사이즈는 딱 맞음, 480*640)
    pygame.display.update() # 게임 화면 다시 설정 (배경은 매 프레임마다 존재해야 함)

pygame.quit()