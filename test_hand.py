import cv2

# Function to classify left and right hands for all hands
def classify_hands(results):
    """
    Classifies the detected hands as "Left hand" or "Right hand" based on their landmark positions.

    This function takes the results from hand detection and classifies each detected hand
    as either a "Left hand" or a "Right hand" based on the positions of key landmarks such
    as the thumb tip, index finger tip, pinky tip, and wrist. It creates a dictionary where
    the keys are "Left hand" and "Right hand", and the values are lists of landmark data
    corresponding to each hand.

    Args:
        results (mediapipe.framework.formats.landmark_pb2.NormalizedLandmarkList): 
            The results of hand detection, containing landmarks for detected hands.

    Returns:
        dict: A dictionary containing lists of landmark data for each classified hand. 
        The keys are "Left hand" and "Right hand", and the values are lists of 
        NormalizedLandmarkList objects representing the detected hands.

    Example:
        >>> results = hands.process(image)
        >>> hand_labels = classify_hands(results)
        >>> left_hand_landmarks = hand_labels["Left hand"]
        >>> right_hand_landmarks = hand_labels["Right hand"]
    """
    hand_labels = {"Left hand": [], "Right hand": []}
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get landmarks for the current hand
            landmarks = hand_landmarks.landmark
            # Extract landmark positions
            thumb_tip = landmarks[4]
            index_finger_tip = landmarks[8]
            pinky_tip = landmarks[20]
            wrist = landmarks[0]
            # Calculate distances between key landmarks
            thumb_index_dist = abs(thumb_tip.x - index_finger_tip.x)
            thumb_pinky_dist = abs(thumb_tip.x - pinky_tip.x)
            # Example logic to determine handedness based on landmark distances
            if thumb_index_dist < thumb_pinky_dist:  # Thumb is closer to index finger
                if wrist.x < index_finger_tip.x:  # Thumb is to the left of index finger
                    hand_labels["Left hand"].append(hand_landmarks)
                else:
                    hand_labels["Right hand"].append(hand_landmarks)
            else:  # Thumb is closer to pinky finger
                if wrist.x < pinky_tip.x:  # Thumb is to the left of pinky finger
                    hand_labels["Left hand"].append(hand_landmarks)
                else:
                    hand_labels["Right hand"].append(hand_landmarks)
    return hand_labels

def classify_hands_with_hand_lanmarks(hand_landmarks):
    """
    Classifies a hand as either "Left hand" or "Right hand" based on its landmarks.

    This function analyzes the positions of key landmarks on a hand and determines 
    whether the hand is a left or right hand. The classification is based on the 
    relative distances between the thumb, index finger, and pinky finger, and the 
    position of the wrist.

    Args:
        hand_landmarks (NormalizedLandmarkList): 
            The landmarks of a single hand. It is expected that the landmarks are 
            ordered as per the Mediapipe hands model, where specific indices correspond 
            to the thumb tip (4), index finger tip (8), pinky tip (20), and wrist (0).

    Returns:
        str: "Left hand" if the hand is determined to be the left hand, "Right hand" 
        if the hand is determined to be the right hand.

    Example:
        >>> hand_landmarks = results.multi_hand_landmarks[0]
        >>> hand_label = classify_hands_with_hand_landmarks(hand_landmarks)
        >>> print(hand_label)
        "Left hand"
    """
    # Get landmarks for the current hand
    landmarks = hand_landmarks.landmark
    # Extract landmark positions
    thumb_tip = landmarks[4]
    index_finger_tip = landmarks[8]
    pinky_tip = landmarks[20]
    wrist = landmarks[0]
    # Calculate distances between key landmarks
    thumb_index_dist = abs(thumb_tip.x - index_finger_tip.x)
    thumb_pinky_dist = abs(thumb_tip.x - pinky_tip.x)
    # Example logic to determine handedness based on landmark distances
    if thumb_index_dist < thumb_pinky_dist:  # Thumb is closer to index finger
        if not wrist.x < index_finger_tip.x:  # Thumb is to the left of index finger
            return "Left hand"
        else:
            return "Right hand"
    else:  # Thumb is closer to pinky finger
        if not wrist.x < pinky_tip.x:  # Thumb is to the left of pinky finger
            return "Left hand"
        else:
            return "Right hand"


def annotate_hands(image, hand_labels):
    """
    Annotates an image with hand labels.

    This function takes an image and a dictionary of hand labels and their corresponding
    landmarks, then draws the hand label on the image at the position of the first landmark
    in the list.

    Args:
        image (numpy.ndarray): 
            The input image to be annotated.
        hand_labels (dict): 
            A dictionary where keys are hand labels (e.g., "Left hand", "Right hand") 
            and values are lists of landmarks for each hand. Each landmark is expected 
            to be an object with `x` and `y` attributes representing normalized coordinates.

    Returns:
        numpy.ndarray: The annotated image with hand labels drawn on it.

    Example:
        >>> image = cv2.imread('path/to/image.jpg')
        >>> hand_labels = {
        >>>     "Left hand": [landmark1, landmark2, ...],
        >>>     "Right hand": [landmark1, landmark2, ...]
        >>> }
        >>> annotated_image = annotate_hands(image, hand_labels)
    """
    # Draw the hand labels on the image
    for hand_label, landmarks_list in hand_labels.items():
        # Check if landmarks_list is not empty
        if landmarks_list:
            # Get the position for the text (using the first landmark)
            text_position = (int(landmarks_list[0].x * image.shape[1]), int(landmarks_list[0].y * image.shape[0]))
            # Draw the text on the image
            cv2.putText(image, hand_label, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    return image