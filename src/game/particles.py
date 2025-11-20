# класс частиц - отклонен
class SimpleParticle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = random.randint(2, 6)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        return self.life > 0

    def draw(self, screen):
        alpha = min(255, self.life * 8)
        color = (255, 200, 100, int(alpha))
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (self.size, self.size), self.size)
        screen.blit(surf, (self.x - self.size, self.y - self.size))