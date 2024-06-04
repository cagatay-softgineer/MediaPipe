import cv2
from util import get_video_name, resize_to_fullscreen
from mediapipe_util import detect_process


def useMediaPipe(video_path = 'videos/Beyaz.mp4',screen_width = 1920, screen_height = 1000):
    """
    Process a video using MediaPipe for hand, pose, and face detection, and display the results.

    Args:
        video_path (str): Path to the input video file.
        screen_width (int): Width of the screen for resizing the frames.
        screen_height (int): Height of the screen for resizing the frames.
    """
    
    cap = cv2.VideoCapture(video_path)

    # Get video name without extension
    video_name = get_video_name(video_path)

    while True:
        success, frame = cap.read()
        if not success:
            # If the video has ended, reset to the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        # Resize the frame to fullscreen while maintaining aspect ratio
        frame_resized = resize_to_fullscreen(frame, screen_width, screen_height)

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)

        frame_resized = detect_process(frame_rgb,frame_resized)

        cv2.putText(frame_resized, video_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # Display the frame
        cv2.imshow('Pose and Hand and Face Blendshapes Landmarks', frame_resized)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()