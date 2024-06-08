# MediaPipe Hand, Pose, and Face Detection

 This project demonstrates the usage of MediaPipe for hand, pose, and face detection in videos.

# Language Stats:

- Python: 39622 bytes
- HTML: 2905 bytes
- Jupyter Notebook: 691 bytes
### Total Size Of Project : 4567 kilobytes
### Total Lines Of Code : 1027

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
 2. Update the Video Path in `main.py.`
 
  ```
  useMediaPipe("videos/Test.mp4")
  ```
 3. Run the `main.py` script:

 ```
 python main.py
 ```

 4. Press 'q' to exit the program.

# WebSocket Usage
 ## 1. Start the WebSocket Server:

  - Navigate to the WebSocketServer folder.
  ### FOR WINDOWS
  - Run the executable `websoc.exe` file to start the WebSocket server.
  ### FOR MACOS OR LINUX
  - Create a script for run websocket.py
  ```
  python3 websoc.py # Use python if not working with python3
  ```
  - Save the file with a `.sh` extension, for example `run_websoc.sh`
  - Make the Script 
  
  + Open Terminal.
  + Navigate to the directory where you saved run_websoc.sh.
  + Make the script executable by running the following command
  ```
  chmod +x run_websoc.sh
  ```
  - Run the Script
  ```
  ./run_websoc.sh
  ```

 ## 2. Add `Send2WSS=True` to:
  ```
  useMediaPipe("videos/Test.mp4",Send2WSS=True)
  ```

# Customization
 - You can customize the screen width and height in the `useMediaPipe` function to adjust the size of the displayed frames.
 - Additional customization can be done by modifying the code in `modelUsageTests.py` according to your requirements.

# License
 This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# Acknowledgments
 - This project uses the MediaPipe library developed by Google.
 - [![alt text](https://www.gstatic.com/devrel-devsite/prod/v2ce49398fbedb6586ec054c8c0e071251fec28eb36277100a1795e671ae7c694/googledevai/images/lockup-new.svg)](https://ai.google.dev/edge/mediapipe/solutions)
 - This project uses the Blender
 - [![alt text](https://docs.blender.org/api/current/_static/blender_logo.svg)](https://www.blender.org/)
