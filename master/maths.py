import mediapipe as mp

denormalize_coordinates = mp.solutions.drawing_utils._normalized_to_pixel_coordinates
_circle_cache = {}


def l2_norm(point_1, point_2):
    dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
    return dist


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


def ear(landmarks, refer_idxs, frame_width, frame_height):
    try:
        coords_points = []
        for i in refer_idxs:
            lm = landmarks[i]
            coord = denormalize_coordinates(
                lm.x, lm.y, frame_width, frame_height)
            coords_points.append(coord)

        p2_p6 = l2_norm(coords_points[1], coords_points[5])
        p3_p5 = l2_norm(coords_points[2], coords_points[4])
        p1_p4 = l2_norm(coords_points[0], coords_points[3])

        ear_value = (p2_p6 + p3_p5) / (2.0 * p1_p4)

    except:
        ear_value = 0.0
        coords_points = None

    return ear_value, coords_points


def avg_ear(landmarks, left_eye_idxs, right_eye_idxs, image_w, image_h):
    left_ear, left_lm_coordinates = ear(
        landmarks, left_eye_idxs, image_w, image_h)
    right_ear, right_lm_coordinates = ear(
        landmarks, right_eye_idxs, image_w, image_h)
    Avg_EAR = (left_ear + right_ear) / 2.0

    return Avg_EAR, (left_lm_coordinates, right_lm_coordinates)
