import pygame

from .settings import (KNOCKBACK_DECAY, KNOCKBACK_FORCE, PLAYER_COLOR,
                       PLAYER_INVULNERABLE_TIME, PLAYER_MAX_HEALTH,
                       PLAYER_SIZE, PLAYER_SPEED, SWORD_COLOR,
                       SWORD_COOLDOWN, SWORD_DURATION, SWORD_SIZE)
from .utils import direction_between, move_with_collisions


class Player:
    def __init__(self, spawn_point):
        self.spawn_point = spawn_point
        self.rect = pygame.Rect(0, 0, PLAYER_SIZE, PLAYER_SIZE)
        self.pos = pygame.Vector2(0, 0)   # posizione precisa (con i decimali)
        self.reset()

    def reset(self):
        """Riporta il giocatore alla situazione iniziale."""
        self.rect.center = self.spawn_point
        self.pos.update(self.rect.topleft)
        self.health = PLAYER_MAX_HEALTH
        self.invulnerable = 0                    # secondi di protezione rimasti
        self.knockback = pygame.Vector2(0, 0)
        self.facing = pygame.Vector2(0, 1)       # all'inizio guarda in giu'
        self.attack_timer = 0                    # > 0 mentre la spada e' attiva
        self.cooldown = 0                        # attesa prima del prossimo colpo

    @property
    def is_attacking(self):
        return self.attack_timer > 0

    def start_attack(self):
        if not self.is_attacking and self.cooldown <= 0:
            self.attack_timer = SWORD_DURATION
            self.cooldown = SWORD_COOLDOWN

    def sword_rect(self):
        """Il rettangolo della spada: compare davanti al giocatore."""
        half = SWORD_SIZE // 2
        if self.facing.x > 0:
            return pygame.Rect(self.rect.right, self.rect.centery - half,
                               SWORD_SIZE, SWORD_SIZE)
        if self.facing.x < 0:
            return pygame.Rect(self.rect.left - SWORD_SIZE, self.rect.centery - half,
                               SWORD_SIZE, SWORD_SIZE)
        if self.facing.y > 0:
            return pygame.Rect(self.rect.centerx - half, self.rect.bottom,
                               SWORD_SIZE, SWORD_SIZE)
        return pygame.Rect(self.rect.centerx - half, self.rect.top - SWORD_SIZE,
                           SWORD_SIZE, SWORD_SIZE)

    def take_hit(self, source_center):
        """Perde un cuore e viene spinto via dalla fonte del colpo."""
        self.health -= 1
        self.invulnerable = PLAYER_INVULNERABLE_TIME
        self.knockback = direction_between(source_center, self.rect.center) * KNOCKBACK_FORCE

    def update(self, dt, obstacles):
        self.attack_timer = max(0, self.attack_timer - dt)
        self.cooldown = max(0, self.cooldown - dt)
        self.invulnerable = max(0, self.invulnerable - dt)

        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        # Lo sguardo cambia solo con movimenti "puliti" (non in diagonale)
        # e non mentre si sta attaccando
        if not self.is_attacking:
            if direction.x != 0 and direction.y == 0:
                self.facing = pygame.Vector2(direction.x, 0)
            elif direction.y != 0 and direction.x == 0:
                self.facing = pygame.Vector2(0, direction.y)

        if direction.length() > 0:
            direction = direction.normalize()

        movement = (direction * PLAYER_SPEED + self.knockback) * dt
        self.knockback *= max(0, 1 - KNOCKBACK_DECAY * dt)
        move_with_collisions(self.rect, self.pos, movement, obstacles)

    def draw(self, surface, camera):
        # Lampeggia mentre e' invulnerabile
        if self.invulnerable <= 0 or int(self.invulnerable * 10) % 2 == 0:
            pygame.draw.rect(surface, PLAYER_COLOR, camera.apply(self.rect))
        if self.is_attacking:
            pygame.draw.rect(surface, SWORD_COLOR, camera.apply(self.sword_rect()))
