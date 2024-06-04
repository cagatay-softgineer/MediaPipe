import mediapipe as mp

# Initialize MediaPipe Hand module
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe drawing module
mp_drawing = mp.solutions.drawing_utils

def detect_process(process_frame,output_frame):
    """
    Detects and draws landmarks on the input frame.

    Args:
        process_frame (numpy.ndarray): Input frame to be processed.
        output_frame (numpy.ndarray): Frame on which landmarks will be drawn.

    Returns:
        numpy.ndarray: Output frame with landmarks drawn.
    """
    
     # Process the frame to detect processes
    results = face_mesh.process(process_frame)
    pose_results = pose.process(process_frame)
    hand_results = hands.process(process_frame)

    # Draw face landmarks on the frame
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw each face landmark
                mp_drawing.draw_landmarks(
                output_frame, face_landmarks, mp_face.FACEMESH_TESSELATION)

    # Draw pose landmarks on the frame
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            output_frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Draw hand landmarks on the frame
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                output_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
    return output_frame