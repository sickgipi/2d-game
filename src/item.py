import math

import pygame

from .assets import load_frames, shadow
from .settings import IMAGES_DIR, ITEM_BLINK_TIME, ITEM_LIFETIME, ITEM_SIZE

# I tipi di oggetto, nell'ordine dei frame di items.png
HEART = "heart"
RUPEE = "rupee"
ITEM_KINDS = [HEART, RUPEE]


def item_image(kind):
    """L'immagine di un oggetto (32x32) presa da items.png."""
    frames = load_frames(IMAGES_DIR / "items.png", 32, 32)[0]
    return frames[ITEM_KINDS.index(kind)]


class Item:
    """Un oggetto a terra che il giocatore puo' raccogliere.
    Dopo un po' di tempo sparisce, lampeggiando prima di farlo."""

    def __init__(self, kind, center):
        self.kind = kind
        self.rect = pygame.Rect(0, 0, ITEM_SIZE, ITEM_SIZE)
        self.rect.center = center
        self.lifetime = ITEM_LIFETIME
        self.image = item_image(kind)

    @property
    def expired(self):
        return self.lifetime <= 0

    def update(self, dt):
        self.lifetime -= dt

    def draw(self, surface, camera):
        # Lampeggia quando sta per sparire
        if self.lifetime < ITEM_BLINK_TIME and int(self.lifetime * 10) % 2 == 0:
            return
        rect = camera.apply(self.rect)
        ground = shadow(ITEM_SIZE, ITEM_SIZE // 3)
        surface.blit(ground, ground.get_rect(center=rect.midbottom))
        # Fluttua su e giu' (math.sin va da -1 a 1)
        float_offset = round(math.sin(self.lifetime * 5) * 2) - 3
        surface.blit(self.image, self.image.get_rect(center=(rect.centerx, rect.centery + float_offset)))
