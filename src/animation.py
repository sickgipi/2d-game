class Animation:
    """Scorre una lista di frame a una certa velocita' (frame al secondo)."""

    def __init__(self, frames, fps):
        self.frames = frames
        self.frame_time = 1 / fps
        self.timer = 0
        self.index = 0

    @property
    def image(self):
        return self.frames[self.index]

    def update(self, dt):
        self.timer += dt
        while self.timer >= self.frame_time:
            self.timer -= self.frame_time
            self.index = (self.index + 1) % len(self.frames)

    def reset(self):
        """Torna al primo frame (la posa 'ferma')."""
        self.index = 0
        self.timer = 0
