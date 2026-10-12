import pygame

pygame.init()

TILE = 32  # lato di ogni tile in pixel

# La mappa: ogni carattere e' un tile
#   .  prato (si cammina)
#   #  muro   T  albero   W  acqua  (bloccano il passaggio)
MAPPA = [
    "#########################",
    "#.......................#",
    "#...TT..............WW..#",
    "#...TT..............WW..#",
    "#.......................#",
    "#.........#####.........#",
    "#.........#...#.........#",
    "#.........#...#.........#",
    "#.......................#",
    "#..WWW..................#",
    "#..WWW.......TT.........#",
    "#............TT.........#",
    "#.......................#",
    "#.....#######...........#",
    "#.......####............#",
    "#.......................#",
    "#.......................#",
    "#########################",
]

COLORI = {
    ".": (34, 139, 34),   # prato
    "#": (110, 110, 110),  # muro
    "T": (0, 90, 0),       # albero
    "W": (40, 120, 220),   # acqua
}
SOLIDI = "#TW"  # i caratteri che bloccano il giocatore

RIGHE = len(MAPPA)
COLONNE = len(MAPPA[0])
schermo = pygame.display.set_mode((COLONNE * TILE, RIGHE * TILE))
pygame.display.set_caption("testing")
clock = pygame.time.Clock()

# Costruiamo una lista di Rect, uno per ogni tile solido, per le collisioni
ostacoli = []
for riga, testo in enumerate(MAPPA):
    for colonna, carattere in enumerate(testo):
        if carattere in SOLIDI:
            ostacoli.append(pygame.Rect(colonna * TILE, riga * TILE, TILE, TILE))

# Il giocatore e' un po' piu' piccolo di un tile, cosi' passa nei varchi
giocatore = pygame.Rect(0, 0, 24, 24)
giocatore.center = (3 * TILE, 8 * TILE)
# I Rect salvano solo numeri interi: teniamo la posizione precisa
# (con i decimali) in un Vector2 e la copiamo nel Rect dopo ogni movimento
pos = pygame.Vector2(giocatore.topleft)
velocita = 200

running = True
while running:
    dt = clock.tick(60) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    tasti = pygame.key.get_pressed()
    direzione = pygame.Vector2(0, 0)
    if tasti[pygame.K_LEFT] or tasti[pygame.K_a]:
        direzione.x -= 1
    if tasti[pygame.K_RIGHT] or tasti[pygame.K_d]:
        direzione.x += 1
    if tasti[pygame.K_UP] or tasti[pygame.K_w]:
        direzione.y -= 1
    if tasti[pygame.K_DOWN] or tasti[pygame.K_s]:
        direzione.y += 1
    if direzione.length() > 0:
        direzione = direzione.normalize()

    # --- MOVIMENTO CON COLLISIONI ---
    # Muoviamo e controlliamo un asse alla volta: cosi' se sbatti contro
    # un muro in diagonale, scivoli lungo il muro invece di bloccarti.

    # Asse X
    pos.x += direzione.x * velocita * dt
    giocatore.x = round(pos.x)
    for ostacolo in ostacoli:
        if giocatore.colliderect(ostacolo):
            if direzione.x > 0:
                giocatore.right = ostacolo.left
            elif direzione.x < 0:
                giocatore.left = ostacolo.right
            pos.x = giocatore.x

    # Asse Y
    pos.y += direzione.y * velocita * dt
    giocatore.y = round(pos.y)
    for ostacolo in ostacoli:
        if giocatore.colliderect(ostacolo):
            if direzione.y > 0:
                giocatore.bottom = ostacolo.top
            elif direzione.y < 0:
                giocatore.top = ostacolo.bottom
            pos.y = giocatore.y

    # --- DISEGNO ---
    for riga, testo in enumerate(MAPPA):
        for colonna, carattere in enumerate(testo):
            rettangolo = (colonna * TILE, riga * TILE, TILE, TILE)
            pygame.draw.rect(schermo, COLORI[carattere], rettangolo)

    pygame.draw.rect(schermo, (30, 60, 200), giocatore)
    pygame.display.flip()

pygame.quit()