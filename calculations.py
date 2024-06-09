import numpy as np
import cv2
import lm_indices as ids

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
    return np.linalg.norm(np.array([pointA.x, pointA.y]) - np.array([pointB.x, pointB.y]))

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
    face_2d = np.array([[int(landmarks[idx].x * img_w), int(landmarks[idx].y * img_h)] for idx in indices], dtype=np.float64)
    face_3d = np.array([[int(landmarks[idx].x * img_w), int(landmarks[idx].y * img_h), landmarks[idx].z] for idx in indices], dtype=np.float64)

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
