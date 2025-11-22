import pygame
import sys
import random
from random import randint
import math
from src.config import *

# Инициализация PyGame
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

# Константы из конфига
WIDTH, HEIGHT = SCREEN_WIDTH, SCREEN_HEIGHT
pi = 3.14

# Глобальные переменные (будут заменены на конфиг)
kx, ky = SCALE_X, SCALE_Y
cut_scene = CURRENT_CUTSCENE

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(PROJECT_NAME)


def load_image_safe(path, default_image=PLACEHOLDER_IMAGE, convert_alpha=True):
    """Безопасно загружает изображение. Если файл не найден, использует изображение-заглушку."""
    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
        return image
    except (pygame.error, FileNotFoundError) as e:
        print(f"[CONFIG] Ошибка {path}: {e}, используем заглушку")
        try:
            if convert_alpha:
                return pygame.image.load(default_image).convert_alpha()
            else:
                return pygame.image.load(default_image).convert()
        except Exception as e2:
            print(f"[CONFIG] Критическая ошибка заглушки: {e2}")
            surf = pygame.Surface((scale_value(50), scale_value(50)))
            surf.fill((255, 0, 255))
            return surf


def main_menu():
    st = 0  # Начинаем с начального экрана
    global cut_scene
    global im
    global DIFFICULTY
    global MUSIC_STATUS
    global CURRENT_SUIT
    global SUBTITLES
    intro_start_time = 0
    vp = 0
    d_arc = 0.0
    time = 0

    expectation = randint(1500, 2200)

    # Загрузка музыки главного меню
    pygame.mixer.music.load(get_music_path("Web Launch.mp3"))
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()

    while True:
        if st == 0:
            # Загружаем и отображаем начальный экран
            intro_image = load_image_safe(get_image_path("main_menu", "Home_screen.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT + scale_value(20)))
            SCREEN.blit(intro_image, (0, 0))

            # Затем текст
            font = pygame.font.Font(get_font_path('gulag'), FONT_SIZES['title'])
            text = font.render('Spider-Man', True, WHITE)
            tx = SCREEN_WIDTH // 2 - text.get_width() // 2
            ty = SCREEN_HEIGHT // 4 - scale_value(60) - scale_value(90)
            SCREEN.blit(text, (tx, ty))

            if intro_start_time == 0:
                intro_start_time = pygame.time.get_ticks()

            # Проверка времени и смена состояния
            if pygame.time.get_ticks() - intro_start_time >= 3000:
                st = 1
                intro_start_time = 0

        if st == 1:
            intro_image = load_image_safe(get_image_path("main_menu", "newgamescreen.jpg"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            font = pygame.font.Font(get_font_path('gulag'), FONT_SIZES['title'])
            text = font.render('START', True, RED)

            # Правильно вычисляем позицию и размеры
            text_width = text.get_width()
            text_height = text.get_height()
            tx = SCREEN_WIDTH // 2 - text_width // 2
            ty = SCREEN_HEIGHT // 4 - text_height // 2 - scale_value(20)

            # Получаем текущую позицию мыши
            mouse_pos = pygame.mouse.get_pos()

            # Проверяем, находится ли мышь над текстом
            if (tx <= mouse_pos[0] <= tx + text_width and
                    ty <= mouse_pos[1] <= ty + text_height):
                text.set_alpha(255)
            else:
                text.set_alpha(50)

            # Отображаем текст
            SCREEN.blit(text, (tx, ty))

            # Обработка событий
            for event1 in pygame.event.get():
                if event1.type == pygame.MOUSEBUTTONDOWN:
                    # Проверяем клик по тексту
                    if (tx <= event1.pos[0] <= tx + text_width and
                            ty <= event1.pos[1] <= ty + text_height):
                        st = 2
                        im = 0

                if event1.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event1.type == pygame.KEYDOWN and event1.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if st == 2:
            intro_image = load_image_safe(get_image_path("main_menu", "BS_menu.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            save_slots = load_image_safe(get_image_path("main_menu", "save_slots.png"))
            save_slots = pygame.transform.scale(save_slots, (scale_value(480), scale_value(810)))
            SCREEN.blit(save_slots, (scale_value(140), scale_value(50)))

            # Отрисовка элементов интерфейса
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(169), scale_value(168 + 91 * im)),
                             (scale_value(172), scale_value(168 + 91 * im)), 1)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(184), scale_value(168 + 91 * im)),
                               scale_value(8), 2)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(184), scale_value(168 + 91 * im)),
                               scale_value(4), 2)

            s = pygame.Surface((scale_value(400), scale_value(85)))
            s.fill(MENU_DARK_BLUE)
            s.set_alpha(160)
            SCREEN.blit(s, (scale_value(196), scale_value(125 + 91 * im)))

            # Границы выделенного элемента
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(196), scale_value(125 + 91 * im)),
                             (scale_value(196), scale_value(145 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(195), scale_value(124 + 91 * im)),
                             (scale_value(216), scale_value(124 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(196), scale_value(189 + 91 * im)),
                             (scale_value(196), scale_value(209 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(195), scale_value(210 + 91 * im)),
                             (scale_value(216), scale_value(210 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(594), scale_value(125 + 91 * im)),
                             (scale_value(594), scale_value(145 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(575), scale_value(124 + 91 * im)),
                             (scale_value(595), scale_value(124 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(594), scale_value(189 + 91 * im)),
                             (scale_value(594), scale_value(209 + 91 * im)), 3)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(575), scale_value(210 + 91 * im)),
                             (scale_value(595), scale_value(210 + 91 * im)), 3)

            # Загрузка и отображение слотов сохранения
            try:
                with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="r") as f:
                    txt = f.readlines()
                    for i in range(len(txt)):
                        line = txt[i].strip()
                        font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['medium'])

                        # Разбираем строку: "номер [опыт]"
                        parts = line.split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            # Есть опыт - отображаем "номер Опыт: число"
                            pygame.draw.rect(SCREEN, MENU_HIGHLIGHT,
                                             (scale_value(203), scale_value(131 + 91 * i),
                                              scale_value(385), scale_value(73)))
                            text = font.render(f"{parts[0]} Опыт: {parts[1]}", True, WHITE)
                            SCREEN.blit(text, (scale_value(220), scale_value(150 + 91 * i)))
            except FileNotFoundError:
                pass

            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 6  # 6 слотов сохранения
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 6
                    if event1.key == pygame.K_x:
                        # Сохраняем выбор слота в файл
                        try:
                            existing_data = {}
                            try:
                                with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="r") as f:
                                    lines = f.readlines()
                                    for i, line in enumerate(lines):
                                        if i < 6:
                                            existing_data[i] = line.strip()
                            except FileNotFoundError:
                                for i in range(6):
                                    existing_data[i] = str(i + 1)

                            with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="w") as f:
                                for i in range(6):
                                    if i == im:
                                        f.write(f"{i + 1} Выбрана\n")
                                    else:
                                        if i in existing_data and "Выбрана" not in existing_data[i]:
                                            f.write(existing_data[i] + "\n")
                                        else:
                                            f.write(f"{i + 1}\n")
                        except Exception as e:
                            print(f"Ошибка сохранения: {e}")

                        st = 3
                        im = 0
                    if event1.key == pygame.K_o:
                        st = 0
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event1.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if st == 3:
            intro_image = load_image_safe(get_image_path("main_menu", "BS_menu.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            # Отрисовка панели выбора сложности
            pygame.draw.rect(SCREEN, MENU_BLUE,
                             (scale_value(140), scale_value(48),
                              scale_value(480), scale_value(341)))
            pygame.draw.rect(SCREEN, MENU_DARK_BLUE,
                             (scale_value(140), scale_value(341),
                              scale_value(480), scale_value(259)))

            s = pygame.Surface((scale_value(480), scale_value(263)))
            s.fill(MENU_BLUE)
            s.set_alpha(125)
            SCREEN.blit(s, (scale_value(140), scale_value(600)))

            # Границы панели
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(48)),
                             (scale_value(140), scale_value(150)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(160)),
                             (scale_value(140), scale_value(163)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(173)),
                             (scale_value(140), scale_value(710)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(720)),
                             (scale_value(140), scale_value(723)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(733)),
                             (scale_value(140), scale_value(861)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(620), scale_value(48)),
                             (scale_value(620), scale_value(150)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(620), scale_value(160)),
                             (scale_value(620), scale_value(163)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(620), scale_value(173)),
                             (scale_value(620), scale_value(710)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(620), scale_value(720)),
                             (scale_value(620), scale_value(723)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(620), scale_value(733)),
                             (scale_value(620), scale_value(861)), 1)

            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['normal'])
            text = font.render("SELECT DIFFICULTY", True, WHITE)
            SCREEN.blit(text, (scale_value(160), scale_value(65)))

            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(160), scale_value(102)),
                             (scale_value(185), scale_value(102)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(190), scale_value(102)),
                             (scale_value(194), scale_value(102)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(200), scale_value(102)),
                             (scale_value(600), scale_value(102)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(165), scale_value(117)),
                             (scale_value(165), scale_value(125)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(165), scale_value(135)),
                             (scale_value(165), scale_value(305)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(165), scale_value(315)),
                             (scale_value(165), scale_value(323)), 2)

            # Отрисовка выбора сложности
            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['small'])
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(171), scale_value(147 + 40 * im)),
                             (scale_value(174), scale_value(147 + 40 * im)), 1)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(185), scale_value(147 + 40 * im)),
                               scale_value(8), 2)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(185), scale_value(147 + 40 * im)),
                               scale_value(4), 2)

            s = pygame.Surface((scale_value(360), scale_value(32)))
            s.fill(MENU_DARK_BLUE)
            s.set_alpha(160)
            SCREEN.blit(s, (scale_value(200), scale_value(130 + 40 * im)))

            # Границы выбранного элемента
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(200), scale_value(130 + 40 * im)),
                             (scale_value(210), scale_value(130 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(200), scale_value(130 + 40 * im)),
                             (scale_value(200), scale_value(140 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(200), scale_value(162 + 40 * im)),
                             (scale_value(210), scale_value(162 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(200), scale_value(152 + 40 * im)),
                             (scale_value(200), scale_value(162 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(550), scale_value(130 + 40 * im)),
                             (scale_value(560), scale_value(130 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(560), scale_value(130 + 40 * im)),
                             (scale_value(560), scale_value(140 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(550), scale_value(162 + 40 * im)),
                             (scale_value(560), scale_value(162 + 40 * im)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(560), scale_value(152 + 40 * im)),
                             (scale_value(560), scale_value(162 + 40 * im)), 2)

            # Тексты сложности
            difficulties = ["FRIENDLY NEIGHBOURHOOD", "THE AMAZING", "SPECTACULAR", "ULTIMATE"]
            for i, diff_text in enumerate(difficulties):
                text = font.render(diff_text, True, WHITE)
                SCREEN.blit(text, (scale_value(210), scale_value(135 + 40 * i)))

            # Индикаторы сложности
            for i in range(3):
                s = pygame.Surface((scale_value(250), scale_value(15)))
                s.fill(UI_ACCENT)
                s.set_alpha(155)
                SCREEN.blit(s, (scale_value(350), scale_value(685 + 30 * i)))
                pygame.draw.rect(SCREEN, WHITE,
                                 (scale_value(349), scale_value(684 + 30 * i),
                                  scale_value(252), scale_value(17)), 2)

            # Описания сложности
            if im == 0:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for expert players who", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(400)))

                text_part1 = font_desc.render("enjoy a brutally ", True, WHITE)
                text_fun = pygame.font.Font(get_font_path('avengeance'), FONT_SIZES['medium']).render("Fun", True,
                                                                                                      WHITE)
                text_part2 = font_desc.render(" experience.", True, WHITE)

                start_x = scale_value(160)
                start_y = scale_value(462)

                SCREEN.blit(text_part1, (start_x, start_y))
                fun_x = start_x + text_part1.get_width()
                SCREEN.blit(text_fun, (fun_x, start_y - scale_value(15)))
                SCREEN.blit(text_part2, (fun_x + text_fun.get_width(), start_y))

                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(686),
                                  scale_value(50), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(716),
                                  scale_value(70), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(746),
                                  scale_value(60), scale_value(13)))

            elif im == 1:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for players who want", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(380)))
                text = font_desc.render("to enjoy the story without", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(442)))
                text = font_desc.render("challenging combat.", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(504)))

                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(686),
                                  scale_value(100), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(716),
                                  scale_value(85), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(746),
                                  scale_value(95), scale_value(13)))

            elif im == 2:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for players who like a", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(380)))
                text = font_desc.render("balanced experience with some", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(442)))
                text = font_desc.render("challenge", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(504)))

                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(686),
                                  scale_value(126), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(716),
                                  scale_value(126), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(746),
                                  scale_value(126), scale_value(13)))

            elif im == 3:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for players who enjoy", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(380)))
                text = font_desc.render("challenging combat. Enemies will be", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(442)))
                text = font_desc.render("stronger and more aggressive.", True, WHITE)
                SCREEN.blit(text, (scale_value(160), scale_value(504)))

                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(686),
                                  scale_value(170), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(716),
                                  scale_value(180), scale_value(13)))
                pygame.draw.rect(SCREEN, HEALTH_RED,
                                 (scale_value(351), scale_value(746),
                                  scale_value(165), scale_value(13)))

            # Логотип паука
            spider_logo = load_image_safe(get_image_path("main_menu", "spider_logo_tr.png"))
            spider_logo = pygame.transform.scale(spider_logo, (scale_value(80), scale_value(80)))
            SCREEN.blit(spider_logo, (scale_value(340), scale_value(560)))

            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(155), scale_value(600)),
                             (scale_value(330), scale_value(600)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(430), scale_value(600)),
                             (scale_value(605), scale_value(600)), 1)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(335), scale_value(600)),
                               scale_value(1), 2)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(425), scale_value(600)),
                               scale_value(1), 2)

            # Подписи характеристик
            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['small'])
            text = font.render("ENEMIES", True, WHITE)
            SCREEN.blit(text, (scale_value(195), scale_value(640)))
            text = font.render("AGRESSIVE", True, WHITE)
            text.set_alpha(155)
            SCREEN.blit(text, (scale_value(195), scale_value(680)))
            text = font.render("DAMAGE", True, WHITE)
            text.set_alpha(155)
            SCREEN.blit(text, (scale_value(195), scale_value(710)))
            text = font.render("HEALTH", True, WHITE)
            text.set_alpha(155)
            SCREEN.blit(text, (scale_value(195), scale_value(740)))

            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 4
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 4
                    if event1.key == pygame.K_x:
                        st = 4
                        im = 0
                        SUBTITLES = 'OFF'
                        difficulty_map = {0: 'FN', 1: 'TA', 2: 'S', 3: 'U'}
                        DIFFICULTY = difficulty_map.get(im, 'TA')
                        DIFFICULTY_MULTIPLIER = DIFFICULTY_SETTINGS[DIFFICULTY]
                    if event1.key == pygame.K_o:
                        st = 2
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event1.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        if st == 4:
            intro_image = load_image_safe(get_image_path("main_menu", "BS_menu.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            pygame.draw.rect(SCREEN, MENU_BLUE,
                             (scale_value(140), scale_value(48),
                              scale_value(720), scale_value(500)))
            s = pygame.Surface((scale_value(720), scale_value(363)))
            s.fill(MENU_BLUE)
            s.set_alpha(125)
            SCREEN.blit(s, (scale_value(140), scale_value(500)))

            # Границы панели
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(48)),
                             (scale_value(140), scale_value(150)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(160)),
                             (scale_value(140), scale_value(163)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(173)),
                             (scale_value(140), scale_value(710)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(720)),
                             (scale_value(140), scale_value(723)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(140), scale_value(733)),
                             (scale_value(140), scale_value(861)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(860), scale_value(48)),
                             (scale_value(860), scale_value(150)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(860), scale_value(160)),
                             (scale_value(860), scale_value(163)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(860), scale_value(173)),
                             (scale_value(860), scale_value(710)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(860), scale_value(720)),
                             (scale_value(860), scale_value(723)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(860), scale_value(733)),
                             (scale_value(860), scale_value(861)), 1)

            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['normal'])
            text = font.render("BEFORE YOU START", True, WHITE)
            SCREEN.blit(text, (scale_value(160), scale_value(65)))

            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(160), scale_value(102)),
                             (scale_value(220), scale_value(102)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(225), scale_value(102)),
                             (scale_value(230), scale_value(102)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(230), scale_value(102)),
                             (scale_value(820), scale_value(102)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(165), scale_value(117)),
                             (scale_value(165), scale_value(127)), 2)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(165), scale_value(137)),
                             (scale_value(165), scale_value(465)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(165), scale_value(475)),
                             (scale_value(165), scale_value(485)), 2)

            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(175), scale_value(158 + 30 * im)),
                             (scale_value(179), scale_value(158 + 30 * im)), 1)

            # Логотип паука
            spider_logo = load_image_safe(get_image_path("main_menu", "spider_logo_tr.png"))
            spider_logo = pygame.transform.scale(spider_logo, (scale_value(80), scale_value(80)))
            SCREEN.blit(spider_logo, (scale_value(470), scale_value(780)))

            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(275), scale_value(820)),
                             (scale_value(465), scale_value(820)), 1)
            pygame.draw.line(SCREEN, WHITE,
                             (scale_value(555), scale_value(820)),
                             (scale_value(745), scale_value(820)), 1)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(475), scale_value(821)),
                               scale_value(1), 3)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(545), scale_value(821)),
                               scale_value(1), 3)

            font = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['normal'])
            text = font.render('More functions in next updates!', True, WHITE)
            SCREEN.blit(text, (scale_value(160), scale_value(505)))

            # Отрисовка выбора
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(193), scale_value(159 + 30 * im)),
                               scale_value(8), 2)
            pygame.draw.circle(SCREEN, WHITE,
                               (scale_value(193), scale_value(159 + 30 * im)),
                               scale_value(4), 2)

            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['small'])
            text = font.render("START", True, WHITE)
            text.set_alpha(255 if im == 0 else 155)
            SCREEN.blit(text, (scale_value(220), scale_value(145)))

            text = font.render("SUBTITLES", True, WHITE)
            text.set_alpha(255 if im == 1 else 155)
            SCREEN.blit(text, (scale_value(220), scale_value(175)))

            # Отображение состояния субтитров
            if SUBTITLES == 'ON':
                text = font.render("< ON >", True, WHITE)
            else:
                text = font.render("< OFF >", True, WHITE)
            SCREEN.blit(text, (scale_value(550), scale_value(175)))

            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 2
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 2
                    if event1.key in (pygame.K_LEFT, pygame.K_RIGHT) and im == 1:
                        SUBTITLES = 'ON' if SUBTITLES == 'OFF' else 'OFF'
                    if event1.key == pygame.K_x:
                        pygame.mixer.music.stop()
                        st = 5
                    if event1.key == pygame.K_o:
                        st = 3
                    if event1.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        if st == 5:
            # Анимация загрузки
            if d_arc < 2 * pi:
                d_arc += pi / 50
            else:
                d_arc = 0.0

            intro_image = load_image_safe(get_image_path("main_menu", "black_screen.webp"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            spider_logo = load_image_safe(get_image_path("main_menu", "spider_logo_tr.png"))
            spider_logo = pygame.transform.scale(spider_logo, (scale_value(70), scale_value(70)))
            SCREEN.blit(spider_logo, (SCREEN_WIDTH - scale_value(100), SCREEN_HEIGHT - scale_value(100)))

            # Анимация круга
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(100), SCREEN_HEIGHT - scale_value(100),
                             scale_value(70), scale_value(70)),
                            pi + d_arc, 5 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(100), SCREEN_HEIGHT - scale_value(100),
                             scale_value(70), scale_value(70)),
                            3 * pi / 2 + d_arc, 7 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(100), SCREEN_HEIGHT - scale_value(100),
                             scale_value(70), scale_value(70)),
                            0 + d_arc, pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(100), SCREEN_HEIGHT - scale_value(100),
                             scale_value(70), scale_value(70)),
                            pi / 2 + d_arc, 3 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(105), SCREEN_HEIGHT - scale_value(105),
                             scale_value(80), scale_value(80)),
                            0 - d_arc, pi / 2 - d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(105), SCREEN_HEIGHT - scale_value(105),
                             scale_value(80), scale_value(80)),
                            2 * pi / 3 - d_arc, 7 * pi / 6 - d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(105), SCREEN_HEIGHT - scale_value(105),
                             scale_value(80), scale_value(80)),
                            4 * pi / 3 - d_arc, 11 * pi / 6 - d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(110), SCREEN_HEIGHT - scale_value(110),
                             scale_value(90), scale_value(90)),
                            0 + d_arc, 5 * pi / 6 + d_arc)
            pygame.draw.arc(SCREEN, WHITE,
                            (SCREEN_WIDTH - scale_value(110), SCREEN_HEIGHT - scale_value(110),
                             scale_value(90), scale_value(90)),
                            pi + d_arc, 11 * pi / 6 + d_arc)

            pygame.time.wait(7)
            time += 23

            if time >= expectation:
                if vp == 0:
                    main_game()

        # Обработка событий выхода
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)
        pygame.display.update()


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
    global im, diff, musst, suit, st, dif_k
    import src.config as config

    mst, choose_sst, st = 1, '', 0
    expectation = randint(1000, 2000)

    # Использование путей из config
    pygame.mixer.music.load(MUSIC_FILES['pause_menu'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(MUSIC_VOLUME)

    red_icons_text = ['', ' MAP', 'SUITS', 'GADGETS', 'SKILLS', 'MISSIONS', 'COLLECTIONS      ', 'BENCHMARKS',
                      'CHARACTERS', 'MOVES LIST           ', '']
    equipments_icon = ['SUIT', 'SUIT POWER', 'SUIT MODS']

    # Используем иконки из папки pause_menu/Suit's Icons
    suits = [
        'cs_icon.png', 'iss_icon.png', 'ws_icon.png', 'us_icon.png',
        'ss_icon.png', 'as_icon.png', 'is_icon.png', 'ads_icon.png'
    ]

    qx, qy, mdx, mdy, ix, iy = 0, 0, 0, 0, 0, 0

    # Используем SCREEN_WIDTH и SCREEN_HEIGHT из конфига
    display_w, display_h = SCREEN_WIDTH, SCREEN_HEIGHT

    # Масштабируемые размеры для меню (оптимизировано)
    red_icons_weight = [
        scale_value(round(6.2 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(4.87 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(4.86 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(6.3 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(5.5 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(6.95 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(8.2 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(8.3 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(8.4 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(7.6 * BASE_SCREEN_WIDTH / 100)),
        scale_value(round(11.8 * BASE_SCREEN_WIDTH / 100))
    ]
    red_icons_height = scale_value(round(9.75 * BASE_SCREEN_HEIGHT / 100))

    # Предварительно вычисленные константы для оптимизации
    EQUIPMENT_PANEL_WIDTH = scale_value(0.11 * BASE_SCREEN_WIDTH)
    EQUIPMENT_PANEL_HEIGHT = scale_value(98)
    SUIT_ICON_WIDTH = scale_value(110)
    SUIT_ICON_HEIGHT = scale_value(63)
    CENTER_SUIT_WIDTH = scale_value(545)
    CENTER_SUIT_HEIGHT = scale_value(370)
    LARGE_SUIT_WIDTH = scale_value(310)
    LARGE_SUIT_HEIGHT = scale_value(620)

    while True:
        # Обработка событий (оптимизировано)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif ev.key == pygame.K_TAB:
                    pygame.mixer.music.unload()
                    return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                mdx, mdy = ev.pos[0], ev.pos[1]

                if mst == 1 and ev.button == 1:
                    # Проверка клика по области костюма
                    if (scale_value(62) < mdx < scale_value(220) and
                            scale_value(142) < mdy < scale_value(239)):
                        mst = 1.1

                elif mst == 1.1 and ev.button == 1:
                    # Проверка клика по иконкам костюмов
                    for i, suit_icon_name in enumerate(suits):
                        ix = scale_value(295 + 132 * (i % 4))
                        iy = scale_value(208 + (i // 4) * 85)

                        if (ix + 1 < mdx < ix + scale_value(109) and
                                iy + 1 < mdy < iy + scale_value(62)):
                            choose_sst = suit_icon_name

                    # Проверка клика по кнопке применения
                    if (scale_value(1349) < mdx < scale_value(1420) and
                            scale_value(226) < mdy < scale_value(256) and
                            choose_sst):
                        config.CURRENT_SUIT = choose_sst.split('_icon.png')[0]

        # Основное состояние меню (mst == 1)
        if mst == 1:
            # Фон меню паузы
            intro_image = load_image_safe(get_image_path("pause_menu", "IMG_4305.JPG"))
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))

            # Верхняя панель с иконками (оптимизировано)
            font = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(17))
            qx = 0  # Сбрасываем позицию X

            for i, weight in enumerate(red_icons_weight):
                # Определяем цвет в зависимости от активного элемента
                is_active = i == 2  # SUITS активен при mst == 1
                color = (161, 3, 34) if is_active else (255, 0, 59)

                # Рисуем прямоугольник иконки
                pygame.draw.rect(SCREEN, color, (qx, 0, weight, red_icons_height))
                if is_active:
                    pygame.draw.rect(SCREEN, WHITE, (qx, 0, weight, scale_value(6)))

                # Текст иконки
                text = font.render(red_icons_text[i], True, (28, 6, 46))
                tx = qx + weight // (len(red_icons_text[i]) + 2)
                ty = red_icons_height // 2 - scale_value(8)
                SCREEN.blit(text, (tx, ty))

                # Разделитель
                qx += weight
                pygame.draw.rect(SCREEN, (28, 6, 46), (qx, 0, scale_value(2), red_icons_height))
                qx += scale_value(2)

            # Панель оборудования (оптимизировано)
            base_x = (red_icons_weight[0] // 2) + scale_value(15)
            for i, equipment in enumerate(equipments_icon):
                text = font.render(equipment, True, WHITE)
                ty = red_icons_height + scale_value(15) + scale_value(0.17 * BASE_SCREEN_HEIGHT * i)
                SCREEN.blit(text, (base_x, ty))

                # Декоративные элементы панели
                panel_y = ty + scale_value(27)
                pygame.draw.rect(SCREEN, WHITE,
                                 (base_x, ty + scale_value(23), scale_value(0.02 * BASE_SCREEN_WIDTH), 1))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y, EQUIPMENT_PANEL_WIDTH, scale_value(3)))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y + scale_value(8), EQUIPMENT_PANEL_WIDTH, 1))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y + scale_value(108), EQUIPMENT_PANEL_WIDTH, 1))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y + scale_value(8), 1, scale_value(100)))
                pygame.draw.rect(SCREEN, WHITE,
                                 (base_x + EQUIPMENT_PANEL_WIDTH, panel_y + scale_value(8), 1, scale_value(100)))
                pygame.draw.rect(SCREEN, WHITE, (base_x - scale_value(5), panel_y, 1, scale_value(30)))

            # Текущая иконка костюма
            tx = (red_icons_weight[0] // 2) + scale_value(16)
            ty = red_icons_height + scale_value(51)

            current_suit_icon = load_image_safe(
                os.path.join(MENU_PAUSE_DIR, "Suit's Icons", f"{config.CURRENT_SUIT}_icon.png"))
            current_suit_icon = pygame.transform.scale(current_suit_icon,
                                                       (EQUIPMENT_PANEL_WIDTH - scale_value(3), EQUIPMENT_PANEL_HEIGHT))
            SCREEN.blit(current_suit_icon, (tx + scale_value(1), ty + scale_value(1)))

            # Правая панель информации
            pygame.draw.rect(SCREEN, UI_BACKGROUND, (qx, 0, display_w - qx, display_h))
            pygame.draw.rect(SCREEN, UI_ACCENT, (qx - scale_value(8), 0, scale_value(3), red_icons_height))
            pygame.draw.rect(SCREEN, WHITE, (qx, red_icons_height, display_w - qx, scale_value(50)))
            pygame.draw.ellipse(SCREEN, WHITE, (qx, red_icons_height, 1, display_h - red_icons_height), 1)

            # Заголовок "EQUIPPED"
            font_large = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(27))
            text = font_large.render('EQUIPPED', True, UI_ACCENT)
            tx_info, ty_info = qx + scale_value(8), red_icons_height + scale_value(10)
            SCREEN.blit(text, (tx_info, ty_info))

            # Отображение текущего экипированного костюма
            equipped_suit_icon = load_image_safe(
                os.path.join(MENU_PAUSE_DIR, "Suit's Icons", f"{config.CURRENT_SUIT}_icon.png"))
            equipped_suit_icon = pygame.transform.scale(equipped_suit_icon, (SUIT_ICON_WIDTH, SUIT_ICON_HEIGHT))
            SCREEN.blit(equipped_suit_icon, (qx + scale_value(10), red_icons_height + scale_value(66)))

            font_medium = pygame.font.Font(get_font_path('monospace_regular'), scale_font_size(18))
            suit_name = SUITS.get(config.CURRENT_SUIT, 'Classic Suit')
            text = font_medium.render(suit_name, True, WHITE)
            tx_name, ty_name = qx + scale_value(125), red_icons_height + scale_value(71)
            SCREEN.blit(text, (tx_name, ty_name))
            pygame.draw.aaline(SCREEN, WHITE, [tx_name, ty_name + scale_value(23)],
                               [display_w, ty_name + scale_value(23)])

            # Декоративные эллипсы
            ellipse_center_x = display_w // 3.5
            ellipse_y = scale_value(590)
            pygame.draw.ellipse(SCREEN, WHITE,
                                (ellipse_center_x, ellipse_y, display_w // 2.3, scale_value(200)), 3)
            pygame.draw.ellipse(SCREEN, WHITE,
                                (ellipse_center_x + scale_value(65), ellipse_y + scale_value(25),
                                 display_w // 2.3 - scale_value(130), scale_value(140)), 1)
            pygame.draw.ellipse(SCREEN, WHITE,
                                (ellipse_center_x + scale_value(228), ellipse_y + scale_value(60),
                                 display_w // 2.3 - scale_value(460), scale_value(70)), 1)

            # Декоративные линии (оптимизировано)
            decor_lines = [
                # Основные соединительные линии
                [[ellipse_center_x + display_w // 4.6 - scale_value(5), ellipse_y + 1],
                 [ellipse_center_x + scale_value(228) + (display_w // 2.3 - scale_value(460)) // 2,
                  ellipse_y + scale_value(57)]],
                [[ellipse_center_x + scale_value(230) + (display_w // 2.3 - scale_value(460)) // 2,
                  ellipse_y + scale_value(131)],
                 [ellipse_center_x + display_w // 4.6 + scale_value(4), ellipse_y + scale_value(197)]],
                # Вспомогательные линии
                [[ellipse_center_x + display_w // 9.2 - scale_value(22), ellipse_y + scale_value(20)],
                 [ellipse_center_x + scale_value(228) + (display_w // 2.3 - scale_value(460)) // 4 - scale_value(13),
                  ellipse_y + scale_value(67)]],
                [[ellipse_center_x + scale_value(390), ellipse_y + scale_value(117)],
                 [ellipse_center_x + scale_value(530), ellipse_y + scale_value(174)]],
                # Горизонтальные линии
                [[ellipse_center_x + 1, ellipse_y + scale_value(93)],
                 [ellipse_center_x + scale_value(228), ellipse_y + scale_value(93)]],
                [[ellipse_center_x + scale_value(407), ellipse_y + scale_value(93)],
                 [ellipse_center_x + display_w // 2.3, ellipse_y + scale_value(93)]],
                # Обратные линии
                [[ellipse_center_x + display_w // 9.2 - scale_value(30), ellipse_y + scale_value(179)],
                 [ellipse_center_x + scale_value(228) + (display_w // 2.3 - scale_value(460)) // 4 - scale_value(13),
                  ellipse_y + scale_value(121)]],
                [[ellipse_center_x + scale_value(500), ellipse_y + scale_value(20)],
                 [ellipse_center_x + scale_value(384), ellipse_y + scale_value(70)]]
            ]

            for line in decor_lines:
                pygame.draw.aaline(SCREEN, WHITE, line[0], line[1])

            # Отображение костюма в центре
            center_suit_path = os.path.join(MENU_PAUSE_DIR, "Suits for Base Menu", f"menu_{config.CURRENT_SUIT}.png")
            center_suit = load_image_safe(center_suit_path)
            center_suit = pygame.transform.scale(center_suit, (CENTER_SUIT_WIDTH, CENTER_SUIT_HEIGHT))
            SCREEN.blit(center_suit, (ellipse_center_x + scale_value(40), scale_value(410)))

            qx, qy = 0, 0  # Сброс позиций

        # Состояние выбора костюма (mst == 1.1)
        elif mst == 1.1:
            # Фон меню паузы
            intro_image = load_image_safe(get_image_path("pause_menu", "IMG_4305.JPG"))
            intro_image = pygame.transform.scale(intro_image, (display_w, display_h))
            SCREEN.blit(intro_image, (0, 0))

            # Верхняя панель с иконками
            font = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(17))
            qx = 0

            for i, weight in enumerate(red_icons_weight):
                is_active = i == 2  # SUITS активен при mst == 1.1
                color = (161, 3, 34) if is_active else (255, 0, 59)

                pygame.draw.rect(SCREEN, color, (qx, 0, weight, red_icons_height))
                if is_active:
                    pygame.draw.rect(SCREEN, WHITE, (qx, 0, weight, scale_value(6)))

                text = font.render(red_icons_text[i], True, UI_ACCENT)
                tx = qx + weight // (len(red_icons_text[i]) + 2)
                ty = red_icons_height // 2 - scale_value(8)
                SCREEN.blit(text, (tx, ty))

                qx += weight
                pygame.draw.rect(SCREEN, UI_ACCENT, (qx, 0, scale_value(2), red_icons_height))
                qx += scale_value(2)

            # Панель оборудования (аналогично mst == 1)
            base_x = (red_icons_weight[0] // 2) + scale_value(15)
            for i, equipment in enumerate(equipments_icon):
                text = font.render(equipment, True, WHITE)
                ty = red_icons_height + scale_value(15) + scale_value(0.17 * BASE_SCREEN_HEIGHT * i)
                SCREEN.blit(text, (base_x, ty))

                panel_y = ty + scale_value(27)
                pygame.draw.rect(SCREEN, WHITE,
                                 (base_x, ty + scale_value(23), scale_value(0.02 * BASE_SCREEN_WIDTH), 1))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y, EQUIPMENT_PANEL_WIDTH, scale_value(3)))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y + scale_value(8), EQUIPMENT_PANEL_WIDTH, 1))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y + scale_value(108), EQUIPMENT_PANEL_WIDTH, 1))
                pygame.draw.rect(SCREEN, WHITE, (base_x, panel_y + scale_value(8), 1, scale_value(100)))
                pygame.draw.rect(SCREEN, WHITE,
                                 (base_x + EQUIPMENT_PANEL_WIDTH, panel_y + scale_value(8), 1, scale_value(100)))
                pygame.draw.rect(SCREEN, WHITE, (base_x - scale_value(5), panel_y, 1, scale_value(30)))

            # Текущая иконка костюма
            tx = (red_icons_weight[0] // 2) + scale_value(16)
            ty = red_icons_height + scale_value(51)

            current_suit_icon = load_image_safe(
                os.path.join(MENU_PAUSE_DIR, "Suit's Icons", f"{config.CURRENT_SUIT}_icon.png"))
            current_suit_icon = pygame.transform.scale(current_suit_icon,
                                                       (EQUIPMENT_PANEL_WIDTH - scale_value(3), EQUIPMENT_PANEL_HEIGHT))
            SCREEN.blit(current_suit_icon, (tx + scale_value(1), ty + scale_value(1)))

            # Декоративные линии перехода
            line_start_x = tx + EQUIPMENT_PANEL_WIDTH
            line_y = red_icons_height + scale_value(97)
            pygame.draw.aalines(SCREEN, WHITE, False,
                                [[line_start_x, line_y], [scale_value(270), line_y]])
            pygame.draw.rect(SCREEN, WHITE,
                             (scale_value(243), line_y - scale_value(2), scale_value(6), scale_value(6)))
            pygame.draw.lines(SCREEN, WHITE, False,
                              [[scale_value(290), line_y], [scale_value(370), line_y]], 2)
            pygame.draw.lines(SCREEN, WHITE, False,
                              [[scale_value(380), line_y], [scale_value(810), line_y]])

            # Заголовок "SUIT"
            font_title = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(22))
            text = font_title.render('SUIT', True, WHITE)
            SCREEN.blit(text, (scale_value(290), red_icons_height + scale_value(65)))

            # Обработка клика по текущей иконке для возврата
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mdx, mdy = ev.pos[0], ev.pos[1]
                    if (tx + scale_value(1) < mdx < tx + EQUIPMENT_PANEL_WIDTH - scale_value(3) and
                            ty + scale_value(1) < mdy < ty + EQUIPMENT_PANEL_HEIGHT):
                        mst = 1

            # Правая панель информации
            pygame.draw.rect(SCREEN, UI_BACKGROUND, (qx, 0, display_w - qx, display_h))
            pygame.draw.rect(SCREEN, UI_ACCENT, (qx - scale_value(8), 0, scale_value(3), red_icons_height))
            pygame.draw.rect(SCREEN, WHITE, (qx, red_icons_height, display_w - qx, scale_value(50)))
            pygame.draw.ellipse(SCREEN, WHITE, (qx, red_icons_height, 1, display_h - red_icons_height), 1)

            # Заголовок "EQUIPPED"
            font_large = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(27))
            text = font_large.render('EQUIPPED', True, UI_ACCENT)
            tx_info, ty_info = qx + scale_value(8), red_icons_height + scale_value(10)
            SCREEN.blit(text, (tx_info, ty_info))

            # Отображение выбранного или текущего костюма
            display_suit = choose_sst if choose_sst else f"{config.CURRENT_SUIT}_icon.png"
            suit_icon_path = os.path.join(MENU_PAUSE_DIR, "Suit's Icons", display_suit)
            displayed_suit_icon = load_image_safe(suit_icon_path)
            displayed_suit_icon = pygame.transform.scale(displayed_suit_icon, (SUIT_ICON_WIDTH, SUIT_ICON_HEIGHT))
            SCREEN.blit(displayed_suit_icon, (qx + scale_value(10), red_icons_height + scale_value(66)))

            # Название костюма
            font_medium = pygame.font.Font(get_font_path('monospace_regular'), scale_font_size(18))
            suit_code = display_suit.split('_icon.png')[0]
            suit_display_name = SUITS.get(suit_code, 'Unknown Suit')
            text = font_medium.render(suit_display_name, True, WHITE)
            tx_name, ty_name = qx + scale_value(125), red_icons_height + scale_value(71)
            SCREEN.blit(text, (tx_name, ty_name))
            pygame.draw.aaline(SCREEN, WHITE, [tx_name, ty_name + scale_value(23)],
                               [display_w, ty_name + scale_value(23)])

            # Рамка для выбора костюмов
            pygame.draw.rect(SCREEN, WHITE,
                             (scale_value(270), scale_value(145), scale_value(560), scale_value(655)), 1)

            # Декоративные угловые элементы
            corner_x = scale_value(817)
            corner_top = scale_value(136)
            corner_bottom = scale_value(809)

            # Верхний правый угол
            pygame.draw.aalines(SCREEN, WHITE, False,
                                [[corner_x, corner_top], [corner_x + scale_value(21), corner_top],
                                 [corner_x + scale_value(21), corner_top + scale_value(19)]])
            pygame.draw.lines(SCREEN, WHITE, False,
                              [[corner_x + scale_value(21), corner_top + scale_value(23)],
                               [corner_x + scale_value(21), corner_top + scale_value(43)]], 3)

            # Нижний правый угол
            pygame.draw.aalines(SCREEN, WHITE, False,
                                [[corner_x, corner_bottom], [corner_x + scale_value(21), corner_bottom],
                                 [corner_x + scale_value(21), corner_bottom - scale_value(19)]])
            pygame.draw.lines(SCREEN, WHITE, False,
                              [[corner_x + scale_value(21), corner_bottom - scale_value(23)],
                               [corner_x + scale_value(21), corner_bottom - scale_value(43)]], 3)

            # Отображение всех костюмов в сетке
            for i, suit_icon_name in enumerate(suits):
                suit_icon_img = load_image_safe(os.path.join(MENU_PAUSE_DIR, "Suit's Icons", suit_icon_name))
                suit_icon_img = pygame.transform.scale(suit_icon_img, (SUIT_ICON_WIDTH, SUIT_ICON_HEIGHT))

                # Вычисление позиции в сетке 4x2
                ix = scale_value(295 + 132 * (i % 4))
                iy = scale_value(208 + (i // 4) * 85)

                SCREEN.blit(suit_icon_img, (ix, iy))

            # Кнопка USE/USED
            font_button = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(22))
            is_different_suit = choose_sst and config.CURRENT_SUIT != choose_sst.split('_icon.png')[0]

            if is_different_suit:
                button_text = 'USE'
                button_width = scale_value(63)
            else:
                button_text = 'USED'
                button_width = scale_value(73)

            text = font_button.render(button_text, True, WHITE)
            tx_button, ty_button = qx + scale_value(175), red_icons_height + scale_value(140)
            SCREEN.blit(text, (tx_button, ty_button))

            # Рамка кнопки
            pygame.draw.rect(SCREEN, WHITE,
                             (tx_button - scale_value(10), ty_button - scale_value(5),
                              button_width, scale_value(32)), 2)

            # Линии от кнопки
            pygame.draw.aaline(SCREEN, WHITE,
                               [tx_button - scale_value(175), ty_button + scale_value(13)],
                               [tx_button - scale_value(11), ty_button + scale_value(13)])
            pygame.draw.aaline(SCREEN, WHITE,
                               [tx_button + button_width - scale_value(10), ty_button + scale_value(13)],
                               [display_w, ty_button + scale_value(13)])

            # Декоративный эллипс справа
            ellipse_right_x = scale_value(865)
            ellipse_right_y = scale_value(730)
            pygame.draw.ellipse(SCREEN, WHITE,
                                (ellipse_right_x, ellipse_right_y, scale_value(290), scale_value(85)), 2)
            pygame.draw.ellipse(SCREEN, WHITE,
                                (ellipse_right_x + scale_value(38), ellipse_right_y + scale_value(10),
                                 scale_value(220), scale_value(55)), 1)
            pygame.draw.ellipse(SCREEN, WHITE,
                                (ellipse_right_x + scale_value(98), ellipse_right_y + scale_value(21),
                                 scale_value(90), scale_value(30)), 1)

            # Декоративные линии вокруг эллипса
            decor_lines_right = [
                [[scale_value(1012), ellipse_right_y + 1], [scale_value(1010), ellipse_right_y + scale_value(20)]],
                [[scale_value(919), ellipse_right_y + scale_value(11)],
                 [scale_value(981), ellipse_right_y + scale_value(23)]],
                [[ellipse_right_x + 1, ellipse_right_y + scale_value(35)],
                 [scale_value(962), ellipse_right_y + scale_value(35)]],
                [[scale_value(895), ellipse_right_y + scale_value(66)],
                 [scale_value(976), ellipse_right_y + scale_value(46)]],
                [[scale_value(1008), ellipse_right_y + scale_value(50)],
                 [scale_value(1006), ellipse_right_y + scale_value(80)]],
                [[scale_value(1035), ellipse_right_y + scale_value(48)],
                 [scale_value(1120), ellipse_right_y + scale_value(70)]],
                [[scale_value(1053), ellipse_right_y + scale_value(35)],
                 [scale_value(1150), ellipse_right_y + scale_value(35)]],
                [[scale_value(1035), ellipse_right_y + scale_value(24)],
                 [scale_value(1105), ellipse_right_y + scale_value(10)]]
            ]

            for line in decor_lines_right:
                pygame.draw.aaline(SCREEN, WHITE, line[0], line[1])

            # Большое изображение выбранного костюма справа
            large_suit_path = os.path.join(MENU_PAUSE_DIR, "Suits for Base Menu", f"menu_{suit_code}_s.png")
            large_suit = load_image_safe(large_suit_path)
            large_suit = pygame.transform.scale(large_suit, (LARGE_SUIT_WIDTH, LARGE_SUIT_HEIGHT))
            SCREEN.blit(large_suit, (scale_value(860), scale_value(210)))

            qx, qy = 0, 0  # Сброс позиций

        pygame.display.update()
        pygame.time.wait(40)


def draw_damage_flash(screen, player):
    """Отрисовка эффектов повреждения, лечения и смерти с масштабированием"""
    flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    # Предварительно вычисленные значения для оптимизации
    pulse_speed_death = 0.015
    pulse_speed_normal = 0.01
    max_alpha_death = 200
    max_alpha_normal = 128

    # Приоритет: смерть > урон > лечение
    if player.death_flash_timer > 0:
        # Эффект смерти - красная рамка увеличенного размера
        pulse = abs(math.sin(pygame.time.get_ticks() * pulse_speed_death)) * 180
        border_width = scale_value(40)  # Масштабируемая толщина рамки
        alpha = min(max_alpha_death, pulse)

        # Рисуем толстую красную рамку по краям экрана
        border_rects = [
            (0, 0, SCREEN_WIDTH, border_width),  # Верх
            (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width),  # Низ
            (0, 0, border_width, SCREEN_HEIGHT),  # Лево
            (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT)  # Право
        ]

        for rect in border_rects:
            pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)), rect)

        # Дополнительно: легкое красное затемнение всего экрана
        overlay_alpha = min(80, pulse * 0.4)
        flash_surface.fill((255, 0, 0, int(overlay_alpha)))

    elif player.damage_flash_timer > 0:
        # Эффект урона (красная рамка) - обычный размер
        pulse = abs(math.sin(pygame.time.get_ticks() * pulse_speed_normal)) * max_alpha_normal
        border_width = scale_value(20)  # Масштабируемая толщина рамки
        alpha = min(FLASH_ALPHA, pulse)

        border_rects = [
            (0, 0, SCREEN_WIDTH, border_width),
            (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width),
            (0, 0, border_width, SCREEN_HEIGHT),
            (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT)
        ]

        for rect in border_rects:
            pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)), rect)

    elif player.heal_flash_timer > 0:
        # Эффект лечения (зеленая рамка)
        pulse = abs(math.sin(pygame.time.get_ticks() * pulse_speed_normal)) * max_alpha_normal
        border_width = scale_value(20)  # Масштабируемая толщина рамки
        alpha = min(FLASH_ALPHA, pulse)

        border_rects = [
            (0, 0, SCREEN_WIDTH, border_width),
            (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width),
            (0, 0, border_width, SCREEN_HEIGHT),
            (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT)
        ]

        for rect in border_rects:
            pygame.draw.rect(flash_surface, (0, 255, 0, int(alpha)), rect)

    # Отображаем поверхность с эффектом
    if player.is_flashing():
        screen.blit(flash_surface, (0, 0))


def save_current_game_state(player, enemies, sdvigx, sdvigy):
    """Сохраняет текущее состояние игры в словарь"""
    state = {
        'player_health': player.health,
        'player_exp': player.exp,
        'player_concentration': player.concentration,
        'sdvigx': sdvigx,
        'sdvigy': sdvigy,
        'player_st': player.st,
        'player_coords_increase': player.coords_increase,
        'player_SMRt': player.SMRt,
        'player_on_ground': player.on_ground,
        'player_facing_right': player.facing_right,
        'player_web_swinging': player.web_swinging,
        'player_swing_cycle': player.swing_cycle,
        'enemies': []
    }

    # Сохраняем каждого врага
    for enemy in enemies:
        state['enemies'].append({
            'world_x': enemy.world_x,
            'health': enemy.health,
            'state': enemy.state,
            'facing_right': enemy.facing_right
        })

    return state


def restore_game_state(player, enemies, saved_state):
    """Восстанавливает состояние игры из сохраненного словаря"""
    # Восстанавливаем состояние игрока
    player.health = saved_state['player_health']
    player.exp = saved_state['player_exp']
    player.concentration = saved_state['player_concentration']
    player.st = saved_state['player_st']
    player.coords_increase = saved_state['player_coords_increase']
    player.SMRt = saved_state['player_SMRt']
    player.on_ground = saved_state['player_on_ground']
    player.facing_right = saved_state['player_facing_right']
    player.web_swinging = saved_state['player_web_swinging']
    player.swing_cycle = saved_state['player_swing_cycle']

    # Восстанавливаем состояние врагов
    for i, enemy_state in enumerate(saved_state['enemies']):
        if i < len(enemies):
            enemies[i].world_x = enemy_state['world_x']
            enemies[i].health = enemy_state['health']
            enemies[i].state = enemy_state['state']
            enemies[i].facing_right = enemy_state['facing_right']

    # Возвращаем сдвиги камеры
    global sdvigx, sdvigy
    sdvigx = saved_state['sdvigx']
    sdvigy = saved_state['sdvigy']


def main_game():
    from src.game.player import Player
    from src.game.enemy import Enemy
    from src import config

    # Глобальная переменная для сохранения состояния игры
    global game_state_before_menu
    game_state_before_menu = None

    # Объявляем глобальные переменные
    global sdvigy, DIFFICULTY, MUSIC_STATUS, CURRENT_SUIT, st, CURRENT_CUTSCENE, SUBTITLES

    CURRENT_CUTSCENE += 1
    st = -100

    # Глобальная переменная для хранения выбранного слота сохранения
    selected_save_slot = 6  # По умолчанию 6 слот

    web_swing_speed_x = 0
    web_swing_speed_y = 0

    # Загрузка фонов с масштабированием
    bg = load_image_safe(get_image_path("backgrounds", "fhomewthspandpavmnt.jpg"), convert_alpha=False)
    bg = pygame.transform.scale(bg, (scale_value(1414), scale_value(2000)))
    road = load_image_safe(get_image_path("backgrounds", "road.jpeg"), convert_alpha=False)
    road = pygame.transform.scale(road, (scale_value(2011), scale_value(354)))

    # Инициализация переменных
    sdvigx = -500
    sdvigy = 1000  # Начальное положение для падения 1400
    tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
    hp = 100

    # Создаем игрока
    player = Player()
    player.st = st
    player.health = hp

    # Определяем выбранный слот сохранения
    try:
        with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="r") as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 2 and parts[1] == "Выбрана":
                    selected_save_slot = int(parts[0])
                    break
    except:
        selected_save_slot = 6  # По умолчанию 6 слот

    # Создаем врагов
    enemies = [
        Enemy(world_x=1500),  # Враг на позиции X, на дороге
        Enemy(world_x=2200),
        Enemy(world_x=2900),
        Enemy(world_x=3300),
        Enemy(world_x=3500),
    ]

    # Предварительно вычисленные константы для оптимизации
    HEALTH_BAR_POS = (scale_value(50), scale_value(50))
    HEALTH_BAR_SIZE = (scale_value(400), scale_value(45))
    HEALTH_TEXT_POS = (scale_value(460), scale_value(53))
    EXP_TEXT_POS = (SCREEN_WIDTH - scale_value(250), scale_value(53))
    HINT_POS_Y = scale_value(150)
    GROUND_LEVEL = scale_value(-415)

    # Основной игровой цикл
    clock = pygame.time.Clock()
    while True:
        ticks = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if config.SHAKE_TIMER > 0:
            config.SHAKE_TIMER -= 1
            offset_x = random.uniform(-config.SHAKE_INTENSITY, config.SHAKE_INTENSITY)
            offset_y = random.uniform(-config.SHAKE_INTENSITY, config.SHAKE_INTENSITY)
        else:
            offset_x = 0
            offset_y = 0

        # Обработка музыки
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(MUSIC_FILES['gameplay'])
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(MUSIC_VOLUME)

        # Обработка состояний движения
        if player.st == -100:  # Начальное падение
            # Разделяем на два диапазона высоты как в старом коде

            # В блоке быстрого падения замените музыку на звук:
            if 900 <= sdvigy:
                # Быстрое падение: sdvigy -= 6
                if player.coords_increase % 3 == 0:
                    sdvigx -= 1
                sdvigy -= 6
                player.coords_increase += 1

                # Воспроизводим звук воздуха как Sound (а не Music)
                if not hasattr(player, 'air_sound_played') or not player.air_sound_played:
                    try:
                        # Используем SOUND_FILES, а не MUSIC_FILES
                        air_sound_path = SOUND_FILES.get('air_sound') or os.path.join(SOUNDS_DIR, "air_sound.mp3")
                        if os.path.exists(air_sound_path):
                            air_sound = pygame.mixer.Sound(air_sound_path)
                            air_sound.set_volume(SOUND_VOLUME)
                            air_sound.play()
                            player.air_sound_played = True
                            print("[SOUND] Запущен звук воздуха")
                        else:
                            print(f"[SOUND] Файл не найден: {air_sound_path}")
                    except Exception as e:
                        print(f"[SOUND] Ошибка воспроизведения звука воздуха: {e}")

            # В блоке замедленного падения (-330 <= sdvigy <= 600) оставьте только движение:
            elif -330 <= sdvigy <= 1000:
                # Замедленное падение: sdvigy -= 2
                if player.coords_increase % 3 == 0:
                    sdvigx -= 1
                sdvigy -= 2
                player.coords_increase += 1

            # Если вышли за нижний предел, продолжаем обычное падение без подсказки
            else:
                if player.coords_increase % 3 == 0:
                    sdvigx -= 1
                sdvigy -= 2
                player.coords_increase += 1

        elif (player.st == 1 or player.st == -1) and keys[pygame.K_LSHIFT]:
            # Горизонталь: вправо для st=1, влево для st=-1
            horiz_speed = 4 * (0.95 ** player.swing_cycle)
            if player.st == 1:  # Полёт вправо
                sdvigx -= horiz_speed
            else:  # Полёт влево (st = -1)
                sdvigx += horiz_speed

            # Вертикаль: одинаковая траектория для обоих направлений
            vert_amp = 3 * (0.95 ** player.swing_cycle)
            if player.coords_increase < 310:
                phase = player.coords_increase / 310
                angle = phase * math.pi
                vertical_movement = -math.sin(angle) * vert_amp
            else:
                phase = (player.coords_increase - 310) / 310
                angle = math.pi + phase * math.pi
                vertical_movement = -math.sin(angle) * vert_amp

            sdvigy += vertical_movement
            player.continue_web_swing()

        # Движение при ходьбе
        if player.st == 0 and player.on_ground and (keys[pygame.K_a] or keys[pygame.K_d]):
            sdvigx = player.apply_movement(sdvigx)

        # Движение при отпускании паутины
        elif player.st == 2:
            if player.facing_right:  # Двигаем вправо если смотрит вправо
                sdvigx -= 4
            else:  # Двигаем влево если смотрит влево
                sdvigx += 4
            sdvigy += 2

        # Движение при свободном падении
        elif player.st == 3:
            if keys[pygame.K_LSHIFT] and sdvigy > 150:  # Добавляем возможность вернуться к полёту на паутине
                player.start_web_swing(ticks)
                player.coords_increase = 0
                player.SMRt = -50
            elif player.facing_right:  # Смотрит вправо
                sdvigx -= 1
                sdvigy -= 5
            else:  # Смотрит влево
                sdvigx += 1
                sdvigy -= 5

        # Движение при прыжке
        elif player.st == 4:
            # Логика прыжка - движение вверх
            if player.facing_right:
                sdvigx -= 2  # Небольшое движение вперед при прыжке
            else:
                sdvigx += 2

            sdvigy += 12  # Движение вверх (отрицательное значение для прыжка)

            # Переход в свободное падение после достижения высшей точки
            player.coords_increase += 1
            if player.coords_increase >= 55:  # Через 30 кадров переходим в падение
                player.st = 3
                player.coords_increase = 0

        # Обновление игрока
        player.update(keys, ticks, sdvigy)

        # Обновление врагов (передаем callback для тряски камеры)
        for enemy in enemies:
            enemy.update(player, sdvigx, enemies)

        # Синхронизация переменных
        st = player.st
        hp = player.health

        # Проверка: если игрок перешёл в состояние 0 из -100, установить sdvigy на "землю"
        if st == 0 and player.on_ground:
            sdvigy = -420

        # Обработка смерти игрока
        if player.health <= 0 and not player.is_dead:
            # Первый раз когда здоровье достигает 0
            player.die()
            MUSIC_STATUS = 0
            pygame.mixer.music.unload()

        # Если игрок мертв, обрабатываем эффекты смерти
        if player.is_dead:
            pygame.mixer.music.unload()
            # Воспроизводим звук смерти один раз в начале смерти
            if not player.death_sound_played:
                try:
                    death_sound_path = SOUND_FILES['death']
                    if os.path.exists(death_sound_path):
                        ss = pygame.mixer.Sound(death_sound_path)
                        ss.set_volume(SOUND_VOLUME)
                        ss.play()
                        player.death_sound_played = True
                        print("Звук смерти воспроизведен")
                except Exception as e:
                    print(f"Ошибка звука смерти: {e}")

            # Ждем пока завершится задержка перед показом экрана смерти
            if player.death_delay_timer <= 0 and not player.death_screen_shown:
                # Устанавливаем флаг, что экран смерти показан
                player.death_screen_shown = True

                # Отрисовываем экран смерти с масштабированием
                SCREEN.fill(BLACK)
                font = pygame.font.Font(get_font_path('gulag'), scale_font_size(25))
                text = font.render('!HELP!', True, RED)
                text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
                SCREEN.blit(text, (text_x, scale_value(250)))

                pygame.draw.line(SCREEN, RED,
                                 [scale_value(400), scale_value(280)],
                                 [scale_value(1080), scale_value(280)], 2)
                pygame.draw.line(SCREEN, RED,
                                 [scale_value(400), scale_value(380)],
                                 [scale_value(1080), scale_value(380)], 2)

                font = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(55))
                text = font.render("YOU'RE FAILED, BUDDY", True, RED)
                text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
                SCREEN.blit(text, (text_x, scale_value(300)))
                pygame.display.update()

                # Ждем 1.5 секунды (1500 мс) перед сбросом
                pygame.time.wait(1500)

                # ПОЛНЫЙ СБРОС ИГРЫ
                st = 0
                sdvigy = -330
                hp = 100
                MUSIC_STATUS = -1

                # Полный сброс игрока
                player.reset()

                # Сброс врагов
                enemies = [
                    Enemy(world_x=1500),
                    Enemy(world_x=2200),
                    Enemy(world_x=2900),
                    Enemy(world_x=3300),
                    Enemy(world_x=3500),
                ]

                # Сброс камеры и других переменных
                sdvigx = -500
                player.coords_increase = 0

                print("Игра перезапущена после смерти")

        # Отрисовка
        SCREEN.fill(BLACK)

        # Отрисовка фона бесконечно в обе стороны
        bg_width = bg.get_width()
        road_width = road.get_width()

        # Вычисляем offset для seamless
        bg_offset = sdvigx % bg_width
        if bg_offset > 0:
            bg_offset -= bg_width

        road_offset = sdvigx % road_width
        if road_offset > 0:
            road_offset -= road_width

        # Количество тайлов: достаточно, чтобы покрыть экран + запас
        tiles = math.ceil(SCREEN_WIDTH / bg_width) + 2  # Для bg
        i = -1  # Начинать с -1 для левой стороны
        while i < tiles:
            SCREEN.blit(bg, (bg_width * i + bg_offset + offset_x, -2000 + SCREEN_HEIGHT - 100 + sdvigy + offset_y))
            i += 1

        # Аналогично для road
        tiles = math.ceil(SCREEN_WIDTH / road_width) + 2
        i = -1
        while i < tiles:
            SCREEN.blit(road, (road_width * i + road_offset + offset_x, 800 + sdvigy + offset_y))
            i += 1

        # Отрисовка здоровья игрока с масштабированием
        health_bar_width, health_bar_height = HEALTH_BAR_SIZE
        health_bar_x, health_bar_y = HEALTH_BAR_POS

        pygame.draw.rect(SCREEN, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height),
                         scale_value(5))

        # Расчет ширины здоровья
        health_width = (player.health / PLAYER_MAX_HEALTH) * (health_bar_width - scale_value(10))
        if health_width < 0:
            health_width = 0

        pygame.draw.rect(SCREEN, HEALTH_GREEN,
                         (health_bar_x + scale_value(5), health_bar_y + scale_value(5),
                          health_width, health_bar_height - scale_value(10)))

        # Отрисовка шкалы концентрации (под здоровьем)
        concentration_bar_width = health_bar_width // 2  # В 2 раза короче
        concentration_bar_height = health_bar_height // 2  # В 2 раза меньше по высоте
        concentration_y = health_bar_y + health_bar_height + scale_value(10)  # Отступ от здоровья

        # Рамка концентрации (белая как у здоровья)
        pygame.draw.rect(SCREEN, WHITE,
                         (health_bar_x, concentration_y, concentration_bar_width, concentration_bar_height),
                         scale_value(3))

        # Расчет ширины заполнения концентрации
        concentration_fill_width = (player.concentration / 100) * (concentration_bar_width - scale_value(6))
        if concentration_fill_width < 0:
            concentration_fill_width = 0

        # Заполнение концентрации (полупрозрачный белый)
        concentration_surface = pygame.Surface((concentration_fill_width, concentration_bar_height - scale_value(6)),
                                               pygame.SRCALPHA)
        concentration_surface.fill((255, 255, 255, 180))  # Белый с альфой 180
        SCREEN.blit(concentration_surface,
                    (health_bar_x + scale_value(3), concentration_y + scale_value(3)))

        # Текст здоровья - ИСПРАВЛЕННАЯ ПОЗИЦИЯ
        font = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(30))
        health_text = font.render(f"{int(player.health)}", True, WHITE)

        # Вычисляем правильную позицию текста - правее шкалы здоровья
        health_text_x = health_bar_x + health_bar_width + scale_value(15)  # Отступ справа от шкалы
        health_text_y = health_bar_y + scale_value(3)
        SCREEN.blit(health_text, (health_text_x, health_text_y))

        # Отрисовка опыта с фоном (справа от здоровья)
        exp_text = font.render(f"Опыт: {player.exp}", True, WHITE)
        # Получаем размеры текста
        text_width = exp_text.get_width()
        text_height = exp_text.get_height()
        # Создаем фон для опыта (такой же, как у подсказок)
        exp_bg_width = text_width + scale_value(20)  # Отступы по 10px с каждой стороны
        exp_bg_height = text_height + scale_value(10)  # Отступы по 5px сверху и снизу
        exp_bg = pygame.Surface((exp_bg_width, exp_bg_height), pygame.SRCALPHA)
        exp_bg.fill((145, 145, 145, 100))  # Тот же серый с прозрачностью
        # Позиция фона (выровнена с текстом)
        exp_bg_x = EXP_TEXT_POS[0] - scale_value(10)  # Смещаем на 10px левее текста
        exp_bg_y = EXP_TEXT_POS[1] - scale_value(5)  # Смещаем на 5px выше текста

        # Отрисовываем фон и текст
        SCREEN.blit(exp_bg, (exp_bg_x, exp_bg_y))
        SCREEN.blit(exp_text, EXP_TEXT_POS)

        # Отрисовка игрока
        player.draw(SCREEN, sdvigx + offset_x, sdvigy + offset_y)

        # Отрисовка врагов
        for enemy in enemies:
            enemy.draw(SCREEN, sdvigx + offset_x, 930 + sdvigy + offset_y)

        # Функция для отрисовки подсказок
        def draw_hint(lines, hint_type="normal"):
            """Универсальная функция отрисовки подсказок"""
            hint_width = scale_value(900)
            hint_height = scale_value(100)
            hint_x = (SCREEN_WIDTH - hint_width) // 2
            hint_y = HINT_POS_Y

            # Фон для подсказки (серый с прозрачностью)
            hint_bg = pygame.Surface((hint_width, hint_height), pygame.SRCALPHA)
            hint_bg.fill((145, 145, 145, 100))
            SCREEN.blit(hint_bg, (hint_x, hint_y))

            # Заголовок подсказки (белый)
            font_title = pygame.font.Font(get_font_path('gulag'), scale_font_size(25))
            text = font_title.render('!HELP!', True, WHITE)

            # Центрируем заголовок внутри подсказки
            title_x = hint_x + (hint_width - text.get_width()) // 2
            title_y = hint_y + scale_value(15)
            SCREEN.blit(text, (title_x, title_y))

            # Декоративные линии (также центрируем)
            line_y = hint_y + scale_value(39)
            line_start_x = hint_x + (hint_width - scale_value(80)) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x, line_y, scale_value(80), scale_value(2)))

            line_y2 = hint_y + scale_value(47)
            line_start_x2 = hint_x + (hint_width - scale_value(820)) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x2, line_y2, scale_value(820), scale_value(2)))

            # Текст подсказки
            font_text = pygame.font.Font(get_font_path('podkova'), scale_font_size(20))

            # Центрируем каждую строку текста
            for i, line in enumerate(lines):
                text = font_text.render(line, True, WHITE)
                line_x = hint_x + (hint_width - text.get_width()) // 2
                line_y = hint_y + scale_value(50) + scale_value(25) * i
                SCREEN.blit(text, (line_x, line_y))


        # Отрисовка подсказки управления (ПОСЛЕ всех объектов)
        if player.st == -100 and -330 <= sdvigy <= 900:
            lines = [
                'Чтобы зацепиться паутиной - зажмите и держите L_SHIFT',
                'Отпустите L_SHIFT для резкого выпрямления и полета вперед'
            ]
            draw_hint(lines, "управления")

        # Отрисовка подсказки про атаку (после приземления и до первой атаки)
        if player.st == 0 and player.on_ground and player.show_attack_hint:
            lines = [
                'Для атаки врага нажмите ЛКМ.',
                'Ваши атаки будут заполнять шкалу концентрации, которую можно тратить на лечение.'
            ]
            draw_hint(lines, "про атаку")

        # Отрисовка подсказки про лечение (при низком здоровье)
        if player.show_heal_hint:
            lines = ['Нажмите 1 для лечения']
            draw_hint(lines, "про лечение")

        # Подсказка опыта при первом убийстве
        if player.exp_hint_timer > 0:
            lines = [
                'За победу над врагами вы получаете опыт,',
                'дающий вам привилегии (впоследствии)'
            ]
            draw_hint(lines, "про опыт")

        # Обработка субтитров
        if SUBTITLES == 'ON':
            if 'subticks' not in locals():
                subticks = ticks
            for i, time_range in enumerate(SUBTITLES_TIMING):
                start, end = map(int, time_range.split())
                if start < ticks - subticks + 1300 < end:
                    font = pygame.font.Font(get_font_path('monospace_bold'), scale_font_size(22))
                    text = font.render(SUBTITLES_TEXT[i], True, WHITE)
                    tx = SCREEN_WIDTH // 2 - len(SUBTITLES_TEXT[i]) // 2 * scale_value(13)
                    ty = SCREEN_HEIGHT - scale_value(200) - len(SUBTITLES_TEXT[i]) // 50 * scale_value(17)
                    SCREEN.blit(text, (tx, ty))
                    break

        # Отрисовка эффектов повреждения
        if player.is_flashing():
            draw_damage_flash(SCREEN, player)

        # Обновление эффектов
        player.update_effects()

        # Обработка событий
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                # Сохраняем прогресс перед выходом, обновляя только выбранный слот
                try:
                    # Читаем все текущие данные
                    all_slots = []
                    try:
                        with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="r") as f:
                            all_slots = f.readlines()
                    except FileNotFoundError:
                        # Если файла нет, создаем базовые слоты
                        for i in range(6):
                            all_slots.append(f"{i + 1}\n")

                    # Обновляем только строку с "Выбрана"
                    updated_slots = []
                    found_selected = False

                    for slot_line in all_slots:
                        parts = slot_line.strip().split()
                        if len(parts) >= 2 and parts[1] == "Выбрана":
                            # Это выбранный слот - заменяем "Выбрана" на количество очков
                            updated_slots.append(f"{parts[0]} {player.exp}\n")
                            found_selected = True
                        else:
                            # Сохраняем другие слоты без изменений
                            updated_slots.append(slot_line)

                    # Если не нашли выбранный слот, используем слот 6 по умолчанию
                    if not found_selected:
                        if len(updated_slots) >= 6:
                            # Заменяем 6 слот
                            parts = updated_slots[5].strip().split()
                            if parts:
                                updated_slots[5] = f"{parts[0]} {player.exp}\n"
                        else:
                            # Если слотов меньше 6, дополняем и устанавливаем в 6
                            while len(updated_slots) < 6:
                                updated_slots.append(f"{len(updated_slots) + 1}\n")
                            updated_slots[5] = f"6 {player.exp}\n"

                    # Записываем все обновленные данные
                    with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="w") as f:
                        f.writelines(updated_slots)

                    print(f"Прогресс сохранен, опыт: {player.exp}")

                except Exception as e:
                    print(f"Ошибка при сохранении: {e}")

                pygame.quit()
                sys.exit()

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:  # удобная кнопка выхода для разработчика
                    pygame.quit()
                    sys.exit()
                elif ev.key == pygame.K_TAB:
                    # Сохраняем состояние перед открытием меню
                    game_state_before_menu = save_current_game_state(player, enemies, sdvigx, sdvigy)

                    # Пауза музыки
                    pygame.mixer.music.unload()

                    # Открываем меню паузы
                    menu()

                    # Восстанавливаем состояние после закрытия меню
                    if game_state_before_menu:
                        restore_game_state(player, enemies, game_state_before_menu)
                elif ev.key in [pygame.K_a, pygame.K_d, pygame.K_SPACE] and player.st in [0, 3, 4]:
                    player.handle_event(ev)
                elif ev.key == pygame.K_1:  # Использование концентрации для лечения
                    if player.use_concentration_for_healing():
                        # Воспроизведение случайного звука лечения
                        try:
                            heal_sounds = SOUND_FILES['heal']
                            if isinstance(heal_sounds, list) and len(heal_sounds) > 0:
                                # Выбираем случайный звук лечения
                                heal_sound_path = random.choice(heal_sounds)
                                if os.path.exists(heal_sound_path):
                                    heal_sound = pygame.mixer.Sound(heal_sound_path)
                                    heal_sound.set_volume(SOUND_VOLUME)
                                    heal_sound.play()
                                    print(f"[HEAL] Воспроизведен звук лечения: {os.path.basename(heal_sound_path)}")
                                else:
                                    print(f"[HEAL] Файл не найден: {heal_sound_path}")
                            else:
                                print("[HEAL] Список звуков лечения пуст")
                        except Exception as e:
                            print(f"[HEAL] Ошибка воспроизведения звука лечения: {e}")

            if ev.type == pygame.MOUSEBUTTONDOWN and sdvigy <= GROUND_LEVEL:
                player.attack(enemies, sdvigx)

        pygame.display.update()
        clock.tick(FPS)


main_menu()
