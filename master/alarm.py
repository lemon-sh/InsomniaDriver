import pygame.mixer


class Alarm:
    TYPE_DEV = 0
    TYPE_PHYSICAL = 1

    def __init__(self, alarm_type, alarm_sound=None):
        if alarm_type not in range(2):
            raise ValueError(f"Invalid alarm type '{alarm_type}'")
        if alarm_sound is None and alarm_type == self.TYPE_DEV:
            raise ValueError("You must supply an alarm sound when using the TYPE_DEV alarm type")
        
        self._on = False
        self._alarm_type = alarm_type
        
        if self._alarm_type == self.TYPE_PHYSICAL:
            # TODO: raspberry pi code
            pass
        else:
            pygame.mixer.music.load(alarm_sound)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.pause()

    def enable(self):
        if self._on:
            return
        if self._alarm_type == self.TYPE_PHYSICAL:
            # TODO: raspberry pi code
            pass
        else:
            pygame.mixer.music.set_pos(0)
            pygame.mixer.music.unpause()
        self._on = True

    def disable(self):
        if not self._on:
            return
        if self._alarm_type == self.TYPE_PHYSICAL:
            # TODO: raspberry pi code
            pass
        else:
            pygame.mixer.music.pause()
        self._on = False

    def get_enabled(self):
        return self._on

