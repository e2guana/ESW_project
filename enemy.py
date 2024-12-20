import random
import time
from PIL import Image

class Enemy:
    def __init__(self, width, size=50, health=20, speed=2, image_path="assets/Enemy.png"):
        self.width = width
        self.size = size
        self.health = health
        self.speed = speed
        self.x = (width - size) // 2   # 화면 위쪽 중앙에서 생성
        self.y = -size + 60
        self.image = Image.open(image_path).convert("RGBA").resize((size, size))
        self.lasers = []
        self.laser_timer = time.time()  # 레이저 발사 간격 타이머
        self.next_laser_interval = random.uniform(1, 2)  # 1~2초 간격으로 레이저 발사
        self.is_destroyed = False
        
        # 히트박스 설정 (0.8 크기)
        self.hitbox_scale = 0.8
        self.hitbox_width = int(self.size * self.hitbox_scale)
        self.hitbox_height = int(self.size * self.hitbox_scale)
        self.hitbox_x_offset = (self.size - self.hitbox_width) // 2
        self.hitbox_y_offset = (self.size - self.hitbox_height) // 2
        
        # 랜덤 방향 변경 타이머
        self.direction_change_timer = time.time()
        self.next_direction_change = random.uniform(1, 3)  # 1~3초 사이 랜덤 시간
        self.current_direction = random.choice([-1, 1])  # -1: 왼쪽, 1: 오른쪽

    def move(self):
        # 적 이동
        if self.health <= 0:  # 제거된 적은 이동하지 않음
            return

        # 방향 변경 타이머 확인
        if time.time() - self.direction_change_timer >= self.next_direction_change:
            self.current_direction = random.choice([-1, 1])  # 새로운 방향 설정
            self.direction_change_timer = time.time()  # 타이머 초기화
            self.next_direction_change = random.uniform(1, 3)  # 다음 변경 시간 설정

        # 현재 방향으로 이동
        self.x += self.current_direction * self.speed
        self.x = max(0, min(self.width - self.size, self.x))  # 화면 경계 제한
        
    def shoot(self):
         # 적 레이저 발사
        if self.health <= 0:  # 제거된 적은 레이저를 발사하지 않음
            return

        if time.time() - self.laser_timer >= self.next_laser_interval:
            self.laser_timer = time.time()  # 타이머 초기화
            self.next_laser_interval = random.uniform(1, 3)  # 다음 발사 간격 설정

            # 1~2발 랜덤 발사
            num_lasers = random.randint(1, 2)
            for _ in range(num_lasers):
                laser_x = self.x + (self.size // 2) + random.randint(-self.size // 4, self.size // 4)  # 랜덤한 X 위치에서 발사
                laser_y = self.y + self.size
                self.lasers.append(EnemyLaser(laser_x, laser_y))
                
    def take_damage(self, damage):
        # 데미지 받으면 체력 감소
        self.health -= damage
        if self.health <= 0:
                self.is_destroyed = True

    
    def draw(self, base_image):
        # 적 구현
        if self.health > 0:
            base_image.paste(self.image, (self.x, self.y), self.image)

        # 적 레이저 구현
        for laser in self.lasers:
            laser.draw(base_image)
            

    def is_destroyed(self):
        # 적이 파괴되었는지 확인
        return self.health
    
    def get_hitbox(self):
        #히트박스 반환
        return (
            self.x + self.hitbox_x_offset,
            self.y + self.hitbox_y_offset,
            self.x + self.hitbox_x_offset + self.hitbox_width,
            self.y + self.hitbox_y_offset + self.hitbox_height,
        )




class EnemyLaser:
    def __init__(self, x, y, speed=5, damage=1, image_path="assets/Laser_Enemy.png"):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.image = Image.open(image_path).convert("RGBA").resize((10, 20))

    def move(self):
        self.y += self.speed

    def draw(self, base_image):
        base_image.paste(self.image, (self.x - self.image.width // 2, self.y), self.image)

    def is_off_screen(self, screen_height):
        return self.y > screen_height
