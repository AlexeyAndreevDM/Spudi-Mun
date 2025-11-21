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
                with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="r") as f:
                    txt = f.readlines()
                    for i in range(len(txt)):
                        line = txt[i].strip()
                        font = pygame.font.Font(get_font_path('monospace_bold'), FONT_SIZES['medium'])

                        # Разбираем строку: "номер [опыт]"
                        parts = line.split()
                        if len(parts) >= 2 and parts[1].isdigit():
                            # Есть опыт - отображаем "номер Опыт: число
                            pygame.draw.rect(SCREEN, MENU_HIGHLIGHT, (203, 131 + 91 * i, 385, 73))
                            text = font.render(f"{parts[0]} Опыт: {parts[1]}", True, WHITE)
                            SCREEN.blit(text, (220, 150 + 91 * i))
            except FileNotFoundError:
                pass

            for event1 in pygame.event.get():
                if event1.type == pygame.KEYDOWN:
                    if event1.key == pygame.K_UP:
                        im = (im - 1) % 6  # 6 слотов сохранения
                    if event1.key == pygame.K_DOWN:
                        im = (im + 1) % 6
                    if event1.key == pygame.K_x:
                        # Сохраняем выбор слота в файл, сохраняя все существующие данные
                        try:
                            # Читаем текущие данные файла
                            existing_data = {}
                            try:
                                with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="r") as f:
                                    lines = f.readlines()
                                    for i, line in enumerate(lines):
                                        if i < 6:  # Только первые 6 слотов
                                            existing_data[i] = line.strip()
                            except FileNotFoundError:
                                # Если файла нет, создаем пустые данные
                                for i in range(6):
                                    existing_data[i] = str(i + 1)

                            # Обновляем выбранный слот и сохраняем все слоты
                            with open(os.path.join(SAVES_DIR, "Saves.txt"), mode="w") as f:
                                for i in range(6):
                                    if i == im:
                                        f.write(f"{i + 1} Выбрана\n")
                                    else:
                                        # Сохраняем существующие данные для других слотов
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


def draw_damage_flash(screen, player):
    """Отрисовка эффектов повреждения, лечения и смерти"""
    flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

    # Приоритет: смерть > урон > лечение
    if player.death_flash_timer > 0:
        # Эффект смерти - красная рамка в 2 раза больше
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.015)) * 180  # Более интенсивная пульсация
        border_width = 40  # В 2 раза больше чем обычная рамка (20)
        alpha = min(200, pulse)  # Более непрозрачная

        # Рисуем толстую красную рамку по краям экрана
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (0, 0, SCREEN_WIDTH, border_width))
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width))
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (0, 0, border_width, SCREEN_HEIGHT))
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT))

        # Дополнительно: легкое красное затемнение всего экрана
        overlay_alpha = min(80, pulse * 0.4)
        flash_surface.fill((255, 0, 0, int(overlay_alpha)))

    elif player.damage_flash_timer > 0:
        # Эффект урона (красная рамка) - обычный размер
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 128
        border_width = 20
        alpha = min(FLASH_ALPHA, pulse)

        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (0, 0, SCREEN_WIDTH, border_width))
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width))
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (0, 0, border_width, SCREEN_HEIGHT))
        pygame.draw.rect(flash_surface, (255, 0, 0, int(alpha)),
                         (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT))

    elif player.heal_flash_timer > 0:
        # Эффект лечения (зеленая рамка)
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 128
        border_width = 20
        alpha = min(FLASH_ALPHA, pulse)

        pygame.draw.rect(flash_surface, (0, 255, 0, int(alpha)),
                         (0, 0, SCREEN_WIDTH, border_width))
        pygame.draw.rect(flash_surface, (0, 255, 0, int(alpha)),
                         (0, SCREEN_HEIGHT - border_width, SCREEN_WIDTH, border_width))
        pygame.draw.rect(flash_surface, (0, 255, 0, int(alpha)),
                         (0, 0, border_width, SCREEN_HEIGHT))
        pygame.draw.rect(flash_surface, (0, 255, 0, int(alpha)),
                         (SCREEN_WIDTH - border_width, 0, border_width, SCREEN_HEIGHT))

    # Отображаем поверхность с эффектом
    if player.is_flashing():
        screen.blit(flash_surface, (0, 0))

def main_game():
    from src.game.player import Player
    from src.game.enemy import Enemy
    from src import config

    # Объявляем глобальные переменные
    global sdvigy, DIFFICULTY, MUSIC_STATUS, CURRENT_SUIT, st, CURRENT_CUTSCENE, SUBTITLES

    CURRENT_CUTSCENE += 1
    st = -100

    # Глобальная переменная для хранения выбранного слота сохранения
    selected_save_slot = 6  # По умолчанию 6 слот

    web_swing_speed_x = 0
    web_swing_speed_y = 0

    # Загрузка фонов
    bg = load_image_safe(get_image_path("backgrounds", "fhomewthspandpavmnt.jpg"), convert_alpha=False)
    bg = pygame.transform.scale(bg, (1414, 2000))
    road = load_image_safe(get_image_path("backgrounds", "дорога.jpeg"), convert_alpha=False)
    road = pygame.transform.scale(road, (2011, 354))

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
        if MUSIC_STATUS == -1 and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(MUSIC_FILES['gameplay'])
            # pygame.mixer.music.play()
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
            # Воспроизводим звук смерти один раз при начале смерти
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

                # Отрисовываем экран смерти
                SCREEN.fill(BLACK)
                font = pygame.font.Font(get_font_path('gulag'), 25)
                text = font.render('!HELP!', True, RED)
                SCREEN.blit(text, (420, 250))
                pygame.draw.line(SCREEN, RED, [400, 280], [1080, 280], 2)
                pygame.draw.line(SCREEN, RED, [400, 380], [1080, 380], 2)
                font = pygame.font.Font(get_font_path('monospace_bold'), 55)
                text = font.render("YOU'RE FAILED, BUDDY", True, RED)
                SCREEN.blit(text, (405, 300))
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

        # Отрисовка здоровья игрока
        health_bar_width = 400
        health_bar_height = 45
        pygame.draw.rect(SCREEN, WHITE, (50, 50, health_bar_width, health_bar_height), 5)

        # Расчет ширины здоровья
        health_width = (player.health / PLAYER_MAX_HEALTH) * 390
        if health_width < 0:
            health_width = 0

        pygame.draw.rect(SCREEN, HEALTH_GREEN, (55, 55, health_width, 35))

        # Отрисовка шкалы концентрации (под здоровьем)
        concentration_bar_width = health_bar_width // 2  # В 2 раза короче
        concentration_bar_height = health_bar_height // 2  # В 2 раза меньше по высоте
        concentration_y = 50 + health_bar_height + 10  # Отступ от здоровья

        # Рамка концентрации (белая как у здоровья)
        pygame.draw.rect(SCREEN, WHITE, (50, concentration_y, concentration_bar_width, concentration_bar_height), 3)

        # Расчет ширины заполнения концентрации
        concentration_fill_width = (player.concentration / 100) * (concentration_bar_width - 6)
        if concentration_fill_width < 0:
            concentration_fill_width = 0

        # Заполнение концентрации (полупрозрачный белый)
        concentration_surface = pygame.Surface((concentration_fill_width, concentration_bar_height - 6),
                                               pygame.SRCALPHA)
        concentration_surface.fill((255, 255, 255, 180))  # Белый с альфой 180
        SCREEN.blit(concentration_surface, (53, concentration_y + 3))

        # Текст здоровья
        font = pygame.font.Font(get_font_path('monospace_bold'), 30)
        health_text = font.render(f"{int(player.health)}", True, WHITE)
        SCREEN.blit(health_text, (460, 53))

        # Отрисовка опыта с фоном (справа от здоровья)
        font = pygame.font.Font(get_font_path('monospace_bold'), 30)
        exp_text = font.render(f"Опыт: {player.exp}", True, WHITE)
        # Получаем размеры текста
        text_width = exp_text.get_width()
        text_height = exp_text.get_height()
        # Создаем фон для опыта (такой же, как у подсказок)
        exp_bg_width = text_width + 20  # Отступы по 10px с каждой стороны
        exp_bg_height = text_height + 10  # Отступы по 5px сверху и снизу
        exp_bg = pygame.Surface((exp_bg_width, exp_bg_height), pygame.SRCALPHA)
        exp_bg.fill((145, 145, 145, 100))  # Тот же серый с прозрачностью
        # Позиция фона (выровнена с текстом)
        exp_bg_x = SCREEN_WIDTH - 250 - 10  # Смещаем на 10px левее текста
        exp_bg_y = 53 - 5  # Смещаем на 5px выше текста

        # Отрисовываем фон и текст
        SCREEN.blit(exp_bg, (exp_bg_x, exp_bg_y))
        SCREEN.blit(exp_text, (SCREEN_WIDTH - 250, 53))

        # Отрисовка игрока
        player.draw(SCREEN, sdvigx + offset_x, sdvigy + offset_y)

        # Отрисовка врагов
        for enemy in enemies:
            enemy.draw(SCREEN, sdvigx + offset_x, 930 + sdvigy + offset_y)

        # Отрисовка подсказки управления (ПОСЛЕ всех объектов)
        if player.st == -100 and -330 <= sdvigy <= 900:
            # Размеры подсказки
            hint_width = 900
            hint_height = 100

            # Центрируем по горизонтали и сдвигаем на 50px ниже
            hint_x = (SCREEN_WIDTH - hint_width) // 2
            hint_y = 150  # Было 100, теперь 150 (на 50px ниже)

            # Фон для подсказки (серый с прозрачностью)
            hint_bg = pygame.Surface((hint_width, hint_height), pygame.SRCALPHA)
            hint_bg.fill((145, 145, 145, 100))  # Серый с прозрачностью
            SCREEN.blit(hint_bg, (hint_x, hint_y))

            # Заголовок подсказки (белый)
            font = pygame.font.Font(get_font_path('gulag'), 25)
            text = font.render('!HELP!', True, WHITE)

            # Центрируем заголовок внутри подсказки
            title_x = hint_x + (hint_width - text.get_width()) // 2
            title_y = hint_y + 15
            SCREEN.blit(text, (title_x, title_y))

            # Декоративные линии (также центрируем)
            line_y = hint_y + 39
            line_start_x = hint_x + (hint_width - 80) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x, line_y, 80, 2))

            line_y2 = hint_y + 47
            line_start_x2 = hint_x + (hint_width - 820) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x2, line_y2, 820, 2))

            # Текст подсказки
            font = pygame.font.Font(get_font_path('podkova'), 20)
            lines = [
                'Чтобы зацепиться паутиной - зажмите и держите L_SHIFT',
                'Отпустите L_SHIFT для резкого выпрямления и полета вперед'
            ]

            # Центрируем каждую строку текста
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                line_x = hint_x + (hint_width - text.get_width()) // 2
                line_y = hint_y + 50 + 25 * i
                SCREEN.blit(text, (line_x, line_y))

        # Отрисовка подсказки про атаку (после приземления и до первой атаки)
        if player.st == 0 and player.on_ground and player.show_attack_hint:
            # Размеры подсказки
            hint_width = 900
            hint_height = 100

            # Центрируем по горизонтали и сдвигаем на 50px ниже
            hint_x = (SCREEN_WIDTH - hint_width) // 2
            hint_y = 150  # Такая же позиция как у предыдущей подсказки

            # Фон для подсказки (серый с прозрачностью)
            hint_bg = pygame.Surface((hint_width, hint_height), pygame.SRCALPHA)
            hint_bg.fill((145, 145, 145, 100))
            SCREEN.blit(hint_bg, (hint_x, hint_y))

            # Заголовок подсказки (белый)
            font = pygame.font.Font(get_font_path('gulag'), 25)
            text = font.render('!HELP!', True, WHITE)

            # Центрируем заголовок внутри подсказки
            title_x = hint_x + (hint_width - text.get_width()) // 2
            title_y = hint_y + 15
            SCREEN.blit(text, (title_x, title_y))

            # Декоративные линии (также центрируем)
            line_y = hint_y + 39
            line_start_x = hint_x + (hint_width - 80) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x, line_y, 80, 2))

            line_y2 = hint_y + 47
            line_start_x2 = hint_x + (hint_width - 820) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x2, line_y2, 820, 2))

            # Текст подсказки про атаку
            font = pygame.font.Font(get_font_path('podkova'), 20)
            lines = [
                'Для атаки врага нажмите ЛКМ.',
                'Ваши атаки будут заполнять шкалу концентрации, которую можно тратить на лечение.'
            ]

            # Центрируем каждую строку текста
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                line_x = hint_x + (hint_width - text.get_width()) // 2
                line_y = hint_y + 50 + 25 * i
                SCREEN.blit(text, (line_x, line_y))

            print("Подсказка про атаку отображена")

        # Отрисовка подсказки про лечение (при низком здоровье)
        if player.show_heal_hint:
            # Размеры подсказки
            hint_width = 900
            hint_height = 100

            # Центрируем по горизонтали и сдвигаем на 50px ниже
            hint_x = (SCREEN_WIDTH - hint_width) // 2
            hint_y = 150  # Такая же позиция как у предыдущих подсказок

            # Фон для подсказки (серый с прозрачностью)
            hint_bg = pygame.Surface((hint_width, hint_height), pygame.SRCALPHA)
            hint_bg.fill((145, 145, 145, 100))
            SCREEN.blit(hint_bg, (hint_x, hint_y))

            # Заголовок подсказки (белый)
            font = pygame.font.Font(get_font_path('gulag'), 25)
            text = font.render('!HELP!', True, WHITE)

            # Центрируем заголовок внутри подсказки
            title_x = hint_x + (hint_width - text.get_width()) // 2
            title_y = hint_y + 15
            SCREEN.blit(text, (title_x, title_y))

            # Декоративные линии (также центрируем)
            line_y = hint_y + 39
            line_start_x = hint_x + (hint_width - 80) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x, line_y, 80, 2))

            line_y2 = hint_y + 47
            line_start_x2 = hint_x + (hint_width - 820) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x2, line_y2, 820, 2))

            # Текст подсказки про лечение
            font = pygame.font.Font(get_font_path('podkova'), 20)
            lines = [
                'Нажмите 1 для лечения'
            ]

            # Центрируем каждую строку текста
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                line_x = hint_x + (hint_width - text.get_width()) // 2
                line_y = hint_y + 50 + 25 * i
                SCREEN.blit(text, (line_x, line_y))

            print("Подсказка про лечение отображена")

        # Подсказка опыта при первом убийстве
        if player.exp_hint_timer > 0:
            # Размеры подсказки
            hint_width = 900
            hint_height = 100

            # Центрируем по горизонтали
            hint_x = (SCREEN_WIDTH - hint_width) // 2
            hint_y = 150  # Такая же позиция как у предыдущих подсказок

            # Фон для подсказки (серый с прозрачностью)
            hint_bg = pygame.Surface((hint_width, hint_height), pygame.SRCALPHA)
            hint_bg.fill((145, 145, 145, 100))
            SCREEN.blit(hint_bg, (hint_x, hint_y))

            # Заголовок подсказки (белый)
            font = pygame.font.Font(get_font_path('gulag'), 25)
            text = font.render('!HELP!', True, WHITE)

            # Центрируем заголовок внутри подсказки
            title_x = hint_x + (hint_width - text.get_width()) // 2
            title_y = hint_y + 15
            SCREEN.blit(text, (title_x, title_y))

            # Декоративные линии (также центрируем)
            line_y = hint_y + 39
            line_start_x = hint_x + (hint_width - 80) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x, line_y, 80, 2))

            line_y2 = hint_y + 47
            line_start_x2 = hint_x + (hint_width - 820) // 2
            pygame.draw.rect(SCREEN, WHITE, (line_start_x2, line_y2, 820, 2))

            # Текст подсказки про опыт
            font = pygame.font.Font(get_font_path('podkova'), 20)
            lines = [
                'За победу над врагами вы получаете опыт,',
                'дающий вам привилегии (впоследствии)'
            ]

            # Центрируем каждую строку текста
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                line_x = hint_x + (hint_width - text.get_width()) // 2
                line_y = hint_y + 50 + 25 * i
                SCREEN.blit(text, (line_x, line_y))

            print("Подсказка про опыт отображена")

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
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif ev.key == pygame.K_TAB:
                    pygame.mixer.music.unload()
                    # menu()  # Раскомментируйте когда будет готова функция menu
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
                    else:
                        # Сообщения об ошибках уже выводятся в методе use_concentration_for_healing
                        pass
            if ev.type == pygame.MOUSEBUTTONDOWN and sdvigy <= -415:
                player.attack(enemies, sdvigx)

        pygame.display.update()
        clock.tick(FPS)


main_menu()
