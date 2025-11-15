import pygame
import sys
import math
import random

# Inisialisasi Pygame
pygame.init()

# Konstanta
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Font
font_small = pygame.font.SysFont('Arial', 16)
font_medium = pygame.font.SysFont('Arial', 24)
font_large = pygame.font.SysFont('Arial', 32)

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

class Card:
    def __init__(self, x, y, width, height, text, color, shape, properties):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.shape = shape  # "circle", "square", "triangle"
        self.properties = properties  # Dictionary berisi properti kartu
        self.dragging = False
        self.original_pos = (x, y)
        self.placed = False
        self.error_feedback = None  # "color", "text", "shape", or None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
    def draw(self, screen):
        # Gambar kartu
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        # Gambar bentuk
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color, self.rect.center, 30)
        elif self.shape == "square":
            shape_rect = pygame.Rect(self.rect.centerx - 30, self.rect.centery - 30, 60, 60)
            pygame.draw.rect(screen, self.color, shape_rect)
        elif self.shape == "triangle":
            points = [
                (self.rect.centerx, self.rect.centery - 30),
                (self.rect.centerx - 30, self.rect.centery + 30),
                (self.rect.centerx + 30, self.rect.centery + 30)
            ]
            pygame.draw.polygon(screen, self.color, points)
            
        # Gambar teks
        text_surf = font_small.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
        screen.blit(text_surf, text_rect)
        
        # Gambar feedback error jika ada
        if self.error_feedback:
            if self.error_feedback == "color":
                # Tanda X pada warna
                if self.shape == "circle":
                    pygame.draw.line(screen, RED, (self.rect.centerx - 20, self.rect.centery - 20), 
                                    (self.rect.centerx + 20, self.rect.centery + 20), 3)
                    pygame.draw.line(screen, RED, (self.rect.centerx + 20, self.rect.centery - 20), 
                                    (self.rect.centerx - 20, self.rect.centery + 20), 3)
                elif self.shape == "square":
                    shape_rect = pygame.Rect(self.rect.centerx - 30, self.rect.centery - 30, 60, 60)
                    pygame.draw.line(screen, RED, (shape_rect.left + 10, shape_rect.top + 10), 
                                    (shape_rect.right - 10, shape_rect.bottom - 10), 3)
                    pygame.draw.line(screen, RED, (shape_rect.right - 10, shape_rect.top + 10), 
                                    (shape_rect.left + 10, shape_rect.bottom - 10), 3)
                elif self.shape == "triangle":
                    pygame.draw.line(screen, RED, (self.rect.centerx - 15, self.rect.centery), 
                                    (self.rect.centerx + 15, self.rect.centery), 3)
            elif self.error_feedback == "text":
                # Tanda X pada teks
                text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
                pygame.draw.line(screen, RED, (text_rect.left - 5, text_rect.top), 
                                (text_rect.right + 5, text_rect.bottom), 3)
                pygame.draw.line(screen, RED, (text_rect.right + 5, text_rect.top), 
                                (text_rect.left - 5, text_rect.bottom), 3)
            elif self.error_feedback == "shape":
                # Tanda X pada bentuk
                if self.shape == "circle":
                    pygame.draw.circle(screen, RED, self.rect.center, 35, 3)
                elif self.shape == "square":
                    shape_rect = pygame.Rect(self.rect.centerx - 35, self.rect.centery - 35, 70, 70)
                    pygame.draw.rect(screen, RED, shape_rect, 3)
                elif self.shape == "triangle":
                    points = [
                        (self.rect.centerx, self.rect.centery - 35),
                        (self.rect.centerx - 35, self.rect.centery + 35),
                        (self.rect.centerx + 35, self.rect.centery + 35)
                    ]
                    pygame.draw.polygon(screen, RED, points, 3)
                    
    def check_drag(self, pos):
        return self.rect.collidepoint(pos)
    
    def start_drag(self, pos):
        self.dragging = True
        self.drag_offset_x = self.rect.x - pos[0]
        self.drag_offset_y = self.rect.y - pos[1]
        
    def stop_drag(self):
        self.dragging = False
        
    def update_position(self, pos):
        if self.dragging:
            self.rect.x = pos[0] + self.drag_offset_x
            self.rect.y = pos[1] + self.drag_offset_y
        
    def reset_position(self):
        self.rect.x, self.rect.y = self.original_pos
        self.placed = False
        self.error_feedback = None

class Plot:
    def __init__(self, x, y, width, height, label, rules):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.rules = rules  # Dictionary berisi aturan untuk petak ini
        self.occupied = False
        self.card = None
        self.shaking = False
        self.shake_time = 0
        
    def draw(self, screen):
        # Efek getar jika ada kesalahan
        offset_x = 0
        if self.shaking:
            offset_x = math.sin(self.shake_time * 10) * 5
            self.shake_time += 0.1
            if self.shake_time > 1:
                self.shaking = False
                self.shake_time = 0
                
        # Gambar petak
        plot_rect = pygame.Rect(self.rect.x + offset_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, LIGHT_BLUE, plot_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, plot_rect, 2, border_radius=10)
        
        # Gambar label
        label_surf = font_medium.render(self.label, True, BLACK)
        label_rect = label_surf.get_rect(center=(plot_rect.centerx, plot_rect.top - 20))
        screen.blit(label_surf, label_rect)
        
        # Gambar aturan
        y_offset = 10
        for rule_name, rule_value in self.rules.items():
            rule_text = f"{rule_name}: {rule_value}"
            rule_surf = font_small.render(rule_text, True, BLACK)
            rule_rect = rule_surf.get_rect(topleft=(plot_rect.left + 10, plot_rect.top + y_offset))
            screen.blit(rule_surf, rule_rect)
            y_offset += 20
            
        # Gambar kartu jika ada
        if self.card:
            self.card.rect.center = plot_rect.center
            self.card.draw(screen)
            
    def place_card(self, card):
        if not self.occupied:
            self.occupied = True
            self.card = card
            card.placed = True
            return True
        return False
        
    def remove_card(self):
        if self.occupied:
            self.occupied = False
            card = self.card
            self.card = None
            card.placed = False
            return card
        return None
        
    def check_card(self, card):
        # Periksa apakah kartu memenuhi semua aturan
        valid = True
        error_type = None
        
        for rule_name, rule_value in self.rules.items():
            if rule_name == "Huruf Awal":
                if not card.text.startswith(rule_value):
                    valid = False
                    error_type = "text"
            elif rule_name == "Angka <":
                try:
                    # Coba ekstrak angka dari teks
                    num = int(''.join(filter(str.isdigit, card.text)))
                    if num >= rule_value:
                        valid = False
                        error_type = "text"
                except:
                    valid = False
                    error_type = "text"
            elif rule_name == "Warna Bukan":
                if card.color == rule_value:
                    valid = False
                    error_type = "color"
            elif rule_name == "Bentuk":
                if card.shape != rule_value:
                    valid = False
                    error_type = "shape"
                    
        if not valid:
            self.shaking = True
            card.error_feedback = error_type
            
        return valid

class SequenceCard:
    def __init__(self, x, y, width, height, text, image_key, step_number):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.image_key = image_key
        self.step_number = step_number
        self.dragging = False
        self.original_pos = (x, y)
        self.placed = False
        self.correct_position = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
    def draw(self, screen):
        # Gambar kartu
        pygame.draw.rect(screen, WHITE, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        # Gambar nomor langkah
        step_surf = font_medium.render(str(self.step_number), True, BLACK)
        step_rect = step_surf.get_rect(topleft=(self.rect.left + 5, self.rect.top + 5))
        screen.blit(step_surf, step_rect)
        
        # Gambar gambar sederhana berdasarkan image_key
        if self.image_key == "bee":
            # Gambar lebah sederhana
            body_rect = pygame.Rect(self.rect.centerx - 20, self.rect.centery - 10, 40, 20)
            pygame.draw.ellipse(screen, YELLOW, body_rect)
            pygame.draw.ellipse(screen, BLACK, body_rect, 2)
            
            # Sayap
            pygame.draw.ellipse(screen, WHITE, (body_rect.left - 10, body_rect.top - 5, 15, 10))
            pygame.draw.ellipse(screen, WHITE, (body_rect.right - 5, body_rect.top - 5, 15, 10))
            
            # Garis hitam di badan
            for i in range(3):
                x = body_rect.left + 10 + i * 10
                pygame.draw.line(screen, BLACK, (x, body_rect.top), (x, body_rect.bottom), 2)
                
        elif self.image_key == "flower":
            # Gambar bunga sederhana
            # Kelopak
            petal_color = PINK
            center_x, center_y = self.rect.centerx, self.rect.centery
            petal_radius = 15
            
            for angle in range(0, 360, 60):
                rad_angle = math.radians(angle)
                petal_x = center_x + math.cos(rad_angle) * 20
                petal_y = center_y + math.sin(rad_angle) * 20
                pygame.draw.circle(screen, petal_color, (int(petal_x), int(petal_y)), petal_radius)
                
            # Tengah bunga
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), 10)
            
        elif self.image_key == "hive":
            # Gambar sarang lebah sederhana
            hive_rect = pygame.Rect(self.rect.centerx - 25, self.rect.centery - 20, 50, 40)
            pygame.draw.polygon(screen, ORANGE, [
                (hive_rect.left, hive_rect.centery),
                (hive_rect.left + hive_rect.width // 3, hive_rect.top),
                (hive_rect.right - hive_rect.width // 3, hive_rect.top),
                (hive_rect.right, hive_rect.centery),
                (hive_rect.right, hive_rect.bottom),
                (hive_rect.left, hive_rect.bottom)
            ])
            
            # Pola sarang
            for y in range(hive_rect.top + 10, hive_rect.bottom, 10):
                pygame.draw.line(screen, BLACK, (hive_rect.left + 5, y), (hive_rect.right - 5, y), 1)
                
        elif self.image_key == "honey":
            # Gambar madu sederhana
            jar_rect = pygame.Rect(self.rect.centerx - 15, self.rect.centery - 20, 30, 40)
            pygame.draw.rect(screen, BROWN, jar_rect, border_radius=5)
            
            # Madu
            honey_rect = pygame.Rect(jar_rect.left + 5, jar_rect.centery, jar_rect.width - 10, jar_rect.bottom - jar_rect.centery - 5)
            pygame.draw.rect(screen, YELLOW, honey_rect, border_radius=3)
            
        # Gambar teks
        text_surf = font_small.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
        screen.blit(text_surf, text_rect)
        
    def check_drag(self, pos):
        return self.rect.collidepoint(pos)
    
    def start_drag(self, pos):
        self.dragging = True
        self.drag_offset_x = self.rect.x - pos[0]
        self.drag_offset_y = self.rect.y - pos[1]
        
    def stop_drag(self):
        self.dragging = False
        
    def update_position(self, pos):
        if self.dragging:
            self.rect.x = pos[0] + self.drag_offset_x
            self.rect.y = pos[1] + self.drag_offset_y
        
    def reset_position(self):
        self.rect.x, self.rect.y = self.original_pos
        self.placed = False

class SequenceSlot:
    def __init__(self, x, y, width, height, index):
        self.rect = pygame.Rect(x, y, width, height)
        self.index = index
        self.occupied = False
        self.card = None
        self.correct = False
        
    def draw(self, screen):
        # Gambar slot
        color = GREEN if self.correct else LIGHT_BLUE
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        # Gambar nomor slot
        num_surf = font_medium.render(str(self.index + 1), True, BLACK)
        num_rect = num_surf.get_rect(center=(self.rect.centerx, self.rect.top - 15))
        screen.blit(num_surf, num_rect)
        
        # Gambar kartu jika ada
        if self.card:
            self.card.rect.center = self.rect.center
            self.card.draw(screen)
            
    def place_card(self, card):
        if not self.occupied:
            self.occupied = True
            self.card = card
            card.placed = True
            card.correct_position = self.index
            return True
        return False
        
    def remove_card(self):
        if self.occupied:
            self.occupied = False
            card = self.card
            self.card = None
            card.placed = False
            return card
        return None

class Bee:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.speed = 2
        self.target_x = x
        self.target_y = y
        self.moving = False
        
    def draw(self, screen):
        # Gambar badan lebah
        body_rect = pygame.Rect(self.x - self.size//2, self.y - self.size//4, self.size, self.size//2)
        pygame.draw.ellipse(screen, YELLOW, body_rect)
        pygame.draw.ellipse(screen, BLACK, body_rect, 2)
        
        # Garis hitam di badan
        for i in range(3):
            x = body_rect.left + 5 + i * 8
            pygame.draw.line(screen, BLACK, (x, body_rect.top), (x, body_rect.bottom), 2)
            
        # Sayap
        wing_offset = math.sin(pygame.time.get_ticks() / 100) * 5
        pygame.draw.ellipse(screen, WHITE, (body_rect.left - 10, body_rect.top - 5 + wing_offset, 15, 10))
        pygame.draw.ellipse(screen, WHITE, (body_rect.right - 5, body_rect.top - 5 - wing_offset, 15, 10))
        
    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y
        self.moving = True
        
    def update(self):
        if self.moving:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bee Literate: Logic Garden")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"  # MENU, LOGIC_PUZZLE, SEQUENCE_PUZZLE, WIN, LOSE
        self.score = 0
        self.level = 1
        self.feedback_timer = 0
        self.feedback_text = ""
        
        # Inisialisasi komponen game
        self.init_game_components()
        
    def init_game_components(self):
        # Tombol menu
        self.menu_buttons = [
            Button(350, 200, 300, 60, "Petak Rumpang Logika", GREEN, LIGHT_BLUE),
            Button(350, 280, 300, 60, "Rantai Pembuatan Madu", YELLOW, LIGHT_BLUE),
            Button(350, 360, 300, 60, "Keluar", RED, LIGHT_BLUE)
        ]
        
        # Tombol kembali
        self.back_button = Button(20, 20, 100, 40, "Kembali", RED, LIGHT_BLUE)
        
        # Tombol cek jawaban
        self.check_button = Button(SCREEN_WIDTH - 150, 20, 130, 40, "Cek Jawaban", GREEN, LIGHT_BLUE)
        
        # Tombol reset
        self.reset_button = Button(SCREEN_WIDTH - 150, 70, 130, 40, "Reset", YELLOW, LIGHT_BLUE)
        
        # Inisialisasi komponen Petak Rumpang Logika
        self.init_logic_puzzle()
        
        # Inisialisasi komponen Rantai Pembuatan Madu
        self.init_sequence_puzzle()
        
    def init_logic_puzzle(self):
        # Petak dengan aturan
        self.plots = [
            Plot(200, 200, 200, 150, "Petak A", {
                "Huruf Awal": "B",
                "Warna Bukan": RED
            }),
            Plot(500, 200, 200, 150, "Petak B", {
                "Angka <": 5,
                "Bentuk": "circle"
            }),
            Plot(800, 200, 200, 150, "Petak C", {
                "Huruf Awal": "M",
                "Bentuk": "square"
            })
        ]
        
        # Kartu pilihan
        self.cards = [
            Card(100, 450, 120, 120, "Bola", BLUE, "circle", {"text": "Bola", "color": BLUE, "shape": "circle"}),
            Card(250, 450, 120, 120, "Meja", RED, "square", {"text": "Meja", "color": RED, "shape": "square"}),
            Card(400, 450, 120, 120, "Buku", GREEN, "square", {"text": "Buku", "color": GREEN, "shape": "square"}),
            Card(550, 450, 120, 120, "3", BLUE, "circle", {"text": "3", "color": BLUE, "shape": "circle"}),
            Card(700, 450, 120, 120, "Mobil", YELLOW, "square", {"text": "Mobil", "color": YELLOW, "shape": "square"}),
            Card(850, 450, 120, 120, "7", RED, "triangle", {"text": "7", "color": RED, "shape": "triangle"})
        ]
        
        # Status game
        self.logic_puzzle_complete = False
        
    def init_sequence_puzzle(self):
        # Slot untuk urutan
        self.sequence_slots = []
        slot_width = 150
        slot_height = 180
        start_x = (SCREEN_WIDTH - (4 * slot_width + 3 * 30)) // 2
        start_y = 200
        
        for i in range(4):
            x = start_x + i * (slot_width + 30)
            self.sequence_slots.append(SequenceSlot(x, start_y, slot_width, slot_height, i))
            
        # Kartu urutan
        self.sequence_cards = [
            SequenceCard(150, 450, 140, 140, "Lebah Terbang ke Bunga", "bee", 1),
            SequenceCard(320, 450, 140, 140, "Lebah Mengumpulkan Nektar", "flower", 2),
            SequenceCard(490, 450, 140, 140, "Lebah Kembali ke Sarang", "hive", 3),
            SequenceCard(660, 450, 140, 140, "Nektar Diolah Menjadi Madu", "honey", 4)
        ]
        
        # Lebah untuk animasi
        self.bee = Bee(100, 300)
        
        # Status game
        self.sequence_puzzle_complete = False
        self.sequence_animation_active = False
        self.animation_step = 0
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            # Menu state
            if self.state == "MENU":
                for button in self.menu_buttons:
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        if button.text == "Petak Rumpang Logika":
                            self.state = "LOGIC_PUZZLE"
                            self.reset_logic_puzzle()
                        elif button.text == "Rantai Pembuatan Madu":
                            self.state = "SEQUENCE_PUZZLE"
                            self.reset_sequence_puzzle()
                        elif button.text == "Keluar":
                            self.running = False
                            
            # Logic Puzzle state
            elif self.state == "LOGIC_PUZZLE":
                self.back_button.check_hover(mouse_pos)
                self.check_button.check_hover(mouse_pos)
                self.reset_button.check_hover(mouse_pos)
                
                if self.back_button.is_clicked(mouse_pos, event):
                    self.state = "MENU"
                elif self.check_button.is_clicked(mouse_pos, event):
                    self.check_logic_puzzle()
                elif self.reset_button.is_clicked(mouse_pos, event):
                    self.reset_logic_puzzle()
                    
                # Drag and drop cards
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in self.cards:
                        if card.check_drag(mouse_pos) and not card.placed:
                            card.start_drag(mouse_pos)
                            break
                            
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for card in self.cards:
                        if card.dragging:
                            card.stop_drag()
                            # Cek apakah kartu diletakkan di petak
                            placed = False
                            for plot in self.plots:
                                if plot.rect.collidepoint(card.rect.center):
                                    if plot.place_card(card):
                                        placed = True
                                        break
                            # Jika tidak diletakkan di petak, kembalikan ke posisi semula
                            if not placed:
                                card.reset_position()
                            break
                            
            # Sequence Puzzle state
            elif self.state == "SEQUENCE_PUZZLE":
                self.back_button.check_hover(mouse_pos)
                self.check_button.check_hover(mouse_pos)
                self.reset_button.check_hover(mouse_pos)
                
                if self.back_button.is_clicked(mouse_pos, event):
                    self.state = "MENU"
                elif self.check_button.is_clicked(mouse_pos, event):
                    self.check_sequence_puzzle()
                elif self.reset_button.is_clicked(mouse_pos, event):
                    self.reset_sequence_puzzle()
                    
                # Drag and drop cards
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for card in self.sequence_cards:
                        if card.check_drag(mouse_pos) and not card.placed:
                            card.start_drag(mouse_pos)
                            break
                            
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for card in self.sequence_cards:
                        if card.dragging:
                            card.stop_drag()
                            # Cek apakah kartu diletakkan di slot
                            placed = False
                            for slot in self.sequence_slots:
                                if slot.rect.collidepoint(card.rect.center):
                                    if slot.place_card(card):
                                        placed = True
                                        break
                            # Jika tidak diletakkan di slot, kembalikan ke posisi semula
                            if not placed:
                                card.reset_position()
                            break
                            
            # Win/Lose state
            elif self.state in ["WIN", "LOSE"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = "MENU"
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                        
        # Handle mouse motion for dragging
        if self.state == "LOGIC_PUZZLE":
            for card in self.cards:
                if card.dragging:
                    card.update_position(mouse_pos)
                    
        elif self.state == "SEQUENCE_PUZZLE":
            for card in self.sequence_cards:
                if card.dragging:
                    card.update_position(mouse_pos)
                    
    def update(self):
        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            
        # Update animasi sequence puzzle
        if self.state == "SEQUENCE_PUZZLE" and self.sequence_animation_active:
            self.bee.update()
            
            # Cek apakah lebah sudah mencapai target
            if not self.bee.moving:
                self.animation_step += 1
                
                # Lanjutkan ke langkah berikutnya
                if self.animation_step == 1:
                    # Langkah 2: Lebah mengumpulkan nektar
                    self.bee.move_to(500, 300)
                elif self.animation_step == 2:
                    # Langkah 3: Lebah kembali ke sarang
                    self.bee.move_to(100, 300)
                elif self.animation_step == 3:
                    # Langkah 4: Nektar diolah menjadi madu
                    self.sequence_animation_active = False
                    self.state = "WIN"
                    self.score += 100
                    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Menu state
        if self.state == "MENU":
            self.draw_menu()
            
        # Logic Puzzle state
        elif self.state == "LOGIC_PUZZLE":
            self.draw_logic_puzzle()
            
        # Sequence Puzzle state
        elif self.state == "SEQUENCE_PUZZLE":
            self.draw_sequence_puzzle()
            
        # Win/Lose state
        elif self.state == "WIN":
            self.draw_win_screen()
        elif self.state == "LOSE":
            self.draw_lose_screen()
            
        pygame.display.flip()
        
    def draw_menu(self):
        # Judul
        title = font_large.render("Bee Literate: Logic Garden", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Subjudul
        subtitle = font_medium.render("Game Edukatif Critical Thinking & Problem Solving", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Tombol
        for button in self.menu_buttons:
            button.draw(self.screen)
            
        # Skor
        score_text = font_medium.render(f"Skor: {self.score}", True, BLACK)
        self.screen.blit(score_text, (20, 20))
        
    def draw_logic_puzzle(self):
        # Judul
        title = font_large.render("Petak Rumpang Logika", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Petunjuk
        instruction = font_medium.render("Letakkan kartu yang sesuai dengan aturan di setiap petak!", True, BLACK)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(instruction, instruction_rect)
        
        # Gambar petak
        for plot in self.plots:
            plot.draw(self.screen)
            
        # Gambar kartu
        for card in self.cards:
            if not card.placed:
                card.draw(self.screen)
                
        # Tombol
        self.back_button.draw(self.screen)
        self.check_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        
        # Feedback
        if self.feedback_timer > 0:
            feedback_surf = font_medium.render(self.feedback_text, True, BLACK)
            feedback_rect = feedback_surf.get_rect(center=(SCREEN_WIDTH // 2, 650))
            pygame.draw.rect(self.screen, YELLOW, feedback_rect.inflate(20, 10))
            pygame.draw.rect(self.screen, BLACK, feedback_rect.inflate(20, 10), 2)
            self.screen.blit(feedback_surf, feedback_rect)
            
    def draw_sequence_puzzle(self):
        # Judul
        title = font_large.render("Rantai Pembuatan Madu", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)
        
        # Petunjuk
        instruction = font_medium.render("Susun kartu dalam urutan yang benar!", True, BLACK)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(instruction, instruction_rect)
        
        # Gambar slot
        for slot in self.sequence_slots:
            slot.draw(self.screen)
            
        # Gambar kartu
        for card in self.sequence_cards:
            if not card.placed:
                card.draw(self.screen)
                
        # Gambar lebah jika animasi aktif
        if self.sequence_animation_active:
            self.bee.draw(self.screen)
            
        # Tombol
        self.back_button.draw(self.screen)
        self.check_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        
        # Feedback
        if self.feedback_timer > 0:
            feedback_surf = font_medium.render(self.feedback_text, True, BLACK)
            feedback_rect = feedback_surf.get_rect(center=(SCREEN_WIDTH // 2, 650))
            pygame.draw.rect(self.screen, YELLOW, feedback_rect.inflate(20, 10))
            pygame.draw.rect(self.screen, BLACK, feedback_rect.inflate(20, 10), 2)
            self.screen.blit(feedback_surf, feedback_rect)
            
    def draw_win_screen(self):
        # Latar belakang
        win_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        win_surf.fill((0, 255, 0, 128))
        self.screen.blit(win_surf, (0, 0))
        
        # Teks menang
        win_text = font_large.render("Tantangan Selesai!", True, BLACK)
        win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(win_text, win_rect)
        
        # Skor
        score_text = font_medium.render(f"Skor: {self.score}", True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Petunjuk
        hint_text = font_medium.render("Tekan SPACE atau ESC untuk kembali ke menu", True, BLACK)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(hint_text, hint_rect)
        
    def draw_lose_screen(self):
        # Latar belakang
        lose_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        lose_surf.fill((255, 0, 0, 128))
        self.screen.blit(lose_surf, (0, 0))
        
        # Teks kalah
        lose_text = font_large.render("Coba Lagi!", True, WHITE)
        lose_rect = lose_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(lose_text, lose_rect)
        
        # Skor
        score_text = font_medium.render(f"Skor: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Petunjuk
        hint_text = font_medium.render("Tekan SPACE atau ESC untuk kembali ke menu", True, WHITE)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(hint_text, hint_rect)
        
    def check_logic_puzzle(self):
        # Periksa semua petak
        all_correct = True
        
        for plot in self.plots:
            if plot.occupied:
                if not plot.check_card(plot.card):
                    all_correct = False
            else:
                all_correct = False
                
        if all_correct:
            self.feedback_text = "Semua petak terisi dengan benar!"
            self.feedback_timer = 120
            self.logic_puzzle_complete = True
            self.state = "WIN"
            self.score += 100
        else:
            self.feedback_text = "Beberapa petak masih salah atau kosong!"
            self.feedback_timer = 120
            
    def check_sequence_puzzle(self):
        # Periksa apakah semua slot terisi
        all_filled = all(slot.occupied for slot in self.sequence_slots)
        
        if not all_filled:
            self.feedback_text = "Isi semua slot terlebih dahulu!"
            self.feedback_timer = 120
            return
            
        # Periksa urutan yang benar
        correct_order = True
        for i, slot in enumerate(self.sequence_slots):
            if slot.card.step_number != i + 1:
                correct_order = False
                slot.correct = False
            else:
                slot.correct = True
                
        if correct_order:
            self.feedback_text = "Urutan benar! Menjalankan animasi..."
            self.feedback_timer = 120
            self.sequence_puzzle_complete = True
            self.sequence_animation_active = True
            self.animation_step = 0
            self.bee.move_to(500, 300)  # Mulai animasi dengan lebah terbang ke bunga
        else:
            self.feedback_text = "Urutan masih salah! Perhatikan langkah-langkahnya."
            self.feedback_timer = 120
            
    def reset_logic_puzzle(self):
        # Kembalikan semua kartu ke posisi semula
        for card in self.cards:
            card.reset_position()
            card.error_feedback = None
            
        # Kosongkan semua petak
        for plot in self.plots:
            if plot.occupied:
                plot.remove_card()
                
        # Reset status
        self.logic_puzzle_complete = False
        self.feedback_timer = 0
        
    def reset_sequence_puzzle(self):
        # Kembalikan semua kartu ke posisi semula
        for card in self.sequence_cards:
            card.reset_position()
            
        # Kosongkan semua slot
        for slot in self.sequence_slots:
            if slot.occupied:
                slot.remove_card()
            slot.correct = False
            
        # Reset status
        self.sequence_puzzle_complete = False
        self.sequence_animation_active = False
        self.feedback_timer = 0
        
        # Reset posisi lebah
        self.bee = Bee(100, 300)
        
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