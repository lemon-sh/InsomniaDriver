import sys
import time
from math import ceil

import cv2
import pygame

import config
import detector
import graphics

if sys.platform == "win32":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif sys.platform == "linux":
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
else:
    cap = cv2.VideoCapture(0)

drowsy_detector = detector.DrowsyDetector()
pygame.init()
pygame.display.init()
pygame.mouse.set_visible(False)
time.sleep(2)

if config.width > 0:
    size = (config.width, config.height)
else:
    display_info = pygame.display.Info()
    width = (config.height * display_info.current_w) / display_info.current_h
    size = (ceil(width), config.height)

print(f"setting size: {size}")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])
screen = pygame.display.set_mode(size, vsync=1)
fps = 0

if config.font_type == "file":
    font = pygame.font.Font(config.font, config.font_size)
elif config.font_type == "sys":
    font = pygame.font.SysFont(config.font, config.font_size)
else:
    font = pygame.font.SysFont(pygame.font.get_default_font(), config.font_size)

fpsf_width, fpsf_height = font.size("FPS: 999.9")
fpsf_pos = (size[0] - fpsf_width - 20, size[1] - fpsf_height - 20)

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
        graphics.draw_text(screen, "Nie wykryto mordy", font, config.red, config.shadow, (20, 20),
                           antialias=config.font_antialias)
    fps_text = f"FPS: {fps}"
    graphics.draw_text(screen, fps_text, font, config.white, config.shadow, fpsf_pos, antialias=config.font_antialias)
    pygame.display.flip()
    fpsc_stop = time.perf_counter()
    fps = round(1 / (fpsc_stop - fpsc_start), 1)

cap.release()
