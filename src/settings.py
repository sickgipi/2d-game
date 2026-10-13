"""Tutte le costanti del gioco in un posto solo.
Per bilanciare o regolare il gioco basta modificare questo file."""
from pathlib import Path

# Percorsi (calcolati dalla posizione di questo file, quindi funzionano
# anche se lanci il gioco da un'altra cartella)
BASE_DIR = Path(__file__).resolve().parent.parent
MAPS_DIR = BASE_DIR / "assets" / "maps"

# Finestra
TITLE = "Testing"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 576
FPS = 60

# Tile
TILE_SIZE = 32
TILE_COLORS = {
    ".": (34, 139, 34),    # prato
    "#": (110, 110, 110),  # muro
    "T": (0, 90, 0),       # albero
    "W": (40, 120, 220),   # acqua
}
SOLID_TILES = "#TW"        # i caratteri che bloccano il passaggio

# Giocatore
PLAYER_SIZE = 24
PLAYER_SPEED = 200
PLAYER_MAX_HEALTH = 5
PLAYER_SPAWN_TILE = (4, 4)       # (colonna, riga)
PLAYER_INVULNERABLE_TIME = 1.0   # secondi di protezione dopo un colpo
PLAYER_COLOR = (30, 60, 200)

# Spada
SWORD_SIZE = 28
SWORD_DURATION = 0.15            # per quanto tempo la spada e' attiva
SWORD_COOLDOWN = 0.35            # attesa prima del colpo successivo
SWORD_COLOR = (240, 240, 120)

# Nemici
ENEMY_SIZE = 24
ENEMY_SPEED = 70
ENEMY_HEALTH = 3
ENEMY_COUNT = 6
ENEMY_CHASE_RADIUS = 160         # distanza (in pixel) entro cui ti insegue
ENEMY_HIT_INVULNERABLE = 0.4
ENEMY_MIN_SPAWN_DISTANCE = 12    # distanza minima dalla partenza, in tile
ENEMY_COLOR = (200, 30, 30)
ENEMY_HIT_COLOR = (255, 150, 150)

# Contraccolpo
KNOCKBACK_FORCE = 300
KNOCKBACK_DECAY = 8              # piu' e' alto, piu' in fretta svanisce
