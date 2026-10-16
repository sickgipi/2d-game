"""Genera gli sprite segnaposto del gioco (pixel art 16x16, ingranditi x2).

Non serve per giocare: serve solo a creare i file PNG in assets/images/.
Quando avrai grafica vera, sostituisci quei PNG (mantenendo la stessa
disposizione dei frame) e questo script non ti servira' piu'.

Uso:  python tools/make_placeholder_assets.py
"""
import os
import random
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
import pygame

pygame.init()

OUT = Path(__file__).resolve().parent.parent / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)

OUTLINE = (25, 20, 30)
SKIN = (245, 205, 160)
GREEN = (70, 170, 70)
DGREEN = (40, 120, 50)
BROWN = (130, 80, 40)
BOOT = (100, 55, 30)
BELT = (200, 150, 50)
EYE = (30, 30, 40)


def new_canvas(w=16, h=16):
    return pygame.Surface((w, h), pygame.SRCALPHA)


def add_outline(surface, color=OUTLINE):
    """Aggiunge un contorno scuro attorno ai pixel colorati."""
    w, h = surface.get_size()
    source = surface.copy()
    for x in range(w):
        for y in range(h):
            if source.get_at((x, y)).a == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and source.get_at((nx, ny)).a > 0:
                        surface.set_at((x, y), color)
                        break
    return surface


def scale(surface, factor=2):
    w, h = surface.get_size()
    return pygame.transform.scale(surface, (w * factor, h * factor))


def save(surface, name):
    pygame.image.save(surface, str(OUT / name))
    print("creato", name, surface.get_size())


# ---------------- giocatore: 4 direzioni x 4 frame ----------------
def player_frame(direction, step):
    s = new_canvas()
    if direction in ("down", "up"):
        left_len = 2 if step == 1 else 3
        right_len = 2 if step == 3 else 3
        s.fill(BOOT, (5, 12, 3, left_len))
        s.fill(BOOT, (9, 12, 3, right_len))
        s.fill(GREEN, (4, 8, 8, 4))
        s.fill(BELT, (4, 11, 8, 1))
        s.fill(SKIN, (3, 9, 1, 2))
        s.fill(SKIN, (12, 9, 1, 2))
        s.fill(DGREEN, (3, 1, 10, 3))
        if direction == "down":
            s.fill(SKIN, (4, 4, 8, 4))
            s.fill(EYE, (6, 5, 1, 2))
            s.fill(EYE, (9, 5, 1, 2))
            s.fill(BROWN, (4, 4, 1, 2))
            s.fill(BROWN, (11, 4, 1, 2))
        else:
            s.fill(BROWN, (4, 4, 8, 4))
    else:  # "left" (la destra si ottiene specchiando)
        a, b = {0: (7, 8), 1: (5, 10), 2: (7, 8), 3: (6, 9)}[step]
        s.fill(BOOT, (a, 12, 3, 3))
        s.fill(BOOT, (b, 12, 3, 3))
        s.fill(GREEN, (5, 8, 6, 4))
        s.fill(BELT, (5, 11, 6, 1))
        s.fill(SKIN, (6, 9, 3, 2))
        s.fill(DGREEN, (3, 1, 10, 3))
        s.fill(DGREEN, (11, 3, 3, 2))   # la "coda" del cappello
        s.fill(SKIN, (4, 4, 8, 4))
        s.fill(EYE, (5, 5, 1, 2))
        s.fill(BROWN, (9, 4, 3, 3))
    return add_outline(s)


def make_player():
    sheet = new_canvas(64, 64)
    for row, direction in enumerate(["down", "left", "right", "up"]):
        for step in range(4):
            if direction == "right":
                frame = pygame.transform.flip(player_frame("left", step), True, False)
            else:
                frame = player_frame(direction, step)
            sheet.blit(frame, (step * 16, row * 16))
    save(scale(sheet), "player.png")


# ---------------- nemico: slime con 4 frame ----------------
def make_enemy():
    sheet = new_canvas(64, 16)
    sizes = {0: (12, 9), 1: (14, 7), 2: (12, 9), 3: (10, 11)}
    for step in range(4):
        s = new_canvas()
        w, h = sizes[step]
        body = pygame.Rect(0, 0, w, h)
        body.midbottom = (8, 15)
        pygame.draw.ellipse(s, (210, 50, 50), body)
        pygame.draw.ellipse(s, (240, 120, 120), (body.x + 2, body.y + 1, max(2, w // 3), 2))
        eye_y = body.y + h // 2 - 1
        for eye_x in (body.centerx - 3, body.centerx + 1):
            s.fill((255, 255, 255), (eye_x, eye_y, 2, 2))
            s.set_at((eye_x + 1, eye_y + 1), (20, 20, 20))
        sheet.blit(add_outline(s), (step * 16, 0))
    save(scale(sheet), "enemy.png")


# ---------------- spada (rivolta verso l'alto) ----------------
def make_sword():
    s = new_canvas()
    s.fill((215, 222, 235), (7, 1, 2, 8))
    s.fill((255, 255, 255), (7, 1, 1, 8))
    s.fill((230, 190, 60), (5, 9, 6, 1))
    s.fill(BROWN, (7, 10, 2, 4))
    s.fill((230, 190, 60), (7, 14, 2, 1))
    save(scale(add_outline(s)), "sword.png")


# ---------------- tileset: prato, muro, albero, acqua ----------------
def tile_grass():
    rng = random.Random(3)
    s = new_canvas()
    s.fill((84, 170, 76))
    for _ in range(14):
        s.set_at((rng.randrange(16), rng.randrange(16)), (64, 145, 60))
    for _ in range(5):
        s.set_at((rng.randrange(16), rng.randrange(16)), (115, 198, 104))
    return s


def tile_wall():
    s = new_canvas()
    s.fill((125, 125, 135))
    mortar = (80, 80, 92)
    for row in range(4):
        y = row * 4 + 3
        s.fill(mortar, (0, y, 16, 1))
        offset = 7 if row % 2 == 0 else 3
        for x in (offset, offset + 8):
            if x < 16:
                s.fill(mortar, (x, row * 4, 1, 3))
    s.fill((150, 150, 160), (0, 0, 16, 1))
    return s


def tile_tree():
    s = tile_grass()
    s.fill(BROWN, (7, 10, 2, 5))
    pygame.draw.circle(s, (40, 110, 50), (8, 6), 6)
    pygame.draw.circle(s, (60, 150, 60), (7, 5), 4)
    s.fill((95, 185, 85), (5, 3, 2, 1))
    return s


def tile_water():
    s = new_canvas()
    s.fill((50, 110, 210))
    for x, y, w in ((2, 3, 4), (9, 7, 4), (4, 11, 4), (11, 14, 3)):
        s.fill((125, 180, 240), (x, y, w, 1))
    return s


def make_tileset():
    sheet = new_canvas(64, 16)
    for i, tile in enumerate([tile_grass(), tile_wall(), tile_tree(), tile_water()]):
        sheet.blit(tile, (i * 16, 0))
    save(scale(sheet), "tileset.png")


# ---------------- cuori: pieno e vuoto ----------------
HEART = [".##.##.",
         "#######",
         "#######",
         ".#####.",
         "..###..",
         "...#..."]


def make_hearts():
    sheet = new_canvas(18, 8)
    for index, color in enumerate([(225, 45, 65), (75, 75, 85)]):
        s = new_canvas(9, 8)
        for y, row in enumerate(HEART):
            for x, char in enumerate(row):
                if char == "#":
                    s.set_at((x + 1, y + 1), color)
        if index == 0:
            s.set_at((2, 2), (255, 190, 190))
        sheet.blit(add_outline(s), (index * 9, 0))
    save(scale(sheet, 3), "hearts.png")


if __name__ == "__main__":
    make_player()
    make_enemy()
    make_sword()
    make_tileset()
    make_hearts()
