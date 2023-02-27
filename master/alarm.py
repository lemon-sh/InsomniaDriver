import pygame.mixer


class Alarm:
    def __init__(self, alarm_sound=None):
        self._on = False

        pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.pause()
            

    def enable(self):
        if self._on:
            return

        pygame.mixer.music.set_pos(0)
        pygame.mixer.music.unpause()

        self._on = True

    def disable(self):
        if not self._on:
            return
        pygame.mixer.music.pause()
        self._on = False

    def get_enabled(self):
        return self._on
