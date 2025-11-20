import os
import pygame

# =============================================
# БАЗОВЫЕ НАСТРОЙКИ ПРОЕКТА
# =============================================

# Корневая директория проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = "Spudi-Mun"

# =============================================
# ПУТИ К ФАЙЛАМ И РЕСУРСАМ
# =============================================

# Основные директории
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Изображения
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
CHARACTERS_DIR = os.path.join(IMAGES_DIR, "characters")
SPIDER_MAN_DIR = os.path.join(CHARACTERS_DIR, "spider_man")
ENEMIES_DIR = os.path.join(CHARACTERS_DIR, "enemies")
BACKGROUNDS_DIR = os.path.join(IMAGES_DIR, "backgrounds")
EFFECTS_DIR = os.path.join(IMAGES_DIR, "effects")

# Конкретные пути для спрайтов паука
SPIDER_CLASSIC_DIR = os.path.join(SPIDER_MAN_DIR, "classic")
SPIDER_IRON_DIR = os.path.join(SPIDER_MAN_DIR, "iron_spider")
SPIDER_WEBBED_DIR = os.path.join(SPIDER_MAN_DIR, "webbed")
SPIDER_UPGRADED_DIR = os.path.join(SPIDER_MAN_DIR, "upgraded")

# Меню
MENU_MAIN_DIR = os.path.join(IMAGES_DIR, "main_menu")
MENU_PAUSE_DIR = os.path.join(IMAGES_DIR, "pause_menu")

# Аудио
AUDIO_DIR = os.path.join(ASSETS_DIR, "audio")
MUSIC_DIR = os.path.join(AUDIO_DIR, "music")
SOUNDS_DIR = os.path.join(AUDIO_DIR, "sounds")
SOUNDS_SWING_DIR = os.path.join(SOUNDS_DIR, "swing")
SOUNDS_PUNCHES_DIR = os.path.join(SOUNDS_DIR, "punches")
SOUNDS_UI_DIR = os.path.join(SOUNDS_DIR, "ui")

# Шрифты
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# Видео
VIDEOS_DIR = os.path.join(ASSETS_DIR, "videos")
CUTSCENES_DIR = os.path.join(VIDEOS_DIR, "cutscenes")

# Данные
SAVES_DIR = os.path.join(DATA_DIR, "saves")

# Заглушка для отсутствующих изображений
PLACEHOLDER_IMAGE = os.path.join(BASE_DIR, "white_cube.png")

# =============================================
# НАСТРОЙКИ ЭКРАНА И ОТОБРАЖЕНИЯ
# =============================================

# Размеры экрана
SCREEN_WIDTH = 1470
SCREEN_HEIGHT = 900
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT + 20)  # +20 для заголовка

# Масштабирование (для разных разрешений)
SCALE_X = 1
SCALE_Y = 1

# Частота кадров
FPS = 60

# =============================================
# ИГРОВЫЕ КОНСТАНТЫ
# =============================================

# Физика
GRAVITY = 0.5
TERMINAL_VELOCITY = 20

# Игрок
PLAYER_WIDTH = 150
PLAYER_HEIGHT = 150
PLAYER_START_X = SCREEN_WIDTH // 2 - 150 + 15
PLAYER_START_Y = SCREEN_HEIGHT // 2 - 200 + 7
PLAYER_SPEED = 5
JUMP_STRENGTH = -10
SWING_STRENGTH = 4

# Сдвиг камеры
SCROLL_SPEED = 2
INITIAL_SCROLL_Y = -330

# Здоровье
PLAYER_MAX_HEALTH = 100
ENEMY_DAMAGE = 10

# Концентрация
MAX_CONCENTRATION = 100
CONCENTRATION_GAIN_PER_HIT = 5
HEALING_PER_FULL_CONCENTRATION = 50  # 100% концентрации = 50 здоровья

# Дистанции между врагами
MIN_DISTANCE_BETWEEN_ENEMIES = 100  # минимальная дистанция между врагами в мировых координатах

# Эффекты повреждений и смерти
DAMAGE_FLASH_DURATION = 15    # кадров для мигания при уроне
HEAL_FLASH_DURATION = 20      # кадров для мигания при лечении
DEATH_FLASH_DURATION = 45     # кадров для мигания при смерти (750 мс)
DEATH_DELAY_DURATION = 90     # кадров задержки перед экраном смерти (1500 мс)
FLASH_ALPHA = 128             # прозрачность эффектов

# =============================================
# НАСТРОЙКИ СЛОЖНОСТИ
# =============================================

DIFFICULTY_SETTINGS = {
    'FN': 0.5,  # Friendly Neighborhood
    'TA': 1.0,  # The Amazing
    'S': 1.8,  # Spectacular
    'U': 3.0  # Ultimate
}

# Текущие настройки (будут меняться в игре)
DIFFICULTY = 'TA'
DIFFICULTY_MULTIPLIER = DIFFICULTY_SETTINGS[DIFFICULTY]
MUSIC_STATUS = -1
CURRENT_SUIT = 'cs'
CURRENT_CUTSCENE = 0
SUBTITLES = 'OFF'

# =============================================
# ЦВЕТА
# =============================================

# Основные цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Игровые цвета
HEALTH_GREEN = (50, 191, 73)
HEALTH_RED = (255, 0, 59)
MENU_BLUE = (53, 108, 161)
MENU_DARK_BLUE = (24, 80, 133)
MENU_HIGHLIGHT = (161, 3, 34)

# UI цвета
UI_BACKGROUND = (29, 31, 36)
UI_ACCENT = (28, 6, 46)

# =============================================
# НАСТРОЙКИ АУДИО
# =============================================

# Громкость
MUSIC_VOLUME = 0.3
SOUND_VOLUME = 0.7

# Конкретные аудиофайлы
MUSIC_FILES = {
    'main_menu': os.path.join(MUSIC_DIR, "Web Launch.mp3"),
    'pause_menu': os.path.join(MUSIC_DIR, "Pause Menu.mp3"),
    'gameplay': os.path.join(MUSIC_DIR, "The Golden Age.mp3")
}

SOUND_FILES = {
    'thwip': [
        os.path.join(SOUNDS_SWING_DIR, "Thwip_sound.wav"),
        os.path.join(SOUNDS_SWING_DIR, "Thwip_sound1.mp3"),
        os.path.join(SOUNDS_SWING_DIR, "Thwip_sound2.mp3"),
        os.path.join(SOUNDS_SWING_DIR, "Thwip_sound3.mp3")
    ],
    'swing': os.path.join(SOUNDS_SWING_DIR, "Swing_sound.mp3"),
    'punch_ground': os.path.join(SOUNDS_PUNCHES_DIR, "spider_punch_ground.mp3"),
    'punch': os.path.join(SOUNDS_PUNCHES_DIR, "spider_punch.mp3"),
    'death': os.path.join(SOUNDS_DIR, "Spider_death.mp3"),
    'air_sound': os.path.join(SOUNDS_DIR, "air_sound.mp3"),
    'heal': [  # Добавляем звуки лечения
        os.path.join(SOUNDS_UI_DIR, "heal1.wav"),
        os.path.join(SOUNDS_UI_DIR, "heal2.wav"),
        os.path.join(SOUNDS_UI_DIR, "heal3.wav")
    ]
}

# =============================================
# НАСТРОЙКИ ШРИФТОВ
# =============================================

FONT_FILES = {
    'gulag': os.path.join(FONTS_DIR, "GULAG.otf"),
    'monospace_bold': os.path.join(FONTS_DIR, "MonospaceBold.ttf"),
    'monospace_regular': os.path.join(FONTS_DIR, "MonospaceRegular.ttf"),
    'old_soviet': os.path.join(FONTS_DIR, "Old-Soviet.otf"),
    'avengeance': os.path.join(FONTS_DIR, "Avengeance.otf"),
    'podkova': os.path.join(FONTS_DIR, "Podkova.ttf")
}

FONT_SIZES = {
    'title': 120,
    'large': 40,
    'medium': 30,
    'normal': 25,
    'small': 20,
    'tiny': 17
}

# =============================================
# НАСТРОЙКИ ТЕКСТА И СУБТИТРОВ
# =============================================

SUBTITLES_TEXT = [
    'Yuri Watanabe: Captain Watanabe',
    'Spider-Man: Did you take him down yet?',
    'Yuri Watanabe: No',
    'Yuri Watanabe: We\'re at Fisk Tower, but still waiting on the warrant',
    'Spider-Man: Mind if I join in on the fun?',
    'Yuri Watanabe: You know how his lawyers are… these one needs to go by the book.',
    'Spider-Man: C\'mon Yuri, I\'ve been waiting eight years for this.',
    'Yuri Watanabe: You really want to help?',
    'Yuri Watanabe: Head to Times Square, sounds like his guys are',
    'trying to keep my backup from reaching the scene…',
    'Spider-Man: You got it - almost there!'
]

SUBTITLES_TIMING = [
    '1000 4000', '4000 5200', '5200 6000', '6000 8500', '8500 11000',
    '11000 14000', '14000 17000', '17000 18500', '18500 22000',
    '22000 24000', '24000 26200'
]

# =============================================
# НАСТРОЙКИ КОСТЮМОВ
# =============================================

SUITS = {
    'cs': 'Classic Suit',
    'iss': 'Iron Spider',
    'ws': 'Webbed Suit',
    'us': 'Upgraded Suit',
    'ss': 'Night Monkey',
    'as': 'Amazing Suit',
    'is': 'Integrated Suit',
    'ios': 'Black and Gold Suit'
}

SUIT_ICONS = [
    'cs_icon.png', 'iss_icon.png', 'ws_icon.png', 'us_icon.png',
    'ss_icon.png', 'as_icon.png', 'is_icon.png', 'ios_icon.png'
]


# =============================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ПУТЯМИ
# =============================================

def get_image_path(*path_parts):
    """Безопасно создает путь к изображению"""
    return os.path.join(IMAGES_DIR, *path_parts)


def get_sound_path(*path_parts):
    """Безопасно создает путь к звуку"""
    return os.path.join(SOUNDS_DIR, *path_parts)


def get_music_path(*path_parts):
    """Безопасно создает путь к музыке"""
    return os.path.join(MUSIC_DIR, *path_parts)


def get_font_path(font_name):
    """Возвращает путь к шрифту"""
    return FONT_FILES.get(font_name, FONT_FILES['monospace_bold'])


def load_image_safe(path, default_image=PLACEHOLDER_IMAGE, convert_alpha=True):
    """Безопасно загружает изображение. Если файл не найден, использует изображение-заглушку."""
    print(f"[CONFIG] Загрузка: {path}")
    print(f"[CONFIG] Заглушка: {default_image}")
    print(f"[CONFIG] Заглушка существует: {os.path.exists(default_image)}")

    try:
        if convert_alpha:
            image = pygame.image.load(path).convert_alpha()
        else:
            image = pygame.image.load(path).convert()
        print(f"[CONFIG] Успешно загружено: {path}")
        return image
    except (pygame.error, FileNotFoundError) as e:
        print(f"[CONFIG] Ошибка {path}: {e}, используем заглушку")
        try:
            if convert_alpha:
                return pygame.image.load(default_image).convert_alpha()
            else:
                return pygame.image.load(default_image).convert()
        except Exception as e2:
            print(f"[CONFIG] Критическая ошибка заглушки: {e2}")
            surf = pygame.Surface((50, 50))
            surf.fill((255, 0, 255))
            return surf


# =============================================
# ПРОВЕРКА СУЩЕСТВОВАНИЯ ДИРЕКТОРИЙ
# =============================================

def ensure_directories():
    """Создает необходимые директории если они не существуют"""
    directories = [
        ASSETS_DIR, IMAGES_DIR, CHARACTERS_DIR, SPIDER_MAN_DIR,
        ENEMIES_DIR, BACKGROUNDS_DIR, EFFECTS_DIR,
        AUDIO_DIR, MUSIC_DIR, SOUNDS_DIR, SOUNDS_SWING_DIR,
        SOUNDS_PUNCHES_DIR, SOUNDS_UI_DIR, FONTS_DIR,
        VIDEOS_DIR, CUTSCENES_DIR, DATA_DIR, SAVES_DIR
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# Автоматически создаем директории при импорте
ensure_directories()
