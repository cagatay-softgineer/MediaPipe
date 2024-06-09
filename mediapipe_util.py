import mediapipe as mp
from calculations import analyze_face_landmarks
import lm_indices as ids
import gloabal_vars as G_var
import json # for messages
import asyncio
import websocket_util
from test_hand import classify_hands_with_hand_lanmarks
from util import parse_landmarks_data_with_regex,extract_coordinates_with_max_possible,draw_circle_on_coord

# Initialize MediaPipe Hand module
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize MediaPipe drawing module

def detect_process(process_frame, output_frame, Send2WSS=False):
    """
    Detects and draws landmarks on the input frame.

    This function processes the input frame to detect landmarks, such as facial features or hand points, 
    and then draws these landmarks on the output frame. Optionally, the detected landmarks can be sent 
    to a WebSocket server.

    Args:
        process_frame (numpy.ndarray): 
            Input frame to be processed. This frame is analyzed to detect landmarks.
        output_frame (numpy.ndarray): 
            Frame on which landmarks will be drawn. This is typically a copy of the input frame or 
            a blank frame of the same dimensions.
        Send2WSS (bool, optional): 
            Flag indicating whether the detected landmarks should be sent to a WebSocket server. 
            Default is False.

    Returns:
        numpy.ndarray: 
            Output frame with landmarks drawn. This frame can be displayed or further processed.
    """
    
     # Process the frame to detect processes
    results = face_mesh.process(process_frame)
    pose_results = pose.process(process_frame)
    hand_results = hands.process(process_frame)
    
    img_h, img_w, img_c = process_frame.shape
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        
        if face_landmarks:
            
            G_var.DATA = analyze_face_landmarks(face_landmarks,img_w,img_h)
            
            #Draw each face landmark
            mp_drawing.draw_landmarks(
                output_frame, face_landmarks, mp_face.FACEMESH_TESSELATION,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),connection_drawing_spec=mp_drawing.DrawingSpec(color=(63, 127, 63),thickness=1, circle_radius=1))

    # Draw pose landmarks on the frame
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            output_frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 127, 255), thickness=1, circle_radius=2),connection_drawing_spec=mp_drawing.DrawingSpec(color=(127, 63, 127),thickness=1, circle_radius=1))
        
    Left_Hand_landmarks = [None]
    Right_Hand_landmarks = [None]
    
    # Draw hand landmarks on the frame
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
           
            hand_label = classify_hands_with_hand_lanmarks(hand_landmarks)
            
            if hand_label=="Left hand":
                    mp_drawing.draw_landmarks(
                        output_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),connection_drawing_spec=mp_drawing.DrawingSpec(color=(127, 63, 63),thickness=1, circle_radius=1))
                    Left_Hand_landmarks = parse_landmarks_data_with_regex([f"{hand_landmarks}"])
                    
            elif hand_label=="Right hand":
                    mp_drawing.draw_landmarks(
                        output_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1, circle_radius=1),connection_drawing_spec=mp_drawing.DrawingSpec(color=(63, 63, 127),thickness=1, circle_radius=1))
                    Right_Hand_landmarks = parse_landmarks_data_with_regex([f"{hand_landmarks}"])
    
    Left_Hands_landmark_coordinates = extract_coordinates_with_max_possible(Left_Hand_landmarks)
    Right_Hands_landmark_coordinates = extract_coordinates_with_max_possible(Right_Hand_landmarks)
    output_frame = draw_circle_on_coord(output_frame,Left_Hands_landmark_coordinates,COLOR_DOTS=(255, 0, 0))
    output_frame = draw_circle_on_coord(output_frame,Right_Hands_landmark_coordinates,COLOR_DOTS=(0, 0, 255))
    
    if Send2WSS:
        landmark_coordinates = {}
        len_hand_constants_names = len(ids.hand_constants_names)-1
        # Iterate over all possible landmarks
        for landmark_id in ids.hand_constants:
            # Check if the landmark is available for left hands
            landmark_coordinates[f"Left_Hand_{ids.hand_constants_names[min(landmark_id,len_hand_constants_names)]}_Pose"] = Left_Hands_landmark_coordinates[landmark_id] if landmark_id < len(Left_Hands_landmark_coordinates) else None

        for landmark_id in ids.hand_constants:
            # Check if the landmark is available for right hands
            landmark_coordinates[f"Right_Hand_{ids.hand_constants_names[min(landmark_id,len_hand_constants_names)]}_Pose"] = Right_Hands_landmark_coordinates[landmark_id] if landmark_id < len(Right_Hands_landmark_coordinates) else None

        # Add the landmark coordinates to the data dictionary
        G_var.DATA.update(landmark_coordinates)

        # Prepare the JSON message with all data
        msg = json.dumps(G_var.DATA) # Velmi to taha dole FPS

        # Send data to ws server
        try:
          asyncio.run(websocket_util.send(msg))
        except ConnectionRefusedError:
          print('WS Server is down')
                
    return output_frame