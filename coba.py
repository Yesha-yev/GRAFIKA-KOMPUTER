import pygame
import sys
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("KataKu - Belajar Kata dengan Seru!")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 100)
ORANGE = (255, 160, 60)
COLORS = [
    (100, 180, 255), (100, 220, 120), (255, 220, 150),
    (255, 160, 80), (255, 120, 120), (200, 150, 255),
    (255, 180, 200), (150, 230, 255)
]

def get_font(size):
    font_list = [
        "Segoe UI Emoji",          
        "Segoe UI Symbol",
        "Noto Color Emoji",           
        "Apple Color Emoji",       
        "JoyPixels",               
        None                       
    ]
    for name in font_list:
        try:
            return pygame.font.SysFont(name, size, bold=True)
        except:
            continue
    return pygame.font.Font(None, size)

font_xl = get_font(90)
font_lg = get_font(50)
font_md = get_font(30)
font_sm = get_font(30)
font_xs = get_font(24)

KATA = {
    'mudah': [('BOLA', '⚽'), ('KUCING', '🐱'), ('APEL', '🍎'), ('BUKU', '📚'), ('MEJA', '🪑')],
    'sedang': [('RUMAH', '🏠'), ('AYAM', '🐔'), ('MOBIL', '🚗'), ('PISANG', '🍌'), ('BURUNG', '🐦')],
    'sulit': [('KELINCI', '🐰'), ('SEPEDA', '🚲'), ('JERAPAH', '🦒'), ('PESAWAT', '✈️'), ('KANGURU', '🦘')]
}

PUJIAN = ["Hebat Sekali! 🌟", "Luar Biasa! ✨", "Pintar Banget! 🧠", "Keren! 🔥", "Jago! 🏆"]
SEMANGAT = ["Ayo Coba Lagi! 💪", "Pasti Bisa! 🌈", "Jangan Menyerah! ⚡", "Semangat Ya! 😊"]
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-8, -3)
        self.color = random.choice(COLORS)
        self.life = 60
        self.size = random.randint(4, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1
        self.size = max(1, self.size - 0.1)

    def draw(self, surf):
        if self.life > 0:
            alpha = int(255 * (self.life / 60))
            s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (self.size, self.size), self.size)
            surf.blit(s, (self.x - self.size, self.y - self.size))

particles = []

def draw_glow_text(surf, text, font, color, pos, glow_color=(255,255,200)):
    x, y = pos
    for dx in [-3,0,3]:
        for dy in [-3,0,3]:
            if dx != 0 or dy != 0:
                glow = font.render(text, True, glow_color)
                surf.blit(glow, (x+dx, y+dy))
    main = font.render(text, True, color)
    surf.blit(main, (x, y))

def draw_radial_gradient(surf, center, radius, color_inner, color_outer):
    for r in range(radius, 0, -4):
        alpha = int(255 * (1 - r / radius))
        color = (*color_inner, max(20, alpha//4))
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, color, (r, r), r)
        surf.blit(s, (center[0]-r, center[1]-r))

def draw_star(surf, cx, cy, spikes, outer, inner, color, rotation=0):
    points = []
    rot = math.radians(rotation)
    for i in range(spikes * 2):
        angle = i * math.pi / spikes + rot
        r = outer if i % 2 == 0 else inner
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        points.append((x, y))
    pygame.draw.polygon(surf, color, points)

class AnimatedButton:
    def __init__(self, rect, text, color, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.font = font
        self.scale = 1.0
        self.target_scale = 1.0
        self.hover = False

    def update(self, mouse_pos, clicked):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.target_scale = 1.15 if self.hover else 1.0
        self.scale += (self.target_scale - self.scale) * 0.2

        if self.hover and clicked:
            for _ in range(15):
                particles.append(Particle(self.rect.centerx, self.rect.centery))
            return True
        return False

    def draw(self, surf):
        scaled_w = int(self.rect.w * self.scale)
        scaled_h = int(self.rect.h * self.scale)
        scaled_rect = pygame.Rect(
            self.rect.centerx - scaled_w // 2,
            self.rect.centery - scaled_h // 2,
            scaled_w, scaled_h
        )

        shadow = scaled_rect.move(6, 6)
        pygame.draw.rect(surf, (0, 0, 0), shadow, border_radius=25)

        base_color = tuple(min(255, c + 40) for c in self.color) if self.hover else self.color
        pygame.draw.rect(surf, base_color, scaled_rect, border_radius=25)

        pygame.draw.rect(surf, WHITE, scaled_rect, 5, border_radius=25)

        txt_surf = self.font.render(self.text, True, WHITE)
        surf.blit(txt_surf, (scaled_rect.centerx - txt_surf.get_width() // 2,
                             scaled_rect.centery - txt_surf.get_height() // 2))

player = {'nama': '', 'xp': 0, 'benar': 0}
state = 'nama'
mode = None
kata_sekarang = None
petunjuk = None
posisi_kosong = []
input_user = ""
pesan = ""
tampil_hasil = False
hasil_benar = False
angle = 0 

buttons = {}
def teks_tengah(surface, text, font, color, y, glow=False):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    rect.centerx = WIDTH // 2  
    rect.y = y
    
    if glow:
        draw_glow_text(surface, text, font, color, (rect.x - 4, rect.y - 4))
    else:
        surface.blit(rendered, rect)
def buat_soal(kata, mode):
    panjang = len(kata)
    if mode == 'mudah':
        persen = 0.3
    elif mode == 'sedang':
        persen = 0.5
    else:
        persen = 0.7
    n = max(1, int(panjang * persen))
    n = min(n, panjang - 1)
    available = list(range(1, panjang))
    return sorted(random.sample(available, n))

def main():
    global state, mode, kata_sekarang, petunjuk, posisi_kosong, input_user
    global tampil_hasil, hasil_benar, angle, pesan_hasil

    running = True
    mouse_clicked = False
    last_click = 0
    last_enter_press = 0 

    while running:
        dt = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        enter_pressed = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.time.get_ticks() - last_click > 200:
                    mouse_clicked = True
                    last_click = pygame.time.get_ticks()

            if state == 'nama':
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        player['nama'] = player['nama'][:-1]
                    elif e.key == pygame.K_RETURN and player['nama']:
                        state = 'menu'
                    elif e.unicode.isalpha() and len(player['nama']) < 12:
                        player['nama'] += e.unicode.upper()

            elif state == 'game' and not tampil_hasil:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        input_user = input_user[:-1]
                    elif e.key == pygame.K_RETURN and len(input_user) == len(posisi_kosong):
                        if pygame.time.get_ticks() - last_enter_press > 500:
                            enter_pressed = True
                            last_enter_press = pygame.time.get_ticks()
                    elif e.key == pygame.K_ESCAPE:
                        state = 'menu'
                        input_user = ""
                        tampil_hasil = False
                    elif e.unicode.isalpha() and len(input_user) < len(posisi_kosong):
                        input_user += e.unicode.upper()

        for p in particles[:]:
            p.update()
            if p.life <= 0:
                particles.remove(p)

        screen.fill((20, 20, 40))

        angle += 0.5

        draw_radial_gradient(screen, (WIDTH//2, HEIGHT//2), 500, (120,80,255), (20,20,60))
        for i in range(12):
            r = 300 + 80 * math.sin(angle*0.02 + i)
            ang = math.radians(i*30 + angle)
            x = WIDTH//2 + math.cos(ang) * r
            y = HEIGHT//2 + math.sin(ang) * r
            draw_star(screen, x, y, 5, 30, 12, (*COLORS[i%len(COLORS)], 100), angle*2)

        if state == 'nama':
            draw_glow_text(screen, "KataKu", font_xl, (255,220,100), (WIDTH//2-200, 150))
            screen.blit(font_lg.render("Belajar Kata Seru!", True, WHITE), (WIDTH//2-240, 250))

            txt = font_md.render("Masukkan Namamu:", True, WHITE)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 380))

            box = pygame.Rect(WIDTH//2 - 250, 450, 500, 80)
            pygame.draw.rect(screen, (255,255,255,50), box, border_radius=30)
            pygame.draw.rect(screen, (100,200,255), box, 5, border_radius=30)
            name_surf = font_lg.render(player['nama'] + ("|" if int(time.time()*2)%2 == 0 else ""), True, BLACK)
            screen.blit(name_surf, (box.centerx - name_surf.get_width()//2, box.centery - name_surf.get_height()//2))

            if len(player['nama']) > 0:
                btn = AnimatedButton((WIDTH//2-150, 600, 300, 80), "Mulai Petualangan!", (80,200,120), font_md)
                if btn.update(mouse_pos, mouse_clicked):
                    state = 'menu'
                btn.draw(screen)

        elif state == 'menu':
            draw_glow_text(screen, f"Halo {player['nama']}!", font_xl, YELLOW, (WIDTH//2-150, 100))

            xp_text = font_md.render(f"XP: {player['xp']}  |  Benar: {player['benar']}", True, (210,255,100))
            screen.blit(xp_text, (WIDTH//2 - xp_text.get_width()//2, 200))

            if not buttons:
                buttons['mudah']  = AnimatedButton((WIDTH//2-400, 320, 250, 100), "MUDAH", (80,220,140), font_lg)
                buttons['sedang'] = AnimatedButton((WIDTH//2-125, 320, 250, 100), "SEDANG", (255,160,60), font_lg)
                buttons['sulit']  = AnimatedButton((WIDTH//2+150, 320, 250, 100), "SULIT", (220,60,100), font_lg)

            for key, btn in buttons.items():
                btn.update(mouse_pos, mouse_clicked)
                btn.draw(screen)

                if mouse_clicked and btn.hover:
                    mode = key
                    kata_sekarang, petunjuk = random.choice(KATA[mode])
                    posisi_kosong = buat_soal(kata_sekarang, mode)
                    input_user = ""
                    tampil_hasil = False
                    state = 'game'
                    buttons.clear() 
                    break

        elif state == 'game':
            header = pygame.Rect(50, 30, WIDTH-100, 90)
            pygame.draw.rect(screen, (255,255,255,80), header, border_radius=30)
            screen.blit(font_md.render(f"Mode: {mode.title()}", True, (100,100,100)), (300, 60))
            screen.blit(font_md.render(f"XP: {player['xp']}", True, YELLOW), (WIDTH-250, 60))

            emotk = font_xl.render(petunjuk, True, WHITE)
            emotb = pygame.transform.smoothscale(emotk, (250, 200)) 
            screen.blit(emotb, (WIDTH//2 - 125,HEIGHT//2-250))

            box_w, box_h = 80, 100
            spacing = 15
            total_w = len(kata_sekarang) * (box_w + spacing) - spacing
            start_x = WIDTH//2 - total_w // 2
            start_y = 380

            idx = 0
            for i, huruf in enumerate(kata_sekarang):
                x = start_x + i * (box_w + spacing)
                rect = pygame.Rect(x, start_y, box_w, box_h)

                if i in posisi_kosong and idx < len(input_user) and input_user[idx] == huruf:
                    draw_radial_gradient(screen, rect.center, 60, (100,255,100), (0,100,0))

                color = YELLOW if i in posisi_kosong and idx >= len(input_user) else WHITE
                if i in posisi_kosong and idx < len(input_user):
                    color = (100,255,100) if input_user[idx] == huruf else (255,100,100)

                shadow = rect.move(8,8)
                pygame.draw.rect(screen, (0,0,0,100), shadow, border_radius=20)
                pygame.draw.rect(screen, color, rect, border_radius=20)
                pygame.draw.rect(screen, (50,50,50), rect, 5, border_radius=20)

                tampil = input_user[idx] if i in posisi_kosong and idx < len(input_user) else ('_' if i in posisi_kosong else huruf)
                txt = font_lg.render(tampil, True, BLACK)
                screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))

                if i in posisi_kosong:
                    idx += 1

            input_rect = pygame.Rect(WIDTH//2 - 300, 550, 600, 80)
            pygame.draw.rect(screen, (255,255,255,50), input_rect, border_radius=25)
            pygame.draw.rect(screen, (100,180,255), input_rect, 6, border_radius=25)
            cursor = "|" if int(time.time()*2) % 2 == 0 else ""
            input_surf = font_lg.render(input_user + cursor, True, BLACK)
            screen.blit(input_surf, (input_rect.centerx - input_surf.get_width()//2, input_rect.centery - input_surf.get_height()//2))

            btn_kembali = AnimatedButton((60, 40, 180, 70), "KEMBALI", (100,100,150), font_md)
            btn_lewat   = AnimatedButton((WIDTH//2 - 420, 680, 380, 90), "LEWATI SOAL", (200,80,80), font_md)
            btn_cek     = AnimatedButton((WIDTH//2 + 40, 680, 380, 90), "CEK JAWABAN", (80,200,100), font_md)

            kembali_ditekan = btn_kembali.update(mouse_pos, mouse_clicked)
            lewat_ditekan   = btn_lewat.update(mouse_pos, mouse_clicked)
            cek_ditekan     = btn_cek.update(mouse_pos, mouse_clicked)

            if kembali_ditekan:
                state = 'menu'
                input_user = ""
                tampil_hasil = False

            if lewat_ditekan:
                hasil_benar = False
                tampil_hasil = True
                pesan_hasil = random.choice(SEMANGAT)
                for _ in range(20):
                    particles.append(Particle(WIDTH//2, 400))

            if cek_ditekan or enter_pressed:
                if len(input_user) == 0:
                    hasil_benar = False
                    tampil_hasil = True
                    pesan_hasil = random.choice(["Ayo isi dulu ya!", "Masih kosong nih!", "Coba tebak dulu dong!", "Yuk isi hurufnya!"])
                    for _ in range(25):
                        particles.append(Particle(WIDTH//2, 400))
                elif len(input_user) == len(posisi_kosong):
                    cek_jawaban()
                else:
                    hasil_benar = False
                    tampil_hasil = True
                    pesan_hasil = random.choice(["Belum lengkap nih!", "Isi semua huruf dulu ya!", "Masih kurang!", "Ayo lengkapi!"])
                    for _ in range(20):
                        particles.append(Particle(WIDTH//2, 400))

            if tampil_hasil:
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))  
                screen.blit(overlay, (0, 0))

                pesan_hasil = pesan_hasil or "Ayo Coba Lagi!"

                warna = (100, 255, 100) if hasil_benar else (255, 180, 80)
                teks_tengah(screen, pesan_hasil, font_xl, warna, 180, glow=True)

                teks_tengah(screen, f"Kata yang benar: {kata_sekarang}", font_lg, WHITE, 320)

                if hasil_benar:
                    xp_gain = 10 * len(posisi_kosong)
                    teks_tengah(screen, f"+{xp_gain} XP!", font_lg, YELLOW, 400)
                    
                    for _ in range(40):
                        particles.append(Particle(
                            WIDTH//2 + random.randint(-150, 150),
                            400 + random.randint(-50, 50)
                        ))

                btn_lanjut = AnimatedButton((WIDTH//2 - 200, 520, 400, 90), "LANJUT SOAL", (80,200,120), font_lg)
                if btn_lanjut.update(mouse_pos, mouse_clicked):
                    kata_sekarang, petunjuk = random.choice(KATA[mode])
                    posisi_kosong = buat_soal(kata_sekarang, mode)
                    input_user = ""
                    tampil_hasil = False
                    pesan_hasil = ""
                btn_lanjut.draw(screen)

            btn_kembali.draw(screen)
            btn_lewat.draw(screen)
            btn_cek.draw(screen)

        for p in particles:
            p.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def cek_jawaban():
    global tampil_hasil, hasil_benar, player, pesan_hasil
    if tampil_hasil:  
        return
    benar = all(input_user[i] == kata_sekarang[posisi_kosong[i]] for i in range(len(posisi_kosong)))
    tampil_hasil = True
    hasil_benar = benar
    if benar:
        xp_gain = 10 * len(posisi_kosong)
        player['xp'] += xp_gain
        player['benar'] += 1
        pesan_hasil = random.choice(PUJIAN)
        for _ in range(30):
            particles.append(Particle(WIDTH//2, HEIGHT//2))
    else:
        pesan_hasil = random.choice(SEMANGAT)

if __name__ == "__main__":
    main()