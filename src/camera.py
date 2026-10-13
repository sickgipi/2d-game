from .settings import WINDOW_HEIGHT, WINDOW_WIDTH


class Camera:
    """Tiene traccia di quale parte del mondo si vede nella finestra.
    (x, y) e' il punto del mondo che finisce nell'angolo in alto a sinistra."""

    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.view_width = WINDOW_WIDTH
        self.view_height = WINDOW_HEIGHT
        self.x = 0
        self.y = 0

    def update(self, target_rect):
        """Centra la camera sul bersaglio, senza uscire dai bordi della mappa."""
        x = target_rect.centerx - self.view_width // 2
        y = target_rect.centery - self.view_height // 2
        self.x = max(0, min(x, self.map_width - self.view_width))
        self.y = max(0, min(y, self.map_height - self.view_height))

    def apply(self, rect):
        """Da coordinate del mondo a coordinate dello schermo."""
        return rect.move(-self.x, -self.y)
