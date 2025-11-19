import pygame
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import *


class Enemy:
    def __init__(self, x):
        self.screen_x = x
        self.width = 170
        self.height = 170

        # Состояния
        self.state = "idle"
        self.facing_right = False
        self.health = 100
        self.speed = 2

        # Анимация
        self.walk_counter = 0
        self.attack_cooldown = 0
        self.hurt_timer = 0

        # Спрайты (создаем один раз при инициализации)
        self.sprites = {}
        self.load_sprites()

        # Кэш для отладочного текста
        self.debug_font = None
        self.last_debug_update = 0

        # Зона обнаружения игрока
        self.detection_range = 300
        self.attack_range = 80

    def load_sprites(self):
        """Загрузка спрайтов врага - ОДИН РАЗ при создании"""
        try:
            # Загружаем настоящий black_cube.png
            black_cube_path = os.path.join(BASE_DIR, "black_cube.png")
            if os.path.exists(black_cube_path):
                base_sprite = load_image_safe(black_cube_path, convert_alpha=True)
                base_sprite = pygame.transform.scale(base_sprite, (self.width, self.height))

                # Создаем варианты для разных состояний из одного спрайта
                self.sprites = {
                    'idle': base_sprite,
                    'walk_1': base_sprite,
                    'walk_2': base_sprite,  # Можно добавить легкое изменение для анимации
                    'attack': base_sprite,
                    'hurt': base_sprite,
                    'dying': base_sprite,
                }
                print("Спрайты врага загружены успешно")
            else:
                # Fallback - простой черный квадрат
                self.create_fallback_sprites()

        except Exception as e:
            print(f"Ошибка загрузки спрайтов врага: {e}")
            self.create_fallback_sprites()

    def create_fallback_sprites(self):
        """Создание fallback спрайтов один раз"""
        surf = pygame.Surface((self.width, self.height))
        surf.fill(BLACK)
        self.sprites = {
            'idle': surf,
            'walk_1': surf,
            'walk_2': surf,
            'attack': surf,
            'hurt': surf,
            'dying': surf,
        }

    def update(self, player):
        """Обновление состояния врага - оптимизировано"""
        if self.state == "dead":
            return

        # Быстрые проверки таймеров
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0 and self.state == "hurt":
                self.state = "idle"

        # Логика поведения
        self.handle_behavior(player)

    def handle_behavior(self, player):
        """Основная логика поведения врага - оптимизировано"""
        distance_to_player = abs(player.screen_x - self.screen_x)

        # Быстрая проверка направления
        self.facing_right = player.screen_x > self.screen_x

        if self.state in ["hurt", "dying"]:
            return

        if distance_to_player <= self.attack_range and self.attack_cooldown == 0:
            self.attack(player)
        elif distance_to_player <= self.detection_range:
            self.move_towards_player()
        else:
            self.patrol()

    def patrol(self):
        """Патрулирование - оптимизировано"""
        if self.state != "walking" or random.random() < 0.02:
            self.state = "walking"
            if random.random() < 0.01:
                self.facing_right = not self.facing_right

        if self.state == "walking":
            if self.facing_right and self.screen_x < SCREEN_WIDTH - self.width:
                self.screen_x += self.speed
            elif not self.facing_right and self.screen_x > 0:
                self.screen_x -= self.speed

            self.walk_counter = (self.walk_counter + 1) % 1000  # Предотвращаем переполнение

    def move_towards_player(self):
        """Движение к игроку - оптимизировано"""
        self.state = "walking"

        if self.facing_right and self.screen_x < SCREEN_WIDTH - self.width:
            self.screen_x += self.speed
        elif not self.facing_right and self.screen_x > 0:
            self.screen_x -= self.speed

        self.walk_counter = (self.walk_counter + 1) % 1000

    def attack(self, player):
        """Атака игрока - БЕЗ УРОНА"""
        self.state = "attacking"
        self.attack_cooldown = 60
        # Убрал вывод в консоль для производительности

    def draw(self, screen, road_y):
        """Отрисовка врага - ОПТИМИЗИРОВАНА"""
        if self.state == "dead":
            return

        # Вычисляем финальную позицию
        final_y = road_y - self.height + 50

        # Получаем спрайт (уже загруженный)
        sprite = self.get_current_sprite()

        # Зеркалим если нужно
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)

        # Отрисовываем врага
        screen.blit(sprite, (self.screen_x, final_y))

        # Отрисовываем здоровье (быстро)
        self.draw_health_bar(screen, final_y)

        # ОТКЛЮЧАЕМ отладочную информацию для производительности
        # self.draw_debug_info(screen, final_y)

    def get_current_sprite(self):
        """Получение текущего спрайта - оптимизировано"""
        # Все состояния используют один спрайт для производительности
        return self.sprites['idle']

    def draw_health_bar(self, screen, y_pos):
        """Отрисовка полоски здоровья - оптимизировано"""
        bar_width = 100
        bar_height = 6  # Уменьшили высоту для производительности
        bar_x = self.screen_x + (self.width - bar_width) // 2
        bar_y = y_pos - 15

        # Рисуем сразу без промежуточных поверхностей
        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_width = max(0, (self.health / 100) * bar_width)
        if health_width > 0:
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))

    # ЗАКОММЕНТИРОВАЛИ отладочную информацию для производительности
    # def draw_debug_info(self, screen, y_pos):
    #     """Отрисовка отладочной информации - ВРЕМЕННО ОТКЛЮЧЕНА"""
    #     pass