"""Funzioni di utilita' usate da piu' parti del gioco."""
import pygame


def move_with_collisions(rect, pos, movement, obstacles):
    """Sposta 'rect' di 'movement' (Vector2 in pixel) gestendo le collisioni
    con 'obstacles', un asse alla volta (cosi' si scivola lungo i muri).
    'pos' e' la posizione precisa (con i decimali) del rect."""
    pos.x += movement.x
    rect.x = round(pos.x)
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            if movement.x > 0:
                rect.right = obstacle.left
            elif movement.x < 0:
                rect.left = obstacle.right
            pos.x = rect.x

    pos.y += movement.y
    rect.y = round(pos.y)
    for obstacle in obstacles:
        if rect.colliderect(obstacle):
            if movement.y > 0:
                rect.bottom = obstacle.top
            elif movement.y < 0:
                rect.top = obstacle.bottom
            pos.y = rect.y


def direction_between(origin, target):
    """Vettore di lunghezza 1 che va da 'origin' a 'target'
    (vettore nullo se i due punti coincidono)."""
    vector = pygame.Vector2(target) - pygame.Vector2(origin)
    if vector.length() == 0:
        return pygame.Vector2(0, 0)
    return vector.normalize()
