import os
import requests
from bs4 import BeautifulSoup
import re

# Base URL for video pages and video files
base_page_url = "https://www.cmpe.boun.edu.tr/tid/?v="
base_video_url = "https://www.cmpe.boun.edu.tr/tid/videos/mp4/"

# Directory to save videos
os.makedirs('videos', exist_ok=True)

def sanitize_filename(name):
    """
    Sanitizes a string to make it suitable for use as a file name.

    This function removes characters that are not allowed in file names according to
    common file system conventions. It replaces characters such as '<', '>', ':', '"', 
    '/', '\\', '|', '?', and '*' with an empty string.

    Args:
        name (str): The input string to be sanitized.

    Returns:
        str: The sanitized string suitable for use as a file name.

    Example:
        >>> filename = "my<file>:name?*"
        >>> sanitized_filename = sanitize_filename(filename)
        >>> print(sanitized_filename)
        "myfilename"
    """
    # Remove invalid characters for file names
    return re.sub(r'[<>:"/\\|?*]', '', name)

for i in range(3, 1355):
    page_url = base_page_url + str(i)
    video_url = base_video_url + str(i) + ".mp4"

    response = requests.get(page_url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page {i}")
        continue

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the tag with the required style
    tag = soup.find('span', style="color:#2D5AC3")
    if not tag:
        print(f"No tag found on page {i}")
        continue

    # Download the video
    video_response = requests.get(video_url)
    if video_response.status_code == 200:
        tag_text = tag.text.strip().replace(' ', '_')
        sanitized_tag_text = sanitize_filename(tag_text)
        video_path = os.path.join('videos', f"{sanitized_tag_text}.mp4")
        with open(video_path, 'wb') as video_file:
            video_file.write(video_response.content)
        print(f"Downloaded video {i} as {video_path}")
    else:
        print(f"Failed to download video from {video_url}")

print("Download completed.")