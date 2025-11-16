import pygame
import sys
import random
import math
import time

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 100, 0)

# Font
font_small = pygame.font.SysFont('Arial', 16)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)
font_xlarge = pygame.font.SysFont('Arial', 48)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surf = font_medium.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class ColorEducation:
    def __init__(self):
        self.colors = [
            (RED, "Merah"),
            (GREEN, "Hijau"),
            (BLUE, "Biru"),
            (YELLOW, "Kuning"),
            (PURPLE, "Ungu"),
            (ORANGE, "Oranye")
        ]
        self.current_color_index = 0
        self.animation_timer = 0
        self.show_name = True
        
    def update(self):
        self.animation_timer += 1
        if self.animation_timer > 120:  # Ganti warna setiap 2 detik
            self.animation_timer = 0
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.show_name = True
            
        # Sembunyikan nama setelah 1 detik
        if self.animation_timer > 60:
            self.show_name = False
            
    def draw(self, screen):
        # Judul
        title = font_large.render("Belajar Warna", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Gambar lingkaran dengan warna saat ini
        color, name = self.colors[self.current_color_index]
        pygame.draw.circle(screen, color, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 150)
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 150, 3)
        
        # Tampilkan nama warna
        if self.show_name:
            name_surf = font_xlarge.render(name, True, BLACK)
            name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250))
            screen.blit(name_surf, name_rect)
            
        # Petunjuk
        hint = font_medium.render("Perhatikan warna dan namanya!", True, BLACK)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint, hint_rect)

class NumberEducation:
    def __init__(self):
        self.current_number = 1
        self.animation_timer = 0
        self.show_number = True
        self.max_number = 10
        
    def update(self):
        self.animation_timer += 1
        if self.animation_timer > 120:  # Ganti angka setiap 2 detik
            self.animation_timer = 0
            self.current_number = (self.current_number % self.max_number) + 1
            self.show_number = True
            
        # Sembunyikan angka setelah 1 detik
        if self.animation_timer > 60:
            self.show_number = False
            
    def draw(self, screen):
        # Judul
        title = font_large.render("Belajar Angka", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Gambar kotak untuk angka
        box_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200)
        pygame.draw.rect(screen, LIGHT_GRAY, box_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, box_rect, 3, border_radius=10)
        
        # Tampilkan angka
        if self.show_number:
            number_surf = font_xlarge.render(str(self.current_number), True, BLACK)
            number_rect = number_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(number_surf, number_rect)
        else:
            # Tampilkan titik sesuai angka
            for i in range(self.current_number):
                angle = 2 * math.pi * i / self.current_number
                x = SCREEN_WIDTH // 2 + 80 * math.cos(angle)
                y = SCREEN_HEIGHT // 2 + 80 * math.sin(angle)
                pygame.draw.circle(screen, BLACK, (int(x), int(y)), 10)
                
        # Petunjuk
        hint = font_medium.render("Hitung jumlah titik!", True, BLACK)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint, hint_rect)

class MathOperationEducation:
    def __init__(self):
        self.operations = ["+", "-", "×"]
        self.current_operation_index = 0
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.animation_timer = 0
        self.show_result = False
        self.result = 0
        
    def update(self):
        self.animation_timer += 1
        if self.animation_timer > 180:  # Ganti operasi setiap 3 detik
            self.animation_timer = 0
            self.current_operation_index = (self.current_operation_index + 1) % len(self.operations)
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
            self.show_result = False
            
        # Tampilkan hasil setelah 1.5 detik
        if self.animation_timer > 90:
            self.show_result = True
            # Hitung hasil
            op = self.operations[self.current_operation_index]
            if op == "+":
                self.result = self.num1 + self.num2
            elif op == "-":
                self.result = self.num1 - self.num2
            elif op == "×":
                self.result = self.num1 * self.num2
                
    def draw(self, screen):
        # Judul
        title = font_large.render("Belajar Operasi Matematika", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Gambar operasi matematika
        op = self.operations[self.current_operation_index]
        
        # Angka pertama
        num1_surf = font_xlarge.render(str(self.num1), True, BLACK)
        num1_rect = num1_surf.get_rect(center=(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        screen.blit(num1_surf, num1_rect)
        
        # Operasi
        op_surf = font_xlarge.render(op, True, BLACK)
        op_rect = op_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(op_surf, op_rect)
        
        # Angka kedua
        num2_surf = font_xlarge.render(str(self.num2), True, BLACK)
        num2_rect = num2_surf.get_rect(center=(SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2))
        screen.blit(num2_surf, num2_rect)
        
        # Garis sama dengan
        if self.show_result:
            pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 80), 
                            (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 80), 3)
            
            # Hasil
            result_surf = font_xlarge.render(str(self.result), True, BLACK)
            result_rect = result_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            screen.blit(result_surf, result_rect)
            
        # Petunjuk
        hint = font_medium.render("Pelajari operasi matematika dasar!", True, BLACK)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint, hint_rect)

class ShapeEducation:
    def __init__(self):
        self.shapes = [
            ("Lingkaran", self.draw_circle),
            ("Kotak", self.draw_square),
            ("Segitiga", self.draw_triangle),
            ("Bintang", self.draw_star),
            ("Hati", self.draw_heart),
            ("Belah Ketupat", self.draw_diamond)
        ]
        self.current_shape_index = 0
        self.animation_timer = 0
        self.show_name = True
        
    def update(self):
        self.animation_timer += 1
        if self.animation_timer > 120:  # Ganti bentuk setiap 2 detik
            self.animation_timer = 0
            self.current_shape_index = (self.current_shape_index + 1) % len(self.shapes)
            self.show_name = True
            
        # Sembunyikan nama setelah 1 detik
        if self.animation_timer > 60:
            self.show_name = False
            
    def draw(self, screen):
        # Judul
        title = font_large.render("Belajar Bentuk Bangun Datar", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)
        
        # Gambar bentuk saat ini
        name, draw_func = self.shapes[self.current_shape_index]
        draw_func(screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 150, BLACK)
        
        # Tampilkan nama bentuk
        if self.show_name:
            name_surf = font_xlarge.render(name, True, BLACK)
            name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250))
            screen.blit(name_surf, name_rect)
            
        # Petunjuk
        hint = font_medium.render("Kenali berbagai bentuk bangun datar!", True, BLACK)
        hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(hint, hint_rect)
        
    def draw_circle(self, screen, x, y, size, color):
        pygame.draw.circle(screen, color, (x, y), size)
        pygame.draw.circle(screen, BLACK, (x, y), size, 3)
        
    def draw_square(self, screen, x, y, size, color):
        rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 3)
        
    def draw_triangle(self, screen, x, y, size, color):
        points = [
            (x, y - size),
            (x - size, y + size),
            (x + size, y + size)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)
        
    def draw_star(self, screen, x, y, size, color):
        points = []
        for i in range(10):
            angle = math.pi * i / 5
            if i % 2 == 0:
                r = size
            else:
                r = size / 2
            px = x + r * math.cos(angle - math.pi / 2)
            py = y + r * math.sin(angle - math.pi / 2)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)
        
    def draw_heart(self, screen, x, y, size, color):
        # Gambar hati sederhana
        pygame.draw.circle(screen, color, (x - size // 2, y - size // 2), size // 2)
        pygame.draw.circle(screen, color, (x + size // 2, y - size // 2), size // 2)
        points = [
            (x - size, y),
            (x, y + size),
            (x + size, y)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.circle(screen, BLACK, (x - size // 2, y - size // 2), size // 2, 2)
        pygame.draw.circle(screen, BLACK, (x + size // 2, y - size // 2), size // 2, 2)
        pygame.draw.polygon(screen, BLACK, points, 2)
        
    def draw_diamond(self, screen, x, y, size, color):
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y)
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)

class Tile:
    def __init__(self, x, y, tile_type, tile_value, is_image=True, layer=0):
        self.rect = pygame.Rect(x, y, 80, 100)
        self.tile_type = tile_type  # "color", "number", "math", "shape"
        self.tile_value = tile_value  # Warna, angka, operasi, atau bentuk
        self.is_image = is_image  # True untuk gambar, False untuk kata
        self.selected = False
        self.matched = False
        self.visible = True
        self.layer = layer  # Lapisan tumpukan
        self.removing = False
        self.remove_timer = 0
        self.alpha = 255  # Untuk efek fade out
        
    def draw(self, screen):
        if not self.visible:
            return
            
        # Efek fade out saat menghilang
        if self.removing:
            self.alpha = max(0, self.alpha - 15)
            if self.alpha <= 0:
                self.visible = False
                return
                
        # Buat surface transparan untuk efek fade
        tile_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        tile_surface.fill((255, 255, 255, self.alpha))
        
        # Gambar border
        border_color = (0, 0, 0, self.alpha)
        if self.selected:
            pygame.draw.rect(tile_surface, (0, 200, 0, self.alpha), (0, 0, self.rect.width, self.rect.height), border_radius=5)
        pygame.draw.rect(tile_surface, border_color, (0, 0, self.rect.width, self.rect.height), 2, border_radius=5)
        
        if self.is_image:
            # Gambar berdasarkan jenis ubin
            if self.tile_type == "color":
                pygame.draw.circle(tile_surface, (*self.tile_value, self.alpha), (self.rect.width // 2, 40), 25)
            elif self.tile_type == "number":
                num_surf = font_large.render(str(self.tile_value), True, (0, 0, 0, self.alpha))
                num_rect = num_surf.get_rect(center=(self.rect.width // 2, 40))
                tile_surface.blit(num_surf, num_rect)
            elif self.tile_type == "math":
                # Gambar operasi matematika
                num1, op, num2 = self.tile_value
                op_text = str(num1) + op + str(num2)
                op_surf = font_medium.render(op_text, True, (0, 0, 0, self.alpha))
                op_rect = op_surf.get_rect(center=(self.rect.width // 2, 40))
                tile_surface.blit(op_surf, op_rect)
            elif self.tile_type == "shape":
                # Gambar bentuk
                if self.tile_value == "Lingkaran":
                    pygame.draw.circle(tile_surface, (0, 0, 0, self.alpha), (self.rect.width // 2, 40), 25)
                elif self.tile_value == "Kotak":
                    shape_rect = pygame.Rect(self.rect.width // 2 - 25, 40 - 25, 50, 50)
                    pygame.draw.rect(tile_surface, (0, 0, 0, self.alpha), shape_rect, 2)
                elif self.tile_value == "Segitiga":
                    points = [
                        (self.rect.width // 2, 15),
                        (self.rect.width // 2 - 25, 65),
                        (self.rect.width // 2 + 25, 65)
                    ]
                    pygame.draw.polygon(tile_surface, (0, 0, 0, self.alpha), points, 2)
                elif self.tile_value == "Bintang":
                    points = []
                    for i in range(10):
                        angle = math.pi * i / 5
                        if i % 2 == 0:
                            r = 25
                        else:
                            r = 12
                        px = self.rect.width // 2 + r * math.cos(angle - math.pi / 2)
                        py = 40 + r * math.sin(angle - math.pi / 2)
                        points.append((px, py))
                    pygame.draw.polygon(tile_surface, (0, 0, 0, self.alpha), points, 2)
                elif self.tile_value == "Hati":
                    # Gambar hati sederhana
                    pygame.draw.circle(tile_surface, (0, 0, 0, self.alpha), (self.rect.width // 2 - 12, 28), 12, 2)
                    pygame.draw.circle(tile_surface, (0, 0, 0, self.alpha), (self.rect.width // 2 + 12, 28), 12, 2)
                    points = [
                        (self.rect.width // 2 - 25, 40),
                        (self.rect.width // 2, 65),
                        (self.rect.width // 2 + 25, 40)
                    ]
                    pygame.draw.polygon(tile_surface, (0, 0, 0, self.alpha), points, 2)
                elif self.tile_value == "Belah Ketupat":
                    points = [
                        (self.rect.width // 2, 15),
                        (self.rect.width // 2 + 25, 40),
                        (self.rect.width // 2, 65),
                        (self.rect.width // 2 - 25, 40)
                    ]
                    pygame.draw.polygon(tile_surface, (0, 0, 0, self.alpha), points, 2)
        else:
            # Gambar teks
            text = self.get_text()
            text_surf = font_small.render(text, True, (0, 0, 0, self.alpha))
            text_rect = text_surf.get_rect(center=(self.rect.width // 2, 70))
            tile_surface.blit(text_surf, text_rect)
            
        # Blit surface ke screen
        screen.blit(tile_surface, (self.rect.x, self.rect.y))
        
    def get_text(self):
        # Menghasilkan teks berdasarkan jenis dan nilai ubin
        if self.tile_type == "color":
            color_names = {
                RED: "Merah",
                GREEN: "Hijau",
                BLUE: "Biru",
                YELLOW: "Kuning",
                PURPLE: "Ungu",
                ORANGE: "Oranye"
            }
            return color_names.get(self.tile_value, "Warna")
        elif self.tile_type == "number":
            return f"Angka {self.tile_value}"
        elif self.tile_type == "math":
            num1, op, num2 = self.tile_value
            # Hitung hasil
            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op == "×":
                result = num1 * num2
            return f"Hasil: {result}"
        elif self.tile_type == "shape":
            return self.tile_value
            
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos) and self.visible and not self.matched and not self.removing
        
    def toggle_selection(self):
        self.selected = not self.selected
        
    def start_remove(self):
        self.removing = True
        self.remove_timer = 0

class MahjongGame:
    def __init__(self):
        self.tiles = []
        self.selected_tiles = []
        self.score = 0
        self.moves = 0
        self.feedback_timer = 0
        self.feedback_text = ""
        self.game_complete = False
        self.layout_type = 0  # 0: Pyramid, 1: Diamond, 2: Cross
        self.layouts = ["Pyramid", "Diamond", "Cross"]
        
    def create_tiles(self):
        # Hapus semua tile yang ada
        self.tiles = []
        self.selected_tiles = []
        
        # Buat pasangan ubin untuk setiap kategori
        tile_pairs = []
        
        # Warna
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
        for color in colors:
            tile_pairs.append(("color", color, True))  # Gambar
            tile_pairs.append(("color", color, False))  # Teks
            
        # Angka
        numbers = [1, 2, 3, 4, 5, 6]
        for number in numbers:
            tile_pairs.append(("number", number, True))  # Gambar
            tile_pairs.append(("number", number, False))  # Teks
            
        # Operasi Matematika
        math_ops = [
            (1, "+", 1),
            (2, "+", 2),
            (3, "+", 3),
            (4, "-", 1),
            (5, "-", 2),
            (6, "-", 3),
            (2, "×", 2),
            (3, "×", 3),
            (4, "×", 1)
        ]
        for op in math_ops:
            tile_pairs.append(("math", op, True))  # Gambar
            tile_pairs.append(("math", op, False))  # Teks
            
        # Bentuk
        shapes = ["Lingkaran", "Kotak", "Segitiga", "Bintang", "Hati", "Belah Ketupat"]
        for shape in shapes:
            tile_pairs.append(("shape", shape, True))  # Gambar
            tile_pairs.append(("shape", shape, False))  # Teks
            
        # Acak ubin
        random.shuffle(tile_pairs)
        
        # Buat layout berdasarkan tipe
        if self.layout_type == 0:  # Pyramid
            self.create_pyramid_layout(tile_pairs)
        elif self.layout_type == 1:  # Diamond
            self.create_diamond_layout(tile_pairs)
        else:  # Cross
            self.create_cross_layout(tile_pairs)
            
    def create_pyramid_layout(self, tile_pairs):
        # Layout piramida dengan 9 baris
        rows = 9
        start_x = SCREEN_WIDTH // 2 - 400
        start_y = 100
        
        tile_index = 0
        for row in range(rows):
            # Jumlah tile di setiap baris
            tiles_in_row = min(row + 1, 9)
            
            # Posisi x awal untuk baris ini
            x_offset = (9 - tiles_in_row) * 45
            
            for col in range(tiles_in_row):
                if tile_index < len(tile_pairs):
                    tile_type, tile_value, is_image = tile_pairs[tile_index]
                    x = start_x + x_offset + col * 90
                    y = start_y + row * 40
                    
                    # Hitung layer (semakin ke bawah semakin tinggi)
                    layer = rows - row
                    
                    self.tiles.append(Tile(x, y, tile_type, tile_value, is_image, layer))
                    tile_index += 1
                    
    def create_diamond_layout(self, tile_pairs):
        # Layout berlian
        rows = 11
        start_x = SCREEN_WIDTH // 2 - 400
        start_y = 100
        
        tile_index = 0
        for row in range(rows):
            # Jumlah tile di setiap baris
            if row < 6:
                tiles_in_row = row + 1
            else:
                tiles_in_row = 11 - row
                
            # Posisi x awal untuk baris ini
            x_offset = (9 - tiles_in_row) * 45
            
            for col in range(tiles_in_row):
                if tile_index < len(tile_pairs):
                    tile_type, tile_value, is_image = tile_pairs[tile_index]
                    x = start_x + x_offset + col * 90
                    y = start_y + row * 40
                    
                    # Hitung layer
                    if row < 6:
                        layer = row
                    else:
                        layer = 10 - row
                        
                    self.tiles.append(Tile(x, y, tile_type, tile_value, is_image, layer))
                    tile_index += 1
                    
    def create_cross_layout(self, tile_pairs):
        # Layout silang
        start_x = SCREEN_WIDTH // 2 - 400
        start_y = 100
        
        # Bagian horizontal
        for i in range(9):
            if i < len(tile_pairs):
                tile_type, tile_value, is_image = tile_pairs[i]
                x = start_x + i * 90
                y = start_y + 200
                self.tiles.append(Tile(x, y, tile_type, tile_value, is_image, 1))
                
        # Bagian vertikal
        for i in range(9):
            if i + 9 < len(tile_pairs):
                tile_type, tile_value, is_image = tile_pairs[i + 9]
                x = start_x + 360
                y = start_y + i * 40
                layer = 2 if i == 4 else 1  # Tengah lebih tinggi
                self.tiles.append(Tile(x, y, tile_type, tile_value, is_image, layer))
                
        # Tambahkan tile di sisi
        for i in range(18):
            if i + 18 < len(tile_pairs):
                tile_type, tile_value, is_image = tile_pairs[i + 18]
                
                # Sisi kiri
                if i < 9:
                    x = start_x - 90
                    y = start_y + i * 40
                    layer = 1
                # Sisi kanan
                else:
                    x = start_x + 810
                    y = start_y + (i - 9) * 40
                    layer = 1
                    
                self.tiles.append(Tile(x, y, tile_type, tile_value, is_image, layer))
                
    def is_tile_selectable(self, tile):
        # Cek apakah tile bisa dipilih (tidak terhalang oleh tile lain)
        if tile.matched or tile.removing:
            return False
            
        # Cek apakah ada tile di atasnya yang menghalangi
        for other_tile in self.tiles:
            if (other_tile != tile and other_tile.visible and not other_tile.matched and 
                not other_tile.removing and other_tile.layer > tile.layer):
                # Cek apakah tile lain menutupi tile ini
                if (abs(other_tile.rect.centerx - tile.rect.centerx) < 40 and
                    abs(other_tile.rect.centery - tile.rect.centery) < 30):
                    return False
                    
        return True
        
    def handle_click(self, pos):
        # Cari tile yang diklik
        for tile in self.tiles:
            if tile.is_clicked(pos) and self.is_tile_selectable(tile):
                # Jika sudah ada 2 tile terpilih, reset pilihan
                if len(self.selected_tiles) >= 2:
                    for selected_tile in self.selected_tiles:
                        selected_tile.toggle_selection()
                    self.selected_tiles = []
                    
                # Tambahkan tile ke pilihan
                tile.toggle_selection()
                self.selected_tiles.append(tile)
                
                # Jika sudah ada 2 tile terpilih, periksa kecocokan
                if len(self.selected_tiles) == 2:
                    self.moves += 1
                    self.check_match()
                break
                
    def check_match(self):
        tile1, tile2 = self.selected_tiles
        
        # Periksa apakah satu tile adalah gambar dan yang lain adalah kata
        if tile1.is_image != tile2.is_image:
            # Periksa apakah jenis dan nilai sama
            if tile1.tile_type == tile2.tile_type and tile1.tile_value == tile2.tile_value:
                # Cocok!
                tile1.start_remove()
                tile2.start_remove()
                self.score += 10
                self.feedback_text = "Cocok! +10 poin"
                self.feedback_timer = 60
                
                # Periksa apakah semua tile telah dicocokkan
                if all(tile.matched or tile.removing for tile in self.tiles):
                    self.game_complete = True
            else:
                # Tidak cocok
                self.feedback_text = "Tidak cocok! Coba lagi"
                self.feedback_timer = 60
        else:
            # Keduanya gambar atau keduanya kata
            self.feedback_text = "Pilih satu gambar dan satu kata!"
            self.feedback_timer = 60
            
    def update(self):
        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            
        # Update tile yang sedang dihapus
        for tile in self.tiles:
            if tile.removing:
                tile.remove_timer += 1
                if tile.remove_timer > 20:  # Setelah 20 frame, tandai sebagai matched
                    tile.matched = True
                    
    def draw(self, screen):
        # Gambar semua tile, diurutkan berdasarkan layer
        sorted_tiles = sorted(self.tiles, key=lambda t: t.layer)
        for tile in sorted_tiles:
            tile.draw(screen)
            
        # Gambar highlight untuk tile yang bisa dipilih
        mouse_pos = pygame.mouse.get_pos()
        for tile in self.tiles:
            if tile.rect.collidepoint(mouse_pos) and self.is_tile_selectable(tile):
                # Gambar highlight
                highlight_surf = pygame.Surface((tile.rect.width, tile.rect.height), pygame.SRCALPHA)
                highlight_surf.fill((255, 255, 0, 50))
                screen.blit(highlight_surf, (tile.rect.x, tile.rect.y))
                
        # Gambar skor dan langkah
        score_text = font_medium.render(f"Skor: {self.score}", True, BLACK)
        screen.blit(score_text, (20, 20))
        
        moves_text = font_medium.render(f"Langkah: {self.moves}", True, BLACK)
        screen.blit(moves_text, (20, 50))
        
        # Gambar layout type
        layout_text = font_medium.render(f"Layout: {self.layouts[self.layout_type]}", True, BLACK)
        screen.blit(layout_text, (20, 80))
        
        # Gambar feedback
        if self.feedback_timer > 0:
            feedback_surf = font_medium.render(self.feedback_text, True, BLACK)
            feedback_rect = feedback_surf.get_rect(center=(SCREEN_WIDTH // 2, 50))
            pygame.draw.rect(screen, YELLOW, feedback_rect.inflate(20, 10))
            pygame.draw.rect(screen, BLACK, feedback_rect.inflate(20, 10), 2)
            screen.blit(feedback_surf, feedback_rect)
            
        # Gambar overlay jika game selesai
        if self.game_complete:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 255, 0, 128))
            screen.blit(overlay, (0, 0))
            
            # Teks menang
            win_text = font_xlarge.render("Selamat! Anda Menang!", True, BLACK)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(win_text, win_rect)
            
            # Skor akhir
            score_text = font_large.render(f"Skor Akhir: {self.score}", True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(score_text, score_rect)
            
            # Langkah
            moves_text = font_large.render(f"Total Langkah: {self.moves}", True, BLACK)
            moves_rect = moves_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(moves_text, moves_rect)
            
            # Tombol layout berikutnya
            next_text = font_medium.render("Tekan SPACE untuk layout berikutnya", True, BLACK)
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
            screen.blit(next_text, next_rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Edukatif Mahjong - Versi Kompleks")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, EDUCATION, EDUCATION_MENU, GAME
        
        # Komponen edukasi
        self.color_education = ColorEducation()
        self.number_education = NumberEducation()
        self.math_education = MathOperationEducation()
        self.shape_education = ShapeEducation()
        
        # Komponen game
        self.mahjong_game = MahjongGame()
        
        # Tombol
        self.init_buttons()
        
    def init_buttons(self):
        # Menu utama
        self.education_button = Button(SCREEN_WIDTH // 2 - 150, 200, 300, 60, "Edukasi", GREEN, LIGHT_GRAY)
        self.game_button = Button(SCREEN_WIDTH // 2 - 150, 280, 300, 60, "Permainan", BLUE, LIGHT_GRAY)
        self.quit_button = Button(SCREEN_WIDTH // 2 - 150, 360, 300, 60, "Keluar", RED, LIGHT_GRAY)
        
        # Menu edukasi
        self.color_button = Button(150, 200, 200, 60, "Warna", RED, LIGHT_GRAY)
        self.number_button = Button(400, 200, 200, 60, "Angka", GREEN, LIGHT_GRAY)
        self.math_button = Button(650, 200, 200, 60, "Matematika", BLUE, LIGHT_GRAY)
        self.shape_button = Button(400, 300, 200, 60, "Bentuk", YELLOW, LIGHT_GRAY)
        self.back_button = Button(20, 20, 100, 40, "Kembali", RED, LIGHT_GRAY)
        
        # Game
        self.reset_button = Button(SCREEN_WIDTH - 120, 20, 100, 40, "Reset", YELLOW, LIGHT_GRAY)
        self.layout_button = Button(SCREEN_WIDTH - 240, 20, 100, 40, "Ganti Layout", PURPLE, LIGHT_GRAY)
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Menu state
            if self.state == "MENU":
                self.education_button.check_hover(mouse_pos)
                self.game_button.check_hover(mouse_pos)
                self.quit_button.check_hover(mouse_pos)
                
                if self.education_button.is_clicked(mouse_pos, event):
                    self.state = "EDUCATION_MENU"
                elif self.game_button.is_clicked(mouse_pos, event):
                    self.state = "GAME"
                    self.mahjong_game = MahjongGame()
                    self.mahjong_game.create_tiles()
                elif self.quit_button.is_clicked(mouse_pos, event):
                    self.running = False
                    
            # Education menu state
            elif self.state == "EDUCATION_MENU":
                self.color_button.check_hover(mouse_pos)
                self.number_button.check_hover(mouse_pos)
                self.math_button.check_hover(mouse_pos)
                self.shape_button.check_hover(mouse_pos)
                self.back_button.check_hover(mouse_pos)
                
                if self.color_button.is_clicked(mouse_pos, event):
                    self.state = "COLOR_EDUCATION"
                elif self.number_button.is_clicked(mouse_pos, event):
                    self.state = "NUMBER_EDUCATION"
                elif self.math_button.is_clicked(mouse_pos, event):
                    self.state = "MATH_EDUCATION"
                elif self.shape_button.is_clicked(mouse_pos, event):
                    self.state = "SHAPE_EDUCATION"
                elif self.back_button.is_clicked(mouse_pos, event):
                    self.state = "MENU"
                    
            # Education states
            elif self.state in ["COLOR_EDUCATION", "NUMBER_EDUCATION", "MATH_EDUCATION", "SHAPE_EDUCATION"]:
                self.back_button.check_hover(mouse_pos)
                
                if self.back_button.is_clicked(mouse_pos, event):
                    self.state = "EDUCATION_MENU"
                    
            # Game state
            elif self.state == "GAME":
                self.back_button.check_hover(mouse_pos)
                self.reset_button.check_hover(mouse_pos)
                self.layout_button.check_hover(mouse_pos)
                
                if self.back_button.is_clicked(mouse_pos, event):
                    self.state = "MENU"
                elif self.reset_button.is_clicked(mouse_pos, event):
                    self.mahjong_game = MahjongGame()
                    self.mahjong_game.create_tiles()
                elif self.layout_button.is_clicked(mouse_pos, event):
                    self.mahjong_game.layout_type = (self.mahjong_game.layout_type + 1) % 3
                    self.mahjong_game = MahjongGame()
                    self.mahjong_game.layout_type = (self.mahjong_game.layout_type + 1) % 3
                    self.mahjong_game.create_tiles()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.mahjong_game.game_complete:
                        self.mahjong_game.handle_click(mouse_pos)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.mahjong_game.game_complete:
                    # Pindah ke layout berikutnya
                    self.mahjong_game.layout_type = (self.mahjong_game.layout_type + 1) % 3
                    self.mahjong_game = MahjongGame()
                    self.mahjong_game.layout_type = (self.mahjong_game.layout_type + 1) % 3
                    self.mahjong_game.create_tiles()
                    
    def update(self):
        # Update komponen edukasi
        if self.state == "COLOR_EDUCATION":
            self.color_education.update()
        elif self.state == "NUMBER_EDUCATION":
            self.number_education.update()
        elif self.state == "MATH_EDUCATION":
            self.math_education.update()
        elif self.state == "SHAPE_EDUCATION":
            self.shape_education.update()
            
        # Update game
        if self.state == "GAME":
            self.mahjong_game.update()
            
    def draw(self):
        self.screen.fill(WHITE)
        
        # Menu state
        if self.state == "MENU":
            self.draw_menu()
            
        # Education menu state
        elif self.state == "EDUCATION_MENU":
            self.draw_education_menu()
            
        # Education states
        elif self.state == "COLOR_EDUCATION":
            self.color_education.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.state == "NUMBER_EDUCATION":
            self.number_education.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.state == "MATH_EDUCATION":
            self.math_education.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.state == "SHAPE_EDUCATION":
            self.shape_education.draw(self.screen)
            self.back_button.draw(self.screen)
            
        # Game state
        elif self.state == "GAME":
            self.draw_game()
            
        pygame.display.flip()
        
    def draw_menu(self):
        # Judul
        title = font_xlarge.render("Game Edukatif Mahjong", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subjudul
        subtitle = font_large.render("Belajar Warna, Angka, Matematika, dan Bentuk", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Tombol
        self.education_button.draw(self.screen)
        self.game_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
    def draw_education_menu(self):
        # Judul
        title = font_xlarge.render("Pilih Materi Edukasi", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Tombol
        self.color_button.draw(self.screen)
        self.number_button.draw(self.screen)
        self.math_button.draw(self.screen)
        self.shape_button.draw(self.screen)
        self.back_button.draw(self.screen)
        
    def draw_game(self):
        # Judul
        title = font_large.render("Game Mahjong: Cocokkan Gambar dengan Kata", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Gambar game
        self.mahjong_game.draw(self.screen)
        
        # Tombol
        self.back_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.layout_button.draw(self.screen)
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()