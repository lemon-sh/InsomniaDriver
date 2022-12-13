print("InsomniaDriver 0.1.0 | PŚK Platynowy Indeks / Team SQL Injection\nLoading libraries...")

import sys
import time

import cv2
import mediapipe as mp
import pygame

import config
import detector
import graphics

print(f"MediaPipe {mp.__version__}\nOpenCV {cv2.__version__}\n")

if sys.platform == "win32":
    print("Windows detected, using DirectShow OpenCV backend")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif sys.platform == "linux":
    print("Linux detected, using V4L2 OpenCV backend")
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
else:
    print("Unknown OS detected, using default OpenCV backend")
    cap = cv2.VideoCapture(0)

drowsy_detector = detector.DrowsyDetector()
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
title_font = get_font(config.font_size * 4)

title_text = "InsomniaDriver"
title_size_x, title_size_y = title_font.size(title_text)
title_x = screen_x / 2 - title_size_x / 2
title_y = screen_y / 2 - title_size_y / 2
sub_text = "Paweł Stolarski & Jakub Piasecki"
sub_size_x, sub_size_y = font.size(sub_text)
sub_x = title_x+title_size_x-sub_size_x
sub_y = title_y+title_size_y

screen.fill(config.shadow)
graphics.draw_text(screen, title_text, title_font, config.white, config.black, (title_x, title_y))
graphics.draw_text(screen, sub_text, font, config.gray, config.black, (sub_x, sub_y))
pygame.display.flip()
time.sleep(10)

fpsf_width, fpsf_height = font.size("FPS: 999.9")
fpsf_pos = (mode[0] - fpsf_width - 20, mode[1] - fpsf_height - 20)
fps = 0

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_x)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_y)

while True:
    fpsc_start = time.perf_counter()
    ret, image = cap.read()
    if not ret:
        break
    drowsy_detector.feed(image, config.ear_threshold, config.wait_time_threshold)
    pgimage = graphics.cvimage_to_pygame(image)
    screen.fill((0, 0, 0))
    screen.blit(pgimage, pgimage.get_rect())
    if drowsy_detector.detection:
        graphics.draw_eye_landmarks(screen, drowsy_detector.coordinates[0], drowsy_detector.coordinates[1], config.blue)
    else:
        graphics.draw_text(screen, "Nie wykryto mordy", font, config.red, config.shadow, (20, 20))
    fps_text = f"FPS: {fps}"
    graphics.draw_text(screen, fps_text, font, config.white, config.shadow, fpsf_pos)
    pygame.display.flip()
    fpsc_stop = time.perf_counter()
    fps = round(1 / (fpsc_stop - fpsc_start), 1)

cap.release()
