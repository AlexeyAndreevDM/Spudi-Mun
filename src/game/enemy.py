import pygame
import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.config import *


class Enemy:
    def __init__(self, world_x):
        # Позиция в мире (независимая от камеры)
        self.world_x = world_x
        self.width = 170
        self.height = 170

        # Состояния
        self.state = "idle"
        self.facing_right = False
        self.health = 100

        # Скорости (только 2: базовая для преследования, в 2 раза медленнее для патрулирования)
        self.base_speed = 2.0
        self.patrol_speed = self.base_speed / 2  # 1.0 - медленное патрулирование
        self.chase_speed = self.base_speed * 1.2  # 2.4 - в 1.2 раза быстрее базовой для преследования

        # Минимальное расстояние до игрока (чтобы не накладываться, +50px запас)
        self.min_approach_distance = 110

        # Анимация и таймеры
        self.walk_counter = 0
        self.attack_cooldown = 0
        self.hurt_timer = 0

        # Спрайты (загружаем один раз)
        self.sprites = {}
        self.load_sprites()

        # Зоны обнаружения
        self.detection_range = 300
        self.attack_range = 140

    def load_sprites(self):
        """Загрузка спрайтов врага - один раз"""
        try:
            black_cube_path = os.path.join(BASE_DIR, "black_cube.png")
            if os.path.exists(black_cube_path):
                base_sprite = load_image_safe(black_cube_path, convert_alpha=True)
                base_sprite = pygame.transform.scale(base_sprite, (self.width, self.height))
                self.sprites = {
                    'idle': base_sprite,
                    'walk_1': base_sprite,
                    'walk_2': base_sprite,
                    'attack': base_sprite,
                    'hurt': base_sprite,
                    'dying': base_sprite,
                }
                print("Спрайты врага загружены успешно")
            else:
                self.create_fallback_sprites()
        except Exception as e:
            print(f"Ошибка загрузки спрайтов врага: {e}")
            self.create_fallback_sprites()

    def create_fallback_sprites(self):
        """Fallback спрайты"""
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

    def update(self, player, sdvigx):
        """Обновление врага - теперь с sdvigx для расчета world позиции игрока"""
        if self.state == "dead":
            return

        # Таймеры
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0 and self.state == "hurt":
                self.state = "idle"

        # Вычисляем world_x игрока: player.screen_x фиксирован, sdvigx - сдвиг камеры
        player_world_x = player.screen_x - sdvigx

        # Логика поведения
        self.handle_behavior(player, player_world_x)

    def handle_behavior(self, player, player_world_x):
        """Логика поведения"""
        distance_to_player = abs(player_world_x - self.world_x)
        self.facing_right = player_world_x > self.world_x

        if self.state in ["hurt", "dying"]:
            return

        if distance_to_player <= self.attack_range and self.attack_cooldown == 0:
            self.attack(player)
        elif distance_to_player <= self.detection_range:
            self.move_towards_player(player_world_x)
        else:
            self.patrol()

    def patrol(self):
        """Медленное патрулирование"""
        if self.state != "walking" or random.random() < 0.02:
            self.state = "walking"
            if random.random() < 0.01:
                self.facing_right = not self.facing_right

        if self.state == "walking":
            dir = 1 if self.facing_right else -1
            self.world_x += self.patrol_speed * dir
            self.walk_counter = (self.walk_counter + 1) % 1000

        # Ограничение мира (чтобы не ушли слишком далеко)
        if self.world_x < -2000:
            self.world_x = -2000
            self.facing_right = True
        elif self.world_x > 3000:
            self.world_x = 3000
            self.facing_right = False

    def move_towards_player(self, player_world_x):
        """Преследование с быстрой скоростью и остановкой на расстоянии"""
        distance_to_player = abs(player_world_x - self.world_x)

        if distance_to_player > self.min_approach_distance:
            self.state = "walking"
            dir = 1 if player_world_x > self.world_x else -1
            self.world_x += self.chase_speed * dir
            self.walk_counter = (self.walk_counter + 1) % 1000
        else:
            self.state = "idle"  # Остановка, чтобы не налезать

    def attack(self, player):
        """Атака с уроном игроку только на земле"""
        self.state = "attacking"
        self.attack_cooldown = 60
        player.take_damage(ENEMY_DAMAGE)  # Вызов метода игрока с проверкой on_ground

    def draw(self, screen, sdvigx, road_y):
        """Отрисовка с учетом sdvigx (камеры)"""
        if self.state == "dead":
            return

        # Экранная позиция = world_x + sdvigx
        screen_x = self.world_x + sdvigx
        final_y = road_y - self.height + 50

        sprite = self.get_current_sprite()
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)

        screen.blit(sprite, (screen_x, final_y))
        self.draw_health_bar(screen, screen_x, final_y)

    def get_current_sprite(self):
        """Текущий спрайт"""
        return self.sprites['idle']

    def draw_health_bar(self, screen, screen_x, y_pos):
        """Полоска здоровья"""
        bar_width = 100
        bar_height = 6
        bar_x = screen_x + (self.width - bar_width) // 2
        bar_y = y_pos - 15

        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_width = max(0, (self.health / 100) * bar_width)
        if health_width > 0:
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))