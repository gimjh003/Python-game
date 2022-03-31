#pip install pygame
import pygame
pygame.init() #초기화 필수
screen_width = 480 #창 너비
screen_height = 640 # 창 높이
screen = pygame.display.set_mode((screen_width, screen_height)) # 디스플레이 너비, 높이 설정 (윈도우)
pygame.display.set_caption("Hello, World!") # 창 제목 설정
running = True # 게임 실행중
while running: # 게임이 실행되는 동안
    for event in pygame.event.get(): # 지속적으로 이벤트 수집
        if event.type == pygame.QUIT: #만약 창이 닫히는 이벤트가 발생했다면
            running = False # 게임 실행 중단
        

pygame.quit() # 게임 종료