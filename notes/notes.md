# 2d game: roadmap del progetto

Adventure RPG 2D su PC, ispirato a *The Legend of Zelda: Minish Cap*.
Fatto con **Python + pygame-ce**, imparando facendo.

**Come usare questo file**: spunta le caselle man mano (`[ ]` diventa `[x]`),
e quando apri una nuova chat incollami questo file: così sappiamo subito a che punto siamo.

Legenda: `[x]` fatto · `[ ]` da fare · 📦 consegnato, da verificare sul tuo PC

---

## Regole di lavoro

- Nomi **in inglese** nel codice (file, classi, variabili), spiegazioni **in italiano**.
- Un passo alla volta: ogni tappa deve essere **giocabile** prima di passare alla successiva.
- Prima di ogni modifica importante: `git commit`.
- Grafica per ultima? No: i quadrati colorati bastano finché la meccanica non funziona.

---

## Fase 0: Ambiente

- [x] Scelta dello strumento: **Pygame** (per imparare anche Python)
- [x] Python 3 installato
- [x] Ambiente virtuale `venv` creato e attivato
- [x] `pygame-ce` installato (il Pygame classico non si compilava con Python 3.14)
- [x] `requirements.txt` creato (`pip freeze > requirements.txt`)
- [x] Repository Git inizializzato (`git init`)

## Fase 1: Fondamenta del gioco

- [x] Finestra e **game loop** (eventi → aggiornamento → disegno)
- [x] Movimento top-down con WASD e frecce, velocità normalizzata in diagonale
- [x] Mappa a **tile** (lista di stringhe) e collisioni con muri, alberi, acqua
- [x] **Camera** che segue il giocatore, mondo più grande della finestra

## Fase 2: Combattimento base

- [x] Spada (hitbox temporanea davanti al giocatore), tasto spazio
- [x] Nemici con IA semplice (vagano, inseguono da vicino)
- [x] Vita, danni, invulnerabilità temporanea, **knockback**
- [x] Stati di gioco: giocando, game over, vittoria, riavvio con R

## Fase 3: Struttura e grafica di base

- [x] Refactor in più file: `settings`, `utils`, `tilemap`, `camera`, `player`, `enemy`, `game`
- [x] Mappa caricata da file (`assets/maps/level1.txt`)
- [x] Sprite e animazioni (spritesheet, classe `Animation`, tileset, cuori)
- [x] Il gioco parte sul tuo PC con la nuova struttura e grafica
- [x] Ombre sotto i personaggi e acqua animata

## Fase 4: I tuoi sprite

- [ ] Scegliere il programma (consigliato: **Piskel**, poi Pixelorama o LibreSprite)
- [ ] Scegliere una palette su lospec.com (8-16 colori)
- [ ] Ritoccare i colori di `player.png`
- [ ] Disegnare un oggetto semplice (albero, moneta, cuore)
- [ ] Disegnare il tuo personaggio fermo, poi le 4 direzioni
- [ ] Ciclo di camminata a 4 frame
- [ ] (Opzionale) Lavorare a 16×16 nativi, con il codice che ingrandisce da solo

## Fase 5: Un gioco "completo"

- [x] **Menu principale** e **pausa** (altri stati di gioco)
- [x] **Oggetti da raccogliere**: cuori che curano, rupie
- [ ] Chiavi
- [x] HUD con contatore rupie
- [ ] **Suoni ed effetti** (colpo di spada, danno, raccolta) e musica

## Fase 6: Mondo vero

- [ ] Installare **Tiled** e `pytmx`, caricare mappe `.tmx`
- [ ] **Layer**: terreno, oggetti, collisioni, e chiome degli alberi disegnate sopra il giocatore
- [ ] **Più aree** collegate da porte e transizioni
- [ ] Ingressi a case e grotte

## Fase 7: Interazione

- [ ] **NPC con dialoghi** (stato "dialogo", testo a comparsa)
- [ ] Porte con chiavi, casse da aprire, interruttori
- [ ] Una piccola missione con inizio e fine
- [ ] Inventario

## Fase 8: Nemici e sfide

- [ ] Più tipi di nemici, con comportamenti diversi
- [x] Drop dai nemici (cuori, rupie)
- [ ] Inseguimento che aggira gli ostacoli (**pathfinding A\***)
- [ ] Un boss

## Fase 9: La meccanica speciale (Minish Cap)

- [ ] Rimpicciolimento del personaggio
- [ ] Due versioni della stessa area (mondo normale e mondo minuscolo)
- [ ] Passaggi e puzzle che richiedono la nuova dimensione

## Fase 10: Rifinitura

- [ ] Salvataggio e caricamento
- [ ] Bilanciamento della difficoltà
- [ ] Eseguibile con **PyInstaller** da condividere

---

## Concetti già incontrati

- [x] Game loop e `dt` (delta time)
- [x] Normalizzazione dei vettori
- [x] `Rect` e `colliderect`, collisioni un asse alla volta
- [x] Coordinate del mondo contro coordinate dello schermo, camera
- [x] Timer a conto alla rovescia (spada, invulnerabilità, cooldown)
- [x] Classi (`Player`, `Enemy`, `Game`) e metodi
- [x] Stati di gioco
- [x] Suddivisione in moduli e dipendenze a senso unico
- [x] Spritesheet, animazione a frame, allineamento ai piedi
- [x] Cache con `lru_cache`

---

## Struttura attuale del progetto

```
gioco-2d/
├── main.py                  # avvia il gioco
├── ROADMAP.md               # questo file
├── requirements.txt         # da creare
├── .gitignore
├── assets/
│   ├── maps/level1.txt
│   ├── images/              # player, enemy, sword, tileset, hearts, items
│   └── sounds/
├── tools/
│   └── make_placeholder_assets.py
└── src/
    ├── settings.py          # tutte le costanti
    ├── utils.py             # movimento con collisioni, direzioni
    ├── assets.py            # caricamento immagini e spritesheet
    ├── animation.py         # classe Animation
    ├── tilemap.py           # mappa
    ├── camera.py            # camera
    ├── player.py            # giocatore
    ├── enemy.py             # nemici
    ├── item.py              # oggetti da raccogliere (cuori, rupie)
    └── game.py              # game loop e coordinamento
```

---

## Comandi utili

Avviare il gioco (Ubuntu):

```
cd ~/gioco-2d
source venv/bin/activate
python main.py
```

Avviare il gioco (Windows, PowerShell):

```
cd C:\percorso\gioco-2d
venv\Scripts\Activate.ps1
python main.py
```

Salvare una versione con Git:

```
git add .
git commit -m "Descrizione di cosa hai fatto"
```

Tornare indietro se hai rotto qualcosa (annulla le modifiche non salvate):

```
git checkout .
```

Ricreare l'ambiente se sparisce `venv`:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Comandi di gioco: **Invio** per iniziare, **WASD / frecce** per muoverti, **spazio** per attaccare,
**P / Esc** per la pausa (in pausa **Q** per uscire), **R** per ricominciare.

---

## Prossimo passo

Scegliere se continuare con la **Fase 4** (i tuoi sprite) o finire la **Fase 5** (chiavi e suoni).
