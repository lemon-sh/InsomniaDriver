import pygame.mixer
import config
import RPi.GPIO as GPIO

class Alarm:
    def __init__(self):
        self._on = False

        if config.alarm_mode == config.ALARMTYPE_SOUND:
            pygame.mixer.init()
            pygame.mixer.music.load(alarm_sound)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.pause()
        else:
            GPIO.setup(config.alarm_led_pin, GPIO.OUT)

    def enable(self):
        if self._on:
            return

        if config.alarm_mode == config.ALARMTYPE_SOUND:
            pygame.mixer.music.set_pos(0)
            pygame.mixer.music.unpause()
        else:
            GPIO.output(config.alarm_led_pin, GPIO.HIGH)

        self._on = True

    def disable(self):
        if not self._on:
            return

        if config.alarm_mode == config.ALARMTYPE_SOUND:
            pygame.mixer.music.pause()
        else:
            GPIO.output(config.alarm_led_pin, GPIO.LOW)
        
        self._on = False

    def get_enabled(self):
        return self._on
