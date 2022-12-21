import pygame.mixer


class Alarm:
    # sound notification
    OUTPUT_SOUND = 0
    # http request to slave
    OUTPUT_EXT = 1

    def __init__(self, output_type, alarm_sound=None):
        if output_type not in range(2):
            raise ValueError("Invalid output type")
        if alarm_sound is None and output_type == self.OUTPUT_SOUND:
            raise ValueError(
                "You must supply an alarm sound when using the OUTPUT_SOUND type")

        self._on = False
        self._output_type = output_type

        if self._output_type == self.OUTPUT_SOUND:
            pygame.mixer.music.load(alarm_sound)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.pause()
        else:
            # TODO: raspberry pi code
            pass

    def enable(self):
        if self._on:
            return

        if self._output_type == self.OUTPUT_SOUND:
            pygame.mixer.music.set_pos(0)
            pygame.mixer.music.unpause()
        else:
            # TODO: raspberry pi code
            pass

        self._on = True

    def disable(self):
        if not self._on:
            return

        if self._output_type == self.OUTPUT_SOUND:
            pygame.mixer.music.pause()
        else:
            # TODO: raspberry pi code
            pass

        self._on = False

    def get_enabled(self):
        return self._on
