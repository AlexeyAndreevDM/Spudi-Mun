import pygame
from src.config import *


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 1.0

    def follow_player(self, player):
        """Следование камеры за игроком с некоторым отставанием"""
        target_x = player.x - self.width // 2
        target_y = player.y - self.height // 2

        # Плавное движение камеры
        self.x += (target_x - self.x) * 0.05
        self.y += (target_y - self.y) * 0.05

        # Ограничения камеры (если нужно)
        self.x = max(0, self.x)
        self.y = max(0, self.y)

    def apply(self, entity):
        """Применение смещения камеры к объекту"""
        return entity.x - self.x, entity.y - self.y

    def update(self, dx, dy):
        """Обновление позиции камеры"""
        self.x += dx
        self.y += dy