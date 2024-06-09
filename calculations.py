import numpy as np
import cv2
import lm_indices as ids
import gloabal_vars as G_var

# Euclidean distance
def eDist(pointA, pointB):
    """
    Calculate the Euclidean distance between two points.

    Args:
        pointA (tuple): Tuple containing (x, y) coordinates of the first point.
        pointB (tuple): Tuple containing (x, y) coordinates of the second point.

    Returns:
        float: The Euclidean distance between the two points.
    """
    return np.linalg.norm(np.array([pointA[ids.X], pointA[ids.Y]]) - np.array([pointB[ids.X], pointB[ids.Y]]))

# Nod and Turn of head
def get_nodturn(landmarks, img_w, img_h):
    """
    Calculate the nod and turn angles based on 3D face landmarks.

    Args:
        landmarks (list): List of 3D face landmarks.
        img_w (int): Width of the image.
        img_h (int): Height of the image.

    Returns:
        tuple: Tuple containing the nod and turn angles.
    """
    # Select relevant landmarks
    indices = [ids.eye_right_right, ids.eye_left_left, ids.nose, ids.lips_right, ids.lips_left, ids.face_bottom]
    face_2d = np.array([[int(landmarks[idx][ids.X] * img_w), int(landmarks[idx][ids.Y] * img_h)] for idx in indices], dtype=np.float64)
    face_3d = np.array([[int(landmarks[idx][ids.X] * img_w), int(landmarks[idx][ids.Y] * img_h), landmarks[idx][ids.Z]] for idx in indices], dtype=np.float64)


    # Camera matrix
    focal_length = img_w
    cam_matrix = np.array([
        [focal_length, 0, img_w / 2],
        [0, focal_length, img_h / 2],
        [0, 0, 1]
    ], dtype=np.float64)

    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    # Solve PnP problem
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
    
    if not success:
        return 0, 0

    rmat, _ = cv2.Rodrigues(rot_vec)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

    return angles[0], angles[1]  # angles[2] is the rotation/roll


# Angle between three points
def calculate_angle(pointA, pointB, pointC):
    """
    Calculate the angle between three points (A-B-C).

    Args:
        pointA (object): Object containing (x, y) attributes for point A.
        pointB (object): Object containing (x, y) attributes for point B (vertex).
        pointC (object): Object containing (x, y) attributes for point C.

    Returns:
        float: The angle in degrees between the three points.
    """
    a = np.array([pointA[ids.X], pointA[ids.Y]])
    b = np.array([pointB[ids.X], pointB[ids.Y]])
    c = np.array([pointC[ids.X], pointC[ids.Y]])
    
    ab = b - a
    cb = b - c
    
    cosine_angle = np.dot(ab, cb) / (np.linalg.norm(ab) * np.linalg.norm(cb))
    angle = np.arccos(cosine_angle)
    
    return np.degrees(angle)

# Ratio calculation
def calculate_ratio(distA, distB):
    """
    Calculate the ratio of two distances.

    Args:
        distA (float): First distance.
        distB (float): Second distance.

    Returns:
        float: The ratio of the first distance to the second distance.
    """
    return distA / distB

def eye_aspect_ratio(eye_landmarks):
    # Calculate Euclidean distances between the vertical eye landmarks
    v_dist_1 = eDist(eye_landmarks[1], eye_landmarks[5])
    v_dist_2 = eDist(eye_landmarks[2], eye_landmarks[4])
    
    # Calculate Euclidean distance between the horizontal eye landmarks
    h_dist = eDist(eye_landmarks[0], eye_landmarks[3])
    
    # Calculate the eye aspect ratio
    ear = (v_dist_1 + v_dist_2) / (2.0 * h_dist)
    
    return ear

def mouth_aspect_ratio(mouth_landmarks):
    # Calculate Euclidean distance between the horizontal mouth landmarks
    h_dist = eDist(mouth_landmarks[0], mouth_landmarks[6])
    
    # Calculate Euclidean distance between the vertical mouth landmarks
    v_dist_1 = eDist(mouth_landmarks[2], mouth_landmarks[10])
    v_dist_2 = eDist(mouth_landmarks[4], mouth_landmarks[8])
    
    # Calculate the mouth aspect ratio
    mar = h_dist / (0.5 * (v_dist_1 + v_dist_2))
    
    return mar

def convert_normalized_landmarks(landmarks, image_width, image_height):
    converted_landmarks = []
    for landmark in landmarks.landmark:
        x = int(landmark.x * image_width)
        y = int(landmark.y * image_height)
        z = landmark.z  # Assuming z-coordinate is already in a meaningful range
        converted_landmarks.append((x, y, z))
    return converted_landmarks

# Example function that uses multiple calculations
def analyze_face_landmarks(face_landmarks, img_w, img_h):
    """
    Analyze various metrics from face landmarks.

    Args:
        face_landmarks (list): List of face landmarks.
        img_w (int): Width of the image.
        img_h (int): Height of the image.

    Returns:
        dict: A dictionary containing various calculated metrics.
    """
    
    face_landmarks = convert_normalized_landmarks(face_landmarks, img_w, img_h)
    
    # Calculate distances
    G_var.EYES_DISTANCE = eDist(face_landmarks[ids.iris_right], face_landmarks[ids.iris_left])
    
    G_var.NOSE_2_CHIN_DIST = eDist(face_landmarks[ids.nose], face_landmarks[ids.face_bottom])
    
    # Calculate nod and turn angles
    G_var.NOD, G_var.TURN = get_nodturn(face_landmarks, img_w, img_h)
    
    # Calculate angles
    G_var.MOUTH_OPNG_ANGLE = calculate_angle(face_landmarks[ids.lips_left], face_landmarks[ids.lips_upper], face_landmarks[ids.lips_right])
    
    # Calculate ratios
    G_var.EYE_2_CHIN_RATIO = calculate_ratio(G_var.EYES_DISTANCE, G_var.NOSE_2_CHIN_DIST)
    
    L_eye_gap_L2R = eDist(face_landmarks[ids.eye_right_right], face_landmarks[ids.eye_right_left])
    L_eye_gap_U2B = eDist(face_landmarks[ids.eye_right_upper], face_landmarks[ids.eye_right_bottom])
    G_var.BLINKL = L_eye_gap_U2B / L_eye_gap_L2R

    R_eye_gap_L2R = eDist(face_landmarks[ids.eye_left_right], face_landmarks[ids.eye_left_left])
    R_eye_gap_U2B = eDist(face_landmarks[ids.eye_left_upper], face_landmarks[ids.eye_left_bottom])
    G_var.BLINKR = R_eye_gap_U2B / R_eye_gap_L2R

    G_var.EYE_L_H = eDist(face_landmarks[ids.iris_left], face_landmarks[ids.eye_left_left]) / R_eye_gap_L2R
    G_var.EYE_R_H = eDist(face_landmarks[ids.iris_right], face_landmarks[ids.eye_right_left]) / L_eye_gap_L2R

    G_var.EYE_L_V = eDist(face_landmarks[ids.iris_left], face_landmarks[ids.eye_left_bottom]) / R_eye_gap_U2B
    G_var.EYE_R_V = eDist(face_landmarks[ids.iris_right], face_landmarks[ids.eye_right_bottom]) / L_eye_gap_U2B
    
    metrics = {
    'gap': G_var.EYES_DISTANCE,
    'nod': G_var.NOD,
    'turn': G_var.TURN,
    'blinkR': G_var.BLINKR,
    'blinkL': G_var.BLINKL,
    'nose_2_chin_dist': G_var.NOSE_2_CHIN_DIST,
    'mouth_opening_angle': G_var.MOUTH_OPNG_ANGLE,
    'eye_2_chin_ratio': G_var.EYE_2_CHIN_RATIO,
    }
    
    return metrics