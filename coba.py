import pygame
import sys
import math
import random
from enum import Enum
import json

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
DARK_GRAY = (80, 80, 80)
LIGHT_BLUE = (173, 216, 230)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
SKIN_COLOR = (255, 220, 177)
HAIR_COLOR = (50, 30, 20)
CLOTHES_COLOR = (0, 100, 200)
PANTS_COLOR = (30, 30, 150)
SHOES_COLOR = (20, 20, 20)
GRASS_GREEN = (34, 139, 34)
SIDEWALK_COLOR = (192, 192, 192)
BUILDING_COLORS = [(200, 200, 220), (180, 180, 200), (210, 210, 230), (190, 190, 210)]

# Enum untuk arah
class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

# Enum untuk state lampu lalu lintas
class TrafficLightState(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2

# Enum untuk jenis misi
class MissionType(Enum):
    QUESTION = 0
    ACTION = 1
    TREASURE = 2

# Enum untuk state game
class GameState(Enum):
    PLAYING = 0
    GAME_OVER = 1
    PAUSED = 2
    ACHIEVEMENT = 3

# Kelas untuk karakter pemain
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20  # Diperkecil dari 30
        self.height = 40  # Diperkecil dari 60
        self.speed = 5
        self.direction = Direction.DOWN
        self.animation_counter = 0
        self.is_moving = False
        self.lives = 3
        self.invulnerable = False
        self.invulnerable_timer = 0
        
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Batasi gerakan di layar
        self.x = max(50, min(self.x, SCREEN_WIDTH - 150))
        self.y = max(50, min(self.y, SCREEN_HEIGHT - 150))
        
        # Tentukan arah berdasarkan gerakan
        if dx > 0:
            self.direction = Direction.RIGHT
        elif dx < 0:
            self.direction = Direction.LEFT
        elif dy > 0:
            self.direction = Direction.DOWN
        elif dy < 0:
            self.direction = Direction.UP
            
        self.is_moving = (dx != 0 or dy != 0)
        
    def hit(self):
        if not self.invulnerable:
            self.lives -= 1
            self.invulnerable = True
            self.invulnerable_timer = 120  # 2 detik invulnerability
            
    def update(self):
        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                
    def draw(self, screen):
        # Efek kedip saat invulnerable
        if self.invulnerable and self.invulnerable_timer % 10 < 5:
            return
            
        # Animasi berjalan
        if self.is_moving:
            self.animation_counter += 0.2
        else:
            self.animation_counter = 0
            
        # Gambar kaki dengan animasi
        leg_offset = 5  # Diperkecil dari 8
        leg_y = self.y + self.height//2
        
        if self.is_moving:
            # Animasi kaki bergerak
            left_leg_x = self.x - leg_offset + math.sin(self.animation_counter) * 5  # Diperkecil dari 8
            right_leg_x = self.x + leg_offset - math.sin(self.animation_counter) * 5  # Diperkecil dari 8
        else:
            left_leg_x = self.x - leg_offset
            right_leg_x = self.x + leg_offset
            
        # Gambar celana
        pygame.draw.rect(screen, PANTS_COLOR, (self.x - self.width//2, self.y - self.height//4, 
                                              self.width, self.height//2 + 5))  # Diperkecil
        
        # Gambar kaki
        pygame.draw.rect(screen, PANTS_COLOR, (left_leg_x - 4, leg_y, 8, 15))  # Diperkecil
        pygame.draw.rect(screen, PANTS_COLOR, (right_leg_x - 4, leg_y, 8, 15))  # Diperkecil
        
        # Gambar sepatu
        pygame.draw.ellipse(screen, SHOES_COLOR, (left_leg_x - 5, leg_y + 13, 10, 8))  # Diperkecil
        pygame.draw.ellipse(screen, SHOES_COLOR, (right_leg_x - 5, leg_y + 13, 10, 8))  # Diperkecil
        
        # Gambar tubuh (baju)
        body_rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                               self.width, self.height//2)
        pygame.draw.rect(screen, CLOTHES_COLOR, body_rect, border_radius=3)  # Diperkecil
        
        # Gambar kepala
        head_radius = 10  # Diperkecil dari 15
        head_pos = (self.x, self.y - self.height//2 - head_radius)
        pygame.draw.circle(screen, SKIN_COLOR, head_pos, head_radius)
        
        # Gambar rambut
        if self.direction == Direction.RIGHT:
            hair_points = [
                (head_pos[0] - head_radius + 2, head_pos[1] - head_radius + 3),
                (head_pos[0] + head_radius - 2, head_pos[1] - head_radius + 3),
                (head_pos[0] + head_radius - 3, head_pos[1] - 1),
                (head_pos[0] - head_radius + 3, head_pos[1] - 1)
            ]
        elif self.direction == Direction.LEFT:
            hair_points = [
                (head_pos[0] - head_radius + 2, head_pos[1] - head_radius + 3),
                (head_pos[0] + head_radius - 2, head_pos[1] - head_radius + 3),
                (head_pos[0] + head_radius - 3, head_pos[1] - 1),
                (head_pos[0] - head_radius + 3, head_pos[1] - 1)
            ]
        else:
            hair_points = [
                (head_pos[0] - head_radius + 2, head_pos[1] - head_radius + 3),
                (head_pos[0] + head_radius - 2, head_pos[1] - head_radius + 3),
                (head_pos[0] + head_radius - 3, head_pos[1] - 1),
                (head_pos[0] - head_radius + 3, head_pos[1] - 1)
            ]
        pygame.draw.polygon(screen, HAIR_COLOR, hair_points)
        
        # Gambar mata
        eye_offset_x = 3  # Diperkecil dari 5
        eye_offset_y = -2  # Diperkecil dari -3
        if self.direction == Direction.RIGHT:
            left_eye = (head_pos[0] + eye_offset_x, head_pos[1] + eye_offset_y)
            right_eye = (head_pos[0] + eye_offset_x + 2, head_pos[1] + eye_offset_y)  # Diperkecil
        elif self.direction == Direction.LEFT:
            left_eye = (head_pos[0] - eye_offset_x - 2, head_pos[1] + eye_offset_y)  # Diperkecil
            right_eye = (head_pos[0] - eye_offset_x, head_pos[1] + eye_offset_y)
        else:
            left_eye = (head_pos[0] - eye_offset_x, head_pos[1] + eye_offset_y)
            right_eye = (head_pos[0] + eye_offset_x, head_pos[1] + eye_offset_y)
            
        pygame.draw.circle(screen, BLACK, left_eye, 1.5)  # Diperkecil
        pygame.draw.circle(screen, BLACK, right_eye, 1.5)  # Diperkecil
        
        # Gambar mulut senyum
        if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
            smile_rect = pygame.Rect(head_pos[0] - 3, head_pos[1] + 3, 6, 3)  # Diperkecil
        else:
            smile_rect = pygame.Rect(head_pos[0] - 3, head_pos[1] + 3, 6, 3)  # Diperkecil
        pygame.draw.arc(screen, BLACK, smile_rect, 0, math.pi, 1)
        
        # Gambar tangan
        hand_offset = 8  # Diperkecil dari 12
        hand_y = self.y - self.height//4
        
        if self.direction == Direction.RIGHT:
            left_hand = (self.x - self.width//2 - hand_offset, hand_y)
            right_hand = (self.x + self.width//2 + hand_offset, hand_y)
        elif self.direction == Direction.LEFT:
            left_hand = (self.x - self.width//2 - hand_offset, hand_y)
            right_hand = (self.x + self.width//2 + hand_offset, hand_y)
        else:
            left_hand = (self.x - self.width//2 - hand_offset, hand_y)
            right_hand = (self.x + self.width//2 + hand_offset, hand_y)
            
        pygame.draw.circle(screen, SKIN_COLOR, left_hand, 5)  # Diperkecil
        pygame.draw.circle(screen, SKIN_COLOR, right_hand, 5)  # Diperkecil
        
        # Gambar lengan
        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen, CLOTHES_COLOR, 
                            (self.x - self.width//2, self.y - self.height//4), 
                            left_hand, 3)  # Diperkecil
            pygame.draw.line(screen, CLOTHES_COLOR, 
                            (self.x + self.width//2, self.y - self.height//4), 
                            right_hand, 3)  # Diperkecil
        elif self.direction == Direction.LEFT:
            pygame.draw.line(screen, CLOTHES_COLOR, 
                            (self.x - self.width//2, self.y - self.height//4), 
                            left_hand, 3)  # Diperkecil
            pygame.draw.line(screen, CLOTHES_COLOR, 
                            (self.x + self.width//2, self.y - self.height//4), 
                            right_hand, 3)  # Diperkecil
        else:
            pygame.draw.line(screen, CLOTHES_COLOR, 
                            (self.x - self.width//2, self.y - self.height//4), 
                            left_hand, 3)  # Diperkecil
            pygame.draw.line(screen, CLOTHES_COLOR, 
                            (self.x + self.width//2, self.y - self.height//4), 
                            right_hand, 3)  # Diperkecil

# Kelas untuk kendaraan
class Vehicle:
    def __init__(self, x, y, direction, color, speed, vehicle_type="car"):
        self.x = x
        self.y = y
        self.width = 80 if vehicle_type == "car" else 120
        self.height = 40 if vehicle_type == "car" else 50
        self.direction = direction
        self.color = color
        self.speed = speed
        self.vehicle_type = vehicle_type
        # Tentukan jalur kendaraan berdasarkan arah
        if direction == Direction.RIGHT or direction == Direction.LEFT:
            self.road_y = y  # Posisi y jalan
            self.road_min_y = y - 20  # Batas atas jalan
            self.road_max_y = y + 20  # Batas bawah jalan
        else:  # UP atau DOWN
            self.road_x = x  # Posisi x jalan
            self.road_min_x = x - 20  # Batas kiri jalan
            self.road_max_x = x + 20  # Batas kanan jalan
        
    def update(self):
        if self.direction == Direction.RIGHT:
            self.x += self.speed
            if self.x > SCREEN_WIDTH:
                self.x = -self.width
            # Pastikan kendaraan tetap di jalurnya
            self.y = self.road_y
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
            if self.x < -self.width:
                self.x = SCREEN_WIDTH
            # Pastikan kendaraan tetap di jalurnya
            self.y = self.road_y
        elif self.direction == Direction.DOWN:
            self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.y = -self.height
            # Pastikan kendaraan tetap di jalurnya
            self.x = self.road_x
        elif self.direction == Direction.UP:
            self.y -= self.speed
            if self.y < -self.height:
                self.y = SCREEN_HEIGHT
            # Pastikan kendaraan tetap di jalurnya
            self.x = self.road_x
                
    def draw(self, screen):
        # Gambar badan kendaraan
        if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
            body_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        else:
            body_rect = pygame.Rect(self.x, self.y, self.height, self.width)
            
        pygame.draw.rect(screen, self.color, body_rect, border_radius=5)
        
        # Gambar jendela
        window_color = (200, 220, 255)
        if self.vehicle_type == "car":
            if self.direction == Direction.RIGHT:
                window_rect = pygame.Rect(self.x + self.width - 25, self.y + 5, 20, self.height - 10)
            elif self.direction == Direction.LEFT:
                window_rect = pygame.Rect(self.x + 5, self.y + 5, 20, self.height - 10)
            else:
                window_rect = pygame.Rect(self.x + 5, self.y + 5, self.height - 10, 20)
        else:  # truck
            if self.direction == Direction.RIGHT:
                window_rect = pygame.Rect(self.x + self.width - 40, self.y + 5, 30, self.height - 10)
            elif self.direction == Direction.LEFT:
                window_rect = pygame.Rect(self.x + 10, self.y + 5, 30, self.height - 10)
            else:
                window_rect = pygame.Rect(self.x + 5, self.y + 5, self.height - 10, 30)
                
        pygame.draw.rect(screen, window_color, window_rect, border_radius=3)
        
        # Gambar roda
        wheel_radius = 8
        wheel_color = BLACK
        if self.direction == Direction.RIGHT or self.direction == Direction.LEFT:
            pygame.draw.circle(screen, wheel_color, (self.x + 20, self.y + self.height), wheel_radius)
            pygame.draw.circle(screen, wheel_color, (self.x + self.width - 20, self.y + self.height), wheel_radius)
        else:
            pygame.draw.circle(screen, wheel_color, (self.x + self.height//2, self.y + 20), wheel_radius)
            pygame.draw.circle(screen, wheel_color, (self.x + self.height//2, self.y + self.width - 20), wheel_radius)
            
        # Gambar lampu depan
        if self.direction == Direction.RIGHT:
            pygame.draw.circle(screen, YELLOW, (self.x + self.width, self.y + self.height//2), 5)
        elif self.direction == Direction.LEFT:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y + self.height//2), 5)
        elif self.direction == Direction.DOWN:
            pygame.draw.circle(screen, YELLOW, (self.x + self.height//2, self.y + self.width), 5)
        elif self.direction == Direction.UP:
            pygame.draw.circle(screen, YELLOW, (self.x + self.height//2, self.y), 5)

# Kelas untuk lampu lalu lintas
class TrafficLight:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 75
        self.state = TrafficLightState.RED
        self.timer = 0
        self.state_duration = {
            TrafficLightState.RED: 180,    # 3 detik
            TrafficLightState.YELLOW: 60,  # 1 detik
            TrafficLightState.GREEN: 120   # 2 detik
        }
        
    def update(self):
        self.timer += 1
        if self.timer >= self.state_duration[self.state]:
            self.timer = 0
            if self.state == TrafficLightState.RED:
                self.state = TrafficLightState.GREEN
            elif self.state == TrafficLightState.GREEN:
                self.state = TrafficLightState.YELLOW
            elif self.state == TrafficLightState.YELLOW:
                self.state = TrafficLightState.RED
                
    def draw(self, screen):
        # Gambar tiang
        pygame.draw.rect(screen, DARK_GRAY, (self.x - 4, self.y, 8, 120))
        
        # Gambar kotak lampu
        box_rect = pygame.Rect(self.x - self.width//2, self.y - self.height, self.width, self.height)
        pygame.draw.rect(screen, DARK_GRAY, box_rect, border_radius=5)
        
        # Gambar lampu
        red_pos = (self.x, self.y - self.height + 20)
        yellow_pos = (self.x, self.y - self.height//2)
        green_pos = (self.x, self.y - 20)
        
        # Lampu merah
        if self.state == TrafficLightState.RED:
            pygame.draw.circle(screen, RED, red_pos, 10)
        else:
            pygame.draw.circle(screen, (100, 0, 0), red_pos, 10)
            
        # Lampu kuning
        if self.state == TrafficLightState.YELLOW:
            pygame.draw.circle(screen, YELLOW, yellow_pos, 10)
        else:
            pygame.draw.circle(screen, (100, 100, 0), yellow_pos, 10)
            
        # Lampu hijau
        if self.state == TrafficLightState.GREEN:
            pygame.draw.circle(screen, GREEN, green_pos, 10)
        else:
            pygame.draw.circle(screen, (0, 100, 0), green_pos, 10)

# Kelas untuk misi
class Mission:
    def __init__(self, x, y, mission_type, question=None, answer=None, action=None):
        self.x = x
        self.y = y
        self.radius = 25
        self.mission_type = mission_type
        self.question = question
        self.answer = answer
        self.action = action
        self.completed = False
        self.active = False
        self.animation_counter = 0
        
    def update(self):
        self.animation_counter += 0.05
        
    def draw(self, screen):
        if self.completed:
            return
            
        # Animasi pulsing
        pulse = math.sin(self.animation_counter) * 3
        radius = self.radius + pulse
        
        # Gambar ikon misi
        if self.mission_type == MissionType.QUESTION:
            # Tanda tanya
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), int(radius))
            pygame.draw.circle(screen, BLACK, (self.x, self.y), int(radius), 2)
            font = pygame.font.SysFont('Arial', 24, bold=True)
            text = font.render("?", True, BLACK)
            text_rect = text.get_rect(center=(self.x, self.y))
            screen.blit(text, text_rect)
        elif self.mission_type == MissionType.ACTION:
            # Tanda seru
            pygame.draw.circle(screen, ORANGE, (self.x, self.y), int(radius))
            pygame.draw.circle(screen, BLACK, (self.x, self.y), int(radius), 2)
            font = pygame.font.SysFont('Arial', 24, bold=True)
            text = font.render("!", True, BLACK)
            text_rect = text.get_rect(center=(self.x, self.y))
            screen.blit(text, text_rect)
        elif self.mission_type == MissionType.TREASURE:
            # Kotak harta karun
            size = int(radius * 1.5)
            pygame.draw.rect(screen, BROWN, (self.x - size//2, self.y - size//2, 
                                            size, size), border_radius=5)
            pygame.draw.rect(screen, YELLOW, (self.x - size//2 + 5, self.y - size//2 + 5, 
                                            size - 10, size - 10), border_radius=3)
            # Gambar kunci
            pygame.draw.rect(screen, YELLOW, (self.x - 3, self.y - size//2 + 10, 6, 10))
            pygame.draw.circle(screen, YELLOW, (self.x, self.y - size//2 + 5), 5, 1)

# Kelas untuk mini map
class MiniMap:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale_x = width / SCREEN_WIDTH
        self.scale_y = height / SCREEN_HEIGHT
        
    def draw(self, screen, player, missions, traffic_lights):
        # Gambar background mini map
        pygame.draw.rect(screen, LIGHT_BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        # Gambar jalan horizontal utama di mini map
        road_width = 40
        pygame.draw.rect(screen, GRAY, (self.x, self.y + self.height//2 - road_width//2, 
                                        self.width, road_width))
        
        # Gambar jalan vertikal utama di mini map
        pygame.draw.rect(screen, GRAY, (self.x + self.width//2 - road_width//2, self.y, 
                                        road_width, self.height))
        
        # Gambar jalan horizontal kedua di mini map
        pygame.draw.rect(screen, GRAY, (self.x, self.y + self.height//4 - road_width//2, 
                                        self.width, road_width))
        
        # Gambar jalan vertikal kedua di mini map
        pygame.draw.rect(screen, GRAY, (self.x + self.width//4 - road_width//2, self.y, 
                                        road_width, self.height))
        
        # Gambar jalan horizontal ketiga di mini map
        pygame.draw.rect(screen, GRAY, (self.x, self.y + 3*self.height//4 - road_width//2, 
                                        self.width, road_width))
        
        # Gambar jalan vertikal ketiga di mini map
        pygame.draw.rect(screen, GRAY, (self.x + 3*self.width//4 - road_width//2, self.y, 
                                        road_width, self.height))
        
        # Gambar posisi pemain
        player_x = self.x + player.x * self.scale_x
        player_y = self.y + player.y * self.scale_y
        pygame.draw.circle(screen, BLUE, (int(player_x), int(player_y)), 4)
        
        # Gambar posisi misi
        for mission in missions:
            if not mission.completed:
                mission_x = self.x + mission.x * self.scale_x
                mission_y = self.y + mission.y * self.scale_y
                if mission.mission_type == MissionType.QUESTION:
                    pygame.draw.circle(screen, YELLOW, (int(mission_x), int(mission_y)), 3)
                elif mission.mission_type == MissionType.ACTION:
                    pygame.draw.circle(screen, ORANGE, (int(mission_x), int(mission_y)), 3)
                elif mission.mission_type == MissionType.TREASURE:
                    pygame.draw.rect(screen, BROWN, (int(mission_x) - 3, int(mission_y) - 3, 6, 6))
        
        # Gambar posisi lampu lalu lintas
        for light in traffic_lights:
            light_x = self.x + light.x * self.scale_x
            light_y = self.y + light.y * self.scale_y
            if light.state == TrafficLightState.RED:
                pygame.draw.circle(screen, RED, (int(light_x), int(light_y)), 3)
            elif light.state == TrafficLightState.GREEN:
                pygame.draw.circle(screen, GREEN, (int(light_x), int(light_y)), 3)
            else:
                pygame.draw.circle(screen, YELLOW, (int(light_x), int(light_y)), 3)

# Kelas untuk Achievement
class Achievement:
    def __init__(self, name, description, condition):
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False
        
    def check_unlock(self, score, lives, missions_completed):
        if not self.unlocked:
            if self.condition == "score_100" and score >= 100:
                self.unlocked = True
                return True
            elif self.condition == "score_200" and score >= 200:
                self.unlocked = True
                return True
            elif self.condition == "all_missions" and missions_completed:
                self.unlocked = True
                return True
            elif self.condition == "no_hit" and lives == 3 and missions_completed >= 5:
                self.unlocked = True
                return True
        return False

# Fungsi untuk menggambar jalan
def draw_road(screen):
    # Gambar jalan horizontal utama
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT//2 - 60, SCREEN_WIDTH, 120))
    
    # Gambar garis tengah jalan
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.rect(screen, YELLOW, (x, SCREEN_HEIGHT//2 - 2, 20, 4))
    
    # Gambar trotoar
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, SCREEN_HEIGHT//2 - 70, SCREEN_WIDTH, 10))
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, SCREEN_HEIGHT//2 + 60, SCREEN_WIDTH, 10))
    
    # Gambar jalan vertikal utama
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH//2 - 60, 0, 120, SCREEN_HEIGHT))
    
    # Gambar garis tengah jalan vertikal
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH//2 - 2, y, 4, 20))
    
    # Gambar zebra cross di persimpangan utama
    for i in range(5):
        y_offset = SCREEN_HEIGHT//2 - 50 + i * 20
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 60, y_offset, 120, 10))
        
    for i in range(5):
        x_offset = SCREEN_WIDTH//2 - 50 + i * 20
        pygame.draw.rect(screen, WHITE, (x_offset, SCREEN_HEIGHT//2 - 60, 10, 120))
    
    # Gambar jalan horizontal kedua (atas)
    pygame.draw.rect(screen, GRAY, (0, SCREEN_HEIGHT//4 - 40, SCREEN_WIDTH, 80))
    
    # Gambar garis tengah jalan horizontal kedua
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.rect(screen, YELLOW, (x, SCREEN_HEIGHT//4 - 2, 20, 4))
    
    # Gambar trotoar jalan horizontal kedua
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, SCREEN_HEIGHT//4 - 50, SCREEN_WIDTH, 10))
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, SCREEN_HEIGHT//4 + 40, SCREEN_WIDTH, 10))
    
    # Gambar jalan horizontal ketiga (bawah)
    pygame.draw.rect(screen, GRAY, (0, 3*SCREEN_HEIGHT//4 - 40, SCREEN_WIDTH, 80))
    
    # Gambar garis tengah jalan horizontal ketiga
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.rect(screen, YELLOW, (x, 3*SCREEN_HEIGHT//4 - 2, 20, 4))
    
    # Gambar trotoar jalan horizontal ketiga
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, 3*SCREEN_HEIGHT//4 - 50, SCREEN_WIDTH, 10))
    pygame.draw.rect(screen, SIDEWALK_COLOR, (0, 3*SCREEN_HEIGHT//4 + 40, SCREEN_WIDTH, 10))
    
    # Gambar jalan vertikal kedua (kiri)
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH//4 - 40, 0, 80, SCREEN_HEIGHT))
    
    # Gambar garis tengah jalan vertikal kedua
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (SCREEN_WIDTH//4 - 2, y, 4, 20))
    
    # Gambar trotoar jalan vertikal kedua
    pygame.draw.rect(screen, SIDEWALK_COLOR, (SCREEN_WIDTH//4 - 50, 0, 10, SCREEN_HEIGHT))
    pygame.draw.rect(screen, SIDEWALK_COLOR, (SCREEN_WIDTH//4 + 40, 0, 10, SCREEN_HEIGHT))
    
    # Gambar jalan vertikal ketiga (kanan)
    pygame.draw.rect(screen, GRAY, (3*SCREEN_WIDTH//4 - 40, 0, 80, SCREEN_HEIGHT))
    
    # Gambar garis tengah jalan vertikal ketiga
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.rect(screen, YELLOW, (3*SCREEN_WIDTH//4 - 2, y, 4, 20))
    
    # Gambar trotoar jalan vertikal ketiga
    pygame.draw.rect(screen, SIDEWALK_COLOR, (3*SCREEN_WIDTH//4 - 50, 0, 10, SCREEN_HEIGHT))
    pygame.draw.rect(screen, SIDEWALK_COLOR, (3*SCREEN_WIDTH//4 + 40, 0, 10, SCREEN_HEIGHT))
    
    # Gambar zebra cross di persimpangan kedua (atas)
    for i in range(5):
        y_offset = SCREEN_HEIGHT//4 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 60, y_offset, 120, 8))
        
    for i in range(5):
        x_offset = SCREEN_WIDTH//2 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (x_offset, SCREEN_HEIGHT//4 - 40, 8, 80))
    
    # Gambar zebra cross di persimpangan ketiga (bawah)
    for i in range(5):
        y_offset = 3*SCREEN_HEIGHT//4 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//2 - 60, y_offset, 120, 8))
        
    for i in range(5):
        x_offset = SCREEN_WIDTH//2 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (x_offset, 3*SCREEN_HEIGHT//4 - 40, 8, 80))
    
    # Gambar zebra cross di persimpangan keempat (kiri)
    for i in range(5):
        y_offset = SCREEN_HEIGHT//2 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH//4 - 40, y_offset, 80, 8))
        
    for i in range(5):
        x_offset = SCREEN_WIDTH//4 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (x_offset, SCREEN_HEIGHT//2 - 60, 8, 120))
    
    # Gambar zebra cross di persimpangan kelima (kanan)
    for i in range(5):
        y_offset = SCREEN_HEIGHT//2 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (3*SCREEN_WIDTH//4 - 40, y_offset, 80, 8))
        
    for i in range(5):
        x_offset = 3*SCREEN_WIDTH//4 - 30 + i * 12
        pygame.draw.rect(screen, WHITE, (x_offset, SCREEN_HEIGHT//2 - 60, 8, 120))

# Fungsi untuk menggambar background
def draw_background(screen):
    # Gambar langit
    screen.fill(LIGHT_BLUE)
    
    # Gambar awan
    for i in range(10):
        x = 100 + i * 140
        y = 50 + (i % 3) * 40
        pygame.draw.ellipse(screen, WHITE, (x, y, 70, 35))
        pygame.draw.ellipse(screen, WHITE, (x + 25, y - 12, 70, 35))
        pygame.draw.ellipse(screen, WHITE, (x + 50, y, 70, 35))
    
    # Gambar area rumput di antara jalan
    grass_areas = [
        {"x": 0, "y": 0, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT//4 - 70},
        {"x": 0, "y": SCREEN_HEIGHT//4 + 50, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT//4 - 110},
        {"x": 0, "y": SCREEN_HEIGHT//2 + 70, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT//4 - 110},
        {"x": 0, "y": 3*SCREEN_HEIGHT//4 + 50, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT - (3*SCREEN_HEIGHT//4 + 50)}
    ]
    
    for grass in grass_areas:
        pygame.draw.rect(screen, GRASS_GREEN, (grass["x"], grass["y"], grass["width"], grass["height"]))
    
    # Gambar gedung di background
    buildings = [
        # Area atas
        {"x": 50, "y": 100, "width": 120, "height": 200, "color": random.choice(BUILDING_COLORS)},
        {"x": 200, "y": 150, "width": 100, "height": 150, "color": random.choice(BUILDING_COLORS)},
        {"x": 330, "y": 80, "width": 150, "height": 220, "color": random.choice(BUILDING_COLORS)},
        {"x": 520, "y": 120, "width": 110, "height": 180, "color": random.choice(BUILDING_COLORS)},
        {"x": 670, "y": 90, "width": 130, "height": 210, "color": random.choice(BUILDING_COLORS)},
        {"x": 840, "y": 140, "width": 100, "height": 160, "color": random.choice(BUILDING_COLORS)},
        {"x": 980, "y": 100, "width": 120, "height": 200, "color": random.choice(BUILDING_COLORS)},
        {"x": 1150, "y": 130, "width": 140, "height": 190, "color": random.choice(BUILDING_COLORS)},
        
        # Area tengah kiri
        {"x": 50, "y": 400, "width": 130, "height": 180, "color": random.choice(BUILDING_COLORS)},
        {"x": 200, "y": 450, "width": 110, "height": 160, "color": random.choice(BUILDING_COLORS)},
        
        # Area tengah kanan
        {"x": 1050, "y": 400, "width": 130, "height": 180, "color": random.choice(BUILDING_COLORS)},
        {"x": 1200, "y": 450, "width": 110, "height": 160, "color": random.choice(BUILDING_COLORS)},
        
        # Area bawah
        {"x": 50, "y": 700, "width": 120, "height": 170, "color": random.choice(BUILDING_COLORS)},
        {"x": 200, "y": 750, "width": 100, "height": 150, "color": random.choice(BUILDING_COLORS)},
        {"x": 350, "y": 680, "width": 140, "height": 190, "color": random.choice(BUILDING_COLORS)},
        {"x": 520, "y": 720, "width": 120, "height": 160, "color": random.choice(BUILDING_COLORS)},
        {"x": 670, "y": 690, "width": 130, "height": 180, "color": random.choice(BUILDING_COLORS)},
        {"x": 840, "y": 740, "width": 110, "height": 150, "color": random.choice(BUILDING_COLORS)},
        {"x": 980, "y": 700, "width": 120, "height": 170, "color": random.choice(BUILDING_COLORS)},
        {"x": 1150, "y": 750, "width": 140, "height": 150, "color": random.choice(BUILDING_COLORS)},
        
        # Area kiri jalan vertikal
        {"x": 50, "y": 250, "width": 100, "height": 120, "color": random.choice(BUILDING_COLORS)},
        {"x": 50, "y": 550, "width": 100, "height": 120, "color": random.choice(BUILDING_COLORS)},
        
        # Area kanan jalan vertikal
        {"x": 1250, "y": 250, "width": 100, "height": 120, "color": random.choice(BUILDING_COLORS)},
        {"x": 1250, "y": 550, "width": 100, "height": 120, "color": random.choice(BUILDING_COLORS)}
    ]
    
    for building in buildings:
        # Gambar badan gedung
        pygame.draw.rect(screen, building["color"], 
                        (building["x"], building["y"], building["width"], building["height"]))
        
        # Gambar atap
        roof_points = [
            (building["x"] - 10, building["y"]),
            (building["x"] + building["width"]//2, building["y"] - 30),
            (building["x"] + building["width"] + 10, building["y"])
        ]
        pygame.draw.polygon(screen, (150, 50, 50), roof_points)
        
        # Gambar jendela
        window_rows = building["height"] // 40
        window_cols = building["width"] // 30
        
        for row in range(window_rows):
            for col in range(window_cols):
                if random.random() > 0.3:  # Beberapa jendela mati
                    window_x = building["x"] + 15 + col * 30
                    window_y = building["y"] + 20 + row * 40
                    pygame.draw.rect(screen, (150, 180, 220), (window_x, window_y, 20, 25))
    
    # Gambar pohon
    trees = [
        # Area atas
        {"x": 150, "y": SCREEN_HEIGHT//4 - 50},
        {"x": 400, "y": SCREEN_HEIGHT//4 - 50},
        {"x": 650, "y": SCREEN_HEIGHT//4 - 50},
        {"x": 900, "y": SCREEN_HEIGHT//4 - 50},
        {"x": 1150, "y": SCREEN_HEIGHT//4 - 50},
        
        # Area tengah
        {"x": 150, "y": SCREEN_HEIGHT//2 - 150},
        {"x": 400, "y": SCREEN_HEIGHT//2 - 150},
        {"x": 650, "y": SCREEN_HEIGHT//2 - 150},
        {"x": 900, "y": SCREEN_HEIGHT//2 - 150},
        {"x": 1150, "y": SCREEN_HEIGHT//2 - 150},
        
        # Area bawah
        {"x": 150, "y": 3*SCREEN_HEIGHT//4 - 50},
        {"x": 400, "y": 3*SCREEN_HEIGHT//4 - 50},
        {"x": 650, "y": 3*SCREEN_HEIGHT//4 - 50},
        {"x": 900, "y": 3*SCREEN_HEIGHT//4 - 50},
        {"x": 1150, "y": 3*SCREEN_HEIGHT//4 - 50},
        
        # Area kiri jalan vertikal
        {"x": SCREEN_WIDTH//4 - 50, "y": 150},
        {"x": SCREEN_WIDTH//4 - 50, "y": 350},
        {"x": SCREEN_WIDTH//4 - 50, "y": 550},
        {"x": SCREEN_WIDTH//4 - 50, "y": 750},
        
        # Area kanan jalan vertikal
        {"x": 3*SCREEN_WIDTH//4 - 50, "y": 150},
        {"x": 3*SCREEN_WIDTH//4 - 50, "y": 350},
        {"x": 3*SCREEN_WIDTH//4 - 50, "y": 550},
        {"x": 3*SCREEN_WIDTH//4 - 50, "y": 750}
    ]
    
    for tree in trees:
        # Gambar batang pohon
        pygame.draw.rect(screen, BROWN, (tree["x"] - 5, tree["y"], 10, 40))
        
        # Gambar daun
        pygame.draw.circle(screen, (0, 150, 0), (tree["x"], tree["y"] - 10), 25)
        pygame.draw.circle(screen, (0, 170, 0), (tree["x"] - 15, tree["y"] - 5), 20)
        pygame.draw.circle(screen, (0, 170, 0), (tree["x"] + 15, tree["y"] - 5), 20)
        pygame.draw.circle(screen, (0, 190, 0), (tree["x"], tree["y"] - 25), 22)

# Fungsi untuk menampilkan dialog
def show_dialog(screen, title, message, options=None):
    # Gambar background dialog
    dialog_width = 700
    dialog_height = 350
    dialog_x = (SCREEN_WIDTH - dialog_width) // 2
    dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
    
    pygame.draw.rect(screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), border_radius=15)
    pygame.draw.rect(screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3, border_radius=15)
    
    # Gambar judul
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    title_text = title_font.render(title, True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 50))
    screen.blit(title_text, title_rect)
    
    # Gambar pesan
    message_font = pygame.font.SysFont('Arial', 24)
    words = message.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        text_width, _ = message_font.size(test_line)
        
        if text_width > dialog_width - 60:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    y_offset = dialog_y + 100
    for line in lines:
        line_text = message_font.render(line, True, BLACK)
        line_rect = line_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(line_text, line_rect)
        y_offset += 35
    
    # Gambar opsi jika ada
    if options:
        option_font = pygame.font.SysFont('Arial', 22)
        option_y = dialog_y + dialog_height - 80
        
        for i, option in enumerate(options):
            option_text = option_font.render(f"{i+1}. {option}", True, BLACK)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, option_y))
            screen.blit(option_text, option_rect)
            option_y += 30

# Fungsi untuk menampilkan game over
def show_game_over(screen, score):
    # Gambar background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    # Gambar kotak game over
    box_width = 600
    box_height = 400
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = (SCREEN_HEIGHT - box_height) // 2
    
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=20)
    pygame.draw.rect(screen, RED, (box_x, box_y, box_width, box_height), 5, border_radius=20)
    
    # Gambar teks
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    title_text = title_font.render("GAME OVER", True, RED)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 80))
    screen.blit(title_text, title_rect)
    
    score_font = pygame.font.SysFont('Arial', 36)
    score_text = score_font.render(f"Skor Akhir: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 160))
    screen.blit(score_text, score_rect)
    
    restart_font = pygame.font.SysFont('Arial', 28)
    restart_text = restart_font.render("Tekan SPACE untuk memulai kembali", True, BLACK)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 250))
    screen.blit(restart_text, restart_rect)

# Fungsi untuk menampilkan achievement
def show_achievement(screen, achievement):
    # Gambar background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    
    # Gambar kotak achievement
    box_width = 600
    box_height = 200
    box_x = (SCREEN_WIDTH - box_width) // 2
    box_y = 100
    
    pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), border_radius=15)
    pygame.draw.rect(screen, YELLOW, (box_x, box_y, box_width, box_height), 3, border_radius=15)
    
    # Gambar teks
    title_font = pygame.font.SysFont('Arial', 32, bold=True)
    title_text = title_font.render("ACHIEVEMENT UNLOCKED!", True, YELLOW)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 50))
    screen.blit(title_text, title_rect)
    
    name_font = pygame.font.SysFont('Arial', 28, bold=True)
    name_text = name_font.render(achievement.name, True, BLACK)
    name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 100))
    screen.blit(name_text, name_rect)
    
    desc_font = pygame.font.SysFont('Arial', 22)
    desc_text = desc_font.render(achievement.description, True, BLACK)
    desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 150))
    screen.blit(desc_text, desc_rect)

# Fungsi untuk menampilkan HUD
def draw_hud(screen, player, score):
    # Gambar background HUD
    pygame.draw.rect(screen, (0, 0, 0, 150), (10, 10, 300, 80), border_radius=10)
    
    # Gambar skor
    score_font = pygame.font.SysFont('Arial', 28, bold=True)
    score_text = score_font.render(f"Skor: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))
    
    # Gambar nyawa
    life_font = pygame.font.SysFont('Arial', 24)
    life_text = life_font.render("Nyawa: ", True, WHITE)
    screen.blit(life_text, (20, 55))
    
    # Gambar ikon nyawa
    for i in range(player.lives):
        heart_x = 90 + i * 30
        heart_y = 60
        # Gambar hati
        pygame.draw.circle(screen, RED, (heart_x, heart_y), 8)
        pygame.draw.circle(screen, RED, (heart_x + 10, heart_y), 8)
        pygame.draw.polygon(screen, RED, [(heart_x - 8, heart_y + 3), 
                                         (heart_x + 18, heart_y + 3), 
                                         (heart_x + 5, heart_y + 15)])

# Fungsi utama game
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Petualangan Lalu Lintas - Belajar Rambu Lalu Lintas")
    clock = pygame.time.Clock()
    
    # Buat objek game
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    
    # Buat kendaraan
    vehicles = [
        # Jalan horizontal utama
        Vehicle(100, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, RED, 2, "car"),
        Vehicle(300, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, BLUE, 3, "car"),
        Vehicle(500, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, GREEN, 2.5, "car"),
        Vehicle(700, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, YELLOW, 2, "car"),
        Vehicle(900, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, (255, 0, 255), 2.5, "car"),
        Vehicle(1100, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, (0, 128, 128), 3, "car"),
        Vehicle(200, SCREEN_HEIGHT//2 - 30, Direction.LEFT, ORANGE, 2.5, "car"),
        Vehicle(400, SCREEN_HEIGHT//2 - 30, Direction.LEFT, (0, 255, 255), 3, "car"),
        Vehicle(600, SCREEN_HEIGHT//2 - 30, Direction.LEFT, (255, 165, 0), 2, "car"),
        Vehicle(800, SCREEN_HEIGHT//2 - 30, Direction.LEFT, (128, 0, 128), 2.5, "car"),
        Vehicle(1000, SCREEN_HEIGHT//2 - 30, Direction.LEFT, (0, 128, 128), 3, "car"),
        Vehicle(1200, SCREEN_HEIGHT//2 - 30, Direction.LEFT, (128, 128, 0), 2.2, "car"),
        
        # Truk di jalan horizontal utama
        Vehicle(150, SCREEN_HEIGHT//2 + 30, Direction.RIGHT, (100, 100, 100), 1.5, "truck"),
        Vehicle(650, SCREEN_HEIGHT//2 - 30, Direction.LEFT, (120, 120, 120), 1.8, "truck"),
        
        # Jalan horizontal kedua (atas)
        Vehicle(100, SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (200, 100, 0), 2.2, "car"),
        Vehicle(400, SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (0, 100, 200), 2.8, "car"),
        Vehicle(700, SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (100, 200, 0), 2.5, "car"),
        Vehicle(1000, SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (200, 0, 100), 2.2, "car"),
        Vehicle(200, SCREEN_HEIGHT//4 - 20, Direction.LEFT, (100, 0, 200), 2.5, "car"),
        Vehicle(500, SCREEN_HEIGHT//4 - 20, Direction.LEFT, (0, 200, 100), 2.8, "car"),
        Vehicle(800, SCREEN_HEIGHT//4 - 20, Direction.LEFT, (200, 100, 0), 2.2, "car"),
        Vehicle(1100, SCREEN_HEIGHT//4 - 20, Direction.LEFT, (100, 200, 0), 2.5, "car"),
        
        # Jalan horizontal ketiga (bawah)
        Vehicle(150, 3*SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (0, 100, 200), 2.5, "car"),
        Vehicle(450, 3*SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (200, 0, 100), 2.2, "car"),
        Vehicle(750, 3*SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (100, 200, 0), 2.8, "car"),
        Vehicle(1050, 3*SCREEN_HEIGHT//4 + 20, Direction.RIGHT, (200, 100, 0), 2.5, "car"),
        Vehicle(250, 3*SCREEN_HEIGHT//4 - 20, Direction.LEFT, (100, 0, 200), 2.2, "car"),
        Vehicle(550, 3*SCREEN_HEIGHT//4 - 20, Direction.LEFT, (0, 200, 100), 2.8, "car"),
        Vehicle(850, 3*SCREEN_HEIGHT//4 - 20, Direction.LEFT, (200, 100, 0), 2.5, "car"),
        Vehicle(1150, 3*SCREEN_HEIGHT//4 - 20, Direction.LEFT, (100, 200, 0), 2.2, "car"),
        
        # Jalan vertikal utama
        Vehicle(SCREEN_WIDTH//2 + 30, 100, Direction.DOWN, (200, 100, 0), 2, "car"),
        Vehicle(SCREEN_WIDTH//2 - 30, 300, Direction.UP, (0, 100, 200), 2.5, "car"),
        Vehicle(SCREEN_WIDTH//2 + 30, 500, Direction.DOWN, (100, 200, 0), 2.2, "car"),
        Vehicle(SCREEN_WIDTH//2 - 30, 700, Direction.UP, (200, 0, 100), 2.8, "car"),
        
        # Jalan vertikal kedua (kiri)
        Vehicle(SCREEN_WIDTH//4 + 20, 150, Direction.DOWN, (100, 0, 200), 2.5, "car"),
        Vehicle(SCREEN_WIDTH//4 - 20, 350, Direction.UP, (0, 200, 100), 2.2, "car"),
        Vehicle(SCREEN_WIDTH//4 + 20, 550, Direction.DOWN, (200, 100, 0), 2.8, "car"),
        Vehicle(SCREEN_WIDTH//4 - 20, 750, Direction.UP, (100, 200, 0), 2.5, "car"),
        
        # Jalan vertikal ketiga (kanan)
        Vehicle(3*SCREEN_WIDTH//4 + 20, 200, Direction.DOWN, (0, 200, 100), 2.2, "car"),
        Vehicle(3*SCREEN_WIDTH//4 - 20, 400, Direction.UP, (200, 100, 0), 2.8, "car"),
        Vehicle(3*SCREEN_WIDTH//4 + 20, 600, Direction.DOWN, (100, 0, 200), 2.5, "car"),
        Vehicle(3*SCREEN_WIDTH//4 - 20, 800, Direction.UP, (0, 100, 200), 2.2, "car")
    ]
    
    # Buat lampu lalu lintas
    traffic_lights = [
        # Persimpangan utama
        TrafficLight(300, SCREEN_HEIGHT//2 - 120),
        TrafficLight(700, SCREEN_HEIGHT//2 - 120),
        TrafficLight(SCREEN_WIDTH//2 - 120, 300),
        TrafficLight(SCREEN_WIDTH//2 + 120, 500),
        
        # Persimpangan atas
        TrafficLight(300, SCREEN_HEIGHT//4 - 80),
        TrafficLight(700, SCREEN_HEIGHT//4 - 80),
        TrafficLight(SCREEN_WIDTH//2 - 120, 150),
        TrafficLight(SCREEN_WIDTH//2 + 120, 250),
        
        # Persimpangan bawah
        TrafficLight(300, 3*SCREEN_HEIGHT//4 - 80),
        TrafficLight(700, 3*SCREEN_HEIGHT//4 - 80),
        TrafficLight(SCREEN_WIDTH//2 - 120, 550),
        TrafficLight(SCREEN_WIDTH//2 + 120, 650),
        
        # Persimpangan kiri
        TrafficLight(SCREEN_WIDTH//4 - 80, 300),
        TrafficLight(SCREEN_WIDTH//4 - 80, 500),
        TrafficLight(150, SCREEN_HEIGHT//2 - 120),
        TrafficLight(250, SCREEN_HEIGHT//2 + 40),
        
        # Persimpangan kanan
        TrafficLight(3*SCREEN_WIDTH//4 - 80, 300),
        TrafficLight(3*SCREEN_WIDTH//4 - 80, 500),
        TrafficLight(1050, SCREEN_HEIGHT//2 - 120),
        TrafficLight(1150, SCREEN_HEIGHT//2 + 40)
    ]
    
    # Buat misi
    missions = [
        # Misi di persimpangan utama
        Mission(200, SCREEN_HEIGHT//2 - 180, MissionType.QUESTION, 
                "Apa arti lampu lalu lintas berwarna merah?", "Berhenti"),
        Mission(500, SCREEN_HEIGHT//2 - 180, MissionType.ACTION, 
                None, None, "Berhenti saat lampu merah"),
        Mission(800, SCREEN_HEIGHT//2 - 180, MissionType.TREASURE),
        Mission(300, SCREEN_HEIGHT//2 + 180, MissionType.QUESTION, 
                "Apa arti rambu berbentuk segitiga dengan warna merah?", "Peringatan"),
        Mission(700, SCREEN_HEIGHT//2 + 180, MissionType.ACTION, 
                None, None, "Jalan saat lampu hijau"),
        
        # Misi di persimpangan atas
        Mission(200, SCREEN_HEIGHT//4 - 120, MissionType.QUESTION, 
                "Apa arti rambu berbentuk lingkaran dengan warna merah dan garis diagonal?", "Dilarang"),
        Mission(500, SCREEN_HEIGHT//4 - 120, MissionType.ACTION, 
                None, None, "Berhati-hati di zebra cross"),
        Mission(800, SCREEN_HEIGHT//4 - 120, MissionType.TREASURE),
        Mission(300, SCREEN_HEIGHT//4 + 80, MissionType.QUESTION, 
                "Apa arti rambu berbentuk segi empat dengan warna biru?", "Kewajiban"),
        Mission(700, SCREEN_HEIGHT//4 + 80, MissionType.ACTION, 
                None, None, "Prioritaskan pejalan kaki"),
        
        # Misi di persimpangan bawah
        Mission(200, 3*SCREEN_HEIGHT//4 - 120, MissionType.QUESTION, 
                "Apa yang harus dilakukan saat melihat rambu berhenti?", "Berhenti total"),
        Mission(500, 3*SCREEN_HEIGHT//4 - 120, MissionType.ACTION, 
                None, None, "Lihat ke kiri dan kanan"),
        Mission(800, 3*SCREEN_HEIGHT//4 - 120, MissionType.TREASURE),
        Mission(300, 3*SCREEN_HEIGHT//4 + 80, MissionType.QUESTION, 
                "Apa arti rambu dengan gambar anak menyeberang?", "Penyeberangan pejalan kaki"),
        Mission(700, 3*SCREEN_HEIGHT//4 + 80, MissionType.ACTION, 
                None, None, "Berjalan di trotoar"),
        
        # Misi di persimpangan kiri
        Mission(SCREEN_WIDTH//4 - 120, 200, MissionType.QUESTION, 
                "Apa arti rambu dengan gambar sepeda?", "Lintasan sepeda"),
        Mission(SCREEN_WIDTH//4 - 120, 400, MissionType.ACTION, 
                None, None, "Hati-hati dengan sepeda"),
        Mission(SCREEN_WIDTH//4 - 120, 600, MissionType.TREASURE),
        
        # Misi di persimpangan kanan
        Mission(3*SCREEN_WIDTH//4 - 120, 200, MissionType.QUESTION, 
                "Apa arti rambu dengan gambar orang berjalan?", "Hanya untuk pejalan kaki"),
        Mission(3*SCREEN_WIDTH//4 - 120, 400, MissionType.ACTION, 
                None, None, "Jangan berjalan di jalan raya"),
        Mission(3*SCREEN_WIDTH//4 - 120, 600, MissionType.TREASURE),
        
        # Misi tambahan di area terbuka
        Mission(SCREEN_WIDTH//4, SCREEN_HEIGHT//4, MissionType.QUESTION, 
                "Apa yang harus dilakukan sebelum menyeberang jalan?", "Lihat kiri kanan kiri lagi"),
        Mission(3*SCREEN_WIDTH//4, SCREEN_HEIGHT//4, MissionType.ACTION, 
                None, None, "Tunggu sampai aman"),
        Mission(SCREEN_WIDTH//4, 3*SCREEN_HEIGHT//4, MissionType.TREASURE),
        Mission(3*SCREEN_WIDTH//4, 3*SCREEN_HEIGHT//4, MissionType.QUESTION, 
                "Mengapa kita harus mematuhi rambu lalu lintas?", "Untuk keselamatan")
    ]
    
    # Buat mini map
    minimap = MiniMap(SCREEN_WIDTH - 200, 20, 180, 140)
    
    # Buat achievement
    achievements = [
        Achievement("Pemula", "Dapatkan skor 100 poin", "score_100"),
        Achievement("Ahli Lalu Lintas", "Dapatkan skor 200 poin", "score_200"),
        Achievement("Petualang Sejati", "Selesaikan semua misi", "all_missions"),
        Achievement("Pemburu Aman", "Selesaikan 5 misi tanpa terkena tabrakan", "no_hit")
    ]
    
    # Variabel game
    running = True
    game_state = GameState.PLAYING
    current_mission = None
    dialog_active = False
    dialog_title = ""
    dialog_message = ""
    dialog_options = []
    score = 0
    font = pygame.font.SysFont('Arial', 24)
    
    # Timer untuk dialog "Berhasil!"
    success_dialog_timer = 0
    
    # Timer untuk dialog "Harta Karun Ditemukan!"
    treasure_dialog_timer = 0
    
    # Timer untuk achievement
    achievement_timer = 0
    current_achievement = None
    achievement_queue = []  # Queue untuk achievement yang akan ditampilkan
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game_state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        # Reset game
                        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
                        score = 0
                        game_state = GameState.PLAYING
                        for mission in missions:
                            mission.completed = False
                        for achievement in achievements:
                            achievement.unlocked = False
                        achievement_queue = []
                        success_dialog_timer = 0
                        treasure_dialog_timer = 0
                elif dialog_active:
                    # Tangani input dialog
                    if event.key >= pygame.K_1 and event.key <= pygame.K_9:
                        option_index = event.key - pygame.K_1
                        if option_index < len(dialog_options):
                            if current_mission and current_mission.mission_type == MissionType.QUESTION:
                                if dialog_options[option_index] == current_mission.answer:
                                    score += 10
                                    current_mission.completed = True
                                    dialog_title = "Jawaban Benar!"
                                    dialog_message = "Kamu mendapat 10 poin."
                                else:
                                    dialog_title = "Jawaban Salah"
                                    dialog_message = "Coba lagi lain kali."
                            dialog_active = False
                    elif event.key == pygame.K_ESCAPE:
                        dialog_active = False
        
        # Update game state
        if game_state == GameState.PLAYING:
            # Keyboard input untuk gerakan pemain
            if not dialog_active:
                keys = pygame.key.get_pressed()
                dx = dy = 0
                if keys[pygame.K_LEFT]:
                    dx = -1
                if keys[pygame.K_RIGHT]:
                    dx = 1
                if keys[pygame.K_UP]:
                    dy = -1
                if keys[pygame.K_DOWN]:
                    dy = 1
                player.move(dx, dy)
            
            # Update game objects
            player.update()
            
            for vehicle in vehicles:
                vehicle.update()
            
            for light in traffic_lights:
                light.update()
                
            for mission in missions:
                mission.update()
            
            # Cek tabrakan dengan kendaraan
            if not player.invulnerable:
                for vehicle in vehicles:
                    # Cek apakah pemain berada di area yang sama dengan kendaraan
                    if (abs(player.x - vehicle.x - vehicle.width/2) < (player.width/2 + vehicle.width/2) and
                        abs(player.y - vehicle.y - vehicle.height/2) < (player.height/2 + vehicle.height/2)):
                        player.hit()
                        if player.lives <= 0:
                            game_state = GameState.GAME_OVER
            
            # Cek interaksi dengan misi
            if not dialog_active:
                for mission in missions:
                    if not mission.completed:
                        distance = math.sqrt((player.x - mission.x)**2 + (player.y - mission.y)**2)
                        if distance < 50:
                            current_mission = mission
                            mission.active = True
                            
                            if mission.mission_type == MissionType.QUESTION:
                                dialog_title = "Pertanyaan"
                                dialog_message = mission.question
                                dialog_options = [mission.answer, "Jalan terus", "Lambat", "Cepat"]
                                random.shuffle(dialog_options)
                                dialog_active = True
                            elif mission.mission_type == MissionType.ACTION:
                                # Cek apakah pemain melakukan aksi yang benar
                                light_nearby = False
                                for light in traffic_lights:
                                    light_distance = math.sqrt((player.x - light.x)**2 + (player.y - light.y)**2)
                                    if light_distance < 100:
                                        light_nearby = True
                                        if light.state == TrafficLightState.RED and not player.is_moving:
                                            score += 15
                                            mission.completed = True
                                            dialog_title = "Berhasil!"
                                            dialog_message = "Kamu berhenti dengan benar saat lampu merah. Dapat 15 poin!"
                                            dialog_active = True
                                            success_dialog_timer = 120  # 2 detik untuk dialog berhasil
                                        elif light.state == TrafficLightState.GREEN and player.is_moving:
                                            score += 15
                                            mission.completed = True
                                            dialog_title = "Berhasil!"
                                            dialog_message = "Kamu jalan dengan benar saat lampu hijau. Dapat 15 poin!"
                                            dialog_active = True
                                            success_dialog_timer = 120  # 2 detik untuk dialog berhasil
                                        break
                                
                                if not light_nearby:
                                    dialog_title = "Aksi"
                                    dialog_message = "Pergilah ke lampu lalu lintas dan lakukan aksi yang benar!"
                                    dialog_active = True
                            elif mission.mission_type == MissionType.TREASURE:
                                score += 20
                                if player.lives < 3:
                                    player.lives += 1
                                    dialog_title = "Harta Karun Ditemukan!"
                                    dialog_message = "Kamu menemukan harta karun! Dapat 20 poin dan 1 nyawa tambahan!"
                                else:
                                    dialog_title = "Harta Karun Ditemukan!"
                                    dialog_message = "Kamu menemukan harta karun! Dapat 20 poin!"
                                mission.completed = True
                                dialog_active = True
                                treasure_dialog_timer = 120  # 2 detik untuk dialog harta karun
                            break
            
            # Cek achievement
            missions_completed = sum(1 for mission in missions if mission.completed)
            for achievement in achievements:
                if achievement.check_unlock(score, player.lives, missions_completed):
                    # Tambahkan achievement ke queue
                    if achievement not in achievement_queue:
                        achievement_queue.append(achievement)
            
            # Jika tidak ada achievement yang sedang ditampilkan dan ada achievement di queue
            if current_achievement is None and achievement_queue and achievement_timer <= 0:
                current_achievement = achievement_queue.pop(0)
                achievement_timer = 180  # 3 detik
        
        # Update timer dialog "Berhasil!"
        if success_dialog_timer > 0:
            success_dialog_timer -= 1
            if success_dialog_timer <= 0:
                dialog_active = False
        
        # Update timer dialog "Harta Karun Ditemukan!"
        if treasure_dialog_timer > 0:
            treasure_dialog_timer -= 1
            if treasure_dialog_timer <= 0:
                dialog_active = False
        
        # Update achievement timer
        if achievement_timer > 0:
            achievement_timer -= 1
            if achievement_timer <= 0:
                current_achievement = None
        
        # Drawing
        draw_background(screen)
        draw_road(screen)
        
        # Gambar lampu lalu lintas
        for light in traffic_lights:
            light.draw(screen)
        
        # Gambar kendaraan
        for vehicle in vehicles:
            vehicle.draw(screen)
        
        # Gambar misi
        for mission in missions:
            mission.draw(screen)
        
        # Gambar pemain
        player.draw(screen)
        
        # Gambar mini map
        minimap.draw(screen, player, missions, traffic_lights)
        
        # Gambar HUD
        draw_hud(screen, player, score)
        
        # Gambar judul game
        title_font = pygame.font.SysFont('Arial', 36, bold=True)
        title_text = title_font.render("Petualangan Lalu Lintas", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        screen.blit(title_text, title_rect)
        
        # Gambar instruksi
        instruction_font = pygame.font.SysFont('Arial', 20)
        instructions = [
            "Gunakan tombol panah untuk bergerak",
            "Kunjungi tanda !, ?, dan kotak coklat untuk misi",
            "Pelajari rambu lalu lintas dan dapatkan poin!",
            "Hati-hati dengan kendaraan!"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = instruction_font.render(instruction, True, BLACK)
            screen.blit(inst_text, (20, SCREEN_HEIGHT - 100 + i * 25))
        
        # Gambar dialog jika aktif
        if dialog_active:
            show_dialog(screen, dialog_title, dialog_message, dialog_options)
        
        # Gambar game over
        if game_state == GameState.GAME_OVER:
            show_game_over(screen, score)
        
        # Gambar achievement
        if current_achievement:
            show_achievement(screen, current_achievement)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()