import pygame
import sys
from random import randint
# from pyvidplayer import Video
import math

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
WIDTH, HEIGHT = 1470, 900
pi = 3.14
diff, musst, suit, cut_scene = '', -1, 'cs', 0
SCREEN = pygame.display.set_mode((1470, 920))
pygame.display.set_caption("Spoody-Mun")
infoObject = pygame.display.Info()
# display_w, display_h = pygame.display.Info().current_w, pygame.display.Info().current_h
display_w, display_h = WIDTH, HEIGHT
kx, ky = 1, 1
cut_scene = 0


def load_image_safe(path, default_image="white_cube.png", convert_alpha=True):
    # Безопасно загружает изображение. Если файл не найден, использует изображение-заглушку.

    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
        return image
    except (pygame.error, FileNotFoundError):
        print(f"Warning: File {path} not found, using default: {default_image}")
        try:
            # Пытаемся загрузить заглушку из той же директории
            import os
            dir_path = os.path.dirname(path)
            default_path = os.path.join(dir_path, default_image)
            if convert_alpha:
                return pygame.image.load(default_path).convert_alpha()
            else:
                return pygame.image.load(default_path).convert()
        except:
            # Если даже заглушка не найдена, создаем простой цветной квадрат
            print(f"Emergency: Creating colored square for {path}")
            surf = pygame.Surface((50, 50))
            surf.fill((255, 0, 255))  # Яркий цвет для заметности
            return surf


def main_menu():
    st = 5
    global cut_scene
    global im
    global diff
    global musst
    global suit
    global subst
    expectation = randint(500, 600)
    # randint(1500, 2600)

    vp = 0
    d_arc = 0.0
    time = 0
    subst = 'OFF'#

    pygame.mixer.music.load("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Music/Web Launch.mp3")
    # pygame.mixer.music.play()#
    while True:
        if st == 0:
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                    "/Fonts/GULAG.otf", 120 * kx)
            text = font.render('Spider-Man', True, pygame.Color('WHITE'))
            tx, ty = display_w // 2 - len('Spider-Man  ') * 120 * kx // 4, display_h // 4 - 60 * ky - 90
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/Home_screen.png")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h + 20))
            SCREEN.blit(intro_image, (0, 0))
            SCREEN.blit(text, (tx, ty))
            pygame.display.update()
            pygame.time.wait(5000)
            # pygame.time.wait(500)
            st = 1
            text = font.render('START', True, pygame.Color('RED'))
            text.set_alpha(50)
            tx, ty = display_w // 2 - len('START') * 120 * kx // 4, display_h // 4 - 60 * ky - 20
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/newgamescreen.jpg")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            SCREEN.blit(text, (tx, ty))
            pygame.display.update()
        if st == 1:
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/newgamescreen.jpg")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                    "/Fonts/GULAG.otf", 120 * kx)
            text = font.render('START', True, pygame.Color('RED'))
            tx, ty = display_w // 2 - len('START') * 120 * kx // 4, display_h // 4 - 120 * ky // 2 - 20
            for event1 in pygame.event.get():
                if event1.type == pygame.MOUSEMOTION:
                    if tx < event1.pos[0] < display_w // 2 + len('START') * 120 * kx // 4 \
                            and ty < event1.pos[1] < display_h // 4 + 120 * ky // 2 + 20:
                        text.set_alpha(255)
                    else:
                        text.set_alpha(50)
                    SCREEN.blit(text, (tx, ty))
                    pygame.display.update()
                else:
                    text.set_alpha(50)
                    SCREEN.blit(text, (tx, ty))
                    pygame.display.update()
                if event1.type == pygame.MOUSEBUTTONDOWN \
                        and tx < event1.pos[0] < display_w // 2 + len('START') * 120 * kx // 4 \
                        and ty < event1.pos[1] < display_h // 4 + 120 * ky // 2 + 20:
                    st = 2
                    im = 0
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        if st == 2:
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/BS_menu.png")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            save_slots = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                         "/Pictures/BS Menu/save_slots.png")
            save_slots = pygame.transform.scale(save_slots, (480, 810))
            SCREEN.blit(save_slots, (140, 50))
            pygame.draw.line(SCREEN, (255, 255, 255), (169 * kx, 168 * ky + 91 * im * ky),
                             (172 * kx, 168 * ky + 91 * im * ky), 1)
            pygame.draw.circle(SCREEN, (255, 255, 255), (184 * kx, 168 + 91 * im), 8, 2)
            pygame.draw.circle(SCREEN, (255, 255, 255), (184 * kx, 168 + 91 * im), 4, 2)
            s = pygame.Surface((400, 85))
            s.fill((21, 57, 92))
            s.set_alpha(160)
            SCREEN.blit(s, (196, 125 * ky + 91 * im * ky))
            pygame.draw.line(SCREEN, (255, 255, 255), (196 * kx, 125 * ky + 91 * im * ky),
                             (196 * kx, 145 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (195 * kx, 124 * ky + 91 * im * ky),
                             (216 * kx, 124 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (196 * kx, 189 * ky + 91 * im * ky),
                             (196 * kx, 209 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (195 * kx, 210 * ky + 91 * im * ky),
                             (216 * kx, 210 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (594 * kx, 125 * ky + 91 * im * ky),
                             (594 * kx, 145 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (575 * kx, 124 * ky + 91 * im * ky),
                             (595 * kx, 124 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (594 * kx, 189 * ky + 91 * im * ky),
                             (594 * kx, 209 * ky + 91 * im * ky), 3)
            pygame.draw.line(SCREEN, (255, 255, 255), (575 * kx, 210 * ky + 91 * im * ky),
                             (595 * kx, 210 * ky + 91 * im * ky), 3)
            f = open("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Saves.txt", mode="r")
            txt = f.readlines()
            for i in txt:
                if i != '':
                    pygame.draw.rect(SCREEN, (161, 3, 34), (203 * kx, 131 * ky + 91 * txt.index(i) * ky, 385, 73))
                    font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                            "Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 40 * kx)
                    text = font.render(str(txt.index(i) + 1), True, (255, 255, 255))
                    tx, ty = 220, 145
                    SCREEN.blit(text, (tx * kx, ty * ky + 91 * txt.index(i) * ky))
            f.close()
            pygame.display.update()
            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        if im > 0:
                            im -= 1
                    if event1.key == pygame.K_DOWN:
                        if im < 5:
                            im += 1
                    if event1.key == pygame.K_x:
                        st = 3
                        im = 0
                    if event1.key == pygame.K_o:
                        st = 0
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        if st == 3:
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/BS_menu.png")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            pygame.draw.rect(SCREEN, (53, 108, 161), (140 * kx, 48 * ky, 480, 341))
            pygame.draw.rect(SCREEN, (24, 80, 133), (140 * kx, 341 * ky, 480, 259))
            s = pygame.Surface((480, 263))
            s.fill((53, 108, 161))
            s.set_alpha(125)
            SCREEN.blit(s, (140, 600))
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 48 * ky),
                             (140 * kx, 150 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 160 * ky),
                             (140 * kx, 163 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 173 * ky),
                             (140 * kx, 710 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 720 * ky),
                             (140 * kx, 723 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 733 * ky),
                             (140 * kx, 861 * ky), 2)

            pygame.draw.line(SCREEN, (255, 255, 255), (620 * kx, 48 * ky),
                             (620 * kx, 150 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (620 * kx, 160 * ky),
                             (620 * kx, 163 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (620 * kx, 173 * ky),
                             (620 * kx, 710 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (620 * kx, 720 * ky),
                             (620 * kx, 723 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (620 * kx, 733 * ky),
                             (620 * kx, 861 * ky), 1)

            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                    "Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 27 * kx)
            text = font.render("SELECT DIFFICULTY", True, (255, 255, 255))
            tx, ty = 160, 65
            SCREEN.blit(text, (tx * kx, ty * ky))
            pygame.draw.line(SCREEN, (255, 255, 255), (160 * kx, 102 * ky),
                             (185 * kx, 102 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (190 * kx, 102 * ky),
                             (194 * kx, 102 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (200 * kx, 102 * ky),
                             (600 * kx, 102 * ky), 1)

            pygame.draw.line(SCREEN, (255, 255, 255), (165 * kx, 117 * ky),
                             (165 * kx, 125 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (165 * kx, 135 * ky),
                             (165 * kx, 305 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (165 * kx, 315 * ky),
                             (165 * kx, 323 * ky), 2)
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                    "Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 23 * kx)
            pygame.draw.line(SCREEN, (255, 255, 255), (171 * kx, 147 * ky + 40 * im * ky),
                             (174 * kx, 147 * ky + 40 * im * ky), 1)
            pygame.draw.circle(SCREEN, (255, 255, 255), (185, 147 + 40 * im), 8, 2)
            pygame.draw.circle(SCREEN, (255, 255, 255), (185 * kx, 147 + 40 * im), 4, 2)
            s = pygame.Surface((360, 32))
            s.fill((21, 57, 92))
            s.set_alpha(160)
            SCREEN.blit(s, (200, 130 * ky + 40 * im * ky))
            pygame.draw.line(SCREEN, (255, 255, 255), (200 * kx, 130 * ky + 40 * im * ky),
                             (210 * kx, 130 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (200 * kx, 130 * ky + 40 * im * ky),
                             (200 * kx, 140 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (200 * kx, 162 * ky + 40 * im * ky),
                             (210 * kx, 162 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (200 * kx, 152 * ky + 40 * im * ky),
                             (200 * kx, 162 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (550 * kx, 130 * ky + 40 * im * ky),
                             (560 * kx, 130 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (560 * kx, 130 * ky + 40 * im * ky),
                             (560 * kx, 140 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (550 * kx, 162 * ky + 40 * im * ky),
                             (560 * kx, 162 * ky + 40 * im * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (560 * kx, 152 * ky + 40 * im * ky),
                             (560 * kx, 162 * ky + 40 * im * ky), 2)
            text = font.render("FRIENDLY NEIGHBOURHOOD", True, (255, 255, 255))
            tx, ty = 210, 135
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("THE AMAZING", True, (255, 255, 255))
            tx, ty = 210, 175
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("SPECTACULAR", True, (255, 255, 255))
            tx, ty = 210, 215
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("ULTIMATE", True, (255, 255, 255))
            tx, ty = 210, 255
            SCREEN.blit(text, (tx * kx, ty * ky))
            for i in range(0, 3):
                s = pygame.Surface((250, 15))
                s.fill((35, 39, 66))
                s.set_alpha(155)
                SCREEN.blit(s, (350, 685 + 30 * i))
                pygame.draw.rect(SCREEN, (255, 255, 255), (349 * kx, 684 * ky + 30 * i, 252, 17), 2)
            if im == 0:
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                        "Marvel's Spider-Man 2D/Fonts/Old-Soviet.otf", 20 * kx)
                text = font.render("This setting is for expert players who", True, (255, 255, 255))
                tx, ty = 160, 400
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("enjoy a brutally         experience.", True, (255, 255, 255))
                tx, ty = 160, 462
                SCREEN.blit(text, (tx * kx, ty * ky))
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                        "Marvel's Spider-Man 2D/Fonts/Avengeance-E1zj.otf", 30 * kx)
                text = font.render("Fun", True, (255, 255, 255))
                tx, ty = 360, 455
                SCREEN.blit(text, (tx * kx, ty * ky))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 686 * ky, 50, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 716 * ky, 70, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 746 * ky, 60, 13))
            elif im == 1:
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                        "Marvel's Spider-Man 2D/Fonts/Old-Soviet.otf", 20 * kx)
                text = font.render("This setting is for players who want", True, (255, 255, 255))
                tx, ty = 160, 380
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("to enjoy the story without", True, (255, 255, 255))
                tx, ty = 160, 442
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("challenging combat.", True, (255, 255, 255))
                tx, ty = 160, 504
                SCREEN.blit(text, (tx * kx, ty * ky))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 686 * ky, 100, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 716 * ky, 85, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 746 * ky, 95, 13))
            elif im == 2:
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                        "Marvel's Spider-Man 2D/Fonts/Old-Soviet.otf", 20 * kx)
                text = font.render("This setting is for players who like a", True, (255, 255, 255))
                tx, ty = 160, 380
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("balanced experience with some", True, (255, 255, 255))
                tx, ty = 160, 442
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("challenge", True, (255, 255, 255))
                tx, ty = 160, 504
                SCREEN.blit(text, (tx * kx, ty * ky))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 686 * ky, 126, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 716 * ky, 126, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 746 * ky, 126, 13))
            elif im == 3:
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                        "Marvel's Spider-Man 2D/Fonts/Old-Soviet.otf", 20 * kx)
                text = font.render("This setting is for players who enjoy", True, (255, 255, 255))
                tx, ty = 160, 380
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("challenging combat. Enemies will be", True, (255, 255, 255))
                tx, ty = 160, 442
                SCREEN.blit(text, (tx * kx, ty * ky))
                text = font.render("stronger and more aggressive.", True, (255, 255, 255))
                tx, ty = 160, 504
                SCREEN.blit(text, (tx * kx, ty * ky))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 686 * ky, 170, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 716 * ky, 180, 13))
                pygame.draw.rect(SCREEN, (255, 0, 43), (351 * kx, 746 * ky, 165, 13))
            spider_logo = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/spider_logo_tr.png")
            spider_logo = pygame.transform.scale(spider_logo, (80 * kx, 80 * ky))
            SCREEN.blit(spider_logo, (340, 560))
            pygame.draw.line(SCREEN, (255, 255, 255), (155 * kx, 600 * ky),
                             (330 * kx, 600 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (430 * kx, 600 * ky),
                             (605 * kx, 600 * ky), 1)
            pygame.draw.circle(SCREEN, (255, 255, 255), (335, 600), 1, 2)
            pygame.draw.circle(SCREEN, (255, 255, 255), (425, 600), 1, 2)

            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                    "Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 23 * kx)
            text = font.render("ENEMIES", True, (255, 255, 255))
            tx, ty = 195, 640
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("AGRESSIVE", True, (255, 255, 255))
            tx, ty = 195, 680
            text.set_alpha(155)
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("DAMAGE", True, (255, 255, 255))
            tx, ty = 195, 710
            text.set_alpha(155)
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("HEALTH", True, (255, 255, 255))
            tx, ty = 195, 740
            text.set_alpha(155)
            SCREEN.blit(text, (tx * kx, ty * ky))
            pygame.display.update()
            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        if im > 0:
                            im -= 1
                    if event1.key == pygame.K_DOWN:
                        if im < 3:
                            im += 1
                    if event1.key == pygame.K_x:
                        st = 4
                        im = 0
                        subst = 'OFF'
                        if im == 0:
                            diff = 'FN'
                            # friendly neighborhood
                        elif im == 1:
                            diff = 'F'
                            # friendly
                        elif im == 1:
                            diff = 'A'
                            # amazing
                        elif im == 1:
                            diff = 'S'
                            # spectacular
                    if event1.key == pygame.K_o:
                        st = 2
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        if st == 4:
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/BS_menu.png")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            pygame.draw.rect(SCREEN, (53, 108, 161), (140 * kx, 48 * ky, 720, 500))
            s = pygame.Surface((720, 363))
            s.fill((53, 108, 161))
            s.set_alpha(125)
            SCREEN.blit(s, (140, 500))
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 48 * ky),
                             (140 * kx, 150 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 160 * ky),
                             (140 * kx, 163 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 173 * ky),
                             (140 * kx, 710 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 720 * ky),
                             (140 * kx, 723 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (140 * kx, 733 * ky),
                             (140 * kx, 861 * ky), 2)

            pygame.draw.line(SCREEN, (255, 255, 255), (860 * kx, 48 * ky),
                             (860 * kx, 150 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (860 * kx, 160 * ky),
                             (860 * kx, 163 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (860 * kx, 173 * ky),
                             (860 * kx, 710 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (860 * kx, 720 * ky),
                             (860 * kx, 723 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (860 * kx, 733 * ky),
                             (860 * kx, 861 * ky), 1)

            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                    "Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 27 * kx)
            text = font.render("BEFORE YOU START", True, (255, 255, 255))
            tx, ty = 160, 65
            SCREEN.blit(text, (tx * kx, ty * ky))
            pygame.draw.line(SCREEN, (255, 255, 255), (160 * kx, 102 * ky),
                             (220 * kx, 102 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (225 * kx, 102 * ky),
                             (230 * kx, 102 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (230 * kx, 102 * ky),
                             (820 * kx, 102 * ky), 1)

            pygame.draw.line(SCREEN, (255, 255, 255), (165 * kx, 117 * ky),
                             (165 * kx, 127 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (165 * kx, 137 * ky),
                             (165 * kx, 465 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (165 * kx, 475 * ky),
                             (165 * kx, 485 * ky), 2)
            pygame.draw.line(SCREEN, (255, 255, 255), (175 * kx, 158 * ky + 30 * im * ky),
                             (179 * kx, 158 * ky + 30 * im * ky), 1)
            spider_logo = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/spider_logo_tr.png")
            spider_logo = pygame.transform.scale(spider_logo, (80 * kx, 80 * ky))
            SCREEN.blit(spider_logo, (470, 780))
            pygame.draw.line(SCREEN, (255, 255, 255), (275 * kx, 820 * ky),
                             (465 * kx, 820 * ky), 1)
            pygame.draw.line(SCREEN, (255, 255, 255), (555 * kx, 820 * ky),
                             (745 * kx, 820 * ky), 1)
            pygame.draw.circle(SCREEN, (255, 255, 255), (475, 821), 1, 3)
            pygame.draw.circle(SCREEN, (255, 255, 255), (545, 821), 1, 3)
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                    "Marvel's Spider-Man 2D/Fonts/Old-Soviet.otf", 25 * kx)
            text = font.render('More functions in next updates!', True, pygame.Color("White"))
            SCREEN.blit(text, (160 * kx, 505 * ky))
            pygame.draw.circle(SCREEN, (255, 255, 255), (193, 159 + 30 * im), 8, 2)
            pygame.draw.circle(SCREEN, (255, 255, 255), (193 * kx, 159 + 30 * im), 4, 2)
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/"
                                    "Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 24 * kx)
            text = font.render("START", True, (255, 255, 255))
            tx, ty = 220, 145
            if im == 0:
                text.set_alpha(255)
            else:
                text.set_alpha(155)
            SCREEN.blit(text, (tx * kx, ty * ky))
            text = font.render("SUBTITLES", True, (255, 255, 255))
            tx, ty = 220, 175
            if im == 1:
                text.set_alpha(255)
            else:
                text.set_alpha(155)
            SCREEN.blit(text, (tx * kx, ty * ky))
            if subst == 'ON':
                text = font.render("< ON >", True, (255, 255, 255))
                tx, ty = 550, 175
                SCREEN.blit(text, (tx * kx, ty * ky))
            else:
                text = font.render("< OFF >", True, (255, 255, 255))
                tx, ty = 550, 175
                SCREEN.blit(text, (tx * kx, ty * ky))
            pygame.display.update()
            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        if im > 0:
                            im -= 1
                    if event1.key == pygame.K_DOWN:
                        if im < 1:
                            im += 1
                    if event1.key == pygame.K_LEFT and im == 1:
                        if subst == 'ON':
                            subst = 'OFF'
                    if event1.key == pygame.K_RIGHT and im == 1:
                        if subst == 'OFF':
                            subst = 'ON'
                    if event1.key == pygame.K_x:
                        pygame.mixer.music.pause()
                        st = 5
                    if event1.key == pygame.K_o:
                        st = 3
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        if st == 5:
            if d_arc < 2 * pi:
                d_arc += pi / 50
            else:
                d_arc = 0.0
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/"
                                          "Marvel's Spider-Man 2D/Pictures/BS Menu/black_screen.webp")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            spider_logo = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/BS Menu/spider_logo_tr.png")
            spider_logo = pygame.transform.scale(spider_logo, (70 * kx, 70 * ky))
            SCREEN.blit(spider_logo, (display_w - 100, display_h - 100))
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 100, display_h - 100, 70, 70),
                            pi + d_arc, 5 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 100, display_h - 100, 70, 70),
                            3 * pi / 2 + d_arc, 7 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 100, display_h - 100, 70, 70),
                            0 + d_arc, pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 100, display_h - 100, 70, 70),
                            pi / 2 + d_arc, 3 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 105, display_h - 105, 80, 80),
                            0 - d_arc, pi / 2 - d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 105, display_h - 105, 80, 80),
                            2 * pi / 3 - d_arc, 7 * pi / 6 - d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 105, display_h - 105, 80, 80),
                            4 * pi / 3 - d_arc, 11 * pi / 6 - d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 110, display_h - 110, 90, 90),
                            0 + d_arc, 5 * pi / 6 + d_arc)
            pygame.draw.arc(SCREEN, pygame.Color('White'),
                            (display_w - 110, display_h - 110, 90, 90),
                            pi + d_arc, 11 * pi / 6 + d_arc)
            pygame.display.update()
            pygame.time.wait(7)
            time += 100
            if time >= expectation:
                if vp == 0:
                    # intro()
                    main_game()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                quit()


# def intro():
#     global st
#     global cut_scene
#     cut_scene += 1
#     st = -100
#     vid = Video("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Cut Scenes/first_cutscene.mp4")
#     vid.set_size((display_w, display_h))
#     font = pygame.font.Font(None, 40 * kx)
#     text = font.render('Skip >>', True, pygame.Color("White"))
#     text.set_alpha(50)
#     tx, ty = display_w - 120, display_h - 40
#     while vid.active:
#         vid.draw(SCREEN, (0, 0))
#         SCREEN.blit(text, (tx, ty))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEMOTION:
#                 if tx < event.pos[0] < display_w and ty < event.pos[1] < display_h:
#                     text.set_alpha(255)
#                 else:
#                     text.set_alpha(50)
#             if event.type == pygame.MOUSEBUTTONDOWN and tx < event.pos[0] < display_w and ty < event.pos[1] < display_h:
#                 vid.close()
#                 main_game()


# def second_cut_scene():
#     global cut_scene
#     global sdvigy
#     global st
#     pygame.mixer.music.unload()
#     cut_scene += 1
#     st, sdvigy = 0, -330
#     vid = Video("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Cut Scenes/second_cutscene.mp4")
#     vid.set_size((display_w, display_h))
#     font = pygame.font.Font(None, 40 * kx)
#     text = font.render('Skip >>', True, pygame.Color("White"))
#     text.set_alpha(50)
#     tx, ty = display_w - 120, display_h - 40
#     while vid.active:
#         vid.draw(SCREEN, (0, 0))
#         SCREEN.blit(text, (tx, ty))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEMOTION:
#                 if tx < event.pos[0] < display_w and ty < event.pos[1] < display_h:
#                     text.set_alpha(255)
#                 else:
#                     text.set_alpha(50)
#             if event.type == pygame.MOUSEBUTTONDOWN and tx < event.pos[0] < display_w and ty < event.pos[1] < display_h:
#                 vid.close()
#                 main_game()


def menu():
    global im
    global diff
    global musst
    global suit
    global st
    global dif_k
    mst, choose_sst, st = 1, '', 0
    expectation = randint(1000, 2000)
    # randint(1500, 2500)
    pygame.mixer.music.load("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Music/Pause Menu.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.4)
    # 144  9 7 7 9 8 10 12 12 12 11 17 30
    red_icons_text = ['', ' MAP', 'SUITS', 'GADGETS', 'SKILLS', 'MISSIONS', 'COLLECTIONS      ', 'BENCHMARKS',
                      'CHARACTERS',
                      'MOVES LIST           ', '']
    equipments_icon = ['SUIT', 'SUIT POWER', 'SUIT MODS']
    suits = ['cs_icon.png', 'iss_icon.png', 'ws_icon.png', 'us_icon.png', 'ss_icon.png', 'as_icon.png',
             'is_icon.png', 'ios_icon.png']
    qx, qy, mdx, mdy, ix, iy = 0, 0, 0, 0, 0, 0
    red_icons_weight = [round(6.2 / 100 * display_w, 0), round(4.87 / 100 * display_w, 0),
                        round(4.86 / 100 * display_w, 0), round(6.3 / 100 * display_w, 0),
                        round(5.5 / 100 * display_w, 0), round(6.95 / 100 * display_w, 0),
                        round(8.2 / 100 * display_w, 0), round(8.3 / 100 * display_w, 0),
                        round(8.4 / 100 * display_w, 0), round(7.6 / 100 * display_w, 0),
                        round(11.8 / 100 * display_w, 0)]
    red_icons_height = round(9.75 / 100 * display_h, 0) * ky
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif ev.key == pygame.K_TAB:
                    pygame.mixer.music.unload()
                    main_game()
            if ev.type == pygame.MOUSEBUTTONDOWN and mst == 1:
                mdx, mdy = ev.pos[0], ev.pos[1]
                if ev.button == 1 and 62 < mdx < 220 and 142 < mdy < 239:
                    mst = 1.1
            if ev.type == pygame.MOUSEBUTTONDOWN and mst == 1.1:
                mdx, mdy = ev.pos[0], ev.pos[1]
                for i in suits:
                    ix, iy = 295 + 132 * (suits.index(i) % 4), 208 + (suits.index(i) // 4) * 85
                    if ev.button == 1 and ix + 1 < mdx < ix + 109 and iy + 1 < mdy < iy + 62:
                        choose_sst = i
                if ev.button == 1 and 1349 < mdx < 1420 and 226 < mdy < 256:
                    suit = choose_sst.split('_icon.png')[0]
        if mst == 1:
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/Base Menu/IMG_4305.JPG")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 17 * kx)
            for i in red_icons_weight:
                if red_icons_weight.index(i) == mst + 1:
                    pygame.draw.rect(SCREEN, (161, 3, 34), (qx, 0, i * kx, red_icons_height))
                    pygame.draw.rect(SCREEN, (255, 255, 255), (qx, 0, i * kx, 6))
                else:
                    pygame.draw.rect(SCREEN, (255, 0, 59), (qx, 0, i * kx, red_icons_height))
                text = font.render(red_icons_text[red_icons_weight.index(i)], True, (28, 6, 46))
                tx, ty = (qx + i * kx // (len(red_icons_text[red_icons_weight.index(i)]) + 2)) * kx, \
                         (red_icons_height // 2 - 8 * ky) * ky
                SCREEN.blit(text, (tx, ty))
                qx += i
                pygame.draw.rect(SCREEN, (28, 6, 46), (qx, 0, 2, red_icons_height))
                qx += 2

            for i in equipments_icon:
                text = font.render(i, True, pygame.Color('White'))
                tx, ty = ((red_icons_weight[0] // 2) + 15) * kx, \
                         (red_icons_height + 15 * ky + 0.17 * display_h * equipments_icon.index(i)) * ky
                SCREEN.blit(text, (tx, ty))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 23 * ky, 0.02 * display_w * kx, 1))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 27 * ky, 0.11 * display_w * kx, 3))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 35 * ky, 0.11 * display_w * kx, 1))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 135 * ky, 0.11 * display_w * kx, 1))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 35 * ky, 1 * kx, 100 * ky))
                pygame.draw.rect(SCREEN, pygame.Color('White'),
                                 (tx + 0.11 * display_w * kx, ty + 35 * ky, 1 * kx, 100 * ky))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx - 5, ty + 27 * ky, 1, 30))

            tx, ty = ((red_icons_weight[0] // 2) + 16) * kx, (red_icons_height + 51) * ky
            if suit == 'cs':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/cs_icon.png")

            elif suit == 'iss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/iss_icon.png")
            elif suit == 'ws':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ws_icon.png")
            elif suit == 'us':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/us_icon.png")
            elif suit == 'ss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ss_icon.png")
            elif suit == 'as':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/as_icon.png")
            elif suit == 'is':
                ssuit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                             "/Pictures/Base Menu/Suit's Icons/is_icon.png")
            elif suit == 'ios':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ios_icon.png")
            suit_icon = pygame.transform.scale(suit_icon, (0.11 * display_w * kx - 3, 98))
            SCREEN.blit(suit_icon, (tx + 1, ty + 1))

            pygame.draw.rect(SCREEN, (29, 31, 36), (qx, 0, display_w - qx, display_h))
            pygame.draw.rect(SCREEN, (28, 6, 46), (qx - 8, 0, 3, red_icons_height))
            pygame.draw.rect(SCREEN, (255, 255, 255), (qx, red_icons_height, display_w - qx, 50))
            pygame.draw.ellipse(SCREEN, (255, 255, 255), (qx, red_icons_height, 1, display_h - red_icons_height), 1)
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 27 * kx)
            text = font.render('EQUIPPED', True, (28, 6, 46))
            tx, ty = qx + 8, red_icons_height + 10
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/cs_icon.png")
            elif suit == 'iss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/iss_icon.png")
            elif suit == 'ws':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ws_icon.png")
            elif suit == 'us':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/us_icon.png")
            elif suit == 'ss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ss_icon.png")
            elif suit == 'as':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/as_icon.png")
            elif suit == 'is':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/is_icon.png")
            elif suit == 'ios':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ios_icon.png")
            suit_icon = pygame.transform.scale(suit_icon, (110, 63))
            SCREEN.blit(suit_icon, (qx + 10, red_icons_height + 66))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceRegular.ttf", 18 * kx)
            if suit == 'cs':
                text = font.render('Classic Suit', True, (255, 255, 255))
            elif suit == 'iss':
                text = font.render('Iron Spider', True, (255, 255, 255))
            elif suit == 'ws':
                text = font.render('Webbed Suit', True, (255, 255, 255))
            elif suit == 'us':
                text = font.render('Upgraded Suit', True, (255, 255, 255))
            elif suit == 'ss':
                text = font.render('Night Monkey', True, (255, 255, 255))
            elif suit == 'as':
                text = font.render('Amazing Suit', True, (255, 255, 255))
            elif suit == 'is':
                text = font.render('Integrated Suit', True, (255, 255, 255))
            if suit == 'ios':
                text = font.render('Black and Gold', True, (255, 255, 255))
                tx, ty = qx + 125, red_icons_height + 71
                SCREEN.blit(text, (tx, ty))
                text = font.render('Suit', True, (255, 255, 255))
                tx, ty = qx + 175, red_icons_height + 90
                SCREEN.blit(text, (tx, ty))
                pygame.draw.aaline(SCREEN, (255, 255, 255), [qx + 125, ty + 23],
                                   [display_w, ty + 23])
            else:
                tx, ty = qx + 125, red_icons_height + 71
                SCREEN.blit(text, (tx, ty))
                pygame.draw.aaline(SCREEN, (255, 255, 255), [qx + 125, ty + 23],
                                   [display_w, ty + 23])

            pygame.draw.ellipse(SCREEN, (255, 255, 255), (display_w // 3.5, 590, display_w // 2.3, 200), 3)
            pygame.draw.ellipse(SCREEN, (255, 255, 255), (display_w // 3.5 + 65, 615, display_w // 2.3 - 130, 140), 1)
            pygame.draw.ellipse(SCREEN, (255, 255, 255), (display_w // 3.5 + 228, 650, display_w // 2.3 - 460, 70), 1)
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + display_w // 4.6 - 5, 591],
                               [display_w // 3.5 + 228 + (display_w // 2.3 - 460) // 2, 647])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + 230 + (display_w // 2.3 - 460) // 2, 721],
                               [display_w // 3.5 + display_w // 4.6 + 4, 787])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + display_w // 9.2 - 22, 610],
                               [display_w // 3.5 + 228 + (display_w // 2.3 - 460) // 4 - 13, 657])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + 390, 707], [display_w // 3.5 + 530, 764])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + 1, 683], [display_w // 3.5 + 228, 683])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + 407, 683],
                               [display_w // 3.5 + display_w // 2.3, 683])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + display_w // 9.2 - 30, 769],
                               [display_w // 3.5 + 228 + (display_w // 2.3 - 460) // 4 - 13, 711])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [display_w // 3.5 + 500, 610], [display_w // 3.5 + 384, 660])

            if suit == 'cs':
                suit_icon = load_image_safe('menu_cs.png')
            elif suit == 'iss':
                suit_icon = load_image_safe('menu_iss.png')
            elif suit == 'ws':
                suit_icon = load_image_safe('menu_ws.png')
            elif suit == 'us':
                suit_icon = load_image_safe('menu_us.png')
            elif suit == 'ss':
                suit_icon = load_image_safe('menu_ss.png')
            elif suit == 'as':
                suit_icon = load_image_safe('menu_as.png')
            elif suit == 'is':
                suit_icon = load_image_safe('menu_is.png')
            elif suit == 'ios':
                suit_icon = load_image_safe('menu_ios.png')
            suit_icon = pygame.transform.scale(suit_icon, (545, 370))
            SCREEN.blit(suit_icon, (display_w // 3.5 + 40, 410))
            qx, qy = 0, 0

        elif mst == 1.1:
            intro_image = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                          "/Pictures/Base Menu/IMG_4305.JPG")
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 17 * kx)
            for i in red_icons_weight:
                if red_icons_weight.index(i) == mst + 0.9:
                    pygame.draw.rect(SCREEN, (161, 3, 34), (qx, 0, i * kx, red_icons_height))
                    pygame.draw.rect(SCREEN, (255, 255, 255), (qx, 0, i * kx, 6))
                else:
                    pygame.draw.rect(SCREEN, (255, 0, 59), (qx, 0, i * kx, red_icons_height))
                text = font.render(red_icons_text[red_icons_weight.index(i)], True, (28, 6, 46))
                tx, ty = (qx + i * kx // (len(red_icons_text[red_icons_weight.index(i)]) + 2)) * kx, \
                         (red_icons_height // 2 - 8 * ky) * ky
                SCREEN.blit(text, (tx, ty))
                qx += i
                pygame.draw.rect(SCREEN, (28, 6, 46), (qx, 0, 2, red_icons_height))
                qx += 2

            for i in equipments_icon:
                text = font.render(i, True, pygame.Color('White'))
                tx, ty = ((red_icons_weight[0] // 2) + 15) * kx, \
                         (red_icons_height + 15 * ky + 0.17 * display_h * equipments_icon.index(i)) * ky
                SCREEN.blit(text, (tx, ty))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 23 * ky, 0.02 * display_w * kx, 1))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 27 * ky, 0.11 * display_w * kx, 3))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 35 * ky, 0.11 * display_w * kx, 1))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 135 * ky, 0.11 * display_w * kx, 1))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx, ty + 35 * ky, 1 * kx, 100 * ky))
                pygame.draw.rect(SCREEN, pygame.Color('White'),
                                 (tx + 0.11 * display_w * kx, ty + 35 * ky, 1 * kx, 100 * ky))
                pygame.draw.rect(SCREEN, pygame.Color('White'), (tx - 5, ty + 27 * ky, 1, 30))

            tx, ty = ((red_icons_weight[0] // 2) + 16) * kx, (red_icons_height + 51) * ky
            if suit == 'cs':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/cs_icon.png")
            elif suit == 'iss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/iss_icon.png")
            elif suit == 'ws':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ws_icon.png")
            elif suit == 'us':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/us_icon.png")
            elif suit == 'ss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ss_icon.png")
            elif suit == 'as':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/as_icon.png")
            elif suit == 'is':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/is_icon.png")
            elif suit == 'ios':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ios_icon.png")
            suit_icon = pygame.transform.scale(suit_icon, (0.11 * display_w * kx - 3, 98))
            SCREEN.blit(suit_icon, (tx + 1, ty + 1))
            pygame.draw.aalines(SCREEN, (255, 255, 255), False, [[tx + 0.11 * display_w * kx, red_icons_height + 97],
                                                                 [270, red_icons_height + 97]])
            pygame.draw.rect(SCREEN, (255, 255, 255), (243, red_icons_height + 95, 6, 6))
            pygame.draw.lines(SCREEN, (255, 255, 255), False, [[290, red_icons_height + 97],
                                                               [370, red_icons_height + 97]], 2)
            pygame.draw.lines(SCREEN, (255, 255, 255), False, [[380, red_icons_height + 97],
                                                               [810, red_icons_height + 97]])
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 22 * kx)
            text = font.render('SUIT', True, (255, 255, 255))
            SCREEN.blit(text, (290, red_icons_height + 65))
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mdx, mdy = ev.pos[0], ev.pos[1]
                    if ev.button == 1 and tx + 1 < mdx < tx + 0.11 * display_w * kx - 3 and ty + 1 < mdy < ty + 98:
                        mst = 1

            pygame.draw.rect(SCREEN, (29, 31, 36), (qx, 0, display_w - qx, display_h))
            pygame.draw.rect(SCREEN, (28, 6, 46), (qx - 8, 0, 3, red_icons_height))
            pygame.draw.rect(SCREEN, (255, 255, 255), (qx, red_icons_height, display_w - qx, 50))
            pygame.draw.ellipse(SCREEN, (255, 255, 255), (qx, red_icons_height, 1, display_h - red_icons_height), 1)
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 27 * kx)
            text = font.render('EQUIPPED', True, (28, 6, 46))
            tx, ty = qx + 8, red_icons_height + 10
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/cs_icon.png")
            elif suit == 'iss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/iss_icon.png")
            elif suit == 'ws':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ws_icon.png")
            elif suit == 'us':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/us_icon.png")
            elif suit == 'ss':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ss_icon.png")
            elif suit == 'as':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/as_icon.png")
            elif suit == 'is':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/is_icon.png")
            elif suit == 'ios':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/ios_icon.png")
            suit_icon = pygame.transform.scale(suit_icon, (110, 63))
            SCREEN.blit(suit_icon, (qx + 10, red_icons_height + 66))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceRegular.ttf", 18 * kx)
            if choose_sst == '':
                if suit == 'cs':
                    text = font.render('Classic Suit', True, (255, 255, 255))
                elif suit == 'iss':
                    text = font.render('Iron Spider', True, (255, 255, 255))
                elif suit == 'ws':
                    text = font.render('Webbed Suit', True, (255, 255, 255))
                elif suit == 'us':
                    text = font.render('Upgraded Suit', True, (255, 255, 255))
                elif suit == 'ss':
                    text = font.render('Night Monkey', True, (255, 255, 255))
                elif suit == 'as':
                    text = font.render('Amazing Suit', True, (255, 255, 255))
                elif suit == 'is':
                    text = font.render('Integrated Suit', True, (255, 255, 255))
                if suit == 'ios':
                    text = font.render('Black and Gold', True, (255, 255, 255))
                    tx, ty = qx + 125, red_icons_height + 71
                    SCREEN.blit(text, (tx, ty))
                    text = font.render('Suit', True, (255, 255, 255))
                    tx, ty = qx + 175, red_icons_height + 90
                    SCREEN.blit(text, (tx, ty))
                    pygame.draw.aaline(SCREEN, (255, 255, 255), [qx + 125, ty + 23],
                                       [display_w, ty + 23])
                else:
                    tx, ty = qx + 125, red_icons_height + 71
                    SCREEN.blit(text, (tx, ty))
                    pygame.draw.aaline(SCREEN, (255, 255, 255), [qx + 125, ty + 23],
                                       [display_w, ty + 23])

            pygame.draw.rect(SCREEN, (255, 255, 255), (270, 145, 560, 655), 1)
            pygame.draw.aalines(SCREEN, (255, 255, 255), False, [[817, 136], [838, 136], [838, 155]])
            pygame.draw.lines(SCREEN, (255, 255, 255), False, [[838, 159], [838, 179]], 3)
            pygame.draw.aalines(SCREEN, (255, 255, 255), False, [[817, 809], [838, 809], [838, 790]])
            pygame.draw.lines(SCREEN, (255, 255, 255), False, [[838, 786], [838, 766]], 3)

            for i in suits:
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/" + i)
                suit_icon = pygame.transform.scale(suit_icon, (110, 63))
                ix, iy = 295 + 132 * (suits.index(i) % 4), 208 + (suits.index(i) // 4) * 85
                SCREEN.blit(suit_icon, (ix, iy))

            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif ev.key == pygame.K_TAB:
                        pygame.mixer.music.unload()
                        main_game()
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mdx, mdy = ev.pos[0], ev.pos[1]
                    for i in suits:
                        ix, iy = 295 + 132 * (suits.index(i) % 4), 208 + (suits.index(i) // 4) * 85
                        if ev.button == 1 and ix + 1 < mdx < ix + 109 and iy + 1 < mdy < iy + 62:
                            choose_sst = i

            if choose_sst != '':
                suit_icon = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                            "/Pictures/Base Menu/Suit's Icons/" + choose_sst)
                suit_icon = pygame.transform.scale(suit_icon, (110, 63))
                SCREEN.blit(suit_icon, (qx + 10, red_icons_height + 66))
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                        "/MonospaceRegular.ttf", 18 * kx)
                if choose_sst == 'cs_icon.png':
                    text = font.render('Classic Suit', True, (255, 255, 255))
                elif choose_sst == 'iss_icon.png':
                    text = font.render('Iron Spider', True, (255, 255, 255))
                elif choose_sst == 'ws_icon.png':
                    text = font.render('Webbed Suit', True, (255, 255, 255))
                elif choose_sst == 'us_icon.png':
                    text = font.render('Upgraded Suit', True, (255, 255, 255))
                elif choose_sst == 'ss_icon.png':
                    text = font.render('Night Monkey', True, (255, 255, 255))
                elif choose_sst == 'as_icon.png':
                    text = font.render('Amazing Suit', True, (255, 255, 255))
                elif choose_sst == 'is_icon.png':
                    text = font.render('Integrated Suit', True, (255, 255, 255))
                if choose_sst == 'ios_icon.png':
                    text = font.render('Black and Gold', True, (255, 255, 255))
                    tx, ty = qx + 125, red_icons_height + 71
                    SCREEN.blit(text, (tx, ty))
                    text = font.render('Suit', True, (255, 255, 255))
                    tx, ty = qx + 175, red_icons_height + 90
                    SCREEN.blit(text, (tx, ty))
                    pygame.draw.aaline(SCREEN, (255, 255, 255), [qx + 125, ty + 23],
                                       [display_w, ty + 23])
                else:
                    tx, ty = qx + 125, red_icons_height + 71
                    SCREEN.blit(text, (tx, ty))
                    pygame.draw.aaline(SCREEN, (255, 255, 255), [qx + 125, ty + 23],
                                       [display_w, ty + 23])
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 22 * kx)
            if suit not in choose_sst:
                text = font.render('USE', True, (255, 255, 255))
                tx, ty = qx + 175, red_icons_height + 140
                SCREEN.blit(text, (tx, ty))
                pygame.draw.rect(SCREEN, (255, 255, 255), (tx - 10, ty - 5, 63, 32), 2)
                pygame.draw.aaline(SCREEN, (255, 255, 255), [tx - 175, ty + 13],
                                   [tx - 11, ty + 13])
                pygame.draw.aaline(SCREEN, (255, 255, 255), [tx + 53, ty + 13],
                                   [display_w, ty + 13])
            else:
                text = font.render('USED', True, (255, 255, 255))
                tx, ty = qx + 175, red_icons_height + 140
                SCREEN.blit(text, (tx, ty))
                pygame.draw.rect(SCREEN, (255, 255, 255), (tx - 10, ty - 5, 73, 32), 2)
                pygame.draw.aaline(SCREEN, (255, 255, 255), [tx - 175, ty + 13],
                                   [tx - 11, ty + 13])
                pygame.draw.aaline(SCREEN, (255, 255, 255), [tx + 64, ty + 13],
                                   [display_w, ty + 13])

            pygame.draw.ellipse(SCREEN, (255, 255, 255), (865, 730, 290, 85), 2)
            pygame.draw.ellipse(SCREEN, (255, 255, 255), (903, 740, 220, 55), 1)
            pygame.draw.ellipse(SCREEN, (255, 255, 255), (963, 751, 90, 30), 1)
            pygame.draw.aaline(SCREEN, (255, 255, 255), [1012, 731], [1010, 750])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [919, 741], [981, 753])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [866, 765], [962, 765])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [895, 796], [976, 776])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [1008, 780], [1006, 810])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [1035, 778], [1120, 800])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [1053, 765], [1150, 765])
            pygame.draw.aaline(SCREEN, (255, 255, 255), [1035, 754], [1105, 740])
            if suit == 'cs':
                suit_icon = load_image_safe('menu_cs_s.png')
            elif suit == 'iss':
                suit_icon = load_image_safe('menu_iss_s.png')
            elif suit == 'ws':
                suit_icon = load_image_safe('menu_ws_s.png')
            elif suit == 'us':
                suit_icon = load_image_safe('menu_us_s.png')
            elif suit == 'ss':
                suit_icon = load_image_safe('menu_ss_s.png')
            elif suit == 'as':
                suit_icon = load_image_safe('menu_as_s.png')
            elif suit == 'is':
                suit_icon = load_image_safe('menu_is_s.png')
            elif suit == 'ios':
                suit_icon = load_image_safe('menu_ios_s.png')
            suit_icon = pygame.transform.scale(suit_icon, (310, 620))
            SCREEN.blit(suit_icon, (860, 210))

            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    mdx, mdy = ev.pos[0], ev.pos[1]
                    for i in suits:
                        ix, iy = 295 + 132 * (suits.index(i) % 4), 208 + (suits.index(i) // 4) * 85
                        if ev.button == 1 and ix + 1 < mdx < ix + 109 and iy + 1 < mdy < iy + 62:
                            choose_sst = i
                    if ev.button == 1 and 1349 < mdx < 1420 and 226 < mdy < 256:
                        suit = choose_sst.split('_icon.png')[0]
                if ev.type == pygame.QUIT:
                    quit()
            qx, qy = 0, 0
        pygame.display.update()
        pygame.time.wait(40)


def main_game():
    global sdvigy
    global imh
    global imset
    global diff
    global musst
    global suit
    global st
    global cut_scene
    global subst
    cut_scene += 1
    st = -100
    bg = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/"
                         "Textures/fhomewthspandpavmnt.jpg", convert_alpha=False)
    bg = pygame.transform.scale(bg, (1414, 2000))
    road = load_image_safe("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/"
                           "Textures/дорога.jpeg", convert_alpha=False)
    road = pygame.transform.scale(road, (2011, 354))
    sdvigx = 0
    tiles = math.ceil(display_w / bg.get_width()) + 1

    if diff == 'FN':
        dif_k = 0.5
    elif diff == 'TA':
        dif_k = 1
    elif diff == 'S':
        dif_k = 1.8
    elif diff == 'U':
        dif_k = 3

    subtitles = ['Yuri Watanabe: Captain Watanabe', 'Spider-Man: Did you take him down yet?', 'Yuri Watanabe: No',
                 'Yuri Watanabe: We’re at Fisk Tower, but still waiting on the warrant',
                 'Spider-Man: Mind if I join in on the fun?',
                 'Yuri Watanabe: You know how his lawyers are… these one needs to go by the book.',
                 'Spider-Man: C’mon Yuri, I’ve been waiting eight years for this.',
                 'Yuri Watanabe: You really want to help?',
                 'Yuri Watanabe: Head to Times Square, sounds like his guys are',
                 'trying to keep my backup from reaching the scene…', 'Spider-Man: You got it - almost there!']

    time_subtitles = ['1000 4000', '4000 5200', '5200 6000', '6000 8500', '8500 11000', '11000 14000', '14000 17000',
                      '17000 18500', '18500 22000', '22000 24000', '24000 26200']

    time_wait = 0
    ticks, sp_ticks, podst, zvukst, thwipsound, dif_image, dif_image_m, hp = 0, 0, 0, 0, 0, 0, 0, 100
    colors = [(127, 127, 127), (210, 150, 75), (200, 190, 140), (200, 190, 140)]
    tx, sdvigx, sdvigy, coords_increase, SMXstart, SMYstart = 0, -500, 0, 0, 0, 0
    fight, ftticks = 0, 0
    sdvigxconst, sdvigyconst, revk, revst, f_t_colors, f_t_coords = 0, 0, 0, 0, [], []
    hcolors, hcoords, hsize, length_ofr = [], [], [], 0
    SMw, SMh = 160, 200
    SMx, SMy = display_w // 2 - 150 + 15, display_h // 2 - 200 + 7
    SMXstart, SMYstart = 0, 0
    SMRt, srt = -50, -40
    coords_increase, sdvigxconst, sdvigyconst, zvukst = 0, 0, 0, 0
    pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
    pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
    font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                            "/Fonts/MonospaceBold.ttf", 30 * kx)
    text = font.render(str(hp), True, (255, 255, 255))
    tx, ty = 460, 53
    SCREEN.blit(text, (tx, ty))
    # pygame.display.update()
    if st == -100:
        sdvigy = 1000
        subticks = 0
    #    pygame.mixer.music.load('first_dialog.mp3')
    #   pygame.mixer.music.play()
    #   pygame.mixer.music.set_volume(0.7)
    while True:
        ticks = pygame.time.get_ticks()
        if musst == -1 and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Music"
                                    "/The Golden Age.mp3")
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(0.3)
        if hp <= 0 and SMx + 27 - coords_increase > 300:
            pygame.mixer.music.unload()
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            if zvukst != 2:
                zvukst = 2
                st, musst = -101, 0
                ss = pygame.mixer.Sound("/Users/aleksej/PycharmProjects/pythonProject"
                                        "/Marvel's Spider-Man 2D/Sounds/Spider_death.mp3")
                ss.play()
                pygame.mixer.music.unload()
            if suit == 'cs':
                Spider_Man = load_image_safe('spider_pose-1_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('spider_pose-1_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('spider_pose-1_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('spider_pose-1_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('spider_pose-1_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('spider_pose-1_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('spider_pose-1_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('spider_pose-1_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 60, SMh - 55))
            SCREEN.blit(Spider_Man, (SMx + 27 - coords_increase, SMy + 140 + coords_increase // 5))
            coords_increase += 2
            # pygame.display.update()

        elif hp <= 0 and SMx + 27 - coords_increase <= 300:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                    "/Fonts/GULAG.otf", 25 * kx)
            text = font.render('!HELP!', True,
                               (255, 0, 0))
            SCREEN.blit(text, (420, 250))
            pygame.draw.line(SCREEN, (255, 0, 0), [400, 280], [1080, 280], 2)
            pygame.draw.line(SCREEN, (255, 0, 0), [400, 380], [1080, 380], 2)
            font = pygame.font.Font('MonospaceBold.ttf', 55 * kx)
            text = font.render("YOU'RE FAILED, BUDDY", True, (255, 0, 0))
            SCREEN.blit(text, (430, 300))
            # pygame.display.update()
            pygame.time.wait(8000)
            st, sdvigy, hp, musst = 0, -330, 100, -1

        elif st == 0 and sdvigy <= -330 and not pygame.key.get_pressed()[pygame.K_d] \
                and not pygame.key.get_pressed()[pygame.K_a] and (ticks - sp_ticks < 2000 or sp_ticks == 0) \
                and not pygame.key.get_pressed()[pygame.K_SPACE] and podst != 1:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while i < tiles:
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1

            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if dif_image != 0:
                dif_image = 0
            if revst == 0:
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 40.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 41.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 48.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 49.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 50.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 51.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 52.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 53.png')
            else:
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 40_rev.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 41_rev.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 48_rev.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 49_rev.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 50_rev.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 51_rev.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 52_rev.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 53_rev.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 15, SMh - 80))
            SCREEN.blit(Spider_Man, (SMx, SMy + 200))
            # pygame.display.update()
            # pygame.time.wait(40)
            time_wait = 40
            if sp_ticks == 0:
                sp_ticks = ticks
        elif st == 0 and pygame.key.get_pressed()[pygame.K_SPACE] and st != 4:
            st = 4
        elif st == 4 and coords_increase < 60:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1

            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigy += 4
            if revst == 0:
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 206.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 207.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 208.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 209.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 210.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 211.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 212.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 213.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 70, SMh - 70))
                SCREEN.blit(Spider_Man, (SMx + 40, SMy + 40))
            else:
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 206_rev.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 207_rev.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 208_rev.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 209_rev.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 210_rev.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 211_rev.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 212_rev.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 213_rev.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 70, SMh - 70))
                SCREEN.blit(Spider_Man, (SMx + 40, SMy + 40))
            coords_increase += 1
            # pygame.display.update()
            if sp_ticks != 0:
                sp_ticks = 0
            if podst != 0:
                podst = 0
        elif st == 0 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            coords_increase, sdvigxconst, sdvigyconst, zvukst = 0, 0, 0, 0
            if revst == 0:
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 143.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 144.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 145.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 146.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 147.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 148.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 149.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 150.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 10, SMh - 40))
                Spider_Man = pygame.transform.rotate(Spider_Man, 10)
            else:
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 143_rev.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 144_rev.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 145_rev.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 146_rev.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 147_rev.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 148_rev.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 149_rev.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 150_rev.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 10, SMh - 40))
            # pygame.time.wait(100)
            SMw, SMh = 160, 200
            SMRt, srt = -50, -40
            SMx, SMy = display_w // 2 - 150, display_h // 2 - 200
            thwipsound = randint(0, 3)
            if thwipsound == 0:
                ts = pygame.mixer.Sound("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Sounds/"
                                        "Thwip_sound.wav")
            elif thwipsound == 1:
                ts = pygame.mixer.Sound("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Sounds/"
                                        "Thwip_sound1.mp3")
            elif thwipsound == 2:
                ts = pygame.mixer.Sound("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Sounds/"
                                        "Thwip_sound2.mp3")
            elif thwipsound == 3:
                ts = pygame.mixer.Sound("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Sounds/"
                                        "Thwip_sound3.mp3")
            ts.play()
            if dif_image == 1 and revst == 0:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx - 25, SMy + SMh // 2 - 60),
                                 (display_w - 300, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image == 2 and revst == 0:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx + 11, SMy + SMh // 2 - 30),
                                 (display_w - 300, 0), 1)
                SCREEN.blit(Spider_Man, (SMx + 40, SMy + 50))
            elif dif_image == 1 and revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 50, SMy + SMh // 2 - 20),
                                 (300, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image == 2 or revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 47, SMy + SMh // 2 - 35),
                                 (300, 0), 1)
                SCREEN.blit(Spider_Man, (SMx + 40, SMy + 50))
            else:
                if revst == 0:
                    pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx + 11, SMy + SMh // 2 - 30),
                                     (display_w - 300, 0), 1)
                    SCREEN.blit(Spider_Man, (SMx + 40, SMy + 50))
                else:
                    pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 47, SMy + SMh // 2 - 35),
                                     (300, 0), 1)
                    SCREEN.blit(Spider_Man, (SMx + 40, SMy + 50))
            # pygame.display.update()
            SMx, SMy = SMx + 15, SMy + 7
            SMXstart, SMYstart = SMx, SMy
            SMRt, srt = -50, -40
            revk, revst = 0, 0
            # pygame.time.wait(700)
            time_wait = 550
            st = 1
            if dif_image != 0:
                dif_image = 0

        elif st == 1 and coords_increase < 220 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            coords_increase += 1
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                # if dif_image == 0:
                dif_image = 2
                if dif_image == 1:
                    sdvigx -= 2
                    if sdvigy > -330:
                        sdvigy -= 2
                    Spider_Man = load_image_safe('fly_pose1.png')
                    Spider_Man = pygame.transform.scale(Spider_Man, (SMw, SMh + 5))
                    Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
                    if coords_increase % 6 == 0:
                        SMRt += 1
                elif dif_image == 2:
                    sdvigx -= 4
                    if sdvigy > -330:
                        sdvigy -= 3
                    Spider_Man = load_image_safe('fly_pose1_cs.png')
                    Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
                    Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
                    if coords_increase % 3 == 0:
                        SMRt += 1
            else:
                sdvigx -= 4
                if sdvigy > -330:
                    sdvigy -= 3
                if suit == 'iss':
                    Spider_Man = load_image_safe('fly_pose1_iss.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('fly_pose1_ws.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('fly_pose1_us.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('fly_pose1_ss.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('fly_pose1_as.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('fly_pose1_is.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('fly_pose1_ios.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
                Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
                if coords_increase % 3 == 0:
                    SMRt += 1
            SMR_pvu = Spider_Man.get_rect()
            if dif_image == 1 and revst == 0:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx - 25, SMy + SMh // 2 - 60),
                                 (display_w - 300 - coords_increase * 3, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image != 1 and revst == 0:
                if coords_increase <= 45:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 70 + SMR_pvu.topright[0], SMy + 140 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 45 < coords_increase <= 120:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 80 + SMR_pvu.topright[0], SMy + 130 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 120 < coords_increase <= 150:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 60 + SMR_pvu.topright[0], SMy + 100 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 150 < coords_increase <= 180:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 50 + SMR_pvu.topright[0], SMy + 85 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 180 < coords_increase <= 220:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 65 + SMR_pvu.topright[0], SMy + 55 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                SCREEN.blit(Spider_Man, (SMx - 40, SMy - 10))
            elif dif_image == 1 and revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 50, SMy + SMh // 2 - 20),
                                 (300 + coords_increase, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image == 2 or revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 47, SMy + SMh // 2 - 35),
                                 (300 + coords_increase, 0), 1)
                SCREEN.blit(Spider_Man, (SMx - 40, SMy + 50))
            # pygame.display.update()

        elif st == 1 and 220 <= coords_increase <= 395 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 4
            sdvigy += 3
            if suit == 'c s':
                Spider_Man = load_image_safe('fly_pose1_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose1_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose1_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose1_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose1_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose1_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose1_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose1_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
            if coords_increase % 3 == 0:
                SMRt += 1

            if dif_image == 1 and revst == 0:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx - 25, SMy + SMh // 2 - 60),
                                 (display_w - 300 - coords_increase * 3, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image != 1 and revst == 0:
                if 220 <= coords_increase <= 250:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 90 + SMR_pvu.topright[0], SMy + 40 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 250 < coords_increase <= 270:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 125 + SMR_pvu.topright[0], SMy + 40 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 270 < coords_increase <= 300:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 155 + SMR_pvu.topright[0], SMy + 50 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 300 < coords_increase <= 340:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 220 + SMR_pvu.topright[0], SMy + 40 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                elif 340 < coords_increase <= 395:
                    pygame.draw.line(SCREEN, pygame.Color('White'),
                                     (SMx - 235 + SMR_pvu.topright[0], SMy + 90 + SMR_pvu.topright[1]),
                                     (display_w - 300 - coords_increase * 2.5, 0), 1)
                SCREEN.blit(Spider_Man, (SMx - 40, SMy - 10))
            elif dif_image == 1 and revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 50, SMy + SMh // 2 - 20),
                                 (300 + coords_increase, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image == 2 or revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 47, SMy + SMh // 2 - 35),
                                 (300 + coords_increase, 0), 1)
                SCREEN.blit(Spider_Man, (SMx - 40, SMy + 50))
            # pygame.display.update()
            coords_increase += 1
            if coords_increase % 3 == 0:
                SMRt += 1

        elif st == 1 and 395 <= coords_increase <= 430 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 4
            sdvigy += 2
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 198.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 199.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 200.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 201.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 202.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 203.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 204.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 205.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 25, SMh - 65))

            if dif_image == 1 and revst == 0:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx - 60, SMy + SMh // 2 - 60),
                                 (display_w - 300 - coords_increase * 3, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image != 1 and revst == 0:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx - 270 + SMR_pvu.topright[0], SMy + 70 + SMR_pvu.topright[1]),
                                 (display_w - 300 - coords_increase * 2.5, 0), 1)
                SCREEN.blit(Spider_Man, (SMx - 40, SMy - 10))
            elif dif_image == 1 and revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 50, SMy + SMh // 2 - 20),
                                 (300 + coords_increase, 0), 1)
                SCREEN.blit(Spider_Man, (SMx, SMy))
            elif dif_image == 2 or revst == 1:
                pygame.draw.line(SCREEN, pygame.Color('White'), (SMx + 47, SMy + SMh // 2 - 35),
                                 (300 + coords_increase, 0), 1)
                SCREEN.blit(Spider_Man, (SMx - 40, SMy + 50))
            # pygame.display.update()
            coords_increase += 1
            if coords_increase % 3 == 0:
                SMRt += 1

        elif st == 1 and 430 <= coords_increase <= 620 and pygame.key.get_pressed()[pygame.K_LSHIFT] and dif_image == 1:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 2
            sdvigy += 1
            if revst == 0:
                if suit == 'cs':
                    if dif_image == 1:
                        Spider_Man = load_image_safe('fly_pose9.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 25, SMh - 65))
                        Spider_Man = pygame.transform.rotate(Spider_Man, srt)
                        SCREEN.blit(Spider_Man, (SMx + 80, SMy - 17))
                    elif dif_image == 2:
                        Spider_Man = load_image_safe('fly_pose9_cs.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 75))
                        Spider_Man = pygame.transform.rotate(Spider_Man, srt + 10)
                        SCREEN.blit(Spider_Man, (SMx + 80, SMy - 17))
                else:
                    if suit == 'iss':
                        Spider_Man = load_image_safe('fly_pose9_iss.png')
                    elif suit == 'ws':
                        Spider_Man = load_image_safe('fly_pose9_ws.png')
                    elif suit == 'us':
                        Spider_Man = load_image_safe('fly_pose9_us.png')
                    elif suit == 'ss':
                        Spider_Man = load_image_safe('fly_pose9_ss.png')
                    elif suit == 'as':
                        Spider_Man = load_image_safe('fly_pose9_as.png')
                    elif suit == 'is':
                        Spider_Man = load_image_safe('fly_pose9_is.png')
                    elif suit == 'ios':
                        Spider_Man = load_image_safe('fly_pose9_ios.png')
                    Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 35, SMh - 50))
                    Spider_Man = pygame.transform.rotate(Spider_Man, srt + 10)
                    SCREEN.blit(Spider_Man, (SMx + 80, SMy - 17))
            else:
                if suit == 'cs':
                    dif_image = randint(1, 2)
                    if dif_image == 1:
                        Spider_Man = load_image_safe('Тема 2_rev.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 20))
                        SCREEN.blit(Spider_Man, (SMx + 7, SMy + 143))
                    elif dif_image == 2:
                        Spider_Man = load_image_safe('spider_stay5_cs_rev.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 5))
                        SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
                else:
                    if suit == 'iss':
                        Spider_Man = load_image_safe('spider_stay5_iss_rev.png')
                    elif suit == 'ws':
                        Spider_Man = load_image_safe('spider_stay5_ws_rev.png')
                    elif suit == 'us':
                        Spider_Man = load_image_safe('spider_stay5_us_rev.png')
                    elif suit == 'ss':
                        Spider_Man = load_image_safe('spider_stay5_ss_rev.png')
                    elif suit == 'as':
                        Spider_Man = load_image_safe('spider_stay5_as_rev.png')
                    elif suit == 'is':
                        Spider_Man = load_image_safe('spider_stay5_is_rev.png')
                    elif suit == 'ios':
                        Spider_Man = load_image_safe('spider_stay5_ios_rev.png')
                    Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 5))
                    SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
            # pygame.display.update()
            coords_increase += 1
            if coords_increase % 9 == 0:
                srt += 1

        elif st == 1 and not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            if zvukst == 0 and coords_increase > 400:
                ss = pygame.mixer.Sound("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Sounds"
                                        "/Swing_sound.mp3")
                ss.play()
                zvukst = 1
                for i in range(15000000):
                    pass
                st, coords_increase, SMRt = 2, 0, 20
            else:
                st = 3

        elif st == 2 and coords_increase <= 175 and not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 4
            sdvigy += 2
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose7_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose7_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose7_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose7_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose7_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose7_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose7_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose7_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 30, SMh - 140))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt - 175)
            SCREEN.blit(Spider_Man, (SMx + 60, SMy + 40))
            # pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx, SMy + SMh // 2 - 40),
            # (display_w // 2, 0), 1)
            # pygame.display.update()
            coords_increase += 1
            if coords_increase % 5 == 0:
                SMRt -= 1

        elif st == 3 and sdvigy >= -330 \
                and not pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if sdvigxconst != 0:
                sdvigxconst = sdvigx
            if sdvigyconst != 0:
                sdvigyconst = sdvigy
            if revst == 0:
                sdvigx -= 1
                sdvigy -= 5
                if suit == 'cs':
                    Spider_Man = load_image_safe('fly_pose8_cs.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('fly_pose8_iss.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('fly_pose8_ws.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('fly_pose8_us.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('fly_pose8_ss.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('fly_pose8_as.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('fly_pose8_is.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('fly_pose8_ios.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 20, SMh - 70))
            else:
                sdvigx += 1
                sdvigy -= 5
                if suit == 'cs':
                    Spider_Man = load_image_safe('fly_pose8_cs_rev.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('fly_pose8_iss_rev.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('fly_pose8_ws_rev.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('fly_pose8_us_rev.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('fly_pose8_ss_rev.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('fly_pose8_as_rev.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('fly_pose8_is_rev.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('fly_pose8_ios_rev.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 20, SMh - 70))
            # Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
            SCREEN.blit(Spider_Man, (SMx, SMy + 150))
            # pygame.draw.line(SCREEN, pygame.Color('White'), (SMw + SMx, SMy + SMh // 2 - 40),
            # (display_w // 2, 0), 1)
            # pygame.display.update()

        elif st == -1 and revst == 0 and revk == 0 and coords_increase < 70 and pygame.key.get_pressed()[
            pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 6
            sdvigy += 4
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose1_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose1_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose1_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose1_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose1_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose1_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose1_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose1_ios.png')
            Spider_Man = load_image_safe('fly_pose1_cs.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
            if coords_increase % 5 == 0:
                SMRt += 1
            SMR_pvu = Spider_Man.get_rect()
            pygame.draw.line(SCREEN, pygame.Color('White'),
                             (SMx - 70 + SMR_pvu.topleft[0], SMy + 140 + SMR_pvu.topleft[1]),
                             (display_w - 300 - coords_increase * 2.5, 0), 1)
            SCREEN.blit(Spider_Man, (SMx, SMy))
            # pygame.display.update()
            coords_increase += 1

        elif (st == -1 or st == -2) and revk < 20 and revst == 0 and 70 <= coords_increase <= 400 - revk * 20 \
                and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx += 4
            if sdvigy > -330:
                if sdvigy % 12 == 0:
                    sdvigy -= 2 + revk
                else:
                    sdvigy -= 2
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose1_cs_rev.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose1_iss_rev.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose1_ws_rev.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose1_us_rev.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose1_ss_rev.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose1_as_rev.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose1_is_rev.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose1_ios_rev.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt - 25)
            if coords_increase % 5 == 0:
                SMRt -= 1
            SMR_pvu = Spider_Man.get_rect()
            if 70 <= coords_increase <= 130:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx + 20 + SMR_pvu.topleft[0], SMy + 60 + SMR_pvu.topleft[1]),
                                 (300 + coords_increase * 1.8, 0), 1)
            elif 130 < coords_increase <= 180:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx + 30 + SMR_pvu.topleft[0], SMy + 60 + SMR_pvu.topleft[1]),
                                 (300 + coords_increase * 1.8, 0), 1)
            elif 180 < coords_increase <= 220:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx + 40 + SMR_pvu.topleft[0], SMy + 60 + SMR_pvu.topleft[1]),
                                 (300 + coords_increase * 1.8, 0), 1)
            elif 220 < coords_increase <= 400:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx + 45 + SMR_pvu.topleft[0], SMy + 60 + SMR_pvu.topleft[1]),
                                 (300 + coords_increase * 1.8, 0), 1)
            SCREEN.blit(Spider_Man, (SMx, SMy))
            # pygame.display.update()
            coords_increase += 1

        elif (st == -1 or st == -2) and revk < 20 and revst == 0 \
                and 400 - revk * 50 < coords_increase <= 500 - revk * 70 \
                and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx += 3
            sdvigy += 2
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose1_cs_rev.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose1_iss_rev.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose1_ws_rev.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose1_us_rev.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose1_ss_rev.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose1_as_rev.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose1_is_rev.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose1_ios_rev.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt - 25)
            if coords_increase % 5 == 0:
                SMRt -= 1
            SMR_pvu = Spider_Man.get_rect()
            pygame.draw.line(SCREEN, pygame.Color('White'),
                             (SMx + 40 + SMR_pvu.topleft[0], SMy + 50 + SMR_pvu.topleft[1]),
                             (300 + coords_increase * 1.8, 0), 1)
            SCREEN.blit(Spider_Man, (SMx, SMy))
            # pygame.display.update()
            coords_increase += 1

        elif st == -2 and revk < 20 and revst == 1 and 70 <= coords_increase <= 400 - revk * 20 \
                and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 3
            if sdvigy > -330:
                if sdvigy % 12 == 0:
                    sdvigy -= 2 + revk
                else:
                    sdvigy -= 2
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose1_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose1_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose1_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose1_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose1_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose1_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose1_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose1_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
            if coords_increase % 4 == 0:
                SMRt += 1
            SMR_pvu = Spider_Man.get_rect()
            if 70 <= coords_increase <= 250:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx - 65 + SMR_pvu.topright[0], SMy + 60 + SMR_pvu.topright[1]),
                                 (display_w - 300 - coords_increase * 1.8, 0), 1)
            elif 250 <= coords_increase <= 400:
                pygame.draw.line(SCREEN, pygame.Color('White'),
                                 (SMx - 100 + SMR_pvu.topright[0], SMy + 60 + SMR_pvu.topright[1]),
                                 (display_w - 300 - coords_increase * 1.8, 0), 1)
            SCREEN.blit(Spider_Man, (SMx, SMy))
            # pygame.display.update()
            coords_increase += 1

        elif st == -2 and revk < 20 and revst == 1 \
                and 400 - revk * 20 < coords_increase <= 500 - revk * 20 \
                and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            sdvigx -= 3
            sdvigy += 2
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose1_cs.png')
            if suit == 'iss':
                Spider_Man = load_image_safe('fly_pose1_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose1_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose1_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose1_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose1_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose1_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose1_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 40, SMh - 65))
            Spider_Man = pygame.transform.rotate(Spider_Man, SMRt)
            if coords_increase % 4 == 0:
                SMRt += 1
            SMR_pvu = Spider_Man.get_rect()
            pygame.draw.line(SCREEN, pygame.Color('White'),
                             (SMx - 100 + SMR_pvu.topright[0], SMy + 60 + SMR_pvu.topright[1]),
                             (display_w - 300 - coords_increase * 1.8, 0), 1)
            SCREEN.blit(Spider_Man, (SMx, SMy))
            # pygame.display.update()
            coords_increase += 1

        elif st == 1 and coords_increase >= 620 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            st, coords_increase, SMRt = -1, 0, 60

        elif st == 0 and sdvigy <= -330 and ((ticks - sp_ticks >= 2000 and sp_ticks != 0) or podst == 1) \
                and not pygame.key.get_pressed()[pygame.K_d] and not pygame.key.get_pressed()[pygame.K_SPACE] \
                and not pygame.key.get_pressed()[pygame.K_a]:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if revst == 0:
                if suit == 'cs':
                    if dif_image == 0:
                        dif_image = randint(1, 2)
                    if dif_image == 1:
                        Spider_Man = load_image_safe('Тема 2.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 20))
                        SCREEN.blit(Spider_Man, (SMx + 7, SMy + 143))
                    elif dif_image == 2:
                        Spider_Man = load_image_safe('spider_stay5_cs.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 5))
                        SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
                else:
                    if suit == 'iss':
                        Spider_Man = load_image_safe('spider_stay5_iss.png')
                    elif suit == 'ws':
                        Spider_Man = load_image_safe('spider_stay5_ws.png')
                    elif suit == 'us':
                        Spider_Man = load_image_safe('spider_stay5_us.png')
                    elif suit == 'ss':
                        Spider_Man = load_image_safe('spider_stay5_ss.png')
                    elif suit == 'as':
                        Spider_Man = load_image_safe('spider_stay5_as.png')
                    elif suit == 'is':
                        Spider_Man = load_image_safe('spider_stay5_is.png')
                    elif suit == 'ios':
                        Spider_Man = load_image_safe('spider_stay5_ios.png')
                    Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 5))
                    SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
            else:
                if suit == 'cs':
                    if dif_image == 0:
                        dif_image = randint(1, 2)
                    if dif_image == 1:
                        Spider_Man = load_image_safe('Тема 2_rev.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 20))
                        SCREEN.blit(Spider_Man, (SMx + 7, SMy + 143))
                    elif dif_image == 2:
                        Spider_Man = load_image_safe('spider_stay5_cs_rev.png')
                        Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 5))
                        SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
                else:
                    if suit == 'iss':
                        Spider_Man = load_image_safe('spider_stay5_iss_rev.png')
                    elif suit == 'ws':
                        Spider_Man = load_image_safe('spider_stay5_ws_rev.png')
                    elif suit == 'us':
                        Spider_Man = load_image_safe('spider_stay5_us_rev.png')
                    elif suit == 'ss':
                        Spider_Man = load_image_safe('spider_stay5_ss_rev.png')
                    elif suit == 'as':
                        Spider_Man = load_image_safe('spider_stay5_as_rev.png')
                    elif suit == 'is':
                        Spider_Man = load_image_safe('spider_stay5_is_rev.png')
                    elif suit == 'ios':
                        Spider_Man = load_image_safe('spider_stay5_ios_rev.png')
                    Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 50, SMh - 5))
                    SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
            # pygame.display.update()
            # pygame.time.wait(40)
            time_wait = 40

        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_d] \
                and (0 <= ticks - sp_ticks <= 150 or sp_ticks == 0):
            if podst != 1:
                podst = 1
            if revst == 1:
                revst = 0
            sdvigx -= 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1

            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if dif_image == 0:
                dif_image = randint(1, 2)
            if dif_image == 1 and suit == 'cs':
                Spider_Man = load_image_safe('Тема 100.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw, SMh - 40))
            elif dif_image == 2 and suit == 'cs':
                Spider_Man = load_image_safe('Тема 82.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 15, SMh - 50))
            else:
                if suit == 'iss':
                    Spider_Man = load_image_safe('Тема 101.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 102.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 103.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 104.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 105.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 106.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 107.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw, SMh - 40))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 157))
            # pygame.display.update()
            if sp_ticks == 0:
                sp_ticks = ticks
        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_d] \
                and 150 <= ticks - sp_ticks <= 220:
            sdvigx -= 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 84.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 85.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 86.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 87.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 88.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 89.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 90.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 91.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 10, SMh - 40))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 145))
            # pygame.display.update()
        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_d] \
                and 220 <= ticks - sp_ticks <= 340:
            sdvigx -= 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 108.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 109.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 110.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 111.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 112.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 113.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 114.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 115.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 10, SMh - 30))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 140))
            # pygame.display.update()
        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_d] \
                and 340 <= ticks - sp_ticks <= 410:
            sdvigx -= 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 116.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 117.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 118.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 119.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 120.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 121.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 122.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 123.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 10, SMh - 40))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 140))
            # pygame.display.update()

        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_a] \
                and (0 <= ticks - sp_ticks <= 150 or sp_ticks == 0):
            if podst != 1:
                podst = 1
            if revst == 0:
                revst = 1
            sdvigx += 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if dif_image == 0:
                dif_image = randint(1, 2)
            if dif_image == 1 and suit == 'cs':
                Spider_Man = load_image_safe('Тема 100_rev.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw, SMh - 40))
            elif dif_image == 2 and suit == 'cs':
                Spider_Man = load_image_safe('Тема 82_rev.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 15, SMh - 50))
            else:
                if suit == 'iss':
                    Spider_Man = load_image_safe('Тема 101_rev.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 102_rev.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 103_rev.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 104_rev.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 105_rev.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 106_rev.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 107_rev.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw, SMh - 40))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 157))
            # pygame.display.update()
            if sp_ticks == 0:
                sp_ticks = ticks
        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_a] \
                and 150 <= ticks - sp_ticks <= 220:
            sdvigx += 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 84_rev.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 85_rev.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 86_rev.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 87_rev.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 88_rev.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 89_rev.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 90_rev.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 91_rev.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 10, SMh - 40))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 145))
            # pygame.display.update()
        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_a] \
                and 220 <= ticks - sp_ticks <= 340:
            sdvigx += 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1

            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 108_rev.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 109_rev.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 110_rev.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 111_rev.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 112_rev.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 113_rev.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 114_rev.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 115_rev.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 10, SMh - 30))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 140))
            # pygame.display.update()
        elif st == 0 and sdvigy <= -330 and pygame.key.get_pressed()[pygame.K_a] \
                and 340 <= ticks - sp_ticks <= 410:
            sdvigx += 2
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject"
                                    "/Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if suit == 'cs':
                Spider_Man = load_image_safe('Тема 116_rev.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('Тема 117_rev.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('Тема 118_rev.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('Тема 119_rev.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('Тема 120_rev.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('Тема 121_rev.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('Тема 122_rev.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('Тема 123_rev.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw - 10, SMh - 40))
            SCREEN.blit(Spider_Man, (SMx + 27, SMy + 140))
            # pygame.display.update()

        elif st == -100 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
            st = 0

        elif st == -100 and 600 <= sdvigy <= 1000:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1
            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject"
                                    "/Marvel's Spider-Man 2D/Fonts/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if coords_increase % 3 == 0:
                sdvigx -= 1
            sdvigy -= 6
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose7_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose7_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose7_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose7_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose7_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose7_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose7_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose7_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 45, SMh - 130))
            Spider_Man = pygame.transform.rotate(Spider_Man, -65)
            SCREEN.blit(Spider_Man, (SMx + 27, SMy))
            # pygame.display.update()
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                        "/Sounds/air_sound.mp3")
                pygame.mixer.music.play()
            coords_increase += 1

        elif st == -100 and -330 <= sdvigy <= 600:
            SCREEN.fill(pygame.Color('Black'))
            i = 0
            while (i < tiles):
                SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                i += 1

            if abs(sdvigx) > bg.get_width():
                sdvigx = 0
            pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
            pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/MonospaceBold.ttf", 30 * kx)
            text = font.render(str(hp), True, (255, 255, 255))
            tx, ty = 460, 53
            SCREEN.blit(text, (tx, ty))
            if coords_increase % 3 == 0:
                sdvigx -= 1
            sdvigy -= 2
            if suit == 'cs':
                Spider_Man = load_image_safe('fly_pose7_cs.png')
            elif suit == 'iss':
                Spider_Man = load_image_safe('fly_pose7_iss.png')
            elif suit == 'ws':
                Spider_Man = load_image_safe('fly_pose7_ws.png')
            elif suit == 'us':
                Spider_Man = load_image_safe('fly_pose7_us.png')
            elif suit == 'ss':
                Spider_Man = load_image_safe('fly_pose7_ss.png')
            elif suit == 'as':
                Spider_Man = load_image_safe('fly_pose7_as.png')
            elif suit == 'is':
                Spider_Man = load_image_safe('fly_pose7_is.png')
            elif suit == 'ios':
                Spider_Man = load_image_safe('fly_pose7_ios.png')
            Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 45, SMh - 130))
            Spider_Man = pygame.transform.rotate(Spider_Man, -65)
            SCREEN.blit(Spider_Man, (SMx + 27, SMy))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                    "/GULAG.otf", 25 * kx)
            text = font.render('!HELP!', True,
                               (255, 255, 255))
            tx, ty = 400, 115
            SCREEN.blit(text, (tx, ty))
            pygame.draw.rect(SCREEN, pygame.Color('White'), (400, 139, 80, 2))
            pygame.draw.rect(SCREEN, pygame.Color('White'), (400, 147, 820, 2))
            font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D"
                                    "/Fonts/Podkova.ttf", 20 * kx)
            text = font.render('Чтобы зацепиться паутиной и лететь на ней зажмите и держите L_Shift', True,
                               (255, 255, 255))
            tx, ty = 400, 150
            SCREEN.blit(text, (tx, ty))
            text = font.render('а затем отпустите его, тогда паук сможет резко выпрямиться и полететь дальше',
                               True, (255, 255, 255))
            tx, ty = 400, 175
            SCREEN.blit(text, (tx, ty))
            # Надпись с инструкцией к полету: Чтобы зацепиться паутиной и лететь на ней зажмите и держите L_Shift, а затем отпустите
            # его, тогда паук сможет резко выпрямиться и полететь дальше
            coords_increase += 1
            # pygame.display.update()

        elif st == -100 and sdvigy <= -330:
            st = 0
            pygame.mixer.music.load("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Sounds"
                                    "/spider_punch_ground.mp3")
            pygame.mixer.music.play()

        else:
            sp_ticks, dif_image = 0, 0
            if st == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                st, coords_increase, SMRt = -1, 0, 60
                revst = 1
                SCREEN.fill(pygame.Color('Black'))
                i = 0
                while (i < tiles):
                    SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                    SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                    i += 1
                if abs(sdvigx) > bg.get_width():
                    sdvigx = 0
                pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
                pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                        "/MonospaceBold.ttf", 30 * kx)
                text = font.render(str(hp), True, (255, 255, 255))
                tx, ty = 460, 53
                SCREEN.blit(text, (tx, ty))
            elif (st == -1 or st == -2) and coords_increase <= 701 \
                    and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                st, coords_increase = -2, 70
                revk += 1
                if revst == 0:
                    revst = 1
                    SMRt = 0
                else:
                    revst = 0
                    SMRt = 40
                SCREEN.fill(pygame.Color('Black'))
                i = 0
                while (i < tiles):
                    SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                    SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                    i += 1
                if abs(sdvigx) > bg.get_width():
                    sdvigx = 0
            elif st == 3 and (pygame.key.get_pressed()[pygame.K_LSHIFT] or sdvigy <= -330):
                st = 0
            else:
                st = 3
                coords_increase = 0

        if subst == 'ON':
            if subticks == 0:
                subticks = ticks
            for i in time_subtitles:
                if int(i.split()[0]) < ticks - subticks + 1300 < int(i.split()[1]):
                    font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                            "/MonospaceBold.ttf", 22 * kx)
                    text = font.render(subtitles[time_subtitles.index(i)], True, (255, 255, 255))
                    tx, ty = display_w // 2 - len(subtitles[time_subtitles.index(i)]) // 2 * 13, \
                             display_h - 200 - len(subtitles[time_subtitles.index(i)]) // 50 * 17
                    SCREEN.blit(text, (tx, ty))
                    break

        if ticks >= 50000 and cut_scene == 1 and fight == 1:
            # second_cut_scene()
            st, sdvigy = 0, -330
            for i in range(5):
                dif_image_m = randint(0, 4)
                if dif_image_m == 0:
                    f_t = load_image_safe('fisk_thug_rack.png')
                elif dif_image_m == 1:
                    f_t = load_image_safe('fisk_thug_rack2.png')
                elif dif_image_m == 2:
                    f_t = load_image_safe('fisk_thug_rack3.png')
                elif dif_image_m == 3:
                    f_t = load_image_safe('fisk_thug_rack4.png')
                elif dif_image_m == 4:
                    f_t = load_image_safe('fisk_thug_rack5.png')
                f_t = pygame.transform.scale(f_t, (120, 220))
                SCREEN.blit(f_t, (display_w // 2 + 100 + 130 * i, display_h // 2 - 53))
                f_t_colors.append(dif_image_m)
                f_t_coords.append((display_w // 2 + 100 + 130 * i, display_h // 2 - 53))
                FTx, FTy = f_t_coords[i]
            # pygame.display.update()
            ftticks = ticks
            fight = 1

        if fight == 1 and hp > 0:
            for i in range(len(f_t_colors)):
                dif_image_m = f_t_colors[i]
                FTx, FTy = f_t_coords[i]
                if ticks - ftticks < 4000:
                    if dif_image_m == 0:
                        f_t = load_image_safe('fisk_thug_rack.png')
                        f_t = pygame.transform.scale(f_t, (120, 220))
                    elif dif_image_m == 1:
                        f_t = load_image_safe('fisk_thug_rack2.png')
                        f_t = pygame.transform.scale(f_t, (120, 220))
                    elif dif_image_m == 2:
                        f_t = load_image_safe('fisk_thug_rack3.png')
                        f_t = pygame.transform.scale(f_t, (120, 220))
                    elif dif_image_m == 3:
                        f_t = load_image_safe('fisk_thug_rack4.png')
                        f_t = pygame.transform.scale(f_t, (130, 220))
                    elif dif_image_m == 4:
                        f_t = load_image_safe('fisk_thug_rack5.png')
                        f_t = pygame.transform.scale(f_t, (130, 220))
                    SCREEN.blit(f_t, (FTx + sdvigx, FTy + 330 + sdvigy))

                elif 4000 <= ticks - ftticks < 4500:
                    if dif_image_m == 0:
                        f_t = load_image_safe('fisk_thug1_threating.png')
                        f_t = pygame.transform.scale(f_t, (120, 220))
                    elif dif_image_m == 1:
                        f_t = load_image_safe('fisk_thug_threating2.png')
                        f_t = pygame.transform.scale(f_t, (150, 220))
                    elif dif_image_m == 2:
                        f_t = load_image_safe('Тема 15.png')
                        f_t = pygame.transform.scale(f_t, (140, 220))
                    elif dif_image_m == 3:
                        f_t = load_image_safe('fisk_threating3.png')
                        f_t = pygame.transform.scale(f_t, (140, 220))
                    elif dif_image_m == 4:
                        f_t = load_image_safe('fisk_threating4.png')
                        f_t = pygame.transform.scale(f_t, (140, 220))
                    SCREEN.blit(f_t, (FTx - 60 + sdvigx, FTy + 330 + sdvigy))

                elif 4500 <= ticks - ftticks <= 5200:
                    if dif_image_m == 0 and i == 0:
                        f_t = load_image_safe('fisk_thug_punch1.png')
                        f_t = pygame.transform.scale(f_t, (214, 185))
                    elif dif_image_m == 0 and i != 0:
                        f_t = load_image_safe('fisk_threating3.png')
                        f_t = pygame.transform.scale(f_t, (160, 220))
                    elif dif_image_m == 1:
                        f_t = load_image_safe('fisk_thug_punch.png')
                        f_t = pygame.transform.scale(f_t, (200, 220))
                    elif dif_image_m == 2:
                        f_t = load_image_safe('fisk_threating3.png')
                        f_t = pygame.transform.scale(f_t, (160, 185))
                    elif dif_image_m == 3:
                        f_t = load_image_safe('fisk_thug_punch.png')
                        f_t = pygame.transform.scale(f_t, (200, 220))
                    elif dif_image_m == 4:
                        f_t = load_image_safe('fisk_threating3.png')
                        f_t = pygame.transform.scale(f_t, (160, 220))
                    SCREEN.blit(f_t, (FTx - 110 + sdvigx, FTy + 330 + sdvigy))
                else:
                    if abs(SMx - FTx) < 170:
                        hp -= round(50 * dif_k)
                    f_t_coords[i] = (FTx - 110, FTy)
                # pygame.display.update()
            if ticks - ftticks > 5200:
                ftticks = ticks
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                quit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    data = []
                    f = open("Saves.txt", mode="r")
                    text = f.readlines()
                    for i in text:
                        data.append(i)
                        print(i)
                    f.close()
                    f = open('Downloads.txt', 'w')
                    f.close()
                    f = open('Downloads.txt', 'w')
                    # for i in range(6):
                    #    if i == im:
                    #        f.write(str(im, dif_k, musst, suit, cut_scene, hp, sdvigx, sdvigy))
                    #   else:
                    #       f.write(data[i])
                    f.close()
                    pygame.quit()
                    sys.exit()
                elif ev.key == pygame.K_TAB:
                    pygame.mixer.music.unload()
                    menu()
            if ev.type == pygame.MOUSEBUTTONDOWN and sdvigy <= -330:
                SCREEN.fill(pygame.Color('Black'))
                i = 0
                while (i < tiles):
                    SCREEN.blit(bg, (bg.get_width() * i + sdvigx, -2000 + display_h - 100 + sdvigy))
                    SCREEN.blit(road, (road.get_width() * i + sdvigx, 800 + sdvigy))
                    i += 1
                if abs(sdvigx) > bg.get_width():
                    sdvigx = 0
                pygame.draw.rect(SCREEN, (255, 255, 255), (50, 50, 400, 45), 5)
                pygame.draw.rect(SCREEN, (50, 191, 73), (55, 55, 390, 35))
                font = pygame.font.Font("/Users/aleksej/PycharmProjects/pythonProject/Marvel's Spider-Man 2D/Fonts"
                                        "/MonospaceBold.ttf", 30 * kx)
                text = font.render(str(hp), True, (255, 255, 255))
                tx, ty = 460, 53
                SCREEN.blit(text, (tx, ty))
                if suit == 'cs':
                    Spider_Man = load_image_safe('Тема 70.png')
                elif suit == 'iss':
                    Spider_Man = load_image_safe('Тема 71.png')
                elif suit == 'ws':
                    Spider_Man = load_image_safe('Тема 72.png')
                elif suit == 'us':
                    Spider_Man = load_image_safe('Тема 73.png')
                elif suit == 'ss':
                    Spider_Man = load_image_safe('Тема 74.png')
                elif suit == 'as':
                    Spider_Man = load_image_safe('Тема 75.png')
                elif suit == 'is':
                    Spider_Man = load_image_safe('Тема 76.png')
                elif suit == 'ios':
                    Spider_Man = load_image_safe('Тема 77.png')
                Spider_Man = pygame.transform.scale(Spider_Man, (SMw + 10, SMh - 25))
                SCREEN.blit(Spider_Man, (SMx + 20, SMy + 140))
                for i in range(len(f_t_colors)):
                    FTx, FTy = f_t_coords[i]
                    if abs(SMx - FTx) <= 170:
                        del f_t_colors[0]
                # pygame.display.update()
                # pygame.time.wait(200)
                st = 0
        pygame.display.update()
        if time_wait != 0:
            pygame.time.wait(time_wait)
            time_wait = 0


main_menu()
