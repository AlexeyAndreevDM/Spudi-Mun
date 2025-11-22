import pygame
import math
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import *


class Player:
    def __init__(self):
        # Фиксированная позиция на экране (масштабируется через конфиг)
        self.screen_x = PLAYER_START_X
        self.screen_y = PLAYER_START_Y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # Состояния (совместимость с оригинальным кодом)
        self.st = -100
        self.facing_right = True
        self.on_ground = False

        # Переменные для совместимости (не масштабируются)
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

        # Здоровье (не масштабируется)
        self.health = PLAYER_MAX_HEALTH

        # Опыт (не масштабируется)
        self.exp = 0
        self.exp_hint_timer = 0  # Таймер подсказки опыта

        # Спрайты (масштабируются через размеры)
        self.sprites = {}
        self.load_sprites()

        # Эффекты повреждения (не масштабируются)
        self.damage_flash_timer = 0
        self.death_flash_timer = 0

        # Эффекты смерти (не масштабируются)
        self.death_flash_timer = 0
        self.death_delay_timer = 0  # Таймер задержки перед экраном смерти
        self.death_sound_played = False  # Флаг для отслеживания воспроизведения звука
        self.death_screen_shown = False  # Добавляем явный флаг

        # Эффекты лечения (не масштабируются)
        self.heal_flash_timer = 0  # Таймер для зеленой рамки лечения

        # Флаги состояния
        self.is_dead = False

        # Атака и кулдаун (не масштабируются)
        self.attack_cooldown = 0
        self.attack_range = scale_value(100)  # Масштабируемая зона атаки
        self.attack_damage = 25

        # Флаги звуков
        self.air_sound_played = False

        # Флаги подсказок
        self.show_attack_hint = True  # Показывать подсказку про атаку
        self.has_attacked = False  # Игрок хотя бы раз атаковал
        self.show_heal_hint = False
        self.heal_hint_shown = False  # Чтобы показывать только один раз за сессию низкого здоровья
        self.exp_hint_shown = False

        # Система концентрации (не масштабируется)
        self.concentration = 50.0  # Изначально заполнена наполовину (50%)
        self.max_concentration = 100.0
        self.concentration_gain_per_hit = 5.0  # +5% за удар
        self.healing_per_full_concentration = 50  # 100% концентрации = 50 здоровья

    def reset(self):
        """Полный сброс игрока"""
        self.__init__()

    def load_sprites(self):
        """Загрузка всех спрайтов для классического костюма с использованием вашей функции"""
        try:
            # Основные позы
            self.sprites = {
                # Поза приземления
                'pose_land': self.load_and_scale_image('TEMA 40.png'),
                'pose_land_rev': self.load_and_scale_image('TEMA 40_rev.png'),
                # Прыжок
                'jump': self.load_and_scale_image('TEMA 206.png'),
                'jump_rev': self.load_and_scale_image('TEMA 206_rev.png'),
                # Паутина
                'web_throw': self.load_and_scale_image('TEMA 143.png'),
                'web_throw_rev': self.load_and_scale_image('TEMA 143_rev.png'),
                'swing_1': self.load_and_scale_image('fly_pose1_cs.png'),
                'swing_1_rev': self.load_and_scale_image('fly_pose1_cs_rev.png'),
                'swing_7': self.load_and_scale_image('fly_pose7_cs.png'),
                'swing_7_rev': self.load_and_scale_image('fly_pose7_cs_rev.png'),
                'swing_8': self.load_and_scale_image('fly_pose8_cs.png'),
                'swing_8_rev': self.load_and_scale_image('fly_pose8_cs_rev.png'),
                'swing_9': self.load_and_scale_image('fly_pose9_cs.png'),
                # Стояние
                'idle_1': self.load_and_scale_image('TEMA 2.png'),
                'idle_2': self.load_and_scale_image('spider_stay5_cs.png'),
                'idle_1_rev': self.load_and_scale_image('TEMA 2_rev.png'),
                'idle_2_rev': self.load_and_scale_image('spider_stay5_cs_rev.png'),
                # Ходьба
                'walk_1': self.load_and_scale_image('TEMA 100.png'),
                'walk_2': self.load_and_scale_image('TEMA 82.png'),
                'walk_3': self.load_and_scale_image('TEMA 84.png'),
                'walk_4': self.load_and_scale_image('TEMA 108.png'),
                'walk_5': self.load_and_scale_image('TEMA 116.png'),
                'walk_1_rev': self.load_and_scale_image('TEMA 100_rev.png'),
                'walk_2_rev': self.load_and_scale_image('TEMA 82_rev.png'),
                'walk_3_rev': self.load_and_scale_image('TEMA 84_rev.png'),
                'walk_4_rev': self.load_and_scale_image('TEMA 108_rev.png'),
                'walk_5_rev': self.load_and_scale_image('TEMA 116_rev.png'),
                # Смерть
                'death': self.load_and_scale_image('spider_pose-1_cs.png'),
                # Удар
                'punch': self.load_and_scale_image('TEMA 70.png'),
            }
            print("Спрайты игрока загружены успешно")
        except Exception as e:
            print(f"Ошибка загрузки спрайтов: {e}")

    def load_and_scale_image(self, filename):
        """Загрузка и масштабирование изображения с использованием ЕДИНОЙ функции из config"""
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
                    # Используем ЕДИНУЮ функцию из config
                    image = load_image_safe(image_path, convert_alpha=True)
                    return pygame.transform.scale(image, (int(self.width), int(self.height)))

            # Если файл не найден - используем функцию из config с заглушкой
            print(f"[DEBUG] Файл не найден, используем заглушку: {filename}")
            placeholder = load_image_safe(PLACEHOLDER_IMAGE, convert_alpha=True)
            return pygame.transform.scale(placeholder, (int(self.width), int(self.height)))

        except Exception as e:
            print(f"[DEBUG] Ошибка загрузки {filename}: {e}")
            # Используем ЕДИНУЮ функцию для заглушки
            placeholder = load_image_safe(PLACEHOLDER_IMAGE, convert_alpha=True)
            return pygame.transform.scale(placeholder, (int(self.width), int(self.height)))

    def handle_input(self, keys, ticks, sdvigy):
        """Обработка ввода пользователя"""
        # Бросок паутины
        if (self.st == 4 or self.st == -100) and keys[pygame.K_LSHIFT] and sdvigy > scale_value(150):
            self.start_web_swing(ticks)
        # Движение влево/вправо
        if self.st == 0 and self.on_ground:
            if keys[pygame.K_d]:
                self.move_right(ticks)
            elif keys[pygame.K_a]:
                self.move_left(ticks)
        # Управление во время полета на паутине
        if (self.st == 1 or self.st == -1) and keys[pygame.K_LSHIFT] and sdvigy > scale_value(150):
            self.continue_web_swing()
        # Отпускание паутины
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
                elif event.key == pygame.K_a and event.key != pygame.K_d:
                    self.facing_right = False
                    self.revst = 1

            elif self.st == 0 and self.st != 4:
                # Прыжок
                if event.key == pygame.K_SPACE:
                    self.st = 4
                    self.coords_increase = 0

    def start_web_swing(self, ticks):
        """Начало полета на паутине"""
        # Учитываем текущее направление при начале полета
        if self.facing_right:
            self.st = 1  # Полет вправо
        else:
            self.st = -1  # Полет влево

        self.coords_increase = 0
        self.SMRt = -50
        self.web_swinging = True
        self.play_web_sound()

    def continue_web_swing(self):
        """Продолжение полета на паутине с цикличной раскачкой"""
        self.coords_increase += 1

        if self.coords_increase % 3 == 0:
            self.SMRt += 1

        if self.coords_increase >= 620:
            self.coords_increase = 0
            self.facing_right = not self.facing_right

            # Переключение между st=1 и st=-1 при развороте
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
        else:
            self.st = 3

    def move_right(self, ticks):
        """Движение вправо"""
        self.moving_right = True
        self.moving_left = False
        self.walking = True
        self.facing_right = True
        self.revst = 0

    def move_left(self, ticks):
        """Движение влево"""
        self.moving_left = True
        self.moving_right = False
        self.walking = True
        self.facing_right = False
        self.revst = 1

    def apply_movement(self, sdvigx):
        """Применяет движение и возвращает новый sdvigx"""
        if self.st == 0 and self.on_ground:  # Только на земле
            if self.moving_right:
                sdvigx -= PLAYER_SPEED  # Движение вправо
            elif self.moving_left:
                sdvigx += PLAYER_SPEED  # Движение влево

        # Сбрасываем флаги движения
        self.moving_right = False
        self.moving_left = False

        return sdvigx

    def take_damage(self, amount):
        """Получение урона с проверкой на смерть"""
        if self.is_dead or not self.on_ground:
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.die()  # Вызываем метод смерти

        from src import config
        config.SHAKE_INTENSITY = max(1.0, amount / 5.0)
        config.SHAKE_TIMER = 10

        # Запускаем эффект красной рамки
        self.damage_flash_timer = DAMAGE_FLASH_DURATION

    def die(self):
        """Обработка смерти игрока"""
        self.is_dead = True
        self.start_death_effect()

    def start_death_effect(self):
        """Запуск эффекта смерти"""
        self.death_flash_timer = DEATH_FLASH_DURATION
        self.death_delay_timer = 90
        self.death_sound_played = False
        self.death_screen_shown = False

    def update_effects(self):
        """Обновление таймеров эффектов"""
        if self.damage_flash_timer > 0:
            self.damage_flash_timer -= 1
        if self.heal_flash_timer > 0:
            self.heal_flash_timer -= 1
        if self.death_flash_timer > 0:
            self.death_flash_timer -= 1
        if self.death_delay_timer > 0:
            self.death_delay_timer -= 1
        if self.exp_hint_timer > 0:
            self.exp_hint_timer -= 1

    def is_flashing(self):
        """Проверка, нужно ли показывать эффект"""
        return (self.damage_flash_timer > 0 or
                self.death_flash_timer > 0 or
                self.heal_flash_timer > 0)

    def can_attack(self):
        """Может ли игрок атаковать?"""
        return self.attack_cooldown == 0 and self.on_ground

    def attack(self, enemies, sdvigx):
        """Атака с возвратом атакованного врага"""
        if not self.can_attack():
            return None

        # Отмечаем, что игрок атаковал (даже если промах)
        if not self.has_attacked:
            self.has_attacked = True
            self.show_attack_hint = False  # Скрываем подсказку после первой атаки

        closest_enemy = None
        min_distance = float('inf')

        player_center_x = self.screen_x + self.width // 2

        for enemy in enemies:
            if enemy.state == "dead":
                continue

            enemy_screen_x = enemy.world_x + sdvigx
            distance = abs(enemy_screen_x - player_center_x)

            if distance < self.attack_range:
                if (self.facing_right and enemy_screen_x > player_center_x) or \
                        (not self.facing_right and enemy_screen_x < player_center_x):

                    if distance < min_distance:
                        min_distance = distance
                        closest_enemy = enemy

        if closest_enemy:
            closest_enemy.take_damage(self.attack_damage)
            self.attack_cooldown = 30
            self.increase_concentration()

            # Увеличиваем xp за убийство врага
            if closest_enemy.health <= 0:
                self.exp += 100
                # Показываем подсказку только при первом убийстве
                if not self.exp_hint_shown:
                    self.exp_hint_timer = 250
                    self.exp_hint_shown = True

            try:
                punch_sound = pygame.mixer.Sound(SOUND_FILES['punch'])
                punch_sound.set_volume(SOUND_VOLUME)
                punch_sound.play()
            except:
                pass

            return closest_enemy  # Возвращаем атакованного врага

        return None

    def increase_concentration(self, amount=None):
        """Увеличение концентрации после удара"""
        if amount is None:
            amount = self.concentration_gain_per_hit

        self.concentration = min(self.max_concentration, self.concentration + amount)

    def use_concentration_for_healing(self):
        """Использование концентрации для лечения - тратится только необходимое количество"""
        # Если здоровье уже полное, не тратим концентрацию
        if self.health >= PLAYER_MAX_HEALTH:
            return False

        # Если концентрация пуста, не можем лечиться
        if self.concentration <= 0:
            return False

        # Вычисляем сколько здоровья не хватает до максимума
        health_needed = PLAYER_MAX_HEALTH - self.health

        # Вычисляем сколько концентрации нужно для этого лечения (2:1)
        concentration_needed = health_needed * 2  # 1 HP = 2% концентрации

        # Определяем сколько концентрации мы фактически потратим
        if self.concentration >= concentration_needed:
            # Если концентрации хватает на полное лечение
            concentration_used = concentration_needed
            health_gained = health_needed
        else:
            # Если концентрации не хватает, используем всю
            concentration_used = self.concentration
            health_gained = self.concentration / 2  # 2% концентрации = 1 HP

        # Применяем лечение
        self.health += health_gained
        self.concentration -= concentration_used

        # Эффект лечения
        self.heal_effect_timer = 30
        self.heal_flash_timer = 40

        return True

    def update(self, keys, ticks, sdvigy):
        """Обновление состояния игрока с проверкой на смерть"""
        if self.is_dead:
            self.update_effects()  # Обновляем только эффекты
            return

        # Умная проверка для показа подсказки лечения
        if (self.health <= 30 and
                self.concentration > 0 and  # Есть что тратить
                not self.heal_hint_shown and
                not self.show_attack_hint):  # Не показывать одновременно с подсказкой атаки

            self.show_heal_hint = True
            self.heal_hint_shown = True

        # Сбрасываем флаг когда здоровье восстанавливается достаточно
        elif self.health >= 50 or self.concentration == 0:
            self.show_heal_hint = False

        # Полный сброс при полном здоровье
        if self.health >= 80:
            self.heal_hint_shown = False

        # Обновляем кулдаун атаки
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Старая логика обновления...
        self.handle_input(keys, ticks, sdvigy)

        # Сбрасываем анимацию ходьбы если не двигаемся
        if self.on_ground and not keys[pygame.K_d] and not keys[pygame.K_a]:
            self.walking = False

        # ОБНОВЛЕНИЕ ДЛЯ ST=2
        if self.st == 2:
            self.coords_increase += 1

            if self.coords_increase % 5 == 0:
                self.SMRt -= 1

            if self.coords_increase >= 175:
                self.st = 3
                self.coords_increase = 0

        # Проверка на землю (масштабированная)
        ground_level = scale_value(-415)
        if sdvigy <= ground_level and not self.web_swinging:
            if self.st == -100:
                self.st = 0
                try:
                    land_sound = pygame.mixer.Sound(SOUND_FILES['punch_ground'])
                    land_sound.play()
                except:
                    pass
            self.on_ground = True
            if self.st in [2, 3]:
                self.st = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Обновляем эффекты
        self.update_effects()

    def draw(self, screen, sdvigx, sdvigy):
        """Отрисовка игрока"""
        sprite_key, draw_position, rotation = self.get_render_info()

        if sprite_key in self.sprites:
            sprite = self.sprites[sprite_key]

            if rotation != 0:
                sprite = pygame.transform.rotate(sprite, rotation)

            # Фиксированная позиция на экране (уже масштабирована через конфиг)
            screen_x = self.screen_x + draw_position[0]
            screen_y = self.screen_y + draw_position[1]

            screen.blit(sprite, (screen_x, screen_y))

            # Отрисовка паутины
            if self.web_swinging:
                self.draw_web_line(screen, sdvigx, sdvigy)

    def get_render_info(self):
        """Определение текущего спрайта с масштабированными смещениями"""
        direction = "" if self.facing_right else "_rev"

        if self.health <= 0:
            return "death", (scale_value(27), scale_value(140)), 0
        if self.st == -100:
            return "swing_7", (scale_value(27), 0), -65
        elif self.st == 0:
            if self.on_ground:
                if hasattr(self, 'walking') and self.walking:
                    walk_cycle = int(pygame.time.get_ticks() / 100) % 5 + 1
                    return f"walk_{walk_cycle}{direction}", (scale_value(20), scale_value(140)), 0
                else:
                    return "idle_1", (scale_value(20), scale_value(140)), 0
            else:
                return f"swing_8{direction}", (0, scale_value(150)), 0
        elif self.st == 1 or self.st == -1:
            if self.coords_increase < 310:
                rotation = -40 + (self.coords_increase / 310) * 40
            else:
                rotation = (self.coords_increase - 310) / 310 * 45
            rotation = max(-40, min(45, rotation))
            if not self.facing_right:
                rotation = -rotation
            return f"swing_1{direction}", (scale_value(20), scale_value(100)), rotation
        elif self.st == 2:
            # Полет после отпускания паутины
            rotation = self.SMRt

            # Инвертируем угол для направления влево
            if not self.facing_right:
                rotation = -rotation

            return f"swing_7{direction}", (scale_value(60), scale_value(40)), rotation
        elif self.st == 3:
            # Свободное падение
            rotation = -65
            if not self.facing_right:
                rotation = -rotation
            return f"swing_7{direction}", (scale_value(27), 0), rotation
        elif self.st == 4:
            return f"jump{direction}", (scale_value(40), scale_value(40)), 0
        return "idle_1", (scale_value(20), scale_value(140)), 0

    def draw_web_line(self, screen, sdvigx, sdvigy):
        """Отрисовка линии паутины с масштабированием"""
        # Примерная высота, где паутина цепляется к зданию
        building_top_y = -2000 + SCREEN_HEIGHT - scale_value(100) + sdvigy + scale_value(100)

        # Вычисляем координаты края спрайта на экране
        sprite_key, draw_position, rotation = self.get_render_info()
        sprite_screen_x = self.screen_x + draw_position[0]
        sprite_screen_y = self.screen_y + draw_position[1]

        # Создаём Rect
        sprite_rect = pygame.Rect(sprite_screen_x, sprite_screen_y, self.width, self.height)

        # Выбираем стартовую точку в зависимости от направления
        if self.facing_right:
            start_x, start_y = sprite_rect.topright
        else:
            start_x, start_y = sprite_rect.topleft

        # end_x — координата на экране, где крепится паутина к зданию
        if self.facing_right:
            end_x = SCREEN_WIDTH - scale_value(250) - self.coords_increase * 2
        else:
            end_x = scale_value(300) + self.coords_increase * 2

        end_y = building_top_y

        # Масштабируем толщину линии
        line_thickness = max(1, scale_value(2))
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), line_thickness)

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