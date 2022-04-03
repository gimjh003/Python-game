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

# 공 만들기 (4개 크기에 대해 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(img_path, "balloon1.png")),
    pygame.image.load(os.path.join(img_path, "balloon2.png")),
    pygame.image.load(os.path.join(img_path, "balloon3.png")),
    pygame.image.load(os.path.join(img_path, "balloon4.png"))]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -5] # index 0, 1, 2, 3 에 해당하는 값

# 공들
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, # 공의 X 좌표
    "pos_y" : 50, # 공의 Y 좌표
    "img_index" : 0, # 공의 이미지 인덱스 (앞으로 공의 인덱스와 관련된 처리는 모두 이것을 이용함)
    "to_x":3, # x축 이동방향, -3이면 왼쪽으로, 3이면 오른쪽으로
    "to_y":-6, # y축 이동방향
    "init_spd_y":ball_speed_y[0] # y 최초 속도
    })

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# 게임 폰트 정의
game_font = pygame.font.Font(None, 40)
game_result = ["GAME OVER", "TIME OUT", "MISSION COMPLETE"]
total_time = 100 # 게임 종료 메시지
start_tick = pygame.time.get_ticks() # 시작 시간 정의

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
                weapons.append([weapon_x_pos, weapon_y_pos]) # SPACE 누르면 현재 캐릭터의 위치정보를 바탕으로 새 무기 위치정보 생성
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width-character_width
    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로 (위로 이동하려면 음수여야 함(맨 위가 0))

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0] # y좌표가 0보다 큰(천장을 넘지 않은) 것들만 w에 집어넣고 리스트 업데이트

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls): # enumerate : 인덱스와 값을 가져온다, ball_idx에는 인덱스, ball_val은 딕셔너리(리스트 안 값)
        ball_pos_x = ball_val["pos_x"] # 공 리스트 안에 있는 딕셔너리 값에서 X좌표와 Y좌표를 가져오고 차례대로 넣어준다.
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_index"] # 공 리스트 안에 있는 딕셔너리 값에서 이미지 인덱스를 가져온다.

        ball_size = ball_images[ball_img_idx].get_rect().size # 공의 이미지 인덱스 값을 바탕으로 알맞은 크기의 이미지를 가져온다.
        ball_width = ball_size[0] # 가로세로 크기 업데이트
        ball_height = ball_size[1]
        
        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x <= 0 or ball_pos_x > screen_width-ball_width: # 공이 왼쪽 경계를 넘거나 오른쪽 경계를 넘으면 X방향을 반대로 전환에서 튕기는 효과
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height-stage_height-ball_height: # 공이 stage 아래로 내려가면 초기 속도로 튕겨서 올라옴
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5 # 속도를 증가하면서 y값이 증가(추락), 그리고 stage 충돌시 상승 (포물선 그리기)
        
        ball_val["pos_x"] += ball_val["to_x"] # 공의 이동방향을 업데이트
        ball_val["pos_y"] += ball_val["to_y"]

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls): # 현재 공들의 정보(딕셔너리)를 가져옴
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_index"]
        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            result = game_result[0]
            running = False
            break # 공에 닿으면 게임오버

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons): # 쏘아진 무기 안에 들어있는 좌표값(계속해서 업데이트되는 무기들의 위치가 모두)
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y # 반복문을 사용해서 무기 리스트 안에 들어있는 위치정보를 토대로 rect 정보를 다 만듦

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정
                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기 (만약 이미지 인덱스가 3(가장 작은 공)이라면 쪼개지는 절차가 사라지고 지워지는 것만 남음)
                if ball_img_idx < 3:
                    # 현재 공 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx+1].get_rect() # +1을 하는 이유는 현재 변수가 나눠진 공이기 때문에 작은 사이즈의 공으로 변경되어야 하기 때문임
                    small_ball_size = small_ball_rect.size
                    small_ball_width = small_ball_size[0]
                    small_ball_height = small_ball_size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x":ball_pos_x+ball_width/2-small_ball_width/2, # 공 중앙에서 나타나는 효과
                        "pos_y":ball_pos_y+ball_height/2-small_ball_height/2, # 공 중앙에서 나타나는 효과
                        "img_index":ball_img_idx+1,
                        "to_x":-3, # 왼쪽으로 튕겨나가야 함
                        "to_y":-6, # 처음 살짝 올라가는 그 속도
                        "init_spd_y":ball_speed_y[ball_img_idx+1]
                    })
                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x":ball_pos_x + ball_width/2 - small_ball_width/2,
                        "pos_y":ball_pos_y + ball_height/2 - small_ball_height/2,
                        "img_index":ball_img_idx+1,
                        "to_x":3,
                        "to_y":-6,
                        "init_spd_y":ball_speed_y[ball_img_idx+1]
                    })

                break
        else: # 계속 게임을 진행
            continue # 안쪽 for문 조건이 맞지 않으면 continue.  바깥 for문 계속 수행
        break # 안쪽 for문에서 브레이크를 만나면 여기로 진입 가능.

# for 공 정보 가져오기:
#   for 무기 rect 업데이트:
#       if 충돌:
#           공 분리
#       break <- 우리는 여기서 공 제거 코드가 실행되기를 기대했지만(기존의 큰 건 사라져야 함), 안쪽 for문만 빠져나오면서 다시 공 정보를 가져오게됨
#   else: 그러면서 동시에 제거되지 않은 무기가 분리된 하나의 대상을 제거하면서 큰 걸 분리했는데 큰 거 하나와 작은거 하나가 남게되는 상황이 연출됨
#       continue <- 이 continue는 안쪽for문이 성공적으로 실행 되면 else를 타게 되면서 자연스럽게 공 정보를 가져오는 바깥 for문으로 이어짐
#   break <- 그러나 만약 공이 분리되면서 break루트를 타게 되면 else를 실행하지 않고 바깥 break까지 탈출하게 되면서 공 제거 코드로 이어지며 해결
# 공 제거 코드
# 무기 제거 코드

# for와 함께 쓰는 else는 break를 만나지 않고 성공적으로 수행되었을 때 안의 명령을 수행하게 됨
# for문이 중간에 break되었는지 안되었는지를 판별하기 위해 사용

    if ball_to_remove > -1: # 일반적인 경우 이 if문이 실행됨 (이미지 인덱스 값은 일반적으로 양수)
        del balls[ball_to_remove] # 사라져야 되는 공의 인덱스 정보를 가지고 공(딕셔너리 값들)을 지움 (del은 인덱스로 지울 수 있음)
        ball_to_remove = -1 # 다시 공이 사라질 때를 기다리기 위해 -1로 변경 (아니라면 가장 큰 공을 지웠을 때 0번째로 설정될 모든 공들이 제거될 수 있음)

    if weapon_to_remove > -1: # 무기 또한 마찬가지로 공과 닿으면 서로 사라져야 함.
        del weapons[weapon_to_remove] # 무기의 좌표값이 지워짐
        weapon_to_remove = -1 # 다시 무기가 사라질 때를 기다림

    screen.blit(background, (0,0)) # 배경 시각정보 업데이트
    screen.blit(stage, (0, screen_height-stage_height)) # 스테이지 시각정보 업데이트
    for weapon_x_pos, weapon_y_pos in weapons: # 무기들의 시각정보 업데이트
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터의 시각정보 업데이트
    for ball_idx, ball_val in enumerate(balls): # balls 안에 있는 딕셔너리 값들을 모조리 불러옴
        ball_pos_x = ball_val["pos_x"] # 모든 공(딕셔너리 값)의 좌표, 이미지 정보를 업데이트
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_index"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y)) # 공의 정보를 계속해서 업데이트

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks()-start_tick) / 1000
    timer = game_font.render("TIME : {}".format(int(total_time - elapsed_time)), True, (255,0,0), (0,0,0))
    screen.blit(timer, (10,10))

    # 시간 초과
    if total_time - elapsed_time <= 0:
        result = game_result[1]
        running = False
    # 모든 공 제거
    if balls == []:
        result = game_result[2]
        running = False

    pygame.display.update() # 화면 전체 정보 업데이트

msg = game_font.render(result, True, (255,0,0), (0,0,0)) # 게임 종료시 메시지를 출력해야함
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2))) # center를 써서 화면 중앙에 메시지를 띄울 수 있게됨
print(msg_rect)
screen.blit(msg, msg_rect)
pygame.display.update()
pygame.time.delay(3000)
pygame.quit()