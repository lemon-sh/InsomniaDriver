import pygame
import maths

_antialias = True


def set_font_antialias(antialias):
    global _antialias
    _antialias = antialias


def draw_text(surface, text, font, fcolor, ocolor, pos, opx=2):
    pos_x, pos_y = pos
    textsurface = font.render(text, _antialias, fcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height() + 2 * opx

    osurf = pygame.Surface((w, h)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    osurf.blit(font.render(text, _antialias, ocolor).convert_alpha(), (0, 0))

    for dx, dy in maths.bresenham_circle(opx):
        surface.blit(osurf, (pos_x + dx + opx, pos_y + dy + opx))

    surface.blit(textsurface, (pos_x + opx, pos_y + opx))


def draw_eye_landmarks(surface, left_lm_coordinates, right_lm_coordinates, color):
    for lm_coordinates in [left_lm_coordinates, right_lm_coordinates]:
        if lm_coordinates:
            for coord in lm_coordinates:
                pygame.draw.circle(surface, color, coord, 2)


def cvimage_to_pygame(image):
    height, width, channels = image.shape
    return pygame.image.frombuffer(image.tostring(), (width, height), "BGR")
