import pygame

pygame.init()

TILE = 32  # lato di ogni tile in pixel

# La mappa: ogni carattere e' un tile
#   .  prato (si cammina)
#   #  muro   T  albero   W  acqua  (bloccano il passaggio)
MAPPA = [
    "##################################################",
    "#.................T..............................#",
    "#..........................T.....................#",
    "#.........T...........................T..........#",
    "#......................T...T.................T...#",
    "#..........T.....................TT...W..........#",
    "#.................................WWWWWWWWW......#",
    "#............T..................WWWWWWWWWWWWW....#",
    "#............T..T...............WWWWWWWWWWWWW....#",
    "#..............................WWWWWWWWWWWWWWW...#",
    "#...................T..T........WWWWWWWWWWWWW.T..#",
    "#...............................WWWWWWWWWWWWW....#",
    "#.....T.T.........................WWWWWWWWW......#",
    "#.............T.....T....T............W..........#",
    "#........TTTTT......T...........................T#",
    "#.....T...T.T..T....................TT.......T...#",
    "#....T...T.TTT.T.TT..............................#",
    "#.....T...TTTTTTT.......................TT....T..#",
    "#....TT........T.T..............T...........T....#",
    "#...TT..T...T.T.TT..........................T....#",
    "#.T...T.TT...T.T.TT.###########T....T............#",
    "#.T....TT....T...T..#.........#............T.....#",
    "#......T......T.T.T.#.........#..................#",
    "#....T...T..T..T..T.#.........#......T...........#",
    "#.....TT.T.T...TT.TT#.........#.......T..........#",
    "#.....TT...T.....T..#.........#...............T..#",
    "#..........T..T...T.####..#####..................#",
    "#........T..TT.T.T...................T...........#",
    "#....T....T..T..T.T.......TT........TT...........#",
    "#.......TT..T....T.......T...............T.......#",
    "#.T.....T....T..T.T...........................T..#",
    "#..T.....T.T...T......T............T.........T...#",
    "#.....T.TTT..T...T......................T........#",
    "#.............................................T..#",
    "#..........................................T.....#",
    "##################################################",
]

COLORI = {
    ".": (34, 139, 34),   # prato
    "#": (110, 110, 110),  # muro
    "T": (0, 90, 0),       # albero
    "W": (40, 120, 220),   # acqua
}
SOLIDI = "#TW"  # i caratteri che bloccano il giocatore

COLONNE = len(MAPPA[0])
RIGHE = len(MAPPA)
MAPPA_LARGHEZZA = COLONNE * TILE  # dimensioni del mondo in pixel
MAPPA_ALTEZZA = RIGHE * TILE

# La finestra ha una dimensione fissa, indipendente dalla mappa
FINESTRA_L, FINESTRA_A = 800, 576
schermo = pygame.display.set_mode((FINESTRA_L, FINESTRA_A))
pygame.display.set_caption("Il mio Zelda")
clock = pygame.time.Clock()

# Un Rect per ogni tile solido, per le collisioni
ostacoli = []
for riga, testo in enumerate(MAPPA):
    for colonna, carattere in enumerate(testo):
        if carattere in SOLIDI:
            ostacoli.append(pygame.Rect(colonna * TILE, riga * TILE, TILE, TILE))

giocatore = pygame.Rect(0, 0, 24, 24)
giocatore.center = (4 * TILE + TILE // 2, 4 * TILE + TILE // 2)
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

    # --- MOVIMENTO CON COLLISIONI (un asse alla volta) ---
    pos.x += direzione.x * velocita * dt
    giocatore.x = round(pos.x)
    for ostacolo in ostacoli:
        if giocatore.colliderect(ostacolo):
            if direzione.x > 0:
                giocatore.right = ostacolo.left
            elif direzione.x < 0:
                giocatore.left = ostacolo.right
            pos.x = giocatore.x

    pos.y += direzione.y * velocita * dt
    giocatore.y = round(pos.y)
    for ostacolo in ostacoli:
        if giocatore.colliderect(ostacolo):
            if direzione.y > 0:
                giocatore.bottom = ostacolo.top
            elif direzione.y < 0:
                giocatore.top = ostacolo.bottom
            pos.y = giocatore.y

    # --- CAMERA ---
    # La camera e' il punto del mondo che corrisponde all'angolo in alto
    # a sinistra della finestra. La centriamo sul giocatore...
    cam_x = giocatore.centerx - FINESTRA_L // 2
    cam_y = giocatore.centery - FINESTRA_A // 2
    # ...ma non la lasciamo uscire dai bordi della mappa
    cam_x = max(0, min(cam_x, MAPPA_LARGHEZZA - FINESTRA_L))
    cam_y = max(0, min(cam_y, MAPPA_ALTEZZA - FINESTRA_A))

    # --- DISEGNO ---
    # Disegniamo solo i tile visibili nella finestra
    prima_col = cam_x // TILE
    ultima_col = min(COLONNE, (cam_x + FINESTRA_L) // TILE + 1)
    prima_riga = cam_y // TILE
    ultima_riga = min(RIGHE, (cam_y + FINESTRA_A) // TILE + 1)

    for riga in range(prima_riga, ultima_riga):
        for colonna in range(prima_col, ultima_col):
            carattere = MAPPA[riga][colonna]
            # posizione sullo schermo = posizione nel mondo - camera
            rettangolo = (colonna * TILE - cam_x, riga * TILE - cam_y, TILE, TILE)
            pygame.draw.rect(schermo, COLORI[carattere], rettangolo)

    pygame.draw.rect(schermo, (30, 60, 200), giocatore.move(-cam_x, -cam_y))
    pygame.display.flip()

pygame.quit()