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
        if self.st == 0 and keys[pygame.K_LSHIFT]:
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

        # Переход из начального состояния
        if self.st == -100 and keys[pygame.K_LSHIFT]:
            self.st = 0

    def start_web_swing(self, ticks):
        """Начало полета на паутине"""
        self.st = 1
        self.coords_increase = 0
        self.SMRt = -50
        self.web_swinging = True
        self.play_web_sound()

    def continue_web_swing(self):
        """Продолжение полета на паутине"""
        self.coords_increase += 1

        if self.coords_increase % 3 == 0:
            self.SMRt += 1

        if self.coords_increase >= 620:
            self.st = -1
            self.coords_increase = 0
            self.SMRt = 60

    def release_web_swing(self, ticks):
        """Отпускание паутины"""
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
        self.handle_input(keys, ticks)

        # Проверка на землю
        if sdvigy <= -330 and not self.web_swinging and self.st != -100:
            self.on_ground = True
            if self.st in [2, 3]:
                self.st = 0
        else:
            self.on_ground = False

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
                self.draw_web_line(screen)

    def get_render_info(self):
        """Определение текущего спрайта"""
        direction = "" if self.facing_right else "_rev"

        if self.health <= 0:
            return "death", (27, 140), 0

        if self.st == -100:
            return "swing_7", (27, 0), -65
        elif self.st == 0:
            if not hasattr(self, 'last_animation_time'):
                self.last_animation_time = pygame.time.get_ticks()
                self.dif_image = random.randint(1, 2)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_animation_time > 2000:
                self.dif_image = random.randint(1, 2)
                self.last_animation_time = current_time

            if self.revst == 0:
                return f"idle_{self.dif_image}", (20, 140), 0
            else:
                return f"idle_{self.dif_image}_rev", (20, 140), 0
        elif self.st == 1:
            return f"swing_1{direction}", (-40, -10), self.SMRt
        elif self.st == 2:
            return "swing_7", (60, 40), self.SMRt - 175
        elif self.st == 3:
            return f"swing_8{direction}", (0, 150), 0
        elif self.st == 4:
            return f"jump{direction}", (40, 40), 0

        return "idle_1", (20, 140), 0

    def draw_web_line(self, screen):
        """Отрисовка линии паутины"""
        if self.facing_right:
            start_x = self.screen_x + 100
            start_y = self.screen_y + 80
            end_x = SCREEN_WIDTH - 300 - self.coords_increase * 2
            end_y = 100
        else:
            start_x = self.screen_x + 50
            start_y = self.screen_y + 80
            end_x = 300 + self.coords_increase * 2
            end_y = 100

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