import pygame
import math
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import *


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

        # Переменные для движения
        self.moving_right = False
        self.moving_left = False
        self.walking = False  # Для анимации ходьбы

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
            self.sprites = { # если не отображается, но работает - надо дописать
                # Поза приземления
                'pose_land': self.load_and_scale_image('TEMA 40.png', self.width, self.height),
                'pose_land_rev': self.load_and_scale_image('TEMA 40_rev.png', self.width, self.height),
                # Прыжок
                'jump': self.load_and_scale_image('TEMA 206.png', self.width, self.height),
                'jump_rev': self.load_and_scale_image('TEMA 206_rev.png', self.width, self.height),
                # Паутина
                'web_throw': self.load_and_scale_image('TEMA 143.png', self.width, self.height),
                'web_throw_rev': self.load_and_scale_image('TEMA 143_rev.png', self.width, self.height),
                'swing_1': self.load_and_scale_image('fly_pose1_cs.png', self.width, self.height),
                'swing_1_rev': self.load_and_scale_image('fly_pose1_cs_rev.png', self.width, self.height),
                'swing_7': self.load_and_scale_image('fly_pose7_cs.png', self.width, self.height),
                'swing_7_rev': self.load_and_scale_image('fly_pose7_cs_rev.png', self.width, self.height),
                'swing_8': self.load_and_scale_image('fly_pose8_cs.png', self.width, self.height),
                'swing_8_rev': self.load_and_scale_image('fly_pose8_cs_rev.png', self.width, self.height),
                'swing_9': self.load_and_scale_image('fly_pose9_cs.png', self.width, self.height),
                # Стояние
                'idle_1': self.load_and_scale_image('TEMA 2.png', self.width, self.height),
                'idle_2': self.load_and_scale_image('spider_stay5_cs.png', self.width, self.height),
                'idle_1_rev': self.load_and_scale_image('TEMA 2_rev.png', self.width, self.height),
                'idle_2_rev': self.load_and_scale_image('spider_stay5_cs_rev.png', self.width, self.height),
                # Ходьба
                'walk_1': self.load_and_scale_image('TEMA 100.png', self.width, self.height),
                'walk_2': self.load_and_scale_image('TEMA 82.png', self.width, self.height),
                'walk_3': self.load_and_scale_image('TEMA 84.png', self.width, self.height),
                'walk_4': self.load_and_scale_image('TEMA 108.png', self.width, self.height),
                'walk_5': self.load_and_scale_image('TEMA 116.png', self.width, self.height),
                'walk_1_rev': self.load_and_scale_image('TEMA 100_rev.png', self.width, self.height),
                'walk_2_rev': self.load_and_scale_image('TEMA 82_rev.png', self.width, self.height),
                'walk_3_rev': self.load_and_scale_image('TEMA 84_rev.png', self.width, self.height),
                'walk_4_rev': self.load_and_scale_image('TEMA 108_rev.png', self.width, self.height),
                'walk_5_rev': self.load_and_scale_image('TEMA 116_rev.png', self.width, self.height),
                # Смерть
                'death': self.load_and_scale_image('spider_pose-1_cs.png', self.width, self.height),
                # Удар
                'punch': self.load_and_scale_image('TEMA 70.png', self.width, self.height),
            }
            print("Спрайты игрока загружены успешно")
        except Exception as e:
            print(f"Ошибка загрузки спрайтов: {e}")

    def load_and_scale_image(self, filename, width, height):
        """Загрузка и масштабирование изображения с использованием ЕДИНОЙ функции из config"""
        # print(f"[DEBUG] Загрузка спрайта: {filename}")

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
                    print(f"[DEBUG] Файл найден: {image_path}")
                    # Используем ЕДИНУЮ функцию из config
                    image = load_image_safe(image_path, convert_alpha=True)
                    return pygame.transform.scale(image, (int(width), int(height)))

            # Если файл не найден - используем функцию из config с заглушкой
            print(f"[DEBUG] Файл не найден, используем заглушку: {filename}")
            placeholder = load_image_safe(PLACEHOLDER_IMAGE, convert_alpha=True)
            return pygame.transform.scale(placeholder, (int(width), int(height)))

        except Exception as e:
            print(f"[DEBUG] Ошибка загрузки {filename}: {e}")
            # Используем ЕДИНУЮ функцию для заглушки
            placeholder = load_image_safe(PLACEHOLDER_IMAGE, convert_alpha=True)
            return pygame.transform.scale(placeholder, (int(width), int(height)))

    def handle_input(self, keys, ticks, sdvigy):
        """Обработка ввода пользователя"""
        # Бросок паутины
        if (self.st == 4 or self.st == -100) and keys[pygame.K_LSHIFT] and sdvigy > 150:
            self.start_web_swing(ticks)
        # Движение влево/вправо - ОБНОВЛЕНО
        if self.st == 0 and self.on_ground:
            if keys[pygame.K_d]:
                self.move_right(ticks)
            elif keys[pygame.K_a]:
                self.move_left(ticks)
        # Управление во время полета на паутине - ОБНОВЛЕНО ДЛЯ st=-1
        if (self.st == 1 or self.st == -1) and keys[pygame.K_LSHIFT] and sdvigy > 150:
            self.continue_web_swing()
        # Отпускание паутины - ОБНОВЛЕНО ДЛЯ st=-1
        if (self.st == 1 or self.st == -1) and not keys[pygame.K_LSHIFT]:
            self.release_web_swing(ticks)

    def handle_event(self, event):
        """Обработка отдельных событий клавиатуры - ТОЛЬКО нажатия"""
        if event.type == pygame.KEYDOWN:
            old_facing = self.facing_right

            if self.st in [3, 4]:
                if event.key == pygame.K_d and event.key != pygame.K_a and self.st in [3, 4]:
                    self.facing_right = True
                    self.revst = 0
                    print(f"[FACING_KEYDOWN] Changed to RIGHT, st={self.st}")
                elif event.key == pygame.K_a and event.key != pygame.K_d:
                    self.facing_right = False
                    self.revst = 1
                    print(f"[FACING_KEYDOWN] Changed to LEFT, st={self.st}")

                # Логируем только если направление действительно изменилось
                if old_facing != self.facing_right:
                    print(f"[FACING_CHANGED] {old_facing} -> {self.facing_right}")
            elif self.st == 0 and self.st != 4:
                # Прыжок
                if event.key == pygame.K_SPACE:
                    self.st = 4
                    self.coords_increase = 0
                    print(f"[JUMP] Starting jump, st={self.st}")  # Для отладки


    def start_web_swing(self, ticks):
        """Начало полета на паутине"""
        print(f"[DEBUG] start_web_swing: called, changing st from {self.st} to 1")
        # ДОБАВЛЕНО: Учитываем текущее направление при начале полета
        if self.facing_right:
            self.st = 1  # Полет вправо
        else:
            self.st = -1  # Полет влево

        self.coords_increase = 0
        self.SMRt = -50
        self.web_swinging = True
        print(f"[DEBUG] start_web_swing: new st = {self.st}, web_swinging = {self.web_swinging}")
        self.play_web_sound()

    def continue_web_swing(self):
        """Продолжение полета на паутине с цикличной раскачкой"""
        self.coords_increase += 1

        if self.coords_increase % 3 == 0:
            self.SMRt += 1

        if self.coords_increase >= 620:
            self.coords_increase = 0
            self.facing_right = not self.facing_right

            # ДОБАВЛЕНО: Переключение между st=1 и st=-1 при развороте
            if self.st == 1:
                self.st = -1  # Переход в обратное направление
            else:
                self.st = 1  # Возврат в прямое направление

            self.swing_cycle += 1
            self.SMRt = -50

    def release_web_swing(self, ticks):
        """Отпускание паутины"""
        self.web_swinging = False
        if self.coords_increase > 500:
            self.play_swing_sound()
            self.st = 2
            self.coords_increase = 0
            self.SMRt = 20  # Начальное значение для st=2
            # print(f"[RELEASE_WEB] Переход в st=2, SMRt={self.SMRt}")
        else:
            self.st = 3
            # print(f"[RELEASE_WEB] Переход в st=3 (короткий бросок)")

    def move_right(self, ticks):
        """Движение вправо"""
        self.moving_right = True
        self.moving_left = False
        self.walking = True
        self.facing_right = True
        self.revst = 0

        # Здесь будет логика изменения sdvigx (как в старом коде)
        # Пока просто устанавливаем флаги

    def move_left(self, ticks):
        """Движение влево"""
        self.moving_left = True
        self.moving_right = False
        self.walking = True
        self.facing_right = False
        self.revst = 1

        # Здесь будет логика изменения sdvigx

    def apply_movement(self, sdvigx):
        """Применяет движение и возвращает новый sdvigx"""
        if self.st == 0 and self.on_ground:  # Только на земле
            if self.moving_right:
                sdvigx -= PLAYER_SPEED  # Движение вправо (как в старом коде)
            elif self.moving_left:
                sdvigx += PLAYER_SPEED  # Движение влево

        # Сбрасываем флаги движения
        self.moving_right = False
        self.moving_left = False

        return sdvigx

    def take_damage(self, amount):
        """Получение урона"""
        if self.on_ground:
            self.health -= amount
            print(f"[PLAYER] Получен урон: {amount}, HP: {self.health}")
        # Можно добавить мигание или звук

    def update(self, keys, ticks, sdvigy):
        """Обновление состояния игрока"""
        # old_st = self.st

        self.handle_input(keys, ticks, sdvigy)

        # Сбрасываем анимацию ходьбы если не двигаемся
        if self.on_ground and not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.walking = False

        # # Логируем изменение состояния
        # if old_st != self.st:
        #     print(f"[STATE_CHANGE] st: {old_st} -> {self.st}")

        # ОБНОВЛЕНИЕ ДЛЯ ST=2: ограниченный полет после отпускания паутины
        if self.st == 2:
            self.coords_increase += 1

            # Уменьшаем угол (как в старом коде)
            if self.coords_increase % 5 == 0:
                self.SMRt -= 1

            # Переход в падение после достижения предела
            if self.coords_increase >= 175:  # Как в старом коде
                self.st = 3
                self.coords_increase = 0
                print(f"[ST2_TO_ST3] Переход из st=2 в st=3")

        # Проверка на землю
        if sdvigy <= -415 and not self.web_swinging:
            if self.st == -100:
                self.st = 0
                try:
                    land_sound = pygame.mixer.Sound(SOUND_FILES['punch'])
                    land_sound.play()
                except:
                    print("NO")
            self.on_ground = True
            if self.st in [2, 3]:
                self.st = 0
            self.on_ground = True
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
                if hasattr(self, 'walking') and self.walking:
                    walk_cycle = int(pygame.time.get_ticks() / 100) % 5 + 1
                    return f"walk_{walk_cycle}{direction}", (20, 140), 0
                else:
                    return "idle_1", (20, 140), 0
            else:
                return f"swing_8{direction}", (0, 150), 0
        elif self.st == 1 or self.st == -1:  # ОБЪЕДИНЕНО ДЛЯ ОБОИХ НАПРАВЛЕНИЙ
            if self.coords_increase < 310:
                rotation = -40 + (self.coords_increase / 310) * 40
            else:
                rotation = (self.coords_increase - 310) / 310 * 45
            rotation = max(-40, min(45, rotation))
            if not self.facing_right:
                rotation = -rotation
            return f"swing_1{direction}", (20, 100), rotation
        elif self.st == 2:
            # Полет после отпускания паутины (как в старом коде)
            rotation = self.SMRt

            # Инвертируем угол для направления влево
            if not self.facing_right:
                rotation = -rotation

            return f"swing_7{direction}", (60, 40), rotation  # Позиция как в старом коде: (60, 40)
        elif self.st == 3:  # Свободное падение - ВСЕГДА ОТОБРАЖАЕМ
            # ИСПРАВЛЕНИЕ: Инвертируем угол для направления влево
            rotation = -65  # Базовый угол
            # Если смотрим влево, инвертируем угол
            if not self.facing_right:
                rotation = -rotation
            return f"swing_7{direction}", (27, 0), rotation
        elif self.st == 4:
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
        # print("Позиции", sprite_rect.topright, sprite_screen_x, sprite_screen_y)

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
