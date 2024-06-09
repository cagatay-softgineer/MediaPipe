import os
import subprocess
import cv2
import re
import lm_indices as ids

# Function to resize image while maintaining aspect ratio
def resize_to_fullscreen(image, screen_width, screen_height):
    """
    Resizes an image to fit within the dimensions of a screen, preserving the aspect ratio.

    This function takes an image and the dimensions of a screen, then resizes the image 
    to fit within the screen dimensions while maintaining the original aspect ratio. 
    It ensures that the resized image will either match the screen width or height exactly,
    without stretching or distorting the image.

    Args:
        image (numpy.ndarray): 
            The input image to be resized.
        screen_width (int): 
            The width of the screen.
        screen_height (int): 
            The height of the screen.

    Returns:
        numpy.ndarray: The resized image that fits within the screen dimensions.

    Example:
        >>> image = cv2.imread('path/to/image.jpg')
        >>> resized_image = resize_to_fullscreen(image, 1920, 1080)
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
    Extracts the base name (without extension) of a video file from its path.

    This function takes the full path of a video file, extracts its base name, 
    and removes the file extension, returning only the name of the video.

    Args:
        video_path (str): 
            The full path to the video file.

    Returns:
        str: The base name of the video file without the extension.

    Example:
        >>> get_video_name('/path/to/video/file.mp4')
        'file'
    """
    base_name = os.path.basename(video_path)
    video_name, _ = os.path.splitext(base_name)
    return video_name

def convert_ts_to_mp4(input_ts_file, output_mp4_file):
    """
    Converts a .ts file to .mp4 format using ffmpeg.

    This function takes an input .ts file and converts it to .mp4 format using the ffmpeg command-line tool.
    The video and audio codecs are copied without re-encoding, ensuring a quick conversion process.

    Args:
        input_ts_file (str): 
            The path to the input .ts file to be converted.
        output_mp4_file (str): 
            The path where the output .mp4 file will be saved.

    Returns:
        None

    Example:
        >>> convert_ts_to_mp4('/path/to/input.ts', '/path/to/output.mp4')
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
    Converts all .ts files in the input folder to .mp4 format and saves them to the output folder.

    This function iterates over all the files in the specified input folder. For each file with a .ts extension,
    it calls the convert_ts_to_mp4 function to convert it to .mp4 format and saves the converted file
    in the specified output folder.

    Args:
        input_folder (str): 
            The path to the folder containing the .ts files to be converted.
        output_folder (str): 
            The path to the folder where the converted .mp4 files will be saved.

    Returns:
        None

    Example:
        >>> batch_convert_ts_to_mp4('/path/to/ts_files', '/path/to/mp4_files')
    """
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.ts'):
            input_ts_file = os.path.join(input_folder, filename)
            output_mp4_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.mp4')
            convert_ts_to_mp4(input_ts_file, output_mp4_file)
            
def repeated_container_to_list(container):
    """
    Converts a RepeatedCompositeContainer to a list of dictionaries.

    This function takes a RepeatedCompositeContainer, typically used in protocol buffer messages, 
    and converts each element into a dictionary. The resulting list of dictionaries can be more 
    easily manipulated or converted to JSON.

    Args:
        container (RepeatedCompositeContainer): 
            The input container to be converted. This is usually a part of a protocol buffer message.

    Returns:
        list: 
            A list of dictionaries, where each dictionary represents an element from the container.
    """
    return [dict(item) for item in container]

def parse_landmarks_data_with_regex(data):
    """
    Parses landmark data using a regular expression to extract x, y, and z coordinates.

    This function processes a list of strings containing landmark data in a specific format.
    It uses a regular expression to find and extract the coordinates for each landmark, 
    converting them into dictionaries and storing them in a list.

    Args:
        data (list of str): 
            A list of strings, each containing landmark data with x, y, and z coordinates.

    Returns:
        list of dict: 
            A list of dictionaries, where each dictionary represents a landmark with x, y, and z keys.
    
    Example:
        >>> data = ["landmark {  x: 0.436380327  y: 0.875187039  z: -8.16272e-009}",
                    "landmark {  x: 0.461619437  y: 0.842042208  z: -0.00249512075}"]
        >>> parse_landmarks_data_with_regex(data)
        [{'x': 0.436380327, 'y': 0.875187039, 'z': -8.16272e-009},
         {'x': 0.461619437, 'y': 0.842042208, 'z': -0.00249512075}]
    """
    
    # Initialize an empty list to store landmarks
    landmarks_list = []

    # Define the pattern for extracting x, y, and z coordinates
    pattern = r"x:\s*(-?\d+\.\d+(?:e-?\d+)?)\s+y:\s*(-?\d+\.\d+(?:e-?\d+)?)\s+z:\s*(-?\d+\.\d+(?:e-?\d+)?)"

    # Loop through each string in the data list
    for item in data:
        # Find all matches of the pattern in the string
        matches = re.findall(pattern, item)
        # Loop through each match and extract x, y, and z coordinates
        for match in matches:
            x, y, z = map(float, match)
            # Create a dictionary for the landmark and append it to the list
            landmark = {"x": x, "y": y, "z": z}
            landmarks_list.append(landmark)

    return landmarks_list

def extract_coordinates(landmark):
    """
    Extracts the x, y, and z coordinates from a landmark dictionary.

    This function takes a dictionary representing a landmark with x, y, and z keys,
    and returns the coordinates as separate values.

    Args:
        landmark (dict): 
            A dictionary containing the x, y, and z coordinates of a landmark.

    Returns:
        tuple: 
            A tuple containing the x, y, and z coordinates as separate float values.
    
    Example:
        >>> landmark = {'x': 0.428059042, 'y': 0.877048731, 'z': -0.0285293739}
        >>> extract_coordinates(landmark)
        (0.428059042, 0.877048731, -0.0285293739)
    """
    x_coord = landmark['x']
    y_coord = landmark['y']
    z_coord = landmark['z']
    return x_coord, y_coord, z_coord

def extract_coordinates_with_max_possible(landmark):
    landmark_coordinates = []
    max_landmark_index = max(ids.hand_constants)
    num_landmarks = len(landmark)
    
    
    for i in range(min(num_landmarks, max_landmark_index + 1)):
        if i in ids.hand_constants:
            x, y, z = 0, 0, 0  # Default values if landmark not present
            if i < len(landmark) and landmark[i] is not None:  # Check if the landmark is not None
                x, y, z = extract_coordinates(landmark[i])
            landmark_coordinates.append((x, y, z))
    return landmark_coordinates

def draw_circle_on_coord(input_frame,landmark_coordinates,COLOR_DOTS):
    output_frame = input_frame.copy()
    num_landmarks = len(landmark_coordinates)
    for constant in ids.hand_constants:
        if constant < num_landmarks:
            # Get the coordinates of the current constant
            coordinates = landmark_coordinates[constant]
            if coordinates is not None:
                x = coordinates[ids.X]
                y = coordinates[ids.Y]
                # Check if both x and y coordinates are not None
                if x is not None and y is not None:
                    # Draw a circle
                    cv2.circle(output_frame, (int(x*input_frame.shape[ids.W]), int(y*input_frame.shape[ids.H])), 10, COLOR_DOTS, 1)
    return output_frame