"""Tutte le costanti del gioco in un posto solo.
Per bilanciare o regolare il gioco basta modificare questo file."""
from pathlib import Path

# Percorsi (calcolati dalla posizione di questo file, quindi funzionano
# anche se lanci il gioco da un'altra cartella)
BASE_DIR = Path(__file__).resolve().parent.parent
MAPS_DIR = BASE_DIR / "assets" / "maps"
IMAGES_DIR = BASE_DIR / "assets" / "images"

# Finestra
TITLE = "Il mio Zelda"
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 576
FPS = 60

# Tile
TILE_SIZE = 32
SOLID_TILES = "#TW"        # i caratteri che bloccano il passaggio
# Quale immagine del tileset usare per ogni carattere della mappa
# (0 = primo quadratino da sinistra in tileset.png, 1 = secondo, ...)
TILE_IMAGE_INDEX = {".": 0, "#": 1, "T": 2, "W": 3}
WATER_FRAMES = (3, 4)      # l'acqua alterna questi due tile, per muoversi
WATER_ANIMATION_FPS = 2

# Grafica
SPRITE_SIZE = 32           # lato di un frame negli spritesheet
HEART_SIZE = (27, 24)
HEART_SPACING = 30

# Giocatore
PLAYER_SIZE = 24
PLAYER_SPEED = 200
PLAYER_MAX_HEALTH = 5
PLAYER_SPAWN_TILE = (4, 4)       # (colonna, riga)
PLAYER_INVULNERABLE_TIME = 1.0   # secondi di protezione dopo un colpo
PLAYER_WALK_FPS = 8              # frame al secondo dell'animazione di camminata

# Spada
SWORD_SIZE = 28
SWORD_DURATION = 0.15            # per quanto tempo la spada e' attiva
SWORD_COOLDOWN = 0.35            # attesa prima del colpo successivo

# Nemici
ENEMY_SIZE = 24
ENEMY_SPEED = 70
ENEMY_HEALTH = 3
ENEMY_COUNT = 6
ENEMY_CHASE_RADIUS = 160         # distanza (in pixel) entro cui ti insegue
ENEMY_HIT_INVULNERABLE = 0.4
ENEMY_MIN_SPAWN_DISTANCE = 12    # distanza minima dalla partenza, in tile
ENEMY_FPS = 6
ENEMY_HIT_TINT = (120, 120, 120)   # quanto si schiarisce quando e' colpito

# Contraccolpo
KNOCKBACK_FORCE = 300
KNOCKBACK_DECAY = 8              # piu' e' alto, piu' in fretta svanisce

# Oggetti lasciati dai nemici
ITEM_SIZE = 14
ITEM_LIFETIME = 10.0             # secondi prima che sparisca
ITEM_BLINK_TIME = 3.0            # negli ultimi secondi lampeggia
HEART_DROP_CHANCE = 0.35         # probabilita' (0-1) che un nemico lasci un cuore
RUPEE_DROP_CHANCE = 0.6          # ...e una rupia
