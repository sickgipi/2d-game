import random
from functools import lru_cache

import pygame

from .animation import Animation
from .assets import load_frames, shadow, tinted
from .settings import (ENEMY_CHASE_RADIUS, ENEMY_FPS, ENEMY_HEALTH,
                       ENEMY_HIT_INVULNERABLE, ENEMY_HIT_TINT, ENEMY_SIZE,
                       ENEMY_SPEED, IMAGES_DIR, KNOCKBACK_DECAY,
                       KNOCKBACK_FORCE, SPRITE_SIZE)
from .utils import direction_between, move_with_collisions


@lru_cache(maxsize=None)
def load_enemy_frames():
    """Frame normali e frame 'schiariti' (quando viene colpito).
    Calcolati una volta sola e condivisi da tutti i nemici."""
    frames = load_frames(IMAGES_DIR / "enemy.png", SPRITE_SIZE, SPRITE_SIZE)[0]
    hit_frames = [tinted(frame, ENEMY_HIT_TINT) for frame in frames]
    return frames, hit_frames


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

        self.frames, self.hit_frames = load_enemy_frames()
        self.animation = Animation(self.frames, ENEMY_FPS)
        # Ogni nemico parte da un frame diverso, cosi' non saltellano in sincrono
        self.animation.index = random.randrange(len(self.frames))

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
        self.animation.update(dt)

    def draw(self, surface, camera):
        ground = shadow(ENEMY_SIZE, ENEMY_SIZE // 3)
        surface.blit(ground, camera.apply(ground.get_rect(center=self.rect.midbottom)))
        frames = self.hit_frames if self.invulnerable > 0 else self.frames
        image = frames[self.animation.index]
        sprite_rect = image.get_rect(midbottom=self.rect.midbottom)
        surface.blit(image, camera.apply(sprite_rect))
