import mediapipe as mp
from calculations import eDist, get_nodturn
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
            # Calculate how big is gap between lips
            #gap = abs(face_landmarks.landmark[ids.lips_upper].y - face_landmarks.landmark[ids.lips_bottom].y)
            G_var.GAP = eDist(face_landmarks.landmark[ids.lips_upper], face_landmarks.landmark[ids.lips_bottom])

            # Calculate head Nod and Turn
            G_var.NOD, G_var.TURN = get_nodturn(face_landmarks.landmark, img_w, img_h)

            # Calculate head rotation
            G_var.ROT = face_landmarks.landmark[ids.face_upper].x - face_landmarks.landmark[ids.face_bottom].x

            # Calculate Blinking
            G_var.ED_R_H = eDist(face_landmarks.landmark[ids.eye_right_right], face_landmarks.landmark[ids.eye_right_left])
            G_var.ED_R_V = eDist(face_landmarks.landmark[ids.eye_right_upper], face_landmarks.landmark[ids.eye_right_bottom])
            G_var.BLINKR = G_var.ED_R_V/G_var.ED_R_H
            
            G_var.ED_L_H = eDist(face_landmarks.landmark[ids.eye_left_right], face_landmarks.landmark[ids.eye_left_left])
            G_var.ED_L_V = eDist(face_landmarks.landmark[ids.eye_left_upper], face_landmarks.landmark[ids.eye_left_bottom])
            G_var.BLINKL = G_var.ED_L_V/G_var.ED_L_H
            
            G_var.EYE_L_H = eDist(face_landmarks.landmark[ids.iris_left], face_landmarks.landmark[ids.eye_left_left]) / eDist(face_landmarks.landmark[ids.eye_left_right], face_landmarks.landmark[ids.eye_left_left])

            G_var.EYE_R_H = eDist(face_landmarks.landmark[ids.iris_right], face_landmarks.landmark[ids.eye_right_left]) / eDist(face_landmarks.landmark[ids.eye_right_right], face_landmarks.landmark[ids.eye_right_left])

            G_var.EYE_L_V = eDist(face_landmarks.landmark[ids.iris_left], face_landmarks.landmark[ids.eye_left_bottom]) / eDist(face_landmarks.landmark[ids.eye_left_upper], face_landmarks.landmark[ids.eye_left_bottom])

            G_var.EYE_R_V = eDist(face_landmarks.landmark[ids.iris_right], face_landmarks.landmark[ids.eye_right_bottom]) / eDist(face_landmarks.landmark[ids.eye_right_upper], face_landmarks.landmark[ids.eye_right_bottom])

            #Draw each face landmark
            mp_drawing.draw_landmarks(
                output_frame, face_landmarks, mp_face.FACEMESH_TESSELATION,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0)))


    # Draw pose landmarks on the frame
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            output_frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0)))
        
    Left_Hand_landmarks = [None]
    Right_Hand_landmarks = [None]
    
    # Draw hand landmarks on the frame
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
           
            hand_label = classify_hands_with_hand_lanmarks(hand_landmarks)
            
            if hand_label=="Left hand":
                    mp_drawing.draw_landmarks(
                        output_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
                    Left_Hand_landmarks = parse_landmarks_data_with_regex([f"{hand_landmarks}"])
                    
            elif hand_label=="Right hand":
                    mp_drawing.draw_landmarks(
                        output_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))
                    Right_Hand_landmarks = parse_landmarks_data_with_regex([f"{hand_landmarks}"])
                    

    
    Left_Hands_landmark_coordinates = extract_coordinates_with_max_possible(Left_Hand_landmarks)
    Right_Hands_landmark_coordinates = extract_coordinates_with_max_possible(Right_Hand_landmarks)
    output_frame = draw_circle_on_coord(output_frame,Left_Hands_landmark_coordinates,COLOR_DOTS=(255, 0, 0))
    output_frame = draw_circle_on_coord(output_frame,Right_Hands_landmark_coordinates,COLOR_DOTS=(0, 0, 255))
    
    data = {
    'gap': G_var.GAP, 
    'rot': G_var.ROT, 
    'nod': G_var.NOD, 
    'turn': G_var.TURN, 
    'blinkR': G_var.BLINKR, 
    'blinkL': G_var.BLINKR,
    'eye_L_H': G_var.EYE_L_H,
    'eye_R_H': G_var.EYE_R_H,
    'eye_L_V': G_var.EYE_L_V,
    'eye_R_V': G_var.EYE_R_V
    }
    
    if Send2WSS:
        landmark_coordinates = {}
        len_hand_constants_names = len(ids.hand_constants_names)-1
        # Iterate over all possible landmarks
        for landmark_id in ids.hand_constants:
            # Check if the landmark is available for left and right hands
            left_hand_coordinate = Left_Hands_landmark_coordinates[landmark_id] if landmark_id < len(Left_Hands_landmark_coordinates) else None
            right_hand_coordinate = Right_Hands_landmark_coordinates[landmark_id] if landmark_id < len(Right_Hands_landmark_coordinates) else None

            # Add the coordinates to the landmark_coordinates dictionary
            landmark_coordinates[f"Left_Hand_{ids.hand_constants_names[min(landmark_id,len_hand_constants_names)]}_Pose"] = left_hand_coordinate
            landmark_coordinates[f"Right_Hand_{ids.hand_constants_names[min(landmark_id,len_hand_constants_names)]}_Pose"] = right_hand_coordinate

        # Add the landmark coordinates to the data dictionary
        data.update(landmark_coordinates)

        # Prepare the JSON message with all data
        msg = json.dumps(data) # Velmi to taha dole FPS

        # Send data to ws server

        try:
          asyncio.run(websocket_util.send(msg))
        except ConnectionRefusedError:
          print('WS Server is down')

                
    return output_frame