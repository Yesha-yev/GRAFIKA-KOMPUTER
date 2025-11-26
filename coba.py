import pygame
import cairo
import random
import numpy as np

# --- 1. KONSTANTA DAN INISIALISASI ---
WIDTH, HEIGHT = 800, 600
FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sambung Kata & Hitung Cepat - Belajar Huruf & Angka")
clock = pygame.time.Clock()

# Inisialisasi Cairo Surface
data = np.zeros((HEIGHT, WIDTH, 4), dtype=np.uint8)
# ARGB32 for cairo, but numpy data is BGRA by default due to how we treat it later
# We will swap axes and channel order when blitting to Pygame screen
cairo_surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
context = cairo.Context(cairo_surface)

# --- 2. FUNGSI-FUNGSI GAMBAR (DRAW FUNCTIONS) ---

# [Semua fungsi gambar yang sudah Anda buat (draw_apple, draw_ball, draw_cat, etc.) 
# akan tetap berada di sini. Saya akan menyertakannya di kode akhir.]
def draw_apple(context, x, y, size=1.0):
    """Gambar apel"""
    context.set_source_rgb(0.9, 0.2, 0.2)
    context.arc(x, y, 25*size, 0, 2 * 3.14)
    context.fill()
    context.set_source_rgb(1, 0.4, 0.4)
    context.arc(x - 8*size, y - 8*size, 10*size, 0, 2 * 3.14)
    context.fill()
    context.set_source_rgb(0.4, 0.2, 0.1)
    context.rectangle(x - 2*size, y - 30*size, 4*size, 12*size)
    context.fill()
    context.set_source_rgb(0.2, 0.7, 0.2)
    context.arc(x + 10*size, y - 25*size, 10*size, 0, 2 * 3.14)
    context.fill()

def draw_ball(context, x, y, size=1.0):
    """Gambar bola"""
    context.set_source_rgb(1, 0, 1)
    context.arc(x, y, 25*size, 0, 2 * 3.14)
    context.fill()
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(2*size)
    for i in range(6):
        angle = i * 3.14 / 3
        context.move_to(x, y)
        context.line_to(x + 25*size * np.cos(angle), y + 25*size * np.sin(angle))
    context.stroke()

def draw_cat(context, x, y, size=1.0):
    """Gambar kucing"""
    context.set_source_rgb(1, 0.6, 0.2)
    context.arc(x, y, 20*size, 0, 2 * 3.14)
    context.fill()
    context.move_to(x - 20*size, y - 10*size)
    context.line_to(x - 15*size, y - 25*size)
    context.line_to(x - 5*size, y - 15*size)
    context.fill()
    context.move_to(x + 5*size, y - 15*size)
    context.line_to(x + 15*size, y - 25*size)
    context.line_to(x + 20*size, y - 10*size)
    context.fill()
    context.set_source_rgb(0, 0, 0)
    context.arc(x - 8*size, y - 5*size, 3*size, 0, 2 * 3.14)
    context.fill()
    context.arc(x + 8*size, y - 5*size, 3*size, 0, 2 * 3.14)
    context.fill()
    context.set_line_width(2*size)
    context.arc(x, y + 5*size, 8*size, 0, 3.14)
    context.stroke()

def draw_car(context, x, y, size=1.0):
    """Gambar mobil"""
    context.set_source_rgb(0.2, 0.4, 0.9)
    context.rectangle(x - 25*size, y - 10*size, 50*size, 15*size)
    context.fill()
    context.rectangle(x - 15*size, y - 20*size, 30*size, 10*size)
    context.fill()
    context.set_source_rgb(0.3, 0.3, 0.3)
    context.arc(x - 15*size, y + 5*size, 8*size, 0, 2 * 3.14)
    context.fill()
    context.arc(x + 15*size, y + 5*size, 8*size, 0, 2 * 3.14)
    context.fill()

def draw_flower(context, x, y, size=1.0):
    """Gambar bunga"""
    context.set_source_rgb(1, 0.2, 0.5)
    for i in range(6):
        angle = i * 3.14 / 3
        petal_x = x + 15*size * np.cos(angle)
        petal_y = y + 15*size * np.sin(angle)
        context.arc(petal_x, petal_y, 8*size, 0, 2 * 3.14)
        context.fill()
    context.set_source_rgb(1, 0.9, 0)
    context.arc(x, y, 8*size, 0, 2 * 3.14)
    context.fill()
    context.set_source_rgb(0.2, 0.7, 0.2)
    context.set_line_width(3*size)
    context.move_to(x, y)
    context.line_to(x, y + 30*size)
    context.stroke()

def draw_fish(context, x, y, size=1.0):
    """Gambar ikan"""
    context.set_source_rgb(1, 0.5, 0)
    context.arc(x + 5*size, y, 15*size, 0, 2 * 3.14)
    context.fill()
    context.move_to(x - 10*size, y)
    context.line_to(x - 25*size, y - 12*size)
    context.line_to(x - 25*size, y + 12*size)
    context.close_path()
    context.fill()
    context.set_source_rgb(0, 0, 0)
    context.arc(x + 15*size, y - 5*size, 3*size, 0, 2 * 3.14)
    context.fill()

def draw_jam(context, x, y, size=1.0):
    """Gambar jam"""
    # Lingkaran jam
    context.set_source_rgb(0.9, 0.9, 0.9)
    context.arc(x, y, 20*size, 0, 2 * 3.14)
    context.fill()
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(2*size)
    context.arc(x, y, 20*size, 0, 2 * 3.14)
    context.stroke()
    
    # Jarum jam
    context.move_to(x, y)
    context.line_to(x, y - 10*size)
    context.stroke()
    context.move_to(x, y)
    context.line_to(x + 7*size, y)
    context.stroke()
    
    # Tambahkan angka jam
    context.set_source_rgb(0, 0, 0)
    context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(5*size) 
    
    # Angka 12 (atas)
    context.move_to(x - 2.5*size, y - 15*size)   
    context.show_text("12")
    
    # Angka 6 (bawah)
    context.move_to(x - 2*size, y + 12*size)   
    context.show_text("6")
    
    # Angka 9 (kiri)
    context.move_to(x - 18*size, y + 2*size)   
    context.show_text("9")
    
    # Angka 3 (kanan)
    context.move_to(x + 14*size, y + 2*size)   
    context.show_text("3")
def draw_chicken(context, x, y, size=1.0):
    """Gambar ayam"""
    edge_width = 1.5*size
    
    # Tubuh ayam (warna putih)
    context.set_source_rgb(1, 1, 1)
    context.arc(x, y, 18*size, 0, 2 * 3.14)
    context.fill_preserve()  # Gunakan fill_preserve, bukan fill
    context.set_source_rgb(0, 0, 0)  # Hitam
    context.set_line_width(edge_width)
    context.stroke()
    
    # Kepala ayam (warna putih)
    context.set_source_rgb(1, 1, 1)
    context.arc(x - 5*size, y - 18*size, 12*size, 0, 2 * 3.14)
    context.fill_preserve()  # Gunakan fill_preserve
    context.set_source_rgb(0, 0, 0)  # Hitam
    context.set_line_width(edge_width)
    context.stroke()
    
    # Jengger (warna merah)
    context.set_source_rgb(1, 0.2, 0)
    context.move_to(x - 5*size, y - 28*size)
    context.line_to(x - 10*size, y - 25*size)
    context.line_to(x - 7*size, y - 22*size)
    context.line_to(x - 5*size, y - 25*size)
    context.line_to(x - 3*size, y - 22*size)
    context.line_to(x, y - 25*size)
    context.close_path()
    context.fill() 

    # Paruh (warna oranye) -  
    context.set_source_rgb(1, 0.5, 0)
    context.move_to(x - 5*size, y - 15*size)
    context.line_to(x - 12*size, y - 13*size)
    context.line_to(x - 5*size, y - 11*size)
    context.close_path()
    context.fill() 

    # Mata kiri
    context.set_source_rgb(0, 0, 0)
    context.arc(x - 8*size, y - 18*size, 2*size, 0, 2 * 3.14)
    context.fill()

    # Mata kanan
    context.set_source_rgb(0, 0, 0)
    context.arc(x - 2*size, y - 18*size, 2*size, 0, 2 * 3.14)
    context.fill()  

    # Pupil mata (titik putih kecil) -  
    context.set_source_rgb(1, 1, 1)
    context.arc(x - 7.5*size, y - 18.5*size, 0.8*size, 0, 2 * 3.14)
    context.fill()  # Menggunakan fill() saja tanpa stroke()

    context.arc(x - 1.5*size, y - 18.5*size, 0.8*size, 0, 2 * 3.14)
    context.fill()
    
    # Kaki kiri
    context.set_source_rgb(1, 0.5, 0)
    context.set_line_width(2*size)
    context.move_to(x - 8*size, y + 15*size)
    context.line_to(x - 8*size, y + 25*size)
    context.stroke()  # Kaki sudah digambar dengan stroke, tidak perlu garis tepi tambahan
    
    # Kaki kanan
    context.move_to(x + 8*size, y + 15*size)
    context.line_to(x + 8*size, y + 25*size)
    context.stroke()  # Kaki sudah digambar dengan stroke, tidak perlu garis tepi tambahan
    
    # Cakar kiri
    context.set_line_width(1.5*size)
    context.move_to(x - 8*size, y + 25*size)
    context.line_to(x - 12*size, y + 28*size)
    context.stroke()
    context.move_to(x - 8*size, y + 25*size)
    context.line_to(x - 8*size, y + 30*size)
    context.stroke()
    context.move_to(x - 8*size, y + 25*size)
    context.line_to(x - 4*size, y + 28*size)
    context.stroke()  # Cakar sudah digambar dengan stroke, tidak perlu garis tepi tambahan
    
    # Cakar kanan
    context.move_to(x + 8*size, y + 25*size)
    context.line_to(x + 4*size, y + 28*size)
    context.stroke()
    context.move_to(x + 8*size, y + 25*size)
    context.line_to(x + 8*size, y + 30*size)
    context.stroke()
    context.move_to(x + 8*size, y + 25*size)
    context.line_to(x + 12*size, y + 28*size)
    context.stroke()    

def draw_penghapus(context, x, y, size=1.0):
    """Gambar penghapus"""
    context.set_source_rgb(1, 0.8, 0.8)
    context.rectangle(x - 15*size, y - 10*size, 30*size, 15*size)
    context.fill()
    context.set_source_rgb(0.9, 0.6, 0.6)
    context.rectangle(x - 15*size, y + 5*size, 30*size, 5*size)
    context.fill()
    
def draw_house(context, x, y, size=1.0):
    """Gambar rumah"""
    context.set_source_rgb(0.9, 0.7, 0.5)
    context.rectangle(x - 20*size, y - 10*size, 40*size, 30*size)
    context.fill()
    context.set_source_rgb(0.8, 0.2, 0.2)
    context.move_to(x - 25*size, y - 10*size)
    context.line_to(x, y - 30*size)
    context.line_to(x + 25*size, y - 10*size)
    context.close_path()
    context.fill()
    context.set_source_rgb(0.4, 0.2, 0.1)
    context.rectangle(x - 8*size, y + 5*size, 16*size, 15*size)
    context.fill()

def draw_book(context, x, y, size=1.0):
    """Gambar buku"""
    context.set_source_rgb(0.2, 0.4, 0.8)
    context.rectangle(x - 15*size, y - 20*size, 30*size, 40*size)
    context.fill()
    context.set_source_rgb(0.1, 0.2, 0.6)
    context.set_line_width(2*size)
    context.move_to(x - 10*size, y - 20*size)
    context.line_to(x - 10*size, y + 20*size)
    context.stroke()
    context.set_source_rgb(0.3, 0.5, 0.9)
    context.rectangle(x - 5*size, y - 12*size, 15*size, 8*size)
    context.fill()

def draw_pencil(context, x, y, size=1.0):
    """Gambar pensil"""
    context.set_source_rgb(1, 0.8, 0.2)
    context.rectangle(x - 3*size, y - 25*size, 6*size, 35*size)
    context.fill()
    context.set_source_rgb(1, 0.6, 0.4)
    context.rectangle(x - 3*size, y - 28*size, 6*size, 5*size)
    context.fill()
    context.set_source_rgb(0.3, 0.3, 0.3)
    context.move_to(x - 3*size, y - 28*size)
    context.line_to(x, y - 35*size)
    context.line_to(x + 3*size, y - 28*size)
    context.close_path()
    context.fill()
    context.set_source_rgb(0.9, 0.6, 0.7)
    context.rectangle(x - 4*size, y + 8*size, 8*size, 5*size)
    context.fill()

def draw_number(context, number, x, y, size=60, bg_scale=1.5):
    """Draw a single number with colorful background"""
    colors = [(0.9, 0.2, 0.2), (0.2, 0.8, 0.4), (0.2, 0.6, 0.9), (0.9, 0.5, 0.2), (0.5, 0.2, 0.8)]
    color = random.choice(colors)
    context.set_source_rgb(*color)
    radius = (size / 2) * bg_scale
    context.arc(x, y, radius, 0, 2 * 3.14)
    context.fill()
    
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(size)
    extents = context.text_extents(str(number))
    text_x = x - extents[2]/2
    text_y = y + extents[3]/2
    context.move_to(text_x, text_y)
    context.show_text(str(number))
    context.stroke()

def draw_pisau(context, x, y, size=1.0):
    """Gambar pisau"""
    context.set_source_rgb(0.6, 0.8, 0.9)  # Warna biru muda untuk blade
    
    # Bentuk blade yang lebih akurat (runcing di ujung)
    context.move_to(x, y - 30*size)  # Ujung paling tajam blade
    context.line_to(x - 8*size, y - 10*size)  # Sisi kiri blade
    context.line_to(x - 6*size, y + 15*size)  # Pangkal kiri blade
    context.line_to(x + 6*size, y + 15*size)  # Pangkal kanan blade
    context.line_to(x + 8*size, y - 10*size)  # Sisi kanan blade
    context.close_path()
    context.fill()
    
    # Gambar gagang pisau (warna coklat)
    context.set_source_rgb(0.6, 0.3, 0.1)  # Warna coklat untuk gagang
    
    # Bentuk gagang yang lebih proporsional
    context.move_to(x - 6*size, y + 15*size)  # Sisi kiri atas gagang
    context.line_to(x - 8*size, y + 25*size)  # Sisi kiri bawah gagang
    context.line_to(x + 8*size, y + 25*size)  # Sisi kanan bawah gagang
    context.line_to(x + 6*size, y + 15*size)  # Sisi kanan atas gagang
    context.close_path()
    context.fill()
    
    # Tambahkan detail garis hitam pada blade
    context.set_source_rgb(0, 0, 0)
    context.set_line_width(0.8*size)
    
    # Garis utama di tengah blade
    context.move_to(x, y - 30*size)
    context.line_to(x, y + 15*size)
    context.stroke()
    
    # Garis detail diagonal di blade
    context.set_line_width(0.6*size)
    context.move_to(x - 4*size, y - 20*size)
    context.line_to(x - 2*size, y + 10*size)
    context.stroke()
    
    context.move_to(x + 4*size, y - 20*size)
    context.line_to(x + 2*size, y + 10*size)
    context.stroke()
    
    # Tambahkan detail pada gagang
    context.set_line_width(0.5*size)
    context.move_to(x - 6*size, y + 18*size)
    context.line_to(x + 6*size, y + 18*size)
    context.stroke()
    
    context.move_to(x - 5*size, y + 21*size)
    context.line_to(x + 5*size, y + 21*size)
    context.stroke()
    
    # Tambahkan garis batas antara blade dan gagang
    context.set_line_width(1.0*size)
    context.move_to(x - 6*size, y + 15*size)
    context.line_to(x + 6*size, y + 15*size)
    context.stroke()
    
def draw_letter(context, letter, x, y, size=60,bg_scale=1.5):
    """Draw a single letter with colorful background"""
    colors = [(0.9, 0.2, 0.2), (0.2, 0.8, 0.4), (0.2, 0.6, 0.9), (0.9, 0.5, 0.2), (0.5, 0.2, 0.8)]
    color = random.choice(colors)
    context.set_source_rgb(*color)
    radius = (size / 2) * bg_scale
    context.arc(x, y, radius, 0, 2 * 3.14)
    context.fill()
    
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(size)
    extents = context.text_extents(letter)
    text_x = x - extents[2]/2
    text_y = y + extents[3]/2
    context.move_to(text_x, text_y)
    context.show_text(letter)
    context.stroke()

def draw_background(context):
    """Draw a colorful gradient background with small star effects"""
    grad = cairo.LinearGradient(0, 0, 0, HEIGHT)
    grad.add_color_stop_rgb(0, 0.6, 0.4, 0.8)
    grad.add_color_stop_rgb(0.5, 0.9, 0.4, 0.7)
    grad.add_color_stop_rgb(1, 0.4, 0.6, 0.9)
    context.set_source(grad)
    context.rectangle(0, 0, WIDTH, HEIGHT)
    context.fill()
    
    context.set_source_rgba(1, 1, 1, 0.3)
    for i in range(20):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT // 3)
        context.arc(x, y, 3, 0, 2 * 3.14)
        context.fill()

def draw_heart(context, x, y, filled):
    """Draw a heart for lives counter"""
    if filled:
        context.set_source_rgb(1, 0.2, 0.2)
    else:
        context.set_source_rgb(0.7, 0.7, 0.7)
    
    context.move_to(x, y + 8)
    context.curve_to(x, y + 5, x - 5, y, x - 10, y)
    context.curve_to(x - 15, y, x - 15, y + 7, x - 15, y + 7)
    context.curve_to(x - 15, y + 12, x - 10, y + 17, x, y + 22)
    context.curve_to(x + 10, y + 17, x + 15, y + 12, x + 15, y + 7)
    context.curve_to(x + 15, y + 7, x + 15, y, x + 10, y)
    context.curve_to(x + 5, y, x, y + 5, x, y + 8)
    context.fill()

def draw_star(context, x, y, size):
    """Draw a star for score or celebration"""
    context.set_source_rgb(1, 0.84, 0)
    context.move_to(x, y - size)
    for i in range(1, 11):
        angle = i * 3.14159 / 5
        r = size if i % 2 == 0 else size / 2
        context.line_to(x + r * np.sin(angle), y - r * np.cos(angle))
    context.close_path()
    context.fill()

# --- 3. KELAS TOMBOL (Button Class) ---

class Button:
    def __init__(self, x, y, width, height, text, color, font_size=30, is_circle=False,text_offset_y=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font_size = font_size
        self.hover = False
        self.is_circle = is_circle
        self.text_offset_y = text_offset_y
        
    def draw(self, context):
        # Background color
        color = [min(c * 1.2, 1) for c in self.color] if self.hover else self.color
        context.set_source_rgb(*color)
        
        if self.is_circle:
            radius = min(self.width, self.height) / 2
            context.arc(self.x + radius, self.y + radius, radius, 0, 2 * 3.14)
            context.fill()
        else:
            # Rounded Rectangle
            radius = 15
            context.arc(self.x + radius, self.y + radius, radius, 3.14, 3 * 3.14 / 2)
            context.arc(self.x + self.width - radius, self.y + radius, radius, 3 * 3.14 / 2, 0)
            context.arc(self.x + self.width - radius, self.y + self.height - radius, radius, 0, 3.14 / 2)
            context.arc(self.x + radius, self.y + self.height - radius, radius, 3.14 / 2, 3.14)
            context.close_path()
            context.fill()
        
        # Text
        context.set_source_rgb(1, 1, 1)
        context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(self.font_size)
        
        extents = context.text_extents(self.text)
        
        text_x = self.x + (self.width - extents[2]) / 2
        text_y = self.y + (self.height + extents[3]) / 2 + self.text_offset_y
        
        context.move_to(text_x, text_y)
        context.show_text(self.text)
        context.stroke()
        
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)
    
    def update_hover(self, pos):
        self.hover = self.is_clicked(pos)

# --- 4. DATABASE PERTANYAAN ---

WORD_DATABASE = [
    {"word": "APEL", "hint": "Buah merah yang segar", "draw_func": draw_apple},
    {"word": "BOLA", "hint": "Mainan bulat untuk ditendang", "draw_func": draw_ball},
    {"word": "KUCING", "hint": "Hewan berbulu suka ikan", "draw_func": draw_cat},
    {"word": "MOBIL", "hint": "Kendaraan beroda empat", "draw_func": draw_car},
    {"word": "BUNGA", "hint": "Tumbuhan indah dan harum", "draw_func": draw_flower},
    {"word": "IKAN", "hint": "Hewan yang hidup di air", "draw_func": draw_fish},
    {"word": "AYAM", "hint": "Hewan berkokok pagi hari", "draw_func": draw_chicken},
    {"word": "RUMAH", "hint": "Tempat tinggal kita", "draw_func": draw_house},
    {"word": "JAM", "hint": "Untuk melihat waktu", "draw_func": draw_jam},
    {"word": "BUKU", "hint": "Untuk membaca dan belajar", "draw_func": draw_book},
    {"word": "PENSIL", "hint": "Alat untuk menulis", "draw_func": draw_pencil},
    {"word": "PISAU", "hint": "Alat untuk memotong", "draw_func": draw_pisau},
    {"word": "PENGHAPUS", "hint": "Untuk menghapus tulisan", "draw_func": draw_penghapus},
]

# --- 5. FUNGSI GENERATOR PERTANYAAN ---

def generate_word_question():
    """Generate a word completion question"""
    word_data = random.choice(WORD_DATABASE)
    word = word_data["word"]
    hint = word_data["hint"]
    draw_func = word_data["draw_func"]
    missing_index = random.randint(0, len(word) - 1)
    correct_letter = word[missing_index]
    
    all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if correct_letter in all_letters:
        all_letters.remove(correct_letter)
    
    # Ensure options are letters and distinct
    wrong_letters = random.sample([l for l in all_letters if l != correct_letter], 2)
    
    options = [correct_letter] + wrong_letters
    random.shuffle(options)
    
    # The 'word' variable here is used to hold the question state in the main loop
    return word, hint, draw_func, missing_index, correct_letter, options, "word"

# --- 6. FUNGSI GAMBAR TAMPILAN EDUKASI ---

# [Fungsi draw_education_menu, draw_letter_learning, draw_word_learning, 
# draw_number_learning, draw_math_learning sudah diimplementasi dengan baik 
# di kode Anda sebelumnya, hanya perlu memastikan integrasi variabel status.]

def draw_education_menu(context, mouse_pos):
    """Draw education menu with letter, word, number, and math learning options"""
    draw_background(context)
    
    # Title
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(25)
    title = "BELAJAR HURUF, KATA & ANGKA"
    extents = context.text_extents(title)
    context.move_to((WIDTH - extents[2]) / 2, 60)
    context.show_text(title)
    context.stroke()
    
    # Instructions
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(20)
    instruction = "Pilih aktivitas belajar:"
    extents = context.text_extents(instruction)
    context.move_to((WIDTH - extents[2]) / 2, 100)
    context.show_text(instruction)
    context.stroke()
    
    # Letter learning button
    letter_btn = Button(100, 150, 150, 150, "HURUF", (0.2, 0.8, 0.4), 35, is_circle=False,text_offset_y=-20) 
    letter_btn.update_hover(mouse_pos)
    letter_btn.draw(context)
    draw_letter(context, "A", 175, 240, 20) 
    draw_letter(context, "B", 175, 280, 20)
    
    # Word learning button
    word_btn = Button(280, 150, 150, 150, "KATA", (0.2, 0.6, 0.9), 35, is_circle=False, text_offset_y=-20)
    word_btn.update_hover(mouse_pos)
    word_btn.draw(context)
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(20)
    context.move_to(330, 240)
    context.show_text("APEL")
    context.stroke()
    draw_apple(context, 355, 270, 0.6)
    
    # Number learning button
    number_btn = Button(460, 150, 150, 150, "ANGKA", (0.9, 0.5, 0.2), 35, is_circle=False, text_offset_y=-20)
    number_btn.update_hover(mouse_pos)
    number_btn.draw(context)
    draw_number(context, 1, 490, 260, 20)
    draw_number(context, 2, 535, 260, 20)
    draw_number(context, 3, 580, 260, 20)
    
    # Math learning button
    math_btn = Button(100, 330, 150, 150, "MATEMATIKA", (0.5, 0.2, 0.8), 20, is_circle=False, text_offset_y=-20)
    math_btn.update_hover(mouse_pos)
    math_btn.draw(context)
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(25)
    context.move_to(125, 430)
    context.show_text("2 + 3 = 5")
    context.stroke()
    
    # Back button
    back_btn = Button(300, 450, 200, 60, "KEMBALI", (0.2, 0.6, 0.9), 20)
    back_btn.update_hover(mouse_pos)
    back_btn.draw(context)
    
    return letter_btn, word_btn, number_btn, math_btn, back_btn

def draw_letter_learning(context, mouse_pos, current_letter_index):
    """Draw letter learning screen"""
    draw_background(context)
    
    # Title
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(40)
    title = "BELAJAR HURUF"
    extents = context.text_extents(title)
    context.move_to((WIDTH - extents[2]) / 2, 60)
    context.show_text(title)
    context.stroke()
    
    # Current letter
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    current_letter = letters[current_letter_index]
    
    draw_letter(context, current_letter, WIDTH//2, 200, 120)
    
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(24)
    context.move_to(WIDTH//2 - 100, 300)
    context.show_text("Kata yang dimulai dengan " + current_letter + ":")
    context.stroke()
    
    # Find words starting with this letter
    example_words = [d for d in WORD_DATABASE if d["word"][0] == current_letter]
    
    y_pos = 340
    for i, word_data in enumerate(example_words[:3]):
        context.set_source_rgb(1, 1, 1)
        context.set_font_size(30)
        context.move_to(WIDTH//2 - 100, y_pos)
        context.show_text(word_data["word"])
        context.stroke()
        
        word_data["draw_func"](context, WIDTH//2 + 100, y_pos - 10, 0.6)
        y_pos += 50
    
    # Navigation buttons
    prev_btn = Button(150, 500, 100, 50, "←", (0.9, 0.5, 0.2), 40)
    next_btn = Button(550, 500, 100, 50, "→", (0.9, 0.5, 0.2), 40)
    back_btn = Button(300, 500, 200, 50, "KEMBALI", (0.2, 0.6, 0.9), 20)
    
    prev_btn.update_hover(mouse_pos)
    next_btn.update_hover(mouse_pos)
    back_btn.update_hover(mouse_pos)
    
    prev_btn.draw(context)
    next_btn.draw(context)
    back_btn.draw(context)
    
    return prev_btn, next_btn, back_btn

def draw_word_learning(context, mouse_pos, current_word_index):
    """Draw word learning screen"""
    draw_background(context)
    
    # Title
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(40)
    title = "BELAJAR KATA"
    extents = context.text_extents(title)
    context.move_to((WIDTH - extents[2]) / 2, 60)
    context.show_text(title)
    context.stroke()
    
    # Current word
    word_data = WORD_DATABASE[current_word_index]
    word = word_data["word"]
    hint = word_data["hint"]
    draw_func = word_data["draw_func"]
    
    # Draw image
    draw_func(context, WIDTH//2, 180, 2.0)
    
    # Draw word
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(60)
    extents = context.text_extents(word)
    context.move_to((WIDTH - extents[2]) / 2, 280)
    context.show_text(word)
    context.stroke()
    
    # Draw hint
    context.set_source_rgb(1, 1, 0.8)
    context.set_font_size(24)
    extents = context.text_extents(hint)
    context.move_to((WIDTH - extents[2]) / 2, 320)
    context.show_text(hint)
    context.stroke()
    
    # Draw spelling
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(20)
    context.move_to(WIDTH//2 - 150, 360)
    context.show_text("Ejaan:")
    context.stroke()
    
    # Draw each letter
    word_width = len(word) * 40 # approx
    x_pos = WIDTH//2 - word_width // 2 + 20
    for i, letter in enumerate(word):
        draw_letter(context, letter, x_pos + i * 40, 400, 30)
    
    # Navigation buttons
    prev_btn = Button(150, 500, 100, 50, "←", (0.9, 0.5, 0.2), 40)
    next_btn = Button(550, 500, 100, 50, "→", (0.9, 0.5, 0.2), 40)
    back_btn = Button(300, 500, 200, 50, "KEMBALI", (0.2, 0.6, 0.9), 20)
    
    prev_btn.update_hover(mouse_pos)
    next_btn.update_hover(mouse_pos)
    back_btn.update_hover(mouse_pos)
    
    prev_btn.draw(context)
    next_btn.draw(context)
    back_btn.draw(context)
    
    return prev_btn, next_btn, back_btn
def generate_level1_question():
    """Generate a level 1 question (melengkapi 1 huruf rumpang)"""
    word_data = random.choice(WORD_DATABASE)
    word = word_data["word"]
    hint = word_data["hint"]
    draw_func = word_data["draw_func"]
    missing_index = random.randint(0, len(word) - 1)
    correct_letter = word[missing_index]
    
    all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    if correct_letter in all_letters:
        all_letters.remove(correct_letter)
    
    wrong_letters = random.sample(all_letters, 2)
    options = [correct_letter] + wrong_letters
    random.shuffle(options)
    
    return word, hint, draw_func, missing_index, correct_letter, options, "level1"

def generate_level2_question():
    """Generate a level 2 question (melengkapi 2-3 huruf rumpang)"""
    word_data = random.choice(WORD_DATABASE)
    word = word_data["word"]
    hint = word_data["hint"]
    draw_func = word_data["draw_func"]
    
    # Tentukan jumlah huruf yang hilang (2 atau 3)
    num_missing = random.randint(2, 3)
    if len(word) <= num_missing:
        num_missing = len(word) - 1
    
    # Pilih posisi huruf yang hilang
    missing_indices = random.sample(range(len(word)), num_missing)
    correct_letters = [word[i] for i in missing_indices]
    
    # Generate opsi untuk setiap huruf yang hilang
    all_options = []
    for correct_letter in correct_letters:
        all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        if correct_letter in all_letters:
            all_letters.remove(correct_letter)
        
        wrong_letters = random.sample(all_letters, 2)
        options = [correct_letter] + wrong_letters
        random.shuffle(options)
        all_options.append(options)
    
    return word, hint, draw_func, missing_indices, correct_letters, all_options, "level2"

def generate_level3_question():
    """Generate a level 3 question (menyusun kata dari huruf-huruf)"""
    word_data = random.choice(WORD_DATABASE)
    word = word_data["word"]
    hint = word_data["hint"]
    draw_func = word_data["draw_func"]
    
    # Acak huruf-huruf kata
    letters = list(word)
    random.shuffle(letters)
    
    # Tambahkan beberapa huruf acak sebagai distraktor
    all_letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    for letter in word:
        if letter in all_letters:
            all_letters.remove(letter)
    
    distractors = random.sample(all_letters, min(3, len(all_letters)))
    all_letters_options = letters + distractors
    random.shuffle(all_letters_options)
    
    return word, hint, draw_func, all_letters_options, "level3"

def generate_level4_question():
    """Generate a level 4 question (mencocokkan kata dengan gambar)"""
    # Pilih kata yang benar
    correct_data = random.choice(WORD_DATABASE)
    correct_word = correct_data["word"]
    correct_hint = correct_data["hint"]
    correct_draw_func = correct_data["draw_func"]
    
    # Pilih 3 kata lain sebagai opsi salah
    other_options = [d for d in WORD_DATABASE if d["word"] != correct_word]
    wrong_options = random.sample(other_options, min(3, len(other_options)))
    
    # Buat list opsi
    options = [{"word": correct_word, "hint": correct_hint, "draw_func": correct_draw_func}]
    for option in wrong_options:
        options.append({"word": option["word"], "hint": option["hint"], "draw_func": option["draw_func"]})
    
    random.shuffle(options)
    
    return correct_word, correct_hint, correct_draw_func, options, "level4"

# --- 6. FUNGSI GAMBAR TAMPILAN EDUKASI ---
# [Fungsi draw_education_menu, draw_letter_learning, draw_word_learning, 
# draw_number_learning sudah diimplementasi dengan baik di kode Anda sebelumnya]

def draw_level_select_menu(context, mouse_pos, unlocked_levels):
    """Draw level selection menu"""
    draw_background(context)
    
    # Title
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(40)
    title = "PILIH LEVEL"
    extents = context.text_extents(title)
    context.move_to((WIDTH - extents[2]) / 2, 60)
    context.show_text(title)
    context.stroke()
    
    # Instructions
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(20)
    instruction = "Klik level yang ingin dimainkan"
    extents = context.text_extents(instruction)
    context.move_to((WIDTH - extents[2]) / 2, 100)
    context.show_text(instruction)
    context.stroke()
    
    # Level buttons
    level_buttons = []
    level_descriptions = [
        "Level 1: Melengkapi 1 huruf rumpang",
        "Level 2: Melengkapi 2-3 huruf rumpang",
        "Level 3: Menyusun kata dari huruf-huruf",
        "Level 4: Mencocokkan kata dengan gambar"
    ]
    
    for i in range(4):
        y_pos = 150 + i * 100
        
        # Determine button color based on unlock status
        if i < unlocked_levels:
            color = (0.2, 0.8, 0.4)  # Green for unlocked
            text_color = (1, 1, 1)    # White text
        else:
            color = (0.5, 0.5, 0.5)  # Gray for locked
            text_color = (0.8, 0.8, 0.8)  # Light gray text
        
        # Create button
        btn = Button(200, y_pos, 400, 80, level_descriptions[i], color, 20)
        btn.update_hover(mouse_pos)
        btn.draw(context)
        level_buttons.append(btn)
        
        # Draw lock icon for locked levels
        if i >= unlocked_levels:
            context.set_source_rgb(*text_color)
            context.set_font_size(30)
            context.move_to(550, y_pos + 50)
            context.show_text("🔒")
            context.stroke()
    
    # Back button
    back_btn = Button(300, 520, 200, 50, "KEMBALI", (0.2, 0.6, 0.9), 20)
    back_btn.update_hover(mouse_pos)
    back_btn.draw(context)
    
    return level_buttons, back_btn

def main():
    score = 0
    lives = 3
    level_scores = [0, 0, 0, 0]  # Skor untuk setiap level
    unlocked_levels = 1  # Hanya level 1 yang terbuka di awal
    
    # Mode Game
    MENU = 0
    WORD_GAME = 1
    EDUCATION_MENU = 2
    LETTER_LEARNING = 3
    WORD_LEARNING = 4
    NUMBER_LEARNING = 5
    LEVEL_SELECT = 6
    
    game_state = MENU
    current_level = 1  # Level yang sedang dimainkan
    
    # State untuk Game
    level1_question = generate_level1_question()
    level2_question = generate_level2_question()
    level3_question = generate_level3_question()
    level4_question = generate_level4_question()
    
    # Variabel untuk game kuis
    current_question = level1_question
    
    # Variabel untuk edukasi
    current_letter_index = 0
    current_word_index = 0
    current_number_index = 1
    
    # Umpan Balik (Feedback)
    feedback = ""
    feedback_timer = 0
    show_celebration = False
    celebration_timer = 0
    
    # Tombol Opsi (Game Kuis)
    button_width = 150
    button_height = 100
    button_spacing = 50
    colors = [(0.2, 0.8, 0.4), (0.2, 0.6, 0.9), (0.9, 0.5, 0.2)]
    
    # Tombol Kembali
    back_btn_game = Button(20, 20, 100, 40, "KEMBALI", (0.9, 0.5, 0.2), 20)
    
    # Variabel untuk level 3 (menyusun kata)
    selected_letters = []
    letter_buttons = []
    
    # Variabel untuk dialog konfirmasi level complete
    show_level_complete_dialog = False
    dialog_buttons = []
    level2_answers = {}  # Untuk melacak jawaban yang dipilih untuk setiap posisi
    
    def reset_game(level):
        nonlocal score, lives, current_question, feedback, feedback_timer, show_celebration, celebration_timer, selected_letters, letter_buttons, show_level_complete_dialog, level2_answers
        score = 0
        lives = 3
        feedback = ""
        feedback_timer = 0
        show_celebration = False
        celebration_timer = 0
        selected_letters = []
        letter_buttons = []
        show_level_complete_dialog = False
        level2_answers = {}  # Reset jawaban level 2
        
        if level == 1:
            current_question = generate_level1_question()
        elif level == 2:
            current_question = generate_level2_question()
        elif level == 3:
            current_question = generate_level3_question()
        elif level == 4:
            current_question = generate_level4_question()
    
    def handle_answer_click(clicked_option, level, position_index=None):
        nonlocal score, lives, current_question, feedback, feedback_timer, show_celebration, celebration_timer, level_scores, selected_letters, show_level_complete_dialog, level2_answers
        
        is_correct = False
        
        if level == 1:
            correct_answer = current_question[4]
            if clicked_option == correct_answer:
                is_correct = True
        elif level == 2:
            # Simpan jawaban untuk posisi ini
            if position_index is not None:
                level2_answers[position_index] = clicked_option
                
                # Periksa apakah semua jawaban sudah benar
                word, hint, draw_func, missing_indices, correct_letters, all_options, _ = current_question
                all_correct = True
                
                for i, correct_letter in enumerate(correct_letters):
                    if i not in level2_answers or level2_answers[i] != correct_letter:
                        all_correct = False
                        break
                
                # Hanya beri poin jika semua jawaban benar
                if all_correct and len(level2_answers) == len(correct_letters):
                    is_correct = True
                    feedback = "BENAR!"
                else:
                    feedback = f"COBA LAGI! ({len(level2_answers)}/{len(correct_letters)})"
                    feedback_timer = 40
        elif level == 3:
            # Untuk level 3, kita perlu memeriksa kata yang disusun
            correct_word = current_question[0]
            if ''.join(selected_letters) == correct_word:
                is_correct = True
        elif level == 4:
            correct_word = current_question[0]
            if clicked_option == correct_word:
                is_correct = True
        
        if is_correct:
            score += 10
            level_scores[level-1] += 10
            feedback = "BENAR!"
            feedback_timer = 60
            show_celebration = True
            celebration_timer = 60
            pygame.time.wait(300) 
            
            # Generate new question
            if level == 1:
                current_question = generate_level1_question()
            elif level == 2:
                current_question = generate_level2_question()
                level2_answers = {}  # Reset jawaban untuk pertanyaan baru
            elif level == 3:
                current_question = generate_level3_question()
                selected_letters = []
            elif level == 4:
                current_question = generate_level4_question()
                
            # Cek apakah level selesai (mencapai skor 200)
            if level_scores[level-1] >= 200 and level < 4:
                # Tampilkan dialog konfirmasi
                show_level_complete_dialog = True
                feedback_timer = 0  # Reset feedback timer
        elif level != 2:  # Jangan kurangi nyawa untuk level 2 jika jawaban belum lengkap
            lives -= 1
            feedback = "COBA LAGI!"
            feedback_timer = 40
            if lives == 0:
                # Game Over
                pass
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == MENU:
                    # Logic for start menu buttons
                    if 250 <= mouse_pos[0] <= 550 and 250 <= mouse_pos[1] <= 330:
                        game_state = EDUCATION_MENU
                    elif 250 <= mouse_pos[0] <= 550 and 350 <= mouse_pos[1] <= 430:
                        game_state = LEVEL_SELECT
                
                elif game_state == LEVEL_SELECT:
                    level_buttons, back_btn = draw_level_select_menu(context, mouse_pos, unlocked_levels)
                    
                    for i, btn in enumerate(level_buttons):
                        if btn.is_clicked(mouse_pos) and i < unlocked_levels:
                            current_level = i + 1
                            game_state = WORD_GAME
                            reset_game(current_level)
                            break
                    
                    if back_btn.is_clicked(mouse_pos):
                        game_state = MENU
                
                elif game_state == EDUCATION_MENU:
                    letter_btn, word_btn, number_btn, back_btn_edu = draw_education_menu(context, mouse_pos)
                    if letter_btn.is_clicked(mouse_pos):
                        game_state = LETTER_LEARNING
                    elif word_btn.is_clicked(mouse_pos):
                        game_state = WORD_LEARNING
                    elif number_btn.is_clicked(mouse_pos):
                        game_state = NUMBER_LEARNING
                    elif back_btn_edu.is_clicked(mouse_pos):
                        game_state = MENU
                        
                elif game_state == LETTER_LEARNING:
                    prev_btn, next_btn, back_btn_learn = draw_letter_learning(context, mouse_pos, current_letter_index)
                    if prev_btn.is_clicked(mouse_pos):
                        current_letter_index = (current_letter_index - 1) % 26
                    elif next_btn.is_clicked(mouse_pos):
                        current_letter_index = (current_letter_index + 1) % 26
                    elif back_btn_learn.is_clicked(mouse_pos):
                        game_state = EDUCATION_MENU
                        
                elif game_state == WORD_LEARNING:
                    prev_btn, next_btn, back_btn_learn = draw_word_learning(context, mouse_pos, current_word_index)
                    if prev_btn.is_clicked(mouse_pos):
                        current_word_index = (current_word_index - 1) % len(WORD_DATABASE)
                    elif next_btn.is_clicked(mouse_pos):
                        current_word_index = (current_word_index + 1) % len(WORD_DATABASE)
                    elif back_btn_learn.is_clicked(mouse_pos):
                        game_state = EDUCATION_MENU
                elif game_state == WORD_GAME and lives > 0:
                    if back_btn_game.is_clicked(mouse_pos):
                        game_state = LEVEL_SELECT
                    if current_level == 1:
                        # Level 1: Melengkapi 1 huruf rumpang
                        for btn in buttons:
                            if btn.is_clicked(mouse_pos):
                                handle_answer_click(btn.text, 1)
                                break
                    elif current_level == 2:
                        # Level 2: Melengkapi 2-3 huruf rumpang
                        for i, btn_group in enumerate(buttons):
                            for btn in btn_group:
                                if btn.is_clicked(mouse_pos):
                                    # Kirim posisi index bersama dengan jawaban
                                    handle_answer_click(btn.text, 2, i)
                                    break
                    elif current_level == 3:
                        # Level 3: Menyusun kata dari huruf-huruf
                        for btn in letter_buttons:
                            if btn.is_clicked(mouse_pos) and btn.text not in selected_letters:
                                selected_letters.append(btn.text)
                                if len(selected_letters) == len(current_question[0]):
                                    handle_answer_click('', 3)
                                break
                    elif current_level == 4:
                        # Level 4: Mencocokkan kata dengan gambar
                        for btn in buttons:
                            if btn.is_clicked(mouse_pos):
                                handle_answer_click(btn.text, 4)
                                break
                
                elif game_state == WORD_GAME and lives > 0:
                    # Game Over screen click to menu
                    game_state = LEVEL_SELECT
                
                # Handle dialog buttons
                if show_level_complete_dialog:
                    for btn in dialog_buttons:
                        if btn.is_clicked(mouse_pos):
                            if btn.text == "YA":
                                # Buka level berikutnya
                                unlocked_levels = current_level + 1
                                current_level += 1
                                reset_game(current_level)
                                feedback = f"SELAMAT DATANG DI LEVEL {current_level}!"
                                feedback_timer = 120
                            else:  # TIDAK
                                # Tetap di level yang sama
                                reset_game(current_level)
                                feedback = f"ANDA TETAP DI LEVEL {current_level}"
                                feedback_timer = 120
                            
                            show_level_complete_dialog = False
                            break

        draw_background(context)
        
        if game_state == MENU:
            # Main Menu Drawing
            context.set_source_rgba(1, 1, 1, 0.95)
            context.rectangle(140, 130, 520, 370) 
            context.fill()
            
            context.set_source_rgb(0.5, 0.2, 0.8)
            context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            context.set_font_size(30)
            text = "KUIS KATA"
            extents = context.text_extents(text)
            context.move_to((WIDTH - extents[2]) / 2, 220)
            context.show_text(text)
            
            context.set_font_size(25)
            text2 = "Belajar Huruf & Kata"
            extents = context.text_extents(text2)
            context.move_to((WIDTH - extents[2]) / 2, 260)
            context.show_text(text2)
            context.stroke()
            
            # Buttons
            edu_btn = Button(250, 280, 300, 50, "BELAJAR", (0.2, 0.6, 0.8), 30)
            word_game_btn = Button(250, 350, 300, 50, "KUIS KATA", (0.2, 0.8, 0.4), 30)
            
            edu_btn.update_hover(mouse_pos)
            word_game_btn.update_hover(mouse_pos)

            edu_btn.draw(context)
            word_game_btn.draw(context)

        elif game_state == LEVEL_SELECT:
            draw_level_select_menu(context, mouse_pos, unlocked_levels)
            
        elif game_state == EDUCATION_MENU:
            draw_education_menu(context, mouse_pos)
            
        elif game_state == LETTER_LEARNING:
            draw_letter_learning(context, mouse_pos, current_letter_index)

        elif game_state == WORD_LEARNING:
            draw_word_learning(context, mouse_pos, current_word_index)

        elif game_state == WORD_GAME and lives > 0:
            # Game Kuis Kata berdasarkan level
            
            # Question Background
            context.set_source_rgba(1, 1, 1, 0.95)
            context.arc(WIDTH//2, 230, 350, 0, 2 * 3.14)
            context.fill()
            
            # Score and Lives
            back_btn_game.update_hover(mouse_pos)
            back_btn_game.draw(context)
            
            context.set_source_rgb(1, 1, 1)
            context.rectangle(20, 70, 150, 60)
            context.fill()
            draw_star(context, 50, 100, 15)
            context.set_source_rgb(0.5, 0.2, 0.8)
            context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            context.set_font_size(30)
            context.move_to(80, 105)
            context.show_text(str(score))
            context.stroke()
            
            # Level indicator
            context.set_source_rgb(1, 1, 1)
            context.rectangle(WIDTH - 170, 70, 150, 60)
            context.fill()
            context.set_source_rgb(0.5, 0.2, 0.8)
            context.set_font_size(30)
            context.move_to(WIDTH - 120, 105)
            context.show_text(f"Level {current_level}")
            context.stroke()
            
            # Progress to next level
            context.set_source_rgb(1, 1, 1)
            context.set_font_size(20)
            progress_text = f"Skor Level: {level_scores[current_level-1]}/200"
            extents = context.text_extents(progress_text)
            context.move_to(WIDTH - extents[2] - 20, 140)
            context.show_text(progress_text)
            context.stroke()
            
            for i in range(3):
                draw_heart(context, WIDTH - 100 + i * 35, 40, i < lives)
                
            # Draw Question Content based on current level
            buttons = []
            
            if current_level == 1:
                word, hint, draw_func, missing_index, correct_letter, options, _ = current_question
                draw_func(context, WIDTH // 2, 170, 2.0)
                
                context.set_source_rgb(0.2, 0.5, 0.8)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(20)
                extents = context.text_extents(hint)
                context.move_to((WIDTH - extents[2]) / 2, 250)
                context.show_text(hint)
                context.stroke()
                
                # Display word with missing letter
                display_word = ""
                for i, letter in enumerate(word):
                    display_word += ("_" if i == missing_index else letter) + " "
                
                context.set_source_rgb(0.3, 0.1, 0.6)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                context.set_font_size(60)
                extents = context.text_extents(display_word)
                context.move_to((WIDTH - extents[2]) / 2, 330)
                context.show_text(display_word)
                context.stroke()
                
                # Create buttons for options
                start_x = (WIDTH - (3 * button_width + 2 * button_spacing)) // 2
                buttons = [Button(start_x + i * (button_width + button_spacing), 400, 
                                button_width, button_height, options[i], colors[i]) for i in range(3)]
                
                # Instruction and Buttons
                context.set_source_rgb(0.4, 0.4, 0.4)
                context.set_font_size(24)
                instruction = "Klik huruf yang tepat!"
                extents = context.text_extents(instruction)
                context.move_to((WIDTH - extents[2]) / 2, 380)
                context.show_text(instruction)
                context.stroke()
                
                for btn in buttons:
                    btn.update_hover(mouse_pos)
                    btn.draw(context)
            
            elif current_level == 2:
                word, hint, draw_func, missing_indices, correct_letters, all_options, _ = current_question
                draw_func(context, WIDTH // 2, 170, 2.0)
                
                context.set_source_rgb(0.2, 0.5, 0.8)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(20)
                extents = context.text_extents(hint)
                context.move_to((WIDTH - extents[2]) / 2, 250)
                context.show_text(hint)
                context.stroke()
                
                # Display word with missing letters
                display_word = ""
                for i, letter in enumerate(word):
                    # Tampilkan huruf yang sudah dijawab dengan benar
                    if i in missing_indices and i in level2_answers:
                        display_word += level2_answers[i] + " "
                    elif i in missing_indices:
                        display_word += "_ "
                    else:
                        display_word += letter + " "
                
                context.set_source_rgb(0.3, 0.1, 0.6)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                context.set_font_size(60)
                extents = context.text_extents(display_word)
                context.move_to((WIDTH - extents[2]) / 2, 330)
                context.show_text(display_word)
                context.stroke()
                
                # Create buttons for each missing letter position
                buttons = []
                for i, options in enumerate(all_options):
                    y_pos = 400 + i * 60
                    btn_group = []
                    start_x = (WIDTH - (3 * button_width + 2 * button_spacing)) // 2
                    
                    # Tampilkan indikator untuk jawaban yang sudah dipilih
                    if i in level2_answers:
                        context.set_source_rgb(0.2, 0.8, 0.3)
                        context.set_font_size(20)
                        context.move_to(start_x - 50, y_pos + 30)
                        context.show_text("✓")
                        context.stroke()
                    
                    for j, option in enumerate(options):
                        # Nonaktifkan tombol jika jawaban untuk posisi ini sudah dipilih
                        if i in level2_answers:
                            color = (0.5, 0.5, 0.5)
                        else:
                            color = colors[j]
                        
                        btn = Button(start_x + j * (button_width + button_spacing), y_pos, 
                                    button_width, button_height, option, color)
                        btn.update_hover(mouse_pos)
                        btn.draw(context)
                        btn_group.append(btn)
                    
                    buttons.append(btn_group)
                
                # Instruction
                context.set_source_rgb(0.4, 0.4, 0.4)
                context.set_font_size(24)
                instruction = "Klik huruf yang tepat untuk setiap posisi!"
                extents = context.text_extents(instruction)
                context.move_to((WIDTH - extents[2]) / 2, 380)
                context.show_text(instruction)
                context.stroke()
                
                # Progress indicator
                context.set_source_rgb(0.2, 0.5, 0.8)
                context.set_font_size(18)
                progress_text = f"Progress: {len(level2_answers)}/{len(correct_letters)} huruf"
                extents = context.text_extents(progress_text)
                context.move_to((WIDTH - extents[2]) / 2, 360)
                context.show_text(progress_text)
                context.stroke()
            
            elif current_level == 3:
                word, hint, draw_func, letters, _ = current_question
                draw_func(context, WIDTH // 2, 170, 2.0)
                
                context.set_source_rgb(0.2, 0.5, 0.8)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(20)
                extents = context.text_extents(hint)
                context.move_to((WIDTH - extents[2]) / 2, 250)
                context.show_text(hint)
                context.stroke()
                
                # Display selected letters
                context.set_source_rgb(0.3, 0.1, 0.6)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                context.set_font_size(60)
                
                word_width = len(word) * 40
                x_pos = WIDTH//2 - word_width // 2 + 20
                for i in range(len(word)):
                    if i < len(selected_letters):
                        context.move_to(x_pos + i * 40 - 15, 340)
                        context.show_text(selected_letters[i])
                    else:
                        context.rectangle(x_pos + i * 40 - 15, 310, 30, 40)
                        context.stroke()
                
                # Create buttons for letters
                letter_buttons = []
                letters_per_row = 6
                for i, letter in enumerate(letters):
                    row = i // letters_per_row
                    col = i % letters_per_row
                    x = 200 + col * 70
                    y = 400 + row * 60
                    
                    # Disable button if letter already selected
                    if letter in selected_letters:
                        color = (0.5, 0.5, 0.5)
                    else:
                        color = (0.2, 0.6, 0.9)
                    
                    btn = Button(x, y, 60, 50, letter, color, 30)
                    btn.update_hover(mouse_pos)
                    btn.draw(context)
                    letter_buttons.append(btn)
                
                # Reset button
                reset_btn = Button(350, 500, 100, 40, "RESET", (0.9, 0.5, 0.2), 20)
                reset_btn.update_hover(mouse_pos)
                reset_btn.draw(context)
                
                if reset_btn.is_clicked(mouse_pos):
                    selected_letters = []
                
                # Instruction
                context.set_source_rgb(0.4, 0.4, 0.4)
                context.set_font_size(24)
                instruction = "Susun huruf-huruf menjadi kata yang tepat!"
                extents = context.text_extents(instruction)
                context.move_to((WIDTH - extents[2]) / 2, 380)
                context.show_text(instruction)
                context.stroke()
            
            elif current_level == 4:
                correct_word, hint, draw_func, options, _ = current_question
                
                context.set_source_rgb(0.2, 0.5, 0.8)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                context.set_font_size(20)
                extents = context.text_extents("Pilih kata yang sesuai dengan gambar:")
                context.move_to((WIDTH - extents[2]) / 2, 100)
                context.show_text(extents)
                context.stroke()
                
                # Draw the image
                draw_func(context, WIDTH // 2, 200, 2.0)
                
                # Create buttons for options
                buttons = []
                for i, option in enumerate(options):
                    y_pos = 320 + i * 60
                    btn = Button(250, y_pos, 300, 50, option["word"], (0.2, 0.6, 0.9), 20)
                    btn.update_hover(mouse_pos)
                    btn.draw(context)
                    buttons.append(btn)
                
                # Instruction
                context.set_source_rgb(0.4, 0.4, 0.4)
                context.set_font_size(24)
                instruction = "Klik kata yang sesuai dengan gambar!"
                extents = context.text_extents(instruction)
                context.move_to((WIDTH - extents[2]) / 2, 290)
                context.show_text(instruction)
                context.stroke()
            
            # Tambahkan dialog konfirmasi jika level selesai
            if show_level_complete_dialog:
                # Draw dialog background
                context.set_source_rgba(0, 0, 0, 0.8)
                context.rectangle(150, 200, 500, 200)
                context.fill()
                
                context.set_source_rgb(1, 1, 1)
                context.set_font_size(30)
                dialog_text = f"LEVEL {current_level} SELESAI!"
                extents = context.text_extents(dialog_text)
                context.move_to((WIDTH - extents[2]) / 2, 240)
                context.show_text(dialog_text)
                
                context.set_font_size(24)
                question_text = "Lanjut ke level selanjutnya?"
                extents = context.text_extents(question_text)
                context.move_to((WIDTH - extents[2]) / 2, 290)
                context.show_text(question_text)
                
                # Create dialog buttons
                dialog_buttons = [
                    Button(250, 330, 100, 50, "YA", (0.2, 0.8, 0.4), 24),
                    Button(450, 330, 100, 50, "TIDAK", (0.9, 0.5, 0.2), 24)
                ]
                
                for btn in dialog_buttons:
                    btn.update_hover(mouse_pos)
                    btn.draw(context)
            
            # Feedback
            if feedback_timer > 0:
                if feedback == "BENAR!":
                    context.set_source_rgb(0.2, 0.8, 0.3)
                else:
                    context.set_source_rgb(0.9, 0.5, 0.2)
                context.set_font_size(50)
                extents = context.text_extents(feedback)
                context.move_to((WIDTH - extents[2]) / 2, HEIGHT - 50)
                context.show_text(feedback)
                context.stroke()
                feedback_timer -= 1
            
            # Celebration
            if show_celebration and celebration_timer > 0:
                for _ in range(5):
                    x = random.randint(100, WIDTH - 100)
                    y = random.randint(50, 250)
                    draw_star(context, x, y, random.randint(10, 20))
                celebration_timer -= 1
                if celebration_timer == 0:
                    show_celebration = False
        
        elif game_state == WORD_GAME and lives == 0:
            # Game Over Screen
            context.set_source_rgba(1, 1, 1, 0.95)
            context.rectangle(150, 150, 500, 350)
            context.fill()
            
            context.set_source_rgb(0.9, 0.2, 0.2)
            context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            context.set_font_size(50)
            text = "GAME SELESAI!"
            extents = context.text_extents(text)
            context.move_to((WIDTH - extents[2]) / 2, 250)
            context.show_text(text)
            
            context.set_font_size(40)
            score_text = f"SKOR AKHIR: {score}"
            extents = context.text_extents(score_text)
            context.move_to((WIDTH - extents[2]) / 2, 320)
            context.show_text(score_text)
            context.stroke()
            
            context.set_source_rgb(0.5, 0.2, 0.8)
            context.set_font_size(20)
            text_kembali = "Klik di mana saja untuk kembali ke Menu Level"
            extents = context.text_extents(text_kembali)
            context.move_to((WIDTH - extents[2]) / 2, 400)
            context.show_text(text_kembali)
            context.stroke()
            
        # --- BLIT CAIRO TO PYGAME ---
        pygame.surfarray.blit_array(screen, data[:, :, [2, 1, 0]].swapaxes(0, 1))
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()