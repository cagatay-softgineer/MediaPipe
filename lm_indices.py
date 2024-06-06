# Identify landmarks indices
# indecis as constatns
nose = 1
lips_upper = 13 #0
lips_bottom = 14 #17
lips_left = 291
lips_right = 61
face_upper = 10
face_bottom = 152
face_right = 234
face_left = 454
iris_right = 468
iris_left = 473
eye_right_upper = 159
eye_right_bottom = 145
eye_right_left = 133
eye_right_right = 33
eye_left_upper = 386
eye_left_bottom = 374
eye_left_left = 263
eye_left_right = 362

WRIST = 0
THUMB_CMC = 1
THUMB_MCP = 2
THUMB_IP = 3
THUMB_TIP = 4
INDEX_FINGER_MCP = 5
INDEX_FINGER_PIP = 6
INDEX_FINGER_DIP = 7
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_MCP = 9
MIDDLE_FINGER_PIP = 10
MIDDLE_FINGER_DIP = 11
MIDDLE_FINGER_TIP = 12
RING_FINGER_MCP = 13
RING_FINGER_PIP = 14
RING_FINGER_DIP = 15
RING_FINGER_TIP = 16
PINKY_MCP = 17
PINKY_PIP = 18
PINKY_DIP = 19
PINKY_TIP = 20

nose = 0
left_eye_inner = 1
left_eye = 2
left_eye_outer = 3
right_eye_inner = 4
right_eye = 5
right_eye_outer = 6
left_ear = 7
right_ear = 8
mouth_left = 9
mouth_right = 10
left_shoulder = 11
right_shoulder = 12
left_elbow = 13
right_elbow = 14
left_wrist = 15
right_wrist = 16
left_pinky = 17
right_pinky = 18
left_index = 19
right_index = 20
left_thumb = 21
right_thumb = 22
left_hip = 23
right_hip = 24
left_knee = 25
right_knee = 26
left_ankle = 27
right_ankle = 28
left_heel = 29
right_heel = 30
left_foot_index = 31
right_foot_index = 32


RIGHT_IRIS = [469, 470, 471, 472]
LEFT_IRIS = [474, 475, 476, 477]



hand_constants = [
    WRIST,
    THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP,
    INDEX_FINGER_MCP, INDEX_FINGER_PIP, INDEX_FINGER_DIP, INDEX_FINGER_TIP,
    MIDDLE_FINGER_MCP, MIDDLE_FINGER_PIP, MIDDLE_FINGER_DIP, MIDDLE_FINGER_TIP,
    RING_FINGER_MCP, RING_FINGER_PIP, RING_FINGER_DIP, RING_FINGER_TIP,
    PINKY_MCP, PINKY_PIP, PINKY_DIP, PINKY_TIP
]

hand_constants_names = [
    "WRIST",
    "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
    "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
    "PINKY_MCP," "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"
]

face_constants = [
    nose,
    lips_upper, lips_bottom, lips_left, lips_right,
    face_upper, face_bottom, face_right, face_left,
    iris_right, iris_left,
    eye_right_upper, eye_right_bottom, eye_right_left, eye_right_right,
    eye_left_upper, eye_left_bottom, eye_left_left, eye_left_right
]

body_constants = [
    nose,
    left_eye_inner, left_eye, left_eye_outer,
    right_eye_inner, right_eye, right_eye_outer,
    left_ear, right_ear,
    mouth_left, mouth_right,
    left_shoulder, right_shoulder,
    left_elbow, right_elbow,
    left_wrist, right_wrist,
    left_pinky, right_pinky,
    left_index, right_index,
    left_thumb, right_thumb,
    left_hip, right_hip,
    left_knee, right_knee,
    left_ankle, right_ankle,
    left_heel, right_heel,
    left_foot_index, right_foot_index
]

iris_constants = [
    *RIGHT_IRIS,
    *LEFT_IRIS
]

X = 0
Y = 1
Z = 2
H = 0
W = 1