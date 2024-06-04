import os
import cv2

# Function to resize image while maintaining aspect ratio
def resize_to_fullscreen(image, screen_width, screen_height):
    """
    Resize an image to fit the screen while maintaining aspect ratio.

    Args:
        image (numpy.ndarray): Input image to be resized.
        screen_width (int): Width of the screen.
        screen_height (int): Height of the screen.

    Returns:
        numpy.ndarray: Resized image.
    """
    img_height, img_width = image.shape[:2]
    aspect_ratio = img_width / img_height

    # Calculate new dimensions
    if screen_width / screen_height > aspect_ratio:
        new_height = screen_height
        new_width = int(screen_height * aspect_ratio)
    else:
        new_width = screen_width
        new_height = int(screen_width / aspect_ratio)

    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

# Function to get video name without extension
def get_video_name(video_path):
    """
    Extracts the name of the video file from its path.

    Args:
        video_path (str): Path to the video file.

    Returns:
        str: Name of the video file without the extension.
    """
    
    base_name = os.path.basename(video_path)
    video_name, _ = os.path.splitext(base_name)
    return video_name