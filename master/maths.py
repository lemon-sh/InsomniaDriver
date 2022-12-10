import mediapipe as mp

denormalize_coordinates = mp.solutions.drawing_utils._normalized_to_pixel_coordinates


def distance(point_1, point_2):
    dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
    return dist


def get_ear(landmarks, refer_idxs, frame_width, frame_height):
    try:
        coords_points = []
        for i in refer_idxs:
            lm = landmarks[i]
            coord = denormalize_coordinates(lm.x, lm.y, frame_width, frame_height)
            coords_points.append(coord)

        p2_p6 = distance(coords_points[1], coords_points[5])
        p3_p5 = distance(coords_points[2], coords_points[4])
        p1_p4 = distance(coords_points[0], coords_points[3])

        ear = (p2_p6 + p3_p5) / (2.0 * p1_p4)

    except:
        ear = 0.0
        coords_points = None

    return ear, coords_points


def calculate_avg_ear(landmarks, left_eye_idxs, right_eye_idxs, image_w, image_h):
    left_ear, left_lm_coordinates = get_ear(landmarks, left_eye_idxs, image_w, image_h)
    right_ear, right_lm_coordinates = get_ear(landmarks, right_eye_idxs, image_w, image_h)
    Avg_EAR = (left_ear + right_ear) / 2.0

    return Avg_EAR, (left_lm_coordinates, right_lm_coordinates)
