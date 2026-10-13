import random

import pygame

from .settings import (ENEMY_CHASE_RADIUS, ENEMY_COLOR, ENEMY_HEALTH,
                       ENEMY_HIT_COLOR, ENEMY_HIT_INVULNERABLE, ENEMY_SIZE,
                       ENEMY_SPEED, KNOCKBACK_DECAY, KNOCKBACK_FORCE)
from .utils import direction_between, move_with_collisions


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, ENEMY_SIZE, ENEMY_SIZE)
        self.rect.center = (x, y)
        self.pos = pygame.Vector2(self.rect.topleft)
        self.health = ENEMY_HEALTH
        self.direction = pygame.Vector2(0, 0)
        self.direction_timer = 0       # tra quanto cambia direzione
        self.invulnerable = 0          # dopo un colpo non puo' essere colpito subito
        self.knockback = pygame.Vector2(0, 0)

    def take_hit(self, source_center):
        self.health -= 1
        self.invulnerable = ENEMY_HIT_INVULNERABLE
        self.knockback = direction_between(source_center, self.rect.center) * KNOCKBACK_FORCE

    def update(self, dt, target_rect, obstacles):
        to_target = pygame.Vector2(target_rect.center) - pygame.Vector2(self.rect.center)

        if 0 < to_target.length() < ENEMY_CHASE_RADIUS:
            # Il giocatore e' vicino: inseguilo
            self.direction = to_target.normalize()
        else:
            # Altrimenti vaga a caso, cambiando direzione ogni tanto
            self.direction_timer -= dt
            if self.direction_timer <= 0:
                self.direction = pygame.Vector2(random.choice(
                    [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]))
                self.direction_timer = random.uniform(0.8, 2.0)

        self.invulnerable = max(0, self.invulnerable - dt)
        movement = (self.direction * ENEMY_SPEED + self.knockback) * dt
        self.knockback *= max(0, 1 - KNOCKBACK_DECAY * dt)
        move_with_collisions(self.rect, self.pos, movement, obstacles)

    def draw(self, surface, camera):
        color = ENEMY_HIT_COLOR if self.invulnerable > 0 else ENEMY_COLOR
        pygame.draw.rect(surface, color, camera.apply(self.rect))
