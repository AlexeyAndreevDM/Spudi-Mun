import pygame
import math
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import *

# Импортируем load_image_safe из основного файла
# Добавим эту строку чтобы использовать вашу функцию
try:
    from main import load_image_safe  # Или откуда у вас эта функция
except ImportError:
    # Если не можем импортировать, создадим простую версию
    def load_image_safe(path, default_image=PLACEHOLDER_IMAGE, convert_alpha=True):
        try:
            if convert_alpha:
                return pygame.image.load(path).convert_alpha()
            else:
                return pygame.image.load(path).convert()
        except:
            print(f"Error loading: {path}")
            surf = pygame.Surface((50, 50))
            surf.fill((255, 0, 255))
            return surf


class Player:
    def __init__(self):
        # Фиксированная позиция на экране (как в оригинале)
        self.screen_x = PLAYER_START_X
        self.screen_y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # Состояния (совместимость с оригинальным кодом)
        self.st = -100
        self.facing_right = True
        self.on_ground = False

        # Переменные для совместимости
        self.coords_increase = 0
        self.SMRt = -50
        self.srt = -40
        self.revst = 0
        self.revk = 0
        self.sp_ticks = 0
        self.dif_image = 0

        # Паутина
        self.web_swinging = False

        self.swing_cycle = 0  # Счетчик циклов раскачки для затухания

        # Здоровье
        self.health = PLAYER_MAX_HEALTH

        # Спрайты
        self.sprites = {}
        self.load_sprites()

    def load_sprites(self):
        """Загрузка всех спрайтов для классического костюма с использованием вашей функции"""
        try:
            # Основные позы
            self.sprites = {
                # Поза приземления
                'pose_land': self.load_and_scale_image('Тема 40.png', self.width, self.height),
                'pose_land_rev': self.load_and_scale_image('Тема 40_rev.png', self.width, self.height),
                # Прыжок
                'jump': self.load_and_scale_image('Тема 206.png', self.width, self.height),
                'jump_rev': self.load_and_scale_image('Тема 206_rev.png', self.width, self.height),
                # Паутина
                'web_throw': self.load_and_scale_image('Тема 143.png', self.width, self.height),
                'web_throw_rev': self.load_and_scale_image('Тема 143_rev.png', self.width, self.height),
                'swing_1': self.load_and_scale_image('fly_pose1_cs.png', self.width, self.height),
                'swing_1_rev': self.load_and_scale_image('fly_pose1_cs_rev.png', self.width, self.height),
                'swing_7': self.load_and_scale_image('fly_pose7_cs.png', self.width, self.height),
                'swing_8': self.load_and_scale_image('fly_pose8_cs.png', self.width, self.height),
                'swing_8_rev': self.load_and_scale_image('fly_pose8_cs_rev.png', self.width, self.height),
                'swing_9': self.load_and_scale_image('fly_pose9_cs.png', self.width, self.height),
                # Стояние
                'idle_1': self.load_and_scale_image('Тема 2.png', self.width, self.height),
                'idle_2': self.load_and_scale_image('spider_stay5_cs.png', self.width, self.height),
                'idle_1_rev': self.load_and_scale_image('Тема 2_rev.png', self.width, self.height),
                'idle_2_rev': self.load_and_scale_image('spider_stay5_cs_rev.png', self.width, self.height),
                # Ходьба
                'walk_1': self.load_and_scale_image('Тема 100.png', self.width, self.height),
                'walk_2': self.load_and_scale_image('Тема 82.png', self.width, self.height),
                'walk_3': self.load_and_scale_image('Тема 84.png', self.width, self.height),
                'walk_4': self.load_and_scale_image('Тема 108.png', self.width, self.height),
                'walk_5': self.load_and_scale_image('Тема 116.png', self.width, self.height),
                'walk_1_rev': self.load_and_scale_image('Тема 100_rev.png', self.width, self.height),
                'walk_2_rev': self.load_and_scale_image('Тема 82_rev.png', self.width, self.height),
                'walk_3_rev': self.load_and_scale_image('Тема 84_rev.png', self.width, self.height),
                'walk_4_rev': self.load_and_scale_image('Тема 108_rev.png', self.width, self.height),
                'walk_5_rev': self.load_and_scale_image('Тема 116_rev.png', self.width, self.height),
                # Смерть
                'death': self.load_and_scale_image('spider_pose-1_cs.png', self.width, self.height),
                # Удар
                'punch': self.load_and_scale_image('Тема 70.png', self.width, self.height),
            }
            print("Спрайты игрока загружены успешно")
        except Exception as e:
            print(f"Ошибка загрузки спрайтов: {e}")

    def load_and_scale_image(self, filename, width, height):
        """Загрузка и масштабирование изображения с использованием вашей функции"""
        try:
            # Пробуем разные пути
            paths_to_try = [
                os.path.join(SPIDER_CLASSIC_DIR, filename),
                os.path.join(SPIDER_MAN_DIR, filename),
                os.path.join(IMAGES_DIR, filename),
                filename  # Прямой путь
            ]
            for image_path in paths_to_try:
                if os.path.exists(image_path):
                    image = load_image_safe(image_path, convert_alpha=True)
                    return pygame.transform.scale(image, (int(width), int(height)))
            # Если файл не найден ни по одному пути
            print(f"Файл не найден: {filename}")
            # МАСШТАБИРУЕМ заглушку до нужного размера
            placeholder = load_image_safe(PLACEHOLDER_IMAGE, convert_alpha=True)
            return pygame.transform.scale(placeholder, (int(width), int(height)))
        except Exception as e:
            print(f"Ошибка загрузки {filename}: {e}")
            # МАСШТАБИРУЕМ заглушку до нужного размера
            placeholder = load_image_safe(PLACEHOLDER_IMAGE, convert_alpha=True)
            return pygame.transform.scale(placeholder, (int(width), int(height)))

    def handle_input(self, keys, ticks):
        """Обработка ввода пользователя"""
        # Прыжок
        if self.st == 0 and keys[pygame.K_SPACE] and self.st != 4:
            self.st = 4
            self.coords_increase = 0
        # Бросок паутины
        # Проверяем возможность начать полёт из состояния 0 или -100
        if (self.st == 4 or self.st == -100) and keys[pygame.K_LSHIFT]:
            print(f"[DEBUG] handle_input: LSHIFT pressed, current st = {self.st}")  # <-- НОВОЕ
            self.start_web_swing(ticks)
        # Движение влево/вправо
        if self.st == 0 and self.on_ground:
            if keys[pygame.K_d]:
                self.move_right(ticks)
                self.facing_right = True
                self.revst = 0
            elif keys[pygame.K_a]:
                self.move_left(ticks)
                self.facing_right = False
                self.revst = 1
        # Управление во время полета на паутине
        if self.st == 1 and keys[pygame.K_LSHIFT]:
            self.continue_web_swing()
        # Отпускание паутины
        if self.st == 1 and not keys[pygame.K_LSHIFT]:
            self.release_web_swing(ticks)

    def start_web_swing(self, ticks):
        """Начало полета на паутине"""
        print(f"[DEBUG] start_web_swing: called, changing st from {self.st} to 1")  # <-- НОВОЕ
        self.st = 1
        self.coords_increase = 0
        self.SMRt = -50
        self.web_swinging = True
        print(f"[DEBUG] start_web_swing: new st = {self.st}, web_swinging = {self.web_swinging}")  # <-- НОВОЕ
        self.play_web_sound()

    def continue_web_swing(self):
        """Продолжение полета на паутине с цикличной раскачкой"""
        self.coords_increase += 1

        if self.coords_increase % 3 == 0:
            self.SMRt += 1

        if self.coords_increase >= 620:
            self.coords_increase = 0
            self.facing_right = not self.facing_right  # Разворот для обратной стороны
            self.swing_cycle += 1  # Увеличить цикл для затухания
            self.SMRt = -50  # Сброс фазы
            # НЕ меняем st! Остается 1 для продолжения раскачки

    def release_web_swing(self, ticks):
        """Отпускание паутины"""
        self.web_swinging = False  # Сброс флага полета
        if self.coords_increase > 400:
            self.play_swing_sound()
            self.st = 2
            self.coords_increase = 0
            self.SMRt = 20
        else:
            self.st = 3

    def move_right(self, ticks):
        """Движение вправо"""
        if self.sp_ticks == 0:
            self.sp_ticks = ticks

    def move_left(self, ticks):
        """Движение влево"""
        if self.sp_ticks == 0:
            self.sp_ticks = ticks

    def update(self, keys, ticks, sdvigy):
        """Обновление состояния игрока"""
        print(f"[DEBUG] update: st = {self.st}, sdvigy = {sdvigy}, web_swinging = {self.web_swinging}")  # <-- НОВОЕ
        self.handle_input(keys, ticks)
        # Проверка на землю
        # Убираем условие self.st != -100, чтобы позволить игроку "приземлиться" из состояния -100
        # Но при этом не выставляем on_ground, если он в полёте (web_swinging)
        if sdvigy <= -415 and not self.web_swinging:
            if self.st == -100:  # <-- Добавить -100 для начального падения
                self.st = 0
                try:
                    land_sound = pygame.mixer.Sound(SOUND_FILES['punch'])
                    land_sound.play()
                except:
                    print("NO")
            self.on_ground = True
            if self.st in [2, 3]:  # <-- Добавить -100 для начального падения
                self.st = 0
            self.on_ground = True
            print(f"[DEBUG] update: on_ground = True, st = {self.st}")  # <-- НОВОЕ
        else:
            self.on_ground = False
            print(f"[DEBUG] update: on_ground = False")  # <-- НОВОЕ

    def draw(self, screen, sdvigx, sdvigy):
        """Отрисовка игрока"""
        sprite_key, draw_position, rotation = self.get_render_info()

        if sprite_key in self.sprites:
            sprite = self.sprites[sprite_key]

            if rotation != 0:
                sprite = pygame.transform.rotate(sprite, rotation)

            # Фиксированная позиция на экране
            screen_x = self.screen_x + draw_position[0]
            screen_y = self.screen_y + draw_position[1]

            screen.blit(sprite, (screen_x, screen_y))

            # Отрисовка паутины
            if self.web_swinging:
                self.draw_web_line(screen, sdvigx, sdvigy)

    def get_render_info(self):
        """Определение текущего спрайта"""
        direction = "" if self.facing_right else "_rev"
        if self.health <= 0:
            return "death", (27, 140), 0
        if self.st == -100:
            return "swing_7", (27, 0), -65
        elif self.st == 0:
            if self.on_ground:
                # Проверяем движение для анимации ходьбы
                if hasattr(self, 'walking') and self.walking:
                    walk_cycle = int(pygame.time.get_ticks() / 100) % 5 + 1  # Пример
                    return f"walk_{walk_cycle}{direction}", (20, 140), 0
                else:
                    return "idle_1", (20, 140), 0
            else:
                return f"swing_8{direction}", (0, 150), 0
        elif self.st == 1:
            if self.coords_increase < 310:
                rotation = -40 + (self.coords_increase / 310) * 40
            else:
                rotation = (self.coords_increase - 310) / 310 * 45
            rotation = max(-40, min(45, rotation))
            if not self.facing_right:
                rotation = -rotation  # Инвертировать вращение для обратного направления
            return f"swing_1{direction}", (20, 100), rotation

        elif self.st == 2:  # <-- Отпускание паутины
            return f"swing_8{direction}", (0, 150), 0
        elif self.st == 3:  # <-- Свободное падение
            return f"swing_7{direction}", (27, 0), -65
        elif self.st == 4:  # <-- Прыжок
            return f"jump{direction}", (40, 40), 0
        return "idle_1", (20, 140), 0

    def draw_web_line(self, screen, sdvigx, sdvigy):
        # Примерная высота, где паутина цепляется к зданию
        building_top_y = -2000 + SCREEN_HEIGHT - 100 + sdvigy + 100

        # Вычисляем координаты края спрайта на экране, откуда тянется паутина
        sprite_key, draw_position, rotation = self.get_render_info()
        sprite_screen_x = self.screen_x + draw_position[0]
        sprite_screen_y = self.screen_y + draw_position[1]

        # Создаём Rect
        sprite_rect = pygame.Rect(sprite_screen_x, sprite_screen_y, self.width, self.height)
        print("Позиции", sprite_rect.topright, sprite_screen_x, sprite_screen_y)

        # Выбираем стартовую точку в зависимости от направления
        if self.facing_right:
            start_x, start_y = sprite_rect.topright  # <-- Правый верхний угол
        else:
            start_x, start_y = sprite_rect.topleft  # <-- Левый верхний угол

        # end_x — координата на экране, где крепится паутина к зданию
        # Привязываем к краю фона в зависимости от направления
        if self.facing_right:
            end_x = SCREEN_WIDTH - 250 * SCALE_X - self.coords_increase * 2
        else:
            end_x = 300 + self.coords_increase * 2

        end_y = building_top_y

        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 2)

    def play_web_sound(self):
        """Воспроизведение звука паутины"""
        try:
            thwip_sound = pygame.mixer.Sound(random.choice(SOUND_FILES['thwip']))
            thwip_sound.play()
        except:
            pass

    def play_swing_sound(self):
        """Воспроизведение звука полета"""
        try:
            swing_sound = pygame.mixer.Sound(SOUND_FILES['swing'])
            swing_sound.play()
        except:
            pass

    def get_health(self):
        return self.health

    def reset(self):
        self.__init__()