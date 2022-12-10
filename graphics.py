import pygame

_circle_cache = {}


def bresenham_circle(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def draw_text(surface, text, font, fcolor, ocolor, pos, opx=2, antialias=True):
    pos_x, pos_y = pos
    textsurface = font.render(text, antialias, fcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height() + 2 * opx

    osurf = pygame.Surface((w, h)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    osurf.blit(font.render(text, antialias, ocolor).convert_alpha(), (0, 0))

    for dx, dy in bresenham_circle(opx):
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
