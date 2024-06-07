# MediaPipe Hand, Pose, and Face Detection

 This project demonstrates the usage of MediaPipe for hand, pose, and face detection in videos.

# Language Stats:

- Python: 39622 bytes
- HTML: 2905 bytes
- Jupyter Notebook: 691 bytes
- Batchfile: 22 bytes
### Total Size Of Project : 4567 kilobytes
### Total Lines Of Code : 1006

# End of Language Stats

# Features

 - Detects hand, pose, and face landmarks using MediaPipe.
 - Displays the detected landmarks overlaid on the video frames.
 - Supports resizing frames to fit the screen while maintaining aspect ratio.
 - Displays the name of the video file as a text overlay on the frames.

# Requirements

 - Python 3.x
 - OpenCV
 - MediaPipe

# Installation

 1. Clone this repository:

 ```
 git clone https://github.com/yourusername/your-repository.git
 ```

 2. Install the required libraries:

 ```
 pip install opencv-python mediapipe
 ```

# Usage
 1. Place your video files in the `videos` directory.
 2. Run the `useMediaPipe.py` script:

 ```
 python useMediaPipe.py
 ```

 3. Press 'q' to exit the program.

# WebSocket Usage
 1. Start the WebSocket Server:

  -Navigate to the WebSocketServer folder.
  -Run the batch file to start the WebSocket server.
 2. Add `Send2WSS=True` to:
  - useMediaPipe("videos/Test.mp4",Send2WSS=True)

# Customization
 - You can customize the screen width and height in the `useMediaPipe` function to adjust the size of the displayed frames.
 - Additional customization can be done by modifying the code in `useMediaPipe.py` according to your requirements.

# License
 This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Acknowledgments
 - This project uses the MediaPipe library developed by Google.