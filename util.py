import os
import subprocess
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

def convert_ts_to_mp4(input_ts_file, output_mp4_file):
    """
    Converts a single .ts file to .mp4 using ffmpeg.
    
    Parameters:
    - input_ts_file: Path to the input .ts file
    - output_mp4_file: Path to save the output .mp4 file
    """
    
    # Command to convert .ts to .mp4 using ffmpeg
    command = [
        'ffmpeg',
        '-i', input_ts_file,  # Input file
        '-c:v', 'copy',  # Copy video codec (no re-encoding)
        '-c:a', 'copy',  # Copy audio codec (no re-encoding)
        output_mp4_file  # Output file
    ]

    try:
        # Execute the ffmpeg command
        subprocess.run(command, check=True)
        print(f"Conversion successful: {input_ts_file} to {output_mp4_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def batch_convert_ts_to_mp4(input_folder, output_folder):
    """
    Converts all .ts files in the input folder to .mp4 and saves them in the output folder.
    
    Parameters:
    - input_folder: Directory containing .ts files
    - output_folder: Directory to save the converted .mp4 files
    """
    
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.ts'):
            input_ts_file = os.path.join(input_folder, filename)
            output_mp4_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.mp4')
            convert_ts_to_mp4(input_ts_file, output_mp4_file)