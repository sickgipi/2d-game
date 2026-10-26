"""Caricamento di immagini e spritesheet."""
from functools import lru_cache

import pygame


def load_image(path):
    """Carica un'immagine mantenendo la trasparenza.
    (Va chiamata dopo aver creato la finestra, per via di convert_alpha.)"""
    return pygame.image.load(path).convert_alpha()


@lru_cache(maxsize=None)
def load_frames(path, frame_width, frame_height):
    """Ritaglia uno spritesheet in una griglia di frame.
    Restituisce una lista di righe, ognuna e' una lista di Surface.
    Il risultato viene memorizzato: caricare lo stesso file piu' volte
    (es. per ogni nemico) non rilegge il disco."""
    sheet = load_image(path)
    rows = []
    for y in range(0, sheet.get_height(), frame_height):
        row = [sheet.subsurface((x, y, frame_width, frame_height))
               for x in range(0, sheet.get_width(), frame_width)]
        rows.append(row)
    return rows


@lru_cache(maxsize=None)
def shadow(width, height):
    """Un'ombra ovale semitrasparente da mettere sotto i personaggi."""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(surface, (0, 0, 0, 70), surface.get_rect())
    return surface


def tinted(image, color):
    """Copia dell'immagine schiarita (per l'effetto 'colpito')."""
    result = image.copy()
    result.fill(color, special_flags=pygame.BLEND_RGB_ADD)
    return result
