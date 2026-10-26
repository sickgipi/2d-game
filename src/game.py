import random

import pygame

from .assets import load_frames
from .camera import Camera
from .enemy import Enemy
from .item import HEART, RUPEE, Item, item_image
from .player import Player
from .settings import (ENEMY_COUNT, ENEMY_MIN_SPAWN_DISTANCE, FPS,
                       HEART_DROP_CHANCE, HEART_SIZE, HEART_SPACING,
                       IMAGES_DIR, MAPS_DIR, PLAYER_MAX_HEALTH,
                       PLAYER_SPAWN_TILE, RUPEE_DROP_CHANCE, TILE_SIZE, TITLE,
                       WINDOW_HEIGHT, WINDOW_WIDTH)
from .tilemap import TileMap

# Gli stati possibili del gioco
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
GAME_OVER = "game_over"
VICTORY = "victory"


def tile_center(col, row):
    """Centro in pixel di un tile dato (colonna, riga)."""
    return (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2)


class Game:
    """Coordina tutto: possiede mappa, camera, giocatore, nemici e oggetti,
    e contiene il game loop."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.font_big = pygame.font.Font(None, 72)
        self.font_small = pygame.font.Font(None, 32)

        # Immagine del cuore: frame 0 = pieno, frame 1 = vuoto
        self.hearts = load_frames(IMAGES_DIR / "hearts.png", *HEART_SIZE)[0]
        self.rupee_icon = item_image(RUPEE)

        self.tilemap = TileMap(MAPS_DIR / "level1.txt")
        self.camera = Camera(self.tilemap.width, self.tilemap.height)
        self.player = Player(tile_center(*PLAYER_SPAWN_TILE))
        self.enemies = self.spawn_enemies()
        self.items = []
        self.state = MENU
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
        self.items = []
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
                self.handle_key(event.key)

    def handle_key(self, key):
        """Cosa fa ogni tasto dipende dallo stato del gioco."""
        if self.state == MENU:
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state = PLAYING
            elif key == pygame.K_ESCAPE:
                self.running = False
        elif self.state == PLAYING:
            if key == pygame.K_SPACE:
                self.player.start_attack()
            elif key in (pygame.K_p, pygame.K_ESCAPE):
                self.state = PAUSED
        elif self.state == PAUSED:
            if key in (pygame.K_p, pygame.K_ESCAPE):
                self.state = PLAYING
            elif key == pygame.K_q:
                self.running = False
        elif key == pygame.K_r:   # game over o vittoria
            self.restart()

    def update(self, dt):
        self.tilemap.update(dt)   # l'acqua si muove anche nel menu e in pausa
        if self.state == PLAYING:
            obstacles = self.tilemap.obstacles
            self.player.update(dt, obstacles)
            for enemy in self.enemies:
                enemy.update(dt, self.player.rect, obstacles)
            for item in self.items:
                item.update(dt)

            self.check_sword_hits()
            self.remove_dead_enemies()
            self.check_enemy_contact()
            self.check_item_pickup()

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

    def remove_dead_enemies(self):
        """Toglie i nemici sconfitti; ognuno puo' lasciare un oggetto."""
        for enemy in self.enemies:
            if enemy.health <= 0:
                self.drop_item(enemy.rect.center)
        self.enemies = [enemy for enemy in self.enemies if enemy.health > 0]

    def drop_item(self, center):
        roll = random.random()
        if roll < HEART_DROP_CHANCE:
            self.items.append(Item(HEART, center))
        elif roll < HEART_DROP_CHANCE + RUPEE_DROP_CHANCE:
            self.items.append(Item(RUPEE, center))

    def check_enemy_contact(self):
        if self.player.invulnerable > 0:
            return
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_hit(enemy.rect.center)
                break  # un solo colpo per volta

    def check_item_pickup(self):
        for item in self.items:
            if self.player.rect.colliderect(item.rect):
                if item.kind == HEART:
                    self.player.heal()
                else:
                    self.player.rupees += 1
                item.lifetime = 0   # raccolto: lo facciamo sparire
        self.items = [item for item in self.items if not item.expired]

    # --- Disegno ---------------------------------------------------
    def draw(self):
        self.tilemap.draw(self.screen, self.camera)
        for item in self.items:
            item.draw(self.screen, self.camera)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
        self.player.draw(self.screen, self.camera)

        if self.state == MENU:
            self.draw_message(TITLE, "Premi INVIO per iniziare",
                              "WASD/frecce: muoviti   Spazio: spada   P: pausa")
        else:
            self.draw_hud()
            if self.state == PAUSED:
                self.draw_message("PAUSA", "Premi P per continuare", "Q per uscire")
            elif self.state == GAME_OVER:
                self.draw_message("GAME OVER", "Sei morto! Premi R per ricominciare")
            elif self.state == VICTORY:
                self.draw_message("HAI VINTO!",
                                  f"Rupie raccolte: {self.player.rupees}",
                                  "Premi R per giocare ancora")
        pygame.display.flip()

    def draw_text(self, text, font, **position):
        """Scrive un testo bianco con un'ombra scura sotto, cosi' si legge
        su qualsiasi sfondo. 'position' e' ad esempio center=(x, y)."""
        shadow = font.render(text, True, (20, 20, 30))
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(**position)
        self.screen.blit(shadow, rect.move(2, 2))
        self.screen.blit(surface, rect)

    def draw_hud(self):
        # Interfaccia fissa sullo schermo: qui NON si usa la camera
        panel = pygame.Surface((PLAYER_MAX_HEALTH * HEART_SPACING + 14, 76), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 110), panel.get_rect(), border_radius=8)
        self.screen.blit(panel, (4, 4))
        for i in range(PLAYER_MAX_HEALTH):
            heart = self.hearts[0] if i < self.player.health else self.hearts[1]
            self.screen.blit(heart, (10 + i * HEART_SPACING, 8))
        self.screen.blit(self.rupee_icon, (6, 38))
        self.draw_text(str(self.player.rupees), self.font_small, midleft=(36, 55))
        self.draw_text(f"Nemici: {len(self.enemies)}", self.font_small, midleft=(68, 55))

    def draw_message(self, title, *lines):
        """Velo scuro con un titolo grande e qualche riga sotto."""
        veil = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        veil.fill((0, 0, 0, 150))
        self.screen.blit(veil, (0, 0))
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        self.draw_text(title, self.font_big, center=(center_x, center_y - 20))
        for i, line in enumerate(lines):
            self.draw_text(line, self.font_small, center=(center_x, center_y + 30 + i * 32))
