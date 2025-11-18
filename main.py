import pygame
import sys
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
    except (pygame.error, FileNotFoundError):
        print(f"Warning: File {path} not found, using default: {default_image}")
        try:
            if convert_alpha:
                return pygame.image.load(default_image).convert_alpha()
            else:
                return pygame.image.load(default_image).convert()
        except:
            print(f"Emergency: Creating colored square for {path}")
            surf = pygame.Surface((50, 50))
            surf.fill((255, 0, 255))
            return surf


def main_menu():
    st = 5  # deafult st = 0
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

    expectation = randint(500, 600)

    # Загрузка музыки главного меню
    pygame.mixer.music.load(get_music_path("Web Launch.mp3"))
    # pygame.mixer.music.play(-1) # разбанить

    clock = pygame.time.Clock()

    while True:
        if st == 0:
            # Загружаем и отображаем начальный экран
            intro_image = load_image_safe(get_image_path("main_menu", "Home_screen.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT + 20))
            SCREEN.blit(intro_image, (0, 0))

            # Затем текст
            font = pygame.font.Font(get_font_path('gulag'), FONT_SIZES['title'])
            text = font.render('Spider-Man', True, WHITE)
            tx = SCREEN_WIDTH // 2 - text.get_width() // 2
            ty = SCREEN_HEIGHT // 4 - 60 - 90
            SCREEN.blit(text, (tx, ty))
            # pygame.display.update()

            # ВАЖНО: Если это первый кадр st == 0, запоминаем время
            # Проверяем, была ли уже установлена intro_start_time для этого состояния.
            # Если intro_start_time == 0, значит, это первый кадр st=0.
            if intro_start_time == 0:
                intro_start_time = pygame.time.get_ticks()

            # Проверка времени и смена состояния
            # Это выполняется в КАЖДОМ кадре, но срабатывает только один раз при переходе
        if st == 0 and pygame.time.get_ticks() - intro_start_time >= 3000:
            st = 1
            intro_start_time = 0  # Сбрасываем для следующего раза, если нужно вернуться в st=0

        if st == 1:
            intro_image = load_image_safe(get_image_path("main_menu", "newgamescreen.jpg"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            font = pygame.font.Font(get_font_path('gulag'), FONT_SIZES['title'])
            text = font.render('START', True, RED)

            # Правильно вычисляем позицию и размеры
            text_width = text.get_width()  # Используем реальную ширину текста
            text_height = text.get_height()
            tx = SCREEN_WIDTH // 2 - text_width // 2
            ty = SCREEN_HEIGHT // 4 - text_height // 2 - 20

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

            # pygame.display.update()

        if st == 2:
            intro_image = load_image_safe(get_image_path("main_menu", "BS_menu.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            save_slots = load_image_safe(get_image_path("main_menu", "save_slots.png"))
            save_slots = pygame.transform.scale(save_slots, (480, 810))
            SCREEN.blit(save_slots, (140, 50))

            # Отрисовка элементов интерфейса
            pygame.draw.line(SCREEN, WHITE, (169, 168 + 91 * im), (172, 168 + 91 * im), 1)
            pygame.draw.circle(SCREEN, WHITE, (184, 168 + 91 * im), 8, 2)
            pygame.draw.circle(SCREEN, WHITE, (184, 168 + 91 * im), 4, 2)

            s = pygame.Surface((400, 85))
            s.fill(MENU_DARK_BLUE)
            s.set_alpha(160)
            SCREEN.blit(s, (196, 125 + 91 * im))

            # Границы выделенного элемента
            pygame.draw.line(SCREEN, WHITE, (196, 125 + 91 * im), (196, 145 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (195, 124 + 91 * im), (216, 124 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (196, 189 + 91 * im), (196, 209 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (195, 210 + 91 * im), (216, 210 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (594, 125 + 91 * im), (594, 145 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (575, 124 + 91 * im), (595, 124 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (594, 189 + 91 * im), (594, 209 + 91 * im), 3)
            pygame.draw.line(SCREEN, WHITE, (575, 210 + 91 * im), (595, 210 + 91 * im), 3)

            # Загрузка и отображение слотов сохранения
            try:
                with open(os.path.join(SAVES_DIR, "saves.txt"), mode="r") as f:
                    txt = f.readlines()
                    for i in txt:
                        if i.strip():
                            pygame.draw.rect(SCREEN, MENU_HIGHLIGHT, (203, 131 + 91 * txt.index(i), 385, 73))
                            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['medium'])
                            text = font.render(str(txt.index(i) + 1), True, WHITE)
                            SCREEN.blit(text, (220, 145 + 91 * txt.index(i)))
            except FileNotFoundError:
                pass

            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 6  # 6 слотов сохранения
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 6
                    if event1.key == pygame.K_x:
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

            # pygame.display.update()

        if st == 3:
            intro_image = load_image_safe(get_image_path("main_menu", "BS_menu.png"))
            intro_image = pygame.transform.scale(intro_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(intro_image, (0, 0))

            # Отрисовка панели выбора сложности
            pygame.draw.rect(SCREEN, MENU_BLUE, (140, 48, 480, 341))
            pygame.draw.rect(SCREEN, MENU_DARK_BLUE, (140, 341, 480, 259))

            s = pygame.Surface((480, 263))
            s.fill(MENU_BLUE)
            s.set_alpha(125)
            SCREEN.blit(s, (140, 600))

            # Границы панели
            pygame.draw.line(SCREEN, WHITE, (140, 48), (140, 150), 1)
            pygame.draw.line(SCREEN, WHITE, (140, 160), (140, 163), 1)
            pygame.draw.line(SCREEN, WHITE, (140, 173), (140, 710), 1)
            pygame.draw.line(SCREEN, WHITE, (140, 720), (140, 723), 2)
            pygame.draw.line(SCREEN, WHITE, (140, 733), (140, 861), 2)
            pygame.draw.line(SCREEN, WHITE, (620, 48), (620, 150), 2)
            pygame.draw.line(SCREEN, WHITE, (620, 160), (620, 163), 2)
            pygame.draw.line(SCREEN, WHITE, (620, 173), (620, 710), 1)
            pygame.draw.line(SCREEN, WHITE, (620, 720), (620, 723), 1)
            pygame.draw.line(SCREEN, WHITE, (620, 733), (620, 861), 1)

            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['normal'])
            text = font.render("SELECT DIFFICULTY", True, WHITE)
            SCREEN.blit(text, (160, 65))

            pygame.draw.line(SCREEN, WHITE, (160, 102), (185, 102), 2)
            pygame.draw.line(SCREEN, WHITE, (190, 102), (194, 102), 2)
            pygame.draw.line(SCREEN, WHITE, (200, 102), (600, 102), 1)
            pygame.draw.line(SCREEN, WHITE, (165, 117), (165, 125), 2)
            pygame.draw.line(SCREEN, WHITE, (165, 135), (165, 305), 1)
            pygame.draw.line(SCREEN, WHITE, (165, 315), (165, 323), 2)

            # Отрисовка выбора сложности
            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['small'])
            pygame.draw.line(SCREEN, WHITE, (171, 147 + 40 * im), (174, 147 + 40 * im), 1)
            pygame.draw.circle(SCREEN, WHITE, (185, 147 + 40 * im), 8, 2)
            pygame.draw.circle(SCREEN, WHITE, (185, 147 + 40 * im), 4, 2)

            s = pygame.Surface((360, 32))
            s.fill(MENU_DARK_BLUE)
            s.set_alpha(160)
            SCREEN.blit(s, (200, 130 + 40 * im))

            # Границы выбранного элемента
            pygame.draw.line(SCREEN, WHITE, (200, 130 + 40 * im), (210, 130 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (200, 130 + 40 * im), (200, 140 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (200, 162 + 40 * im), (210, 162 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (200, 152 + 40 * im), (200, 162 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (550, 130 + 40 * im), (560, 130 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (560, 130 + 40 * im), (560, 140 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (550, 162 + 40 * im), (560, 162 + 40 * im), 2)
            pygame.draw.line(SCREEN, WHITE, (560, 152 + 40 * im), (560, 162 + 40 * im), 2)

            # Тексты сложности
            difficulties = ["FRIENDLY NEIGHBOURHOOD", "THE AMAZING", "SPECTACULAR", "ULTIMATE"]
            for i, diff_text in enumerate(difficulties):
                text = font.render(diff_text, True, WHITE)
                SCREEN.blit(text, (210, 135 + 40 * i))

            # Индикаторы сложности
            for i in range(3):
                s = pygame.Surface((250, 15))
                s.fill(UI_ACCENT)
                s.set_alpha(155)
                SCREEN.blit(s, (350, 685 + 30 * i))
                pygame.draw.rect(SCREEN, WHITE, (349, 684 + 30 * i, 252, 17), 2)

            # Описания сложности
            if im == 0:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])

                # Первая строка
                text = font_desc.render("This setting is for expert players who", True, WHITE)
                SCREEN.blit(text, (160, 400))

                # Вторая строка разбита на части
                text_part1 = font_desc.render("enjoy a brutally ", True, WHITE)
                text_fun = pygame.font.Font(get_font_path('avengeance'), FONT_SIZES['medium']).render("Fun", True,
                                                                                                      WHITE)
                text_part2 = font_desc.render(" experience.", True, WHITE)

                # Вычисляем позиции для правильного расположения
                start_x = 160
                start_y = 462

                # Отображаем части текста
                SCREEN.blit(text_part1, (start_x, start_y))
                fun_x = start_x + text_part1.get_width()
                SCREEN.blit(text_fun, (fun_x, start_y - 15))  # Смещаем немного вверх для выравнивания
                SCREEN.blit(text_part2, (fun_x + text_fun.get_width(), start_y))

                # Индикаторы сложности
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 686, 50, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 716, 70, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 746, 60, 13))

            elif im == 1:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for players who want", True, WHITE)
                SCREEN.blit(text, (160, 380))
                text = font_desc.render("to enjoy the story without", True, WHITE)
                SCREEN.blit(text, (160, 442))
                text = font_desc.render("challenging combat.", True, WHITE)
                SCREEN.blit(text, (160, 504))

                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 686, 100, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 716, 85, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 746, 95, 13))

            elif im == 2:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for players who like a", True, WHITE)
                SCREEN.blit(text, (160, 380))
                text = font_desc.render("balanced experience with some", True, WHITE)
                SCREEN.blit(text, (160, 442))
                text = font_desc.render("challenge", True, WHITE)
                SCREEN.blit(text, (160, 504))

                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 686, 126, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 716, 126, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 746, 126, 13))

            elif im == 3:
                font_desc = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['tiny'])
                text = font_desc.render("This setting is for players who enjoy", True, WHITE)
                SCREEN.blit(text, (160, 380))
                text = font_desc.render("challenging combat. Enemies will be", True, WHITE)
                SCREEN.blit(text, (160, 442))
                text = font_desc.render("stronger and more aggressive.", True, WHITE)
                SCREEN.blit(text, (160, 504))

                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 686, 170, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 716, 180, 13))
                pygame.draw.rect(SCREEN, HEALTH_RED, (351, 746, 165, 13))

            # Логотип паука
            spider_logo = load_image_safe(get_image_path("main_menu", "spider_logo_tr.png"))
            spider_logo = pygame.transform.scale(spider_logo, (80, 80))
            SCREEN.blit(spider_logo, (340, 560))

            pygame.draw.line(SCREEN, WHITE, (155, 600), (330, 600), 1)
            pygame.draw.line(SCREEN, WHITE, (430, 600), (605, 600), 1)
            pygame.draw.circle(SCREEN, WHITE, (335, 600), 1, 2)
            pygame.draw.circle(SCREEN, WHITE, (425, 600), 1, 2)

            # Подписи характеристик
            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['small'])
            text = font.render("ENEMIES", True, WHITE)
            SCREEN.blit(text, (195, 640))
            text = font.render("AGRESSIVE", True, WHITE)
            text.set_alpha(155)
            SCREEN.blit(text, (195, 680))
            text = font.render("DAMAGE", True, WHITE)
            text.set_alpha(155)
            SCREEN.blit(text, (195, 710))
            text = font.render("HEALTH", True, WHITE)
            text.set_alpha(155)
            SCREEN.blit(text, (195, 740))

            # pygame.display.update()

            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 4  # 4 уровня сложности
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 4
                    if event1.key == pygame.K_x:
                        st = 4
                        im = 0
                        SUBTITLES = 'OFF'
                        # Установка сложности
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

            pygame.draw.rect(SCREEN, MENU_BLUE, (140, 48, 720, 500))
            s = pygame.Surface((720, 363))
            s.fill(MENU_BLUE)
            s.set_alpha(125)
            SCREEN.blit(s, (140, 500))

            # Границы панели
            pygame.draw.line(SCREEN, WHITE, (140, 48), (140, 150), 1)
            pygame.draw.line(SCREEN, WHITE, (140, 160), (140, 163), 1)
            pygame.draw.line(SCREEN, WHITE, (140, 173), (140, 710), 1)
            pygame.draw.line(SCREEN, WHITE, (140, 720), (140, 723), 2)
            pygame.draw.line(SCREEN, WHITE, (140, 733), (140, 861), 2)
            pygame.draw.line(SCREEN, WHITE, (860, 48), (860, 150), 2)
            pygame.draw.line(SCREEN, WHITE, (860, 160), (860, 163), 2)
            pygame.draw.line(SCREEN, WHITE, (860, 173), (860, 710), 1)
            pygame.draw.line(SCREEN, WHITE, (860, 720), (860, 723), 1)
            pygame.draw.line(SCREEN, WHITE, (860, 733), (860, 861), 1)

            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['normal'])
            text = font.render("BEFORE YOU START", True, WHITE)
            SCREEN.blit(text, (160, 65))

            pygame.draw.line(SCREEN, WHITE, (160, 102), (220, 102), 2)
            pygame.draw.line(SCREEN, WHITE, (225, 102), (230, 102), 2)
            pygame.draw.line(SCREEN, WHITE, (230, 102), (820, 102), 1)
            pygame.draw.line(SCREEN, WHITE, (165, 117), (165, 127), 2)
            pygame.draw.line(SCREEN, WHITE, (165, 137), (165, 465), 1)
            pygame.draw.line(SCREEN, WHITE, (165, 475), (165, 485), 2)

            pygame.draw.line(SCREEN, WHITE, (175, 158 + 30 * im), (179, 158 + 30 * im), 1)

            # Логотип паука
            spider_logo = load_image_safe(get_image_path("main_menu", "spider_logo_tr.png"))
            spider_logo = pygame.transform.scale(spider_logo, (80, 80))
            SCREEN.blit(spider_logo, (470, 780))

            pygame.draw.line(SCREEN, WHITE, (275, 820), (465, 820), 1)
            pygame.draw.line(SCREEN, WHITE, (555, 820), (745, 820), 1)
            pygame.draw.circle(SCREEN, WHITE, (475, 821), 1, 3)
            pygame.draw.circle(SCREEN, WHITE, (545, 821), 1, 3)

            font = pygame.font.Font(get_font_path('old_soviet'), FONT_SIZES['normal'])
            text = font.render('More functions in next updates!', True, WHITE)
            SCREEN.blit(text, (160, 505))

            # Отрисовка выбора
            pygame.draw.circle(SCREEN, WHITE, (193, 159 + 30 * im), 8, 2)
            pygame.draw.circle(SCREEN, WHITE, (193, 159 + 30 * im), 4, 2)

            font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['small'])
            text = font.render("START", True, WHITE)
            text.set_alpha(255 if im == 0 else 155)
            SCREEN.blit(text, (220, 145))

            text = font.render("SUBTITLES", True, WHITE)
            text.set_alpha(255 if im == 1 else 155)
            SCREEN.blit(text, (220, 175))

            # Отображение состояния субтитров
            if SUBTITLES == 'ON':
                text = font.render("< ON >", True, WHITE)
            else:
                text = font.render("< OFF >", True, WHITE)
            SCREEN.blit(text, (550, 175))

            # pygame.display.update()

            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 2  # 2 пункта меню
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 2
                    if event1.key in (pygame.K_LEFT, pygame.K_RIGHT) and im == 1:
                        # Переключаем состояние субтитров
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
            spider_logo = pygame.transform.scale(spider_logo, (70, 70))
            SCREEN.blit(spider_logo, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100))

            # Анимация круга
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 70, 70), pi + d_arc,
                            5 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 70, 70), 3 * pi / 2 + d_arc,
                            7 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 70, 70), 0 + d_arc, pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, 70, 70), pi / 2 + d_arc,
                            3 * pi / 4 + d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 105, SCREEN_HEIGHT - 105, 80, 80), 0 - d_arc, pi / 2 - d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 105, SCREEN_HEIGHT - 105, 80, 80), 2 * pi / 3 - d_arc,
                            7 * pi / 6 - d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 105, SCREEN_HEIGHT - 105, 80, 80), 4 * pi / 3 - d_arc,
                            11 * pi / 6 - d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 110, SCREEN_HEIGHT - 110, 90, 90), 0 + d_arc,
                            5 * pi / 6 + d_arc)
            pygame.draw.arc(SCREEN, WHITE, (SCREEN_WIDTH - 110, SCREEN_HEIGHT - 110, 90, 90), pi + d_arc,
                            11 * pi / 6 + d_arc)

            # pygame.display.update()
            pygame.time.wait(7)
            # time += 7
            time += 100#

            if time >= expectation:
                if vp == 0:
                    # Здесь будет переход к игре
                    main_game()

        # Обработка событий выхода
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(60)  # Ограничиваем до 60 FPS
        pygame.display.update()  # единое обновление


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
    from src.game.player import Player

    # Объявляем глобальные переменные
    global sdvigy, DIFFICULTY, MUSIC_STATUS, CURRENT_SUIT, st, CURRENT_CUTSCENE, SUBTITLES

    CURRENT_CUTSCENE += 1
    st = -100

    web_swing_speed_x = 0
    web_swing_speed_y = 0

    # Загрузка фонов
    bg = load_image_safe(get_image_path("backgrounds", "fhomewthspandpavmnt.jpg"), convert_alpha=False)
    bg = pygame.transform.scale(bg, (1414, 2000))
    road = load_image_safe(get_image_path("backgrounds", "дорога.jpeg"), convert_alpha=False)
    road = pygame.transform.scale(road, (2011, 354))

    # Инициализация переменных
    sdvigx = -500
    sdvigy = 1000  # Начальное положение для падения
    tiles = math.ceil(SCREEN_WIDTH / bg.get_width()) + 1
    hp = 100

    # Создаем игрока
    player = Player()
    player.st = st
    player.health = hp

    # Основной игровой цикл
    clock = pygame.time.Clock()
    while True:
        ticks = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Обработка музыки
        if MUSIC_STATUS == -1 and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(MUSIC_FILES['gameplay'])
            # pygame.mixer.music.play()
            pygame.mixer.music.set_volume(MUSIC_VOLUME)

        # ОБРАБОТКА ДВИЖЕНИЯ ФОНА - ИСПРАВЛЕННАЯ ВЕРСИЯ ДЛЯ РАСКАЧКИ
        if player.st == -100:  # Начальное падение
            if sdvigy > -415:
                sdvigy -= 6  # Двигаем фон вниз (игрок "падает")

        elif player.st == 1 and keys[pygame.K_LSHIFT]:
            # Горизонталь: всегда в направлении facing_right (раскачка влево-вправо)
            horiz_speed = 4 * (0.95 ** player.swing_cycle)  # Затухание скорости
            if player.facing_right:
                sdvigx -= horiz_speed
            else:
                sdvigx += horiz_speed

            # Вертикаль: ТОГДА ЖЕ траектория (дуга подъём-спуск), без инверсии!
            vert_amp = 3 * (0.95 ** player.swing_cycle)  # Затухание амплитуды
            if player.coords_increase < 310:
                phase = player.coords_increase / 310
                angle = phase * math.pi
                vertical_movement = -math.sin(angle) * vert_amp  # Всегда подъём в первой половине
            else:
                phase = (player.coords_increase - 310) / 310
                angle = math.pi + phase * math.pi
                vertical_movement = -math.sin(angle) * vert_amp  # Спуск во второй

            sdvigy += vertical_movement  # БЕЗ инверсии для not facing_right!

            player.continue_web_swing()

        elif player.st == -1 and keys[pygame.K_LSHIFT]:
            player.st = 1  # Вернуть в ст=1 для продолжения
            player.facing_right = not player.facing_right  # Разворот
            player.coords_increase = 0
            player.SMRt = -50

        # Движение при ходьбе
        elif player.st == 0 and player.on_ground:
            if keys[pygame.K_d]:  # Вправо
                sdvigx -= SCROLL_SPEED
            elif keys[pygame.K_a]:  # Влево
                sdvigx += SCROLL_SPEED

        # Движение при отпускании паутины
        elif player.st == 2:
            sdvigx -= 4
            sdvigy += 2

        # Движение при свободном падении
        elif player.st == 3:
            if player.revst == 0:  # Смотрит вправо
                sdvigx -= 1
                sdvigy -= 5
            else:  # Смотрит влево
                sdvigx += 1
                sdvigy -= 5

        # Обновление игрока
        player.update(keys, ticks, sdvigy)

        # if player.st == -100 and sdvigy <= -415:
        #     player.st = 0
        #     sdvigy = -420
        #     player.on_ground = True
        #     try:
        #         land_sound = pygame.mixer.Sound(SOUND_FILES['punch'])
        #         land_sound.play()
        #     except:
        #         print("NO")
        #     print("NOOOO")

        # Синхронизация переменных
        st = player.st
        hp = player.health

        # Проверка: если игрок перешёл в состояние 0 из -100, установить sdvigy на "землю"
        if st == 0 and player.on_ground:
            sdvigy = -420

        # Обработка смерти игрока
        if hp <= 0:
            if player.x + 27 - player.coords_increase > 300:
                # Анимация смерти в воздухе
                if 'zvukst' not in locals() or zvukst != 2:
                    zvukst = 2
                    st, MUSIC_STATUS = -101, 0
                    try:
                        ss = pygame.mixer.Sound(SOUND_FILES['death'])
                        ss.play()
                        pygame.mixer.music.unload()
                    except:
                        pass
                player.coords_increase += 2
            else:
                # Экраны поражения
                SCREEN.fill(BLACK)
                font = pygame.font.Font(get_font_path('gulag'), 25)
                text = font.render('!HELP!', True, RED)
                SCREEN.blit(text, (420, 250))
                pygame.draw.line(SCREEN, RED, [400, 280], [1080, 280], 2)
                pygame.draw.line(SCREEN, RED, [400, 380], [1080, 380], 2)
                font = pygame.font.Font(get_font_path('monospace_bold'), 55)
                text = font.render("YOU'RE FAILED, BUDDY", True, RED)
                SCREEN.blit(text, (430, 300))
                pygame.display.update()
                pygame.time.wait(8000)
                st, sdvigy, hp, MUSIC_STATUS = 0, -330, 100, -1
                player.reset()

        # Отрисовка
        SCREEN.fill(BLACK)

        # Отрисовка фона
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
            SCREEN.blit(bg, (bg_width * i + bg_offset, -2000 + SCREEN_HEIGHT - 100 + sdvigy))
            i += 1

        # Аналогично для road
        tiles = math.ceil(SCREEN_WIDTH / road_width) + 2
        i = -1
        while i < tiles:
            SCREEN.blit(road, (road_width * i + road_offset, 800 + sdvigy))
            i += 1

        # Отрисовка здоровья игрока
        pygame.draw.rect(SCREEN, WHITE, (50, 50, 400, 45), 5)
        pygame.draw.rect(SCREEN, HEALTH_GREEN, (55, 55, 390, 35))
        font = pygame.font.Font(get_font_path('monospace_bold'), 30)
        text = font.render(str(hp), True, WHITE)
        SCREEN.blit(text, (460, 53))

        # Отрисовка игрока
        player.draw(SCREEN, sdvigx, sdvigy)

        # Обработка субтитров
        if SUBTITLES == 'ON':
            if 'subticks' not in locals():
                subticks = ticks
            for i, time_range in enumerate(SUBTITLES_TIMING):
                start, end = map(int, time_range.split())
                if start < ticks - subticks + 1300 < end:
                    font = pygame.font.Font(get_font_path('monospace_bold'), 22)
                    text = font.render(SUBTITLES_TEXT[i], True, WHITE)
                    tx = SCREEN_WIDTH // 2 - len(SUBTITLES_TEXT[i]) // 2 * 13
                    ty = SCREEN_HEIGHT - 200 - len(SUBTITLES_TEXT[i]) // 50 * 17
                    SCREEN.blit(text, (tx, ty))
                    break

        # Обработка событий
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
                    # menu()  # Раскомментируйте когда будет готова функция menu
            if ev.type == pygame.MOUSEBUTTONDOWN and sdvigy <= -415:
                player.st = 0

        pygame.display.update()
        clock.tick(FPS)


main_menu()
