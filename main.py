print("InsomniaDriver | PŚK Platynowy Indeks\nLoading libraries...")

from alarm import Alarm
from detector import DrowsyDetector
import graphics
import config
import pygame
import mediapipe as mp
import cv2
import time
import sys
import RPi.GPIO as GPIO


mpver = mp.__version__ if hasattr(mp, '__version__') else '<unknown>'
cv2ver = cv2.__version__
print(f"MediaPipe {mpver}\nOpenCV {cv2ver}\n")

print("Intializing display...")
pygame.init()
pygame.display.init()
pygame.mouse.set_visible(False)

cur_modes = pygame.display.list_modes()
mode = None
for own_mode in config.supported_video_modes:
    if own_mode in cur_modes:
        mode = own_mode
        print(f"Setting mode: {mode}")

if not mode:
    mode = config.supported_video_modes[0]
    print(f"Couldn't find a supported video mode, using default {mode}")

screen = pygame.display.set_mode(mode, vsync=1)
screen_x, screen_y = mode

if config.font_type == "file":
    def get_font(size):
        return pygame.font.Font(config.font, size)
elif config.font_type == "sys":
    def get_font(size):
        return pygame.font.SysFont(config.font, size)
else:
    def get_font(size):
        return pygame.font.SysFont(pygame.font.get_default_font(), size)

font = get_font(config.font_size)
alert_font = get_font(config.font_size * 2)
title_font = get_font(config.font_size * 4)

title_text = "InsomniaDriver"
title_size_x, title_size_y = title_font.size(title_text)
title_x = screen_x / 2 - title_size_x / 2
title_y = screen_y / 2 - title_size_y / 2

sub_text = "Paweł Stolarski © 2023"
sub_size_x, sub_size_y = font.size(sub_text)
sub_x = title_x + title_size_x - sub_size_x
sub_y = title_y + title_size_y

init_text = "Wczytywanie..."
init_size_x, init_size_y = font.size(init_text)
init_x = screen_x / 2 - init_size_x / 2
init_y = sub_y + init_size_y + 40

screen.fill(config.shadow)
graphics.draw_text(screen, title_text, title_font,
                   config.white, config.black, (title_x, title_y))
graphics.draw_text(screen, sub_text, font, config.gray,
                   config.black, (sub_x, sub_y))
graphics.draw_text(screen, init_text, font, config.green,
                   config.black, (init_x, init_y))
pygame.display.flip()

if sys.platform == "win32":
    print("Windows detected, using DirectShow OpenCV backend")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif sys.platform == "linux":
    print("Linux detected, using V4L2 OpenCV backend")
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
else:
    print("Unknown OS detected, using default OpenCV backend")
    cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_x)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_y)
render_next = True

if config.input_mode == "rpi" or config.alarm_mode == config.ALARMTYPE_LED:
    GPIO.setmode(GPIO.BCM)

if config.input_mode == "keyboard":
    def process_input():
        global render_next
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    alarm.disable()
                elif event.key == pygame.K_q:
                    render_next = False
elif config.input_mode == "rpi":
    GPIO.setup(config.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def process_input():
        pygame.event.pump()
        if GPIO.input(21) == 0:
            alarm.disable()
else:
    raise ValueError(f"Invalid input mode '{config.input_mode}'.")

alarm = Alarm()

fpsf_width, fpsf_height = font.size("FPS: 999.9")
flash_pos = (20, 20)
stats_pos = (20, screen_y - fpsf_height - 20)
fpsf_pos = (screen_x - fpsf_width - 20, screen_y - fpsf_height - 20)

drowsy_detector = DrowsyDetector()
fps = 0
graphics.set_font_antialias(config.font_antialias)

while render_next:
    fpsc_start = time.perf_counter()

    ret, image = cap.read()
    if not ret:
        break
    drowsy_detector.feed(image, config.ear_threshold,
                         config.wait_time_threshold)
    pgimage = graphics.cvimage_to_pygame(image)
    screen.fill((0, 0, 0))
    screen.blit(pgimage, pgimage.get_rect())

    if drowsy_detector.detection:
        graphics.draw_eye_landmarks(
            screen, drowsy_detector.coordinates[0], drowsy_detector.coordinates[1], config.blue)
        ear = round(drowsy_detector.ear, 3)
        drowsy_time = round(drowsy_detector.drowsy_time, 3)
        color = config.lightred if drowsy_detector.eyes_closed else config.blue
        graphics.draw_text(screen, f"EAR: {ear}; Przysypianie: {drowsy_time}", font, color, config.shadow,
                           stats_pos)
        if drowsy_detector.alarm:
            alarm.enable()

        if alarm.get_enabled():
            graphics.draw_text(screen, "Alert!", alert_font,
                               config.red, config.shadow, flash_pos)
        else:
            graphics.draw_text(screen, "Gotowość.", font,
                               config.green, config.shadow, flash_pos)
    else:
        graphics.draw_text(screen, "Nie wykryto twarzy", font,
                           config.red, config.shadow, flash_pos)

    process_input()

    graphics.draw_text(
        screen, f"FPS: {fps}", font, config.white, config.shadow, fpsf_pos)
    pygame.display.flip()
    fpsc_stop = time.perf_counter()
    fps = round(1 / (fpsc_stop - fpsc_start), 1)

cap.release()
