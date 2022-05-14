import pygame
pygame.init()
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hello, World!")
background = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\background.png")
character = pygame.image.load("C:\\Users\\김정협\\Desktop\\Python game\\character.png") # 캐릭터 이미지 불러오기
character_size = character.get_rect().size # 이미지 크기를 구한다
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = screen_width/2 - character_width/2 # 화면 가로의 절반 크기에 해당하는 곳에 위치 (가로)
character_y_pos = screen_height - character_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치 (세로)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()

pygame.quit()