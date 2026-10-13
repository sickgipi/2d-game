import random

import pygame

from .camera import Camera
from .enemy import Enemy
from .player import Player
from .settings import (ENEMY_COUNT, ENEMY_MIN_SPAWN_DISTANCE, FPS, MAPS_DIR,
                       PLAYER_MAX_HEALTH, PLAYER_SPAWN_TILE, TILE_SIZE, TITLE,
                       WINDOW_HEIGHT, WINDOW_WIDTH)
from .tilemap import TileMap

# Gli stati possibili del gioco
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"


def tile_center(col, row):
    """Centro in pixel di un tile dato (colonna, riga)."""
    return (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2)


class Game:
    """Coordina tutto: possiede mappa, camera, giocatore e nemici,
    e contiene il game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 32)

        self.tilemap = TileMap(MAPS_DIR / "level1.txt")
        self.camera = Camera(self.tilemap.width, self.tilemap.height)
        self.player = Player(tile_center(*PLAYER_SPAWN_TILE))
        self.enemies = self.spawn_enemies()
        self.state = PLAYING
        self.running = True

    # --- Creazione e riavvio ---------------------------------------
    def spawn_enemies(self):
        """Mette i nemici su tile di prato lontani dalla partenza."""
        spawn_col, spawn_row = PLAYER_SPAWN_TILE
        candidates = [(col, row) for col, row in self.tilemap.free_tiles()
                      if abs(col - spawn_col) + abs(row - spawn_row) > ENEMY_MIN_SPAWN_DISTANCE]
        return [Enemy(*tile_center(col, row))
                for col, row in random.sample(candidates, ENEMY_COUNT)]

    def restart(self):
        self.player.reset()
        self.enemies = self.spawn_enemies()
        self.state = PLAYING

    # --- Il game loop: eventi -> aggiornamento -> disegno ----------
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == PLAYING:
                    self.player.start_attack()
                elif event.key == pygame.K_r and self.state != PLAYING:
                    self.restart()

    def update(self, dt):
        if self.state == PLAYING:
            obstacles = self.tilemap.obstacles
            self.player.update(dt, obstacles)
            for enemy in self.enemies:
                enemy.update(dt, self.player.rect, obstacles)

            self.check_sword_hits()
            self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]
            self.check_enemy_contact()

            if self.player.health <= 0:
                self.state = GAME_OVER
            elif not self.enemies:
                self.state = VICTORY

        self.camera.update(self.player.rect)

    def check_sword_hits(self):
        if not self.player.is_attacking:
            return
        sword = self.player.sword_rect()
        for enemy in self.enemies:
            if sword.colliderect(enemy.rect) and enemy.invulnerable <= 0:
                enemy.take_hit(self.player.rect.center)

    def check_enemy_contact(self):
        if self.player.invulnerable > 0:
            return
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_hit(enemy.rect.center)
                break  # un solo colpo per volta

    # --- Disegno ---------------------------------------------------
    def draw(self):
        self.tilemap.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)
        self.draw_hud()
        if self.state != PLAYING:
            self.draw_end_screen()
        pygame.display.flip()

    def draw_hud(self):
        # Interfaccia fissa sullo schermo: qui NON si usa la camera
        for i in range(PLAYER_MAX_HEALTH):
            color = (220, 40, 60) if i < self.player.health else (70, 70, 70)
            pygame.draw.rect(self.screen, color, (10 + i * 28, 10, 22, 22))
        text = self.font_small.render(f"Nemici: {len(self.enemies)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 40))

    def draw_end_screen(self):
        veil = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 150))
        self.screen.blit(veil, (0, 0))
        title = "GAME OVER" if self.state == GAME_OVER else "HAI VINTO!"
        line1 = self.font_big.render(title, True, (255, 255, 255))
        line2 = self.font_small.render("Premi R per ricominciare", True, (255, 255, 255))
        self.screen.blit(line1, line1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)))
        self.screen.blit(line2, line2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)))
