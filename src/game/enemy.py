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

        # Масштабируемые размеры
        self.width = scale_value(170)
        self.height = scale_value(170)

        # Состояния
        self.state = "idle"
        self.facing_right = False
        self.health = 100

        # Скорости (не масштабируются - геймплейные параметры)
        self.base_speed = 2.0
        self.patrol_speed = self.base_speed / 2  # 1.0 - медленное патрулирование
        self.chase_speed = self.base_speed * 1.2  # 2.4 - в 1.2 раза быстрее базовой для преследования

        # Минимальное расстояние до игрока (масштабируется)
        self.min_approach_distance = scale_value(110)

        # Для предотвращения наложения
        self.avoidance_force = 0

        # Анимация и таймеры (не масштабируются)
        self.walk_counter = 0
        self.attack_cooldown = 0
        self.hurt_timer = 0

        # Спрайты (загружаем один раз)
        self.sprites = {}
        self.load_sprites()

        # Зоны обнаружения (масштабируются)
        self.detection_range = scale_value(300)
        self.attack_range = scale_value(140)

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

    def take_damage(self, amount):
        """Получение урона врагом"""
        if self.state == "dead":
            return

        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.state = "dying"
            # Через некоторое время переходим в dead
            self.hurt_timer = 30  # 30 кадров для анимации смерти
        else:
            self.state = "hurt"
            self.hurt_timer = 20  # 20 кадров для анимации получения урона

    def avoid_other_enemies(self, enemies):
        """Оптимизированное избегание других врагов"""
        avoidance_radius = MIN_DISTANCE_BETWEEN_ENEMIES
        separation_force = 0
        nearby_count = 0

        for other in enemies:
            if other is self or other.state == "dead":
                continue

            distance = abs(other.world_x - self.world_x)
            if distance < avoidance_radius:
                nearby_count += 1
                # Вычисляем силу отталкивания
                force = (avoidance_radius - distance) / avoidance_radius

                if self.world_x < other.world_x:
                    separation_force -= force
                else:
                    separation_force += force

        # Усредняем силу, если врагов несколько
        if nearby_count > 0:
            separation_force /= nearby_count

        self.avoidance_force = separation_force * 3  # Множитель для усиления эффекта

    def update(self, player, sdvigx, enemies):
        """Обновление состояния врага"""
        if self.state == "dead":
            return
        elif self.state == "dying":
            self.hurt_timer -= 1
            if self.hurt_timer <= 0:
                self.state = "dead"
            return

        # Таймеры
        self.attack_cooldown = max(0, self.attack_cooldown - 1)
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
            if self.hurt_timer == 0 and self.state == "hurt":
                self.state = "idle"

        # Вычисляем world_x игрока: player.screen_x фиксирован, sdvigx - сдвиг камеры
        player_world_x = player.screen_x - sdvigx

        # Избегание других врагов (если передан список)
        if enemies is not None:
            self.avoid_other_enemies(enemies)

        # Логика поведения
        self.handle_behavior(player, player_world_x)

        # Применяем силу отталкивания от других врагов
        if abs(self.avoidance_force) > 0.1:
            self.world_x += self.avoidance_force
            # Плавное затухание силы
            self.avoidance_force *= 0.8

    def handle_behavior(self, player, player_world_x):
        """Логика поведения"""
        distance_to_player = abs(player_world_x - self.world_x)
        self.facing_right = player_world_x > self.world_x

        if self.state in ["hurt", "dying"]:
            return

        # Если есть сильное отталкивание, временно приостанавливаем обычное поведение
        if abs(self.avoidance_force) > 1.5:
            self.state = "idle"
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
        final_y = road_y - self.height + scale_value(50)  # Масштабируем отступ от дороги

        sprite = self.get_current_sprite()
        if not self.facing_right:
            sprite = pygame.transform.flip(sprite, True, False)

        screen.blit(sprite, (screen_x, final_y))
        self.draw_health_bar(screen, screen_x, final_y)

    def get_current_sprite(self):
        """Текущий спрайт"""
        return self.sprites['idle']

    def draw_health_bar(self, screen, screen_x, y_pos):
        """Полоска здоровья (масштабируется)"""
        bar_width = scale_value(100)
        bar_height = scale_value(6)
        bar_x = screen_x + (self.width - bar_width) // 2
        bar_y = y_pos - scale_value(15)  # Масштабируем отступ сверху

        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        health_width = max(0, (self.health / 100) * bar_width)
        if health_width > 0:
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
