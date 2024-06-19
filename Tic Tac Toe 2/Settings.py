import sys
from Button import*
from Computer import*

def load_image(filename, size=None):
    image = pygame.image.load(f"images/{filename}").convert_alpha()
    if size:
        image = pygame.transform.scale_by(image, size)
    return image

def load_audio(filename):
    return pygame.mixer.Sound(f"audio/{filename}")


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 570

SIZE = 5
MUSIC_VOLUME = 0.5

FADE = 200

THINKING_DELAY = 25