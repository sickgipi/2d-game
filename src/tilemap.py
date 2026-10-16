import pygame

from .assets import load_frames
from .settings import (IMAGES_DIR, SOLID_TILES, TILE_IMAGE_INDEX, TILE_SIZE)


class TileMap:
    """Si occupa solo della mappa: la legge da file, sa dove sono gli
    ostacoli e sa disegnarsi. Non sa nulla di giocatore o nemici."""

    def __init__(self, path):
        with open(path, encoding="utf-8") as file:
            self.rows = [line.rstrip("\n") for line in file if line.strip()]

        self.cols = len(self.rows[0])
        self.num_rows = len(self.rows)
        self.width = self.cols * TILE_SIZE     # dimensioni in pixel
        self.height = self.num_rows * TILE_SIZE

        # Il tileset e' una riga di quadratini: associamo a ogni carattere
        # della mappa l'immagine corrispondente
        tileset = load_frames(IMAGES_DIR / "tileset.png", TILE_SIZE, TILE_SIZE)[0]
        self.tile_images = {char: tileset[index]
                            for char, index in TILE_IMAGE_INDEX.items()}

        # Un Rect per ogni tile solido, per le collisioni
        self.obstacles = []
        for row_index, row in enumerate(self.rows):
            for col_index, tile in enumerate(row):
                if tile in SOLID_TILES:
                    self.obstacles.append(pygame.Rect(
                        col_index * TILE_SIZE, row_index * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE))

    def free_tiles(self):
        """Lista di (colonna, riga) dei tile di prato."""
        return [(col_index, row_index)
                for row_index, row in enumerate(self.rows)
                for col_index, tile in enumerate(row)
                if tile == "."]

    def draw(self, surface, camera):
        """Disegna solo i tile visibili nella finestra."""
        first_col = camera.x // TILE_SIZE
        last_col = min(self.cols, (camera.x + camera.view_width) // TILE_SIZE + 1)
        first_row = camera.y // TILE_SIZE
        last_row = min(self.num_rows, (camera.y + camera.view_height) // TILE_SIZE + 1)

        for row_index in range(first_row, last_row):
            for col_index in range(first_col, last_col):
                image = self.tile_images[self.rows[row_index][col_index]]
                surface.blit(image, (col_index * TILE_SIZE - camera.x,
                                     row_index * TILE_SIZE - camera.y))
