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

def draw_apples_for_counting(context, count, x, y, size=1.0):
    """Draw multiple apples for counting, max 5 per row"""
    max_row = 5
    for i in range(count):
        row = i // max_row
        col = i % max_row
        draw_apple(context, x + col * 40 * size, y + row * 40 * size, size)

def draw_balls_for_counting(context, count, x, y, size=1.0):
    """Draw multiple balls for counting, max 5 per row"""
    max_row = 5
    for i in range(count):
        row = i // max_row
        col = i % max_row
        draw_ball(context, x + col * 40 * size, y + row * 40 * size, size)

def draw_math_visualization(context, operation, num1, num2, x, y, size=1.0):
    """Draw visualization for math operations (addition/subtraction)"""
    # The visualization logic is simplified for better display

    # Common text style
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(40)
    
    # Starting position adjustment based on maximum items (num1 is the max)
    max_items = num1 
    start_x_visual = x - max_items * 40 * size / 2

    # Draw first group
    draw_apples_for_counting(context, num1, start_x_visual, y, size)
    
    if operation == "+":
        # Draw plus sign
        context.move_to(start_x_visual + num1 * 40 * size + 10, y + 20)
        context.show_text("+")
        context.stroke()
        
        # Draw second group
        draw_balls_for_counting(context, num2, start_x_visual + num1 * 40 * size + 60, y, size)
        
        # Draw equals sign
        context.move_to(start_x_visual + (num1+num2) * 40 * size + 80, y + 20)
        context.show_text("=")
        context.stroke()
        
        # Draw result (conceptual location)
        result = num1 + num2
        # Center the result apples
        result_x = x - (result * 40 * size) / 2 + 200 # A bit far right for space
        draw_apples_for_counting(context, result, result_x, y, size)
        
    elif operation == "-":
        # Draw minus sign
        context.move_to(start_x_visual + num1 * 40 * size + 10, y + 20)
        context.show_text("-")
        context.stroke()
        
        # Draw second number (as crossed-out items for visualization)
        # Re-draw the first group and cross out items equal to num2
        
        # New starting position for the "result" part of the equation
        result_start_x = start_x_visual + num1 * 40 * size + 60
        
        # Draw the 'subtracted' balls/apples
        for i in range(num2):
            ball_x = result_start_x + i * 40 * size
            draw_ball(context, ball_x, y, size)
            # Draw strikethrough
            context.set_source_rgb(1, 0, 0)
            context.set_line_width(5)
            context.move_to(ball_x - 15, y - 15)
            context.line_to(ball_x + 15, y + 15)
            context.stroke()
        
        # Draw equals sign
        context.set_source_rgb(1, 1, 1)
        context.move_to(result_start_x + num2 * 40 * size + 10, y + 20)
        context.show_text("=")
        context.stroke()
        
        # Draw result
        result = num1 - num2
        draw_apples_for_counting(context, result, result_start_x + num2 * 40 * size + 60, y, size)


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

MATH_DATABASE = [
    {"question": "2 + 3", "answer": "5", "operation": "+", "num1": 2, "num2": 3},
    {"question": "5 - 2", "answer": "3", "operation": "-", "num1": 5, "num2": 2},
    {"question": "1 + 4", "answer": "5", "operation": "+", "num1": 1, "num2": 4},
    {"question": "6 - 3", "answer": "3", "operation": "-", "num1": 6, "num2": 3},
    {"question": "3 + 2", "answer": "5", "operation": "+", "num1": 3, "num2": 2},
    {"question": "4 - 1", "answer": "3", "operation": "-", "num1": 4, "num2": 1},
    {"question": "2 + 2", "answer": "4", "operation": "+", "num1": 2, "num2": 2},
    {"question": "7 - 4", "answer": "3", "operation": "-", "num1": 7, "num2": 4},
    {"question": "3 + 3", "answer": "6", "operation": "+", "num1": 3, "num2": 3},
    {"question": "5 - 3", "answer": "2", "operation": "-", "num1": 5, "num2": 3},
    {"question": "4 + 2", "answer": "6", "operation": "+", "num1": 4, "num2": 2},
    {"question": "8 - 5", "answer": "3", "operation": "-", "num1": 8, "num2": 5},
    {"question": "1 + 1", "answer": "2", "operation": "+", "num1": 1, "num2": 1},
    {"question": "9 - 6", "answer": "3", "operation": "-", "num1": 9, "num2": 6},
    {"question": "2 + 4", "answer": "6", "operation": "+", "num1": 2, "num2": 4},
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

def generate_math_question():
    """Generate a math question (addition/subtraction)"""
    math_data = random.choice(MATH_DATABASE)
    question = math_data["question"]
    answer = math_data["answer"]
    operation = math_data["operation"]
    num1 = math_data["num1"]
    num2 = math_data["num2"]
    
    all_numbers = list("0123456789")
    if answer in all_numbers:
        all_numbers.remove(answer)
    
    # Generate wrong options, max 2 or fewer if few numbers left
    num_to_sample = min(2, len(all_numbers))
    wrong_numbers = random.sample(all_numbers, num_to_sample)
    
    options = [answer] + wrong_numbers
    # Pad with random numbers if less than 3 options were initially created
    while len(options) < 3:
        rand_num = str(random.randint(0, 9))
        if rand_num not in options:
            options.append(rand_num)

    random.shuffle(options)
    
    # The 'word' variable in the main loop will hold the question string here
    # 'hint' will hold the correct answer string
    return question, answer, operation, num1, num2, options, "math"

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

def draw_number_learning(context, mouse_pos, current_number_index):
    """Draw number learning screen"""
    draw_background(context)
    
    # Title
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(40)
    title = "BELAJAR ANGKA"
    extents = context.text_extents(title)
    context.move_to((WIDTH - extents[2]) / 2, 60)
    context.show_text(title)
    context.stroke()
    
    # Current number
    current_number = current_number_index
    
    draw_number(context, current_number, WIDTH//2, 200, 120)
    
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(24)
    context.move_to(WIDTH//2 - 100, 300)
    context.show_text("Jumlah:")
    context.stroke()
    
    # Draw counting representation
    draw_apples_for_counting(context, current_number, WIDTH//2 - 100, 350, 0.8)
    
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

def draw_math_learning(context, mouse_pos, current_math_index):
    """Draw math learning screen with detailed explanation"""
    draw_background(context)
    
    # Title
    context.set_source_rgb(1, 1, 1)
    context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    context.set_font_size(40)
    title = "BELAJAR MATEMATIKA"
    extents = context.text_extents(title)
    context.move_to((WIDTH - extents[2]) / 2, 60)
    context.show_text(title)
    context.stroke()
    
    # Current math problem
    math_data = MATH_DATABASE[current_math_index]
    question = math_data["question"]
    answer = math_data["answer"]
    operation = math_data["operation"]
    num1 = math_data["num1"]
    num2 = math_data["num2"]
    
    # Draw the math problem
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(60)
    extents = context.text_extents(question + " = ?")
    context.move_to((WIDTH - extents[2]) / 2, 120)
    context.show_text(question + " = ?")
    context.stroke()
    
    # Draw visual representation
    draw_math_visualization(context, operation, num1, num2, WIDTH//2, 220, 0.7)
    
    # Draw the answer
    context.set_source_rgb(1, 1, 0.8)
    context.set_font_size(40)
    answer_text = "Jawaban: " + answer
    extents = context.text_extents(answer_text)
    context.move_to((WIDTH - extents[2]) / 2, 320)
    context.show_text(answer_text)
    context.stroke()
    
    # Draw detailed explanation
    context.set_source_rgb(1, 1, 1)
    context.set_font_size(20)
    
    if operation == "+":
        explanation = [
            "Penjumlahan: menggabungkan dua kelompok",
            f"1. Kelompok pertama ada {num1} apel",
            f"2. Kelompok kedua ada {num2} bola",
            f"3. Total benda: {num1} + {num2} = {answer}"
        ]
    else:
        explanation = [
            "Pengurangan: mengambil dari kelompok",
            f"1. Kita punya {num1} apel",
            f"2. Kita ambil {num2} bola (dicoret)",
            f"3. Sisanya: {num1} - {num2} = {answer}"
        ]
    
    y_pos = 360
    for line in explanation:
        extents = context.text_extents(line)
        context.move_to((WIDTH - extents[2]) / 2, y_pos)
        context.show_text(line)
        context.stroke()
        y_pos += 25
    
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

# --- 7. FUNGSI LOGIKA UTAMA (main) ---

def main():
    # --- Inisialisasi Status Game ---
    score = 0
    lives = 3
    
    # Mode Game
    MENU = 0
    WORD_GAME = 1
    MATH_GAME = 2
    EDUCATION_MENU = 3
    LETTER_LEARNING = 4
    WORD_LEARNING = 5
    NUMBER_LEARNING = 6
    MATH_LEARNING = 7
    
    game_state = MENU
    
    # State untuk Game
    word_question = generate_word_question()
    math_question = generate_math_question()
    
    # Variabel untuk game kuis
    current_question = word_question
    
    # Variabel untuk edukasi
    current_letter_index = 0
    current_word_index = 0
    current_number_index = 1 
    current_math_index = 0
    
    # Umpan Balik (Feedback)
    feedback = ""
    feedback_timer = 0
    show_celebration = False
    celebration_timer = 0
    
    # Tombol Opsi (Game Kuis)
    button_width = 150
    button_height = 100
    button_spacing = 50
    start_x = (WIDTH - (3 * button_width + 2 * button_spacing)) // 2
    start_y = 400
    colors = [(0.2, 0.8, 0.4), (0.2, 0.6, 0.9), (0.9, 0.5, 0.2)]
    buttons = [Button(start_x + i * (button_width + button_spacing), start_y, 
                      button_width, button_height, "", colors[i]) for i in range(3)]

    # Tombol Kembali
    back_btn_game = Button(20, 20, 100, 40, "KEMBALI", (0.9, 0.5, 0.2), 20)
    
    def reset_game(mode):
        nonlocal score, lives, current_question, feedback, feedback_timer, show_celebration, celebration_timer
        score = 0
        lives = 3
        feedback = ""
        feedback_timer = 0
        show_celebration = False
        celebration_timer = 0
        
        if mode == WORD_GAME:
            current_question = generate_word_question()
        elif mode == MATH_GAME:
            current_question = generate_math_question()
        
        # Update button text for the new question
        options = current_question[5]
        for i, btn in enumerate(buttons):
            btn.text = options[i]
    
    def handle_answer_click(clicked_option, is_math_game):
        nonlocal score, lives, current_question, feedback, feedback_timer, show_celebration, celebration_timer
        
        correct_answer = current_question[4] if not is_math_game else current_question[1]

        if clicked_option == correct_answer:
            score += 10
            feedback = "BENAR!"
            feedback_timer = 60
            show_celebration = True
            celebration_timer = 60
            pygame.time.wait(300) 
            
            if is_math_game:
                current_question = generate_math_question()
            else:
                current_question = generate_word_question()
            
            # Update button text
            options = current_question[5]
            for i, btn in enumerate(buttons):
                btn.text = options[i]
                
        else:
            lives -= 1
            feedback = "COBA LAGI!"
            feedback_timer = 40
            if lives == 0:
                # Game Over
                pass # Logic to handle game over will be in main loop drawing
    
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
                        game_state = WORD_GAME
                        reset_game(WORD_GAME)
                    elif 250 <= mouse_pos[0] <= 550 and 450 <= mouse_pos[1] <= 530:
                        game_state = MATH_GAME
                        reset_game(MATH_GAME)
                
                elif game_state == EDUCATION_MENU:
                    letter_btn, word_btn, number_btn, math_btn, back_btn_edu = draw_education_menu(context, mouse_pos)
                    if letter_btn.is_clicked(mouse_pos):
                        game_state = LETTER_LEARNING
                    elif word_btn.is_clicked(mouse_pos):
                        game_state = WORD_LEARNING
                    elif number_btn.is_clicked(mouse_pos):
                        game_state = NUMBER_LEARNING
                    elif math_btn.is_clicked(mouse_pos):
                        game_state = MATH_LEARNING
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

                elif game_state == NUMBER_LEARNING:
                    prev_btn, next_btn, back_btn_learn = draw_number_learning(context, mouse_pos, current_number_index)
                    if prev_btn.is_clicked(mouse_pos):
                        current_number_index = (current_number_index - 1)
                        if current_number_index < 1: current_number_index = 10
                    elif next_btn.is_clicked(mouse_pos):
                        current_number_index = (current_number_index + 1) % 11
                        if current_number_index == 0: current_number_index = 1 # Keep 1-10
                    elif back_btn_learn.is_clicked(mouse_pos):
                        game_state = EDUCATION_MENU
                        
                elif game_state == MATH_LEARNING:
                    prev_btn, next_btn, back_btn_learn = draw_math_learning(context, mouse_pos, current_math_index)
                    if prev_btn.is_clicked(mouse_pos):
                        current_math_index = (current_math_index - 1) % len(MATH_DATABASE)
                    elif next_btn.is_clicked(mouse_pos):
                        current_math_index = (current_math_index + 1) % len(MATH_DATABASE)
                    elif back_btn_learn.is_clicked(mouse_pos):
                        game_state = EDUCATION_MENU

                elif game_state in [WORD_GAME, MATH_GAME] and lives > 0:
                    if back_btn_game.is_clicked(mouse_pos):
                        game_state = MENU
                        
                    for btn in buttons:
                        if btn.is_clicked(mouse_pos):
                            handle_answer_click(btn.text, game_state == MATH_GAME)
                            break
                
                elif game_state in [WORD_GAME, MATH_GAME] and lives == 0:
                    # Game Over screen click to menu
                    game_state = MENU

        draw_background(context)
        
        if game_state == MENU:
            # Main Menu Drawing
            context.set_source_rgba(1, 1, 1, 0.95)
            context.rectangle(140, 130, 520, 370) 
            context.fill()
            
            context.set_source_rgb(0.5, 0.2, 0.8)
            context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            context.set_font_size(30)
            text = "SAMBUNG KATA & HITUNG CEPAT"
            extents = context.text_extents(text)
            context.move_to((WIDTH - extents[2]) / 2, 220)
            context.show_text(text)
            
            context.set_font_size(25)
            text2 = "Belajar Huruf & Angka"
            extents = context.text_extents(text2)
            context.move_to((WIDTH - extents[2]) / 2, 260)
            context.show_text(text2)
            context.stroke()
            
            # Buttons
            edu_btn = Button(250, 280, 300, 50, "BELAJAR", (0.2, 0.6, 0.8), 30)
            word_game_btn = Button(250, 350, 300, 50, "KUIS KATA", (0.2, 0.8, 0.4), 30)
            math_game_btn = Button(250, 420, 300, 50, "KUIS MATEMATIKA", (0.9, 0.5, 0.2), 30)
            
            edu_btn.update_hover(mouse_pos)
            word_game_btn.update_hover(mouse_pos)
            math_game_btn.update_hover(mouse_pos)

            edu_btn.draw(context)
            word_game_btn.draw(context)
            math_game_btn.draw(context)

        elif game_state == EDUCATION_MENU:
            draw_education_menu(context, mouse_pos)
            
        elif game_state == LETTER_LEARNING:
            draw_letter_learning(context, mouse_pos, current_letter_index)

        elif game_state == WORD_LEARNING:
            draw_word_learning(context, mouse_pos, current_word_index)
            
        elif game_state == NUMBER_LEARNING:
            draw_number_learning(context, mouse_pos, current_number_index)
            
        elif game_state == MATH_LEARNING:
            draw_math_learning(context, mouse_pos, current_math_index)

        elif game_state in [WORD_GAME, MATH_GAME] and lives > 0:
            # Game Kuis (Word/Math)
            
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
            
            for i in range(3):
                draw_heart(context, WIDTH - 100 + i * 35, 40, i < lives)
                
            # Draw Question Content
            if game_state == WORD_GAME:
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

            else: # MATH_GAME
                question, answer, operation, num1, num2, options, _ = current_question
                
                draw_math_visualization(context, operation, num1, num2, WIDTH//2, 180, 0.7)
                
                context.set_source_rgb(0.3, 0.1, 0.6)
                context.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                context.set_font_size(60)
                math_question_display = question + " = ?"
                extents = context.text_extents(math_question_display)
                context.move_to((WIDTH - extents[2]) / 2, 330)
                context.show_text(math_question_display)
                context.stroke()
            
            # Instruction and Buttons
            context.set_source_rgb(0.4, 0.4, 0.4)
            context.set_font_size(24)
            instruction = "Klik jawaban yang tepat!"
            extents = context.text_extents(instruction)
            context.move_to((WIDTH - extents[2]) / 2, 380)
            context.show_text(instruction)
            context.stroke()
            
            for btn in buttons:
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
        
        elif game_state in [WORD_GAME, MATH_GAME] and lives == 0:
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
            text_kembali = "Klik di mana saja untuk kembali ke Menu"
            extents = context.text_extents(text_kembali)
            context.move_to((WIDTH - extents[2]) / 2, 400)
            context.show_text(text_kembali)
            context.stroke()
            
        # --- BLIT CAIRO TO PYGAME ---
        # Swap axes and color channels (ARGB -> BGRA for Pygame compatibility)
        pygame.surfarray.blit_array(screen, data[:, :, [2, 1, 0]].swapaxes(0, 1))
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()