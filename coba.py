import pygame
import sys
import random
import math

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 1200, 800
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 180, 255)
GREEN = (100, 220, 120)
YELLOW = (255, 220, 80)
ORANGE = (255, 160, 80)
RED = (255, 120, 120)
PURPLE = (200, 150, 255)
PINK = (255, 180, 200)
CYAN = (150, 230, 255)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)

# Setup layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KataKu - Belajar Kata")
clock = pygame.time.Clock()

# Font - menggunakan font yang mendukung emoji
try:
    # Coba gunakan font yang mendukung emoji
    font_xl = pygame.font.SysFont("segoe ui emoji", 80)
    font_l = pygame.font.SysFont("segoe ui emoji", 30)
    font_m = pygame.font.SysFont("segoe ui emoji", 30)
    font_s = pygame.font.SysFont("segoe ui emoji", 30)
    font_xs = pygame.font.SysFont("segoe ui emoji", 20)
except:
    # Jika tidak tersedia, gunakan font default
    font_xl = pygame.font.Font(None, 80)
    font_l = pygame.font.Font(None, 30)
    font_m = pygame.font.Font(None, 45)
    font_s = pygame.font.Font(None, 35)
    font_xs = pygame.font.Font(None, 20)

# Data Kata dari KBBI untuk anak TK dengan emoji
KATA = {
    'mudah': [
        ('BOLA', '⚽ Mainan bulat ditendang'),
        ('KUCING', '🐱 Hewan berbulu suka ikan'),
        ('APEL', '🍎 Buah merah atau hijau'),
        ('BUKU', '📚 Untuk membaca cerita'),
        ('MEJA', '🪑 Tempat menulis'),
        ('SAPI', '🐄 Hewan besar beri susu'),
        ('NASI', '🍚 Makanan dari beras'),
        ('MATA', '👀 Untuk melihat'),
        ('TOPI', '🧢 Penutup kepala'),
        ('KAKI', '🦶 Untuk berjalan'),
    ],
    'sedang': [
        ('RUMAH', '🏠 Tempat tinggal'),
        ('AYAM', '🐔 Hewan berkokok'),
        ('JERUK', '🍊 Buah bulat oranye'),
        ('PENSIL', '✏️ Alat tulis dari kayu'),
        ('GAJAH', '🐘 Hewan punya belalai'),
        ('MOBIL', '🚗 Kendaraan roda empat'),
        ('PISANG', '🍌 Buah kuning panjang'),
        ('BURUNG', '🐦 Hewan bisa terbang'),
        ('JAGUNG', '🌽 Tanaman bulir kuning'),
        ('RANTAI', '⛓️ Pengikat dari logam'),
        ('ANGGUR', '🍇 Buah kecil bergerombol'),
        ('KURSI', '🪑 Tempat duduk'),
    ],
    'sulit': [
        ('KELINCI', '🐰 Hewan melompat telinga panjang'),
        ('SEMANGKA', '🍉 Buah besar hijau merah'),
        ('SEPEDA', '🚲 Kendaraan roda dua'),
        ('JERAPAH', '🦒 Hewan leher panjang'),
        ('TELEVISI', '📺 Alat untuk menonton'),
        ('PAYUNG', '☂️ Pelindung dari hujan'),
        ('PESAWAT', '✈️ Kendaraan terbang'),
        ('KANGURU', '🦘 Hewan punya kantong'),
        ('KOMPUTER', '💻 Alat elektronik untuk bekerja'),
        ('DINOSAURUS', '🦕 Hewan purba besar'),
        ('HELICOPTER', '🚁 Kendaraan terbang baling-baling'),
        ('STRAWBERRY', '🍓 Buah merah berbintik'),
    ]
}

# Progress pemain
player = {'nama': '', 'xp': 0, 'benar': 0}

# Pesan motivasi dengan emoji
PUJIAN = ["Keren! 🌟", "Wow! 🎉", "Bagus! 👍", "Hebat! 💪", "Pintar! 🧠", "Mantap! 🔥", "Luar Biasa! ✨", "Top! 👑", "Jago! 🏆", "Bravo! 👏"]
SEMANGAT = ["Coba Lagi! 😊", "Pasti Bisa! 💪", "Jangan Menyerah! 🌈", "Yuk Semangat! ⚡", "Ayo Lagi! 🔄"]

def gradient(surf, c1, c2):
    """Gambar gradient background"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        color = tuple(int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3))
        pygame.draw.line(surf, color, (0, y), (WIDTH, y))

def rounded_rect(surf, color, rect, radius=20):
    """Gambar kotak sudut bulat"""
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def buat_soal(kata, mode):
    """Buat soal dengan huruf hilang berdasarkan tingkat kesulitan"""
    panjang = len(kata)
    
    # Tingkat kesulitan yang lebih jelas
    if mode == 'mudah':
        jumlah_kosong = max(1, int(panjang * 0.30))
    elif mode == 'sedang':
        jumlah_kosong = max(2, int(panjang * 0.45))
    else:  # sulit
        jumlah_kosong = max(3, int(panjang * 0.60))
    
    # Batasi jumlah maksimal huruf kosong
    jumlah_kosong = min(jumlah_kosong, panjang - 1)
    
    # Pilih posisi random (tidak termasuk huruf pertama agar lebih mudah)
    posisi_tersedia = list(range(1, panjang))
    posisi_kosong = random.sample(posisi_tersedia, jumlah_kosong)
    posisi_kosong.sort()
    
    return posisi_kosong

def draw_button(surf, rect, color, text, font, hover=False):
    """Gambar tombol dengan efek hover"""
    if hover:
        bright_color = tuple(min(255, c + 30) for c in color)
        rounded_rect(surf, bright_color, rect, 20)
    else:
        rounded_rect(surf, color, rect, 20)
    
    pygame.draw.rect(surf, WHITE, rect, 3, border_radius=20)
    txt_surf = font.render(text, True, WHITE)
    surf.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, 
                         rect.centery - txt_surf.get_height()//2))

def main():
    state = 'nama'
    mode = None
    kata_sekarang = None
    petunjuk = None
    posisi_kosong = []
    input_user = ""
    pesan = ""
    warna_pesan = WHITE
    tampil_hasil = False
    hasil_benar = False
    xp_dapat = 0
    pesan_hasil = ""
    
    cek_tekan = False
    mouse_clicked = False
    last_click_time = 0
    
    running = True
    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                if current_time - last_click_time > 200:
                    mouse_clicked = True
                    last_click_time = current_time
            
            if state == 'nama':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player['nama'] = player['nama'][:-1]
                    elif event.key == pygame.K_RETURN and len(player['nama']) > 0:
                        state = 'menu'
                    elif event.unicode.isalpha() and len(player['nama']) < 15:
                        player['nama'] += event.unicode.upper()
            
            elif state == 'game' and not tampil_hasil:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_user = input_user[:-1]
                        pesan = ""
                    elif event.key == pygame.K_RETURN and len(input_user) == len(posisi_kosong):
                        cek_tekan = True
                    elif event.key == pygame.K_ESCAPE:
                        state = 'menu'
                    elif event.unicode.isalpha() and len(input_user) < len(posisi_kosong):
                        input_user += event.unicode.upper()
                        pesan = ""
        
        screen.fill(WHITE)
        
        # ===== LAYAR INPUT NAMA =====
        if state == 'nama':
            gradient(screen, CYAN, BLUE)
            
            # Judul dengan emoji
            judul = font_xl.render("KataKu 📚", True, WHITE)
            screen.blit(judul, (WIDTH//2 - judul.get_width()//2, 120))
            
            subjudul = font_l.render("Belajar Kata dengan Menyenangkan!", True, WHITE)
            screen.blit(subjudul, (WIDTH//2 - subjudul.get_width()//2, 210))
            
            tanya = font_m.render("Siapa namamu?", True, WHITE)
            screen.blit(tanya, (WIDTH//2 - tanya.get_width()//2, 320))
            
            input_box = pygame.Rect(WIDTH//2 - 200, 390, 400, 70)
            rounded_rect(screen, WHITE, input_box, 20)
            pygame.draw.rect(screen, ORANGE, input_box, 4, border_radius=20)
            
            nama_txt = font_l.render(player['nama'], True, BLACK)
            screen.blit(nama_txt, (input_box.centerx - nama_txt.get_width()//2, 
                                  input_box.centery - nama_txt.get_height()//2))
            
            if len(player['nama']) > 0:
                mulai_btn = pygame.Rect(WIDTH//2 - 100, 520, 200, 70)
                hover_mulai = mulai_btn.collidepoint(mouse_pos)
                draw_button(screen, mulai_btn, GREEN, "Mulai! 🎮", font_l, hover_mulai)
                
                if mouse_clicked and hover_mulai:
                    state = 'menu'
            
            info = font_s.render("Ketik nama lalu tekan Enter atau klik Mulai", True, WHITE)
            screen.blit(info, (WIDTH//2 - info.get_width()//2, 650))
        
        # ===== LAYAR MENU UTAMA =====
        elif state == 'menu':
            gradient(screen, PURPLE, PINK)
            
            header = pygame.Rect(100, 50, WIDTH - 200, 100)
            rounded_rect(screen, WHITE, header, 25)
            
            sapa = font_l.render(f"Halo, {player['nama']}! 👋", True, PURPLE)
            screen.blit(sapa, (WIDTH//2 - sapa.get_width()//2, 70))
            
            stat = font_s.render(f"XP: {player['xp']} | Benar: {player['benar']}", True, GRAY)
            screen.blit(stat, (WIDTH//2 - stat.get_width()//2, 110))
            
            judul = font_m.render("Pilih Tingkat Kesulitan:", True, WHITE)
            screen.blit(judul, (WIDTH//2 - judul.get_width()//2, 210))
            
            btn_mudah = pygame.Rect(WIDTH//2 - 500, 280, 300, 70)
            hover_mudah = btn_mudah.collidepoint(mouse_pos)
            draw_button(screen, btn_mudah, GREEN, "Mudah 😊", font_l, hover_mudah)
            
            info_mudah = font_xs.render("~30% huruf hilang", True, WHITE)
            screen.blit(info_mudah, (btn_mudah.centerx - info_mudah.get_width()//2, 360))
            
            btn_sedang = pygame.Rect(WIDTH//2 - 150, 280, 300, 70)
            hover_sedang = btn_sedang.collidepoint(mouse_pos)
            draw_button(screen, btn_sedang, ORANGE, "Sedang 🤔", font_l, hover_sedang)
            
            info_sedang = font_xs.render("~45% huruf hilang", True, WHITE)
            screen.blit(info_sedang, (btn_sedang.centerx - info_sedang.get_width()//2, 360))
            
            btn_sulit = pygame.Rect(WIDTH//2 + 200, 280, 300, 70)
            hover_sulit = btn_sulit.collidepoint(mouse_pos)
            draw_button(screen, btn_sulit, RED, "Sulit 🏆", font_l, hover_sulit)
            
            info_sulit = font_xs.render("~60% huruf hilang", True, WHITE)
            screen.blit(info_sulit, (btn_sulit.centerx - info_sulit.get_width()//2, 360))
            
            if mouse_clicked:
                if hover_mudah:
                    mode = 'mudah'
                    kata_sekarang, petunjuk = random.choice(KATA['mudah'])
                    posisi_kosong = buat_soal(kata_sekarang, mode)
                    input_user = ""
                    pesan = ""
                    tampil_hasil = False
                    state = 'game'
                elif hover_sedang:
                    mode = 'sedang'
                    kata_sekarang, petunjuk = random.choice(KATA['sedang'])
                    posisi_kosong = buat_soal(kata_sekarang, mode)
                    input_user = ""
                    pesan = ""
                    tampil_hasil = False
                    state = 'game'
                elif hover_sulit:
                    mode = 'sulit'
                    kata_sekarang, petunjuk = random.choice(KATA['sulit'])
                    posisi_kosong = buat_soal(kata_sekarang, mode)
                    input_user = ""
                    pesan = ""
                    tampil_hasil = False
                    state = 'game'
            
            info_box = pygame.Rect(150, 430, WIDTH - 300, 200)
            rounded_rect(screen, WHITE, info_box, 20)
            
            info_judul = font_m.render("Cara Bermain:", True, PURPLE)
            screen.blit(info_judul, (180, 460))
            
            cara1 = font_s.render("1. Lihat petunjuk dan kata", True, BLACK)
            cara2 = font_s.render("2. Isi huruf yang kosong (_)", True, BLACK)
            cara3 = font_s.render("3. Tekan Enter atau tombol Cek", True, BLACK)
            
            screen.blit(cara1, (200, 500))
            screen.blit(cara2, (200, 540))
            screen.blit(cara3, (200, 580))
        
        # ===== LAYAR GAME =====
        elif state == 'game':
            if tampil_hasil:
                if hasil_benar:
                    gradient(screen, GREEN, CYAN)
                else:
                    gradient(screen, ORANGE, YELLOW)
                
                # Pesan dengan emoji
                pesan_surf = font_xl.render(pesan_hasil, True, WHITE)
                screen.blit(pesan_surf, (WIDTH//2 - pesan_surf.get_width()//2, 200))
                
                label = font_m.render("Kata yang benar:", True, WHITE)
                screen.blit(label, (WIDTH//2 - label.get_width()//2, 320))
                
                kata_surf = font_l.render(kata_sekarang, True, WHITE)
                kata_box = pygame.Rect(WIDTH//2 - kata_surf.get_width()//2 - 30, 385, 
                                      kata_surf.get_width() + 60, 70)
                rounded_rect(screen, PURPLE, kata_box, 15)
                screen.blit(kata_surf, (WIDTH//2 - kata_surf.get_width()//2, 400))
                
                if hasil_benar:
                    xp_txt = font_l.render(f"+{xp_dapat} XP ⭐", True, YELLOW)
                    screen.blit(xp_txt, (WIDTH//2 - xp_txt.get_width()//2, 500))
                
                lanjut_btn = pygame.Rect(WIDTH//2 - 250, 620, 220, 70)
                hover_lanjut = lanjut_btn.collidepoint(mouse_pos)
                draw_button(screen, lanjut_btn, GREEN, "Lanjut", font_l, hover_lanjut)
                
                kembali_btn = pygame.Rect(WIDTH//2 + 30, 620, 220, 70)
                hover_kembali = kembali_btn.collidepoint(mouse_pos)
                draw_button(screen, kembali_btn, DARK_GRAY, "Menu", font_l, hover_kembali)
                
                if mouse_clicked:
                    if hover_lanjut:
                        kata_sekarang, petunjuk = random.choice(KATA[mode])
                        posisi_kosong = buat_soal(kata_sekarang, mode)
                        input_user = ""
                        pesan = ""
                        tampil_hasil = False
                        pygame.time.wait(200)
                    elif hover_kembali:
                        state = 'menu'
            
            else:
                gradient(screen, CYAN, BLUE)
                
                header = pygame.Rect(50, 30, WIDTH - 100, 80)
                rounded_rect(screen, WHITE, header, 20)
                
                back_btn = pygame.Rect(70, 45, 120, 50)
                hover_back = back_btn.collidepoint(mouse_pos)
                draw_button(screen, back_btn, DARK_GRAY if hover_back else GRAY, "Menu", font_s, False)
                
                if mouse_clicked and hover_back:
                    state = 'menu'
                
                mode_colors = {'mudah': GREEN, 'sedang': ORANGE, 'sulit': RED}
                mode_names = {'mudah': 'Mudah 😊', 'sedang': 'Sedang 🤔', 'sulit': 'Sulit 🏆'}
                
                mode_txt = font_m.render(f"Mode: {mode_names[mode]}", True, mode_colors[mode])
                screen.blit(mode_txt, (WIDTH//2 - mode_txt.get_width()//2, 55))
                
                xp_txt = font_m.render(f"XP: {player['xp']} ⭐", True, YELLOW)
                screen.blit(xp_txt, (WIDTH - 200, 55))
                
                petunjuk_box = pygame.Rect(150, 140, WIDTH - 300, 100)
                rounded_rect(screen, YELLOW, petunjuk_box, 20)
                pygame.draw.rect(screen, ORANGE, petunjuk_box, 4, border_radius=20)
                
                petunjuk_txt = font_m.render(petunjuk, True, BLACK)
                screen.blit(petunjuk_txt, (WIDTH//2 - petunjuk_txt.get_width()//2, 175))
                
                box_w = 70
                box_h = 80
                spacing = 10
                total_w = len(kata_sekarang) * (box_w + spacing) - spacing
                start_x = WIDTH//2 - total_w//2
                start_y = 300
                
                input_idx = 0
                for i, huruf in enumerate(kata_sekarang):
                    x = start_x + i * (box_w + spacing)
                    box = pygame.Rect(x, start_y, box_w, box_h)
                    
                    if i in posisi_kosong:
                        if input_idx < len(input_user):
                            if input_user[input_idx] == huruf:
                                rounded_rect(screen, GREEN, box, 12)
                            else:
                                rounded_rect(screen, RED, box, 12)
                            huruf_tampil = input_user[input_idx]
                        else:
                            rounded_rect(screen, YELLOW, box, 12)
                            huruf_tampil = '_'
                        input_idx += 1
                    else:
                        rounded_rect(screen, WHITE, box, 12)
                        huruf_tampil = huruf
                    
                    pygame.draw.rect(screen, BLACK, box, 3, border_radius=12)
                    
                    huruf_surf = font_l.render(huruf_tampil, True, BLACK)
                    screen.blit(huruf_surf, (box.centerx - huruf_surf.get_width()//2, 
                                            box.centery - huruf_surf.get_height()//2))
                
                input_box = pygame.Rect(WIDTH//2 - 200, 440, 400, 60)
                rounded_rect(screen, WHITE, input_box, 15)
                pygame.draw.rect(screen, BLUE, input_box, 3, border_radius=15)
                
                label = font_s.render("Huruf yang hilang:", True, BLACK)
                screen.blit(label, (WIDTH//2 - label.get_width()//2, 405))
                
                input_txt = font_l.render(input_user, True, BLACK)
                screen.blit(input_txt, (input_box.centerx - input_txt.get_width()//2, 
                                       input_box.centery - input_txt.get_height()//2))
                
                if pesan:
                    pesan_surf = font_l.render(pesan, True, warna_pesan)
                    screen.blit(pesan_surf, (WIDTH//2 - pesan_surf.get_width()//2, 540))
                
                btn_cek = pygame.Rect(WIDTH//2 - 230, 640, 200, 60)
                hover_cek = btn_cek.collidepoint(mouse_pos)
                draw_button(screen, btn_cek, GREEN, "Cek", font_m, hover_cek)
                
                btn_lewat = pygame.Rect(WIDTH//2 + 30, 640, 200, 60)
                hover_lewat = btn_lewat.collidepoint(mouse_pos)
                draw_button(screen, btn_lewat, GRAY, "Lewati", font_m, hover_lewat)
                
                if (cek_tekan or (mouse_clicked and hover_cek)) and len(input_user) == len(posisi_kosong):
                    cek_tekan = False
                    benar = all(input_user[i] == kata_sekarang[posisi_kosong[i]] 
                               for i in range(len(posisi_kosong)))
                    
                    if benar:
                        hasil_benar = True
                        xp_dapat = 10 * len(posisi_kosong)
                        player['xp'] += xp_dapat
                        player['benar'] += 1
                        pesan_hasil = random.choice(PUJIAN)
                    else:
                        hasil_benar = False
                        xp_dapat = 0
                        pesan_hasil = random.choice(SEMANGAT)
                    
                    tampil_hasil = True
                
                elif (cek_tekan or (mouse_clicked and hover_cek)):
                    pesan = "Isi semua huruf dulu ya! 😊"
                    warna_pesan = ORANGE
                    cek_tekan = False
                
                if mouse_clicked and hover_lewat:
                    hasil_benar = False
                    xp_dapat = 0
                    pesan_hasil = random.choice(SEMANGAT)
                    tampil_hasil = True
                
                esc_info = font_xs.render("Tekan ESC untuk kembali ke menu", True, WHITE)
                screen.blit(esc_info, (WIDTH//2 - esc_info.get_width()//2, 730))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()