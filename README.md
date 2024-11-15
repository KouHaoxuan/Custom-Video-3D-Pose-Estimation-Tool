# 3D Human Pose Estimation - Video Processing Tool

This project provides a front-end interface for a 3D human pose estimation system, enabling video selection, processing, and playback within an intuitive GUI. Built with Python, Tkinter, and OpenCV, the tool allows users to load, process, and visualize video data, supporting 2D-to-3D pose transformation and frame-by-frame pose estimation through custom processing steps.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Commands](#commands)

## Features
- **GUI-based Video Processing**: Load and process videos through a Tkinter-based GUI.
- **Real-Time Pose Estimation**: Applies pre-trained models for 2D keypoint inference and processes these for 3D pose estimation.
- **Step-wise Processing**: Modular functions for each processing step, enabling custom 2D-to-3D transformations.
- **Threaded Operations**: Multi-threaded command execution to maintain responsive UI.

## Project Structure
```
.
├── VideoPlayer           # Handles video display and controls
├── VideoProcessorApp     # Main GUI application, handles video selection, processing steps, and playback
└── run_command           # Command execution in a separate thread to avoid UI blocking
```

### Main Components
1. **VideoPlayer** (`VideoPlayer` Class): 
   - Controls video loading, frame resizing, and real-time playback within the GUI.
   - Methods:
     - `open(video_path)`: Opens the selected video file.
     - `play()`: Displays frames on the canvas and handles playback.
     - `stop()`: Stops video playback and releases resources.

2. **VideoProcessorApp** (`VideoProcessorApp` Class):
   - Main application interface with Tkinter.
   - Components:
     - `canvas`: Displays the video feed.
     - `output_text`: Text box to display command output in real time.
     - `status`: Status bar to indicate application state.
   - Processing Methods:
     - `select_video()`: Loads and previews the video.
     - `process_video1()`, `process_video2()`, `process_video3()`, `process_video4()`: Executes video processing steps in sequence.
     - `play_processed_video()`: Plays back the processed video.

3. **Command Execution** (`run_command` Function):
   - Runs terminal commands in a separate thread, updating the GUI output text box with real-time feedback.

## Dependencies
- **Python 3.x**
- **Tkinter**: GUI framework (included in standard Python libraries).
- **OpenCV**: For video frame handling and manipulation.
- **Pillow (PIL)**: Image processing library for frame transformations.

Install dependencies using:
```bash
pip install opencv-python pillow
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/KouHaoxuan/Custom-Video-3D-Pose-Estimation-Tool
   cd 3D-human-pose-estimation
   ```
2. Install the required packages (listed above).

## Usage
1. **Run the Application**:
   ```bash
   python Main.py
   ```
2. **Select Video**: Click “选择视频” to choose an `.mp4` file.
3. **Process Steps**:
   - Execute each processing step (1-4) sequentially:
     - Step 1: Initial video setup.
     - Step 2: 2D keypoint inference using `inference/infer_video_d2.py`.
     - Step 3: Generate a custom dataset from the 2D keypoint output.
     - Step 4: Run 3D pose estimation and save the final output.
4. **Playback**: Once processed, select “播放处理后的视频” to view the final processed video.

## Technical Details
### Processing Steps
- **Step 1**: Prepares the environment.
- **Step 2**: Runs 2D keypoint detection.
  ```python
  command = "python inference/infer_video_d2.py --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml --output-dir <output_directory> --image-ext mp4 <input_directory>"
  ```
- **Step 3**: Prepares a custom dataset for 3D estimation.
  ```python
  command = "python prepare_data_2d_custom.py -i <output_directory> -o myvideos"
  ```
- **Step 4**: Runs the main 3D pose estimation and visualization.
  ```python
  command = "python run.py -d custom -k myvideos -arc 3,3,3,3,3 -c checkpoint --evaluate pretrained_h36m_detectron_coco.bin --render --viz-video <input_video_path> --viz-output <output_path>"
  ```

### Multi-threading
- **Function**: `run_command` executes commands in a separate thread, ensuring the UI remains responsive.

## Commands
- **Select Video**: Opens a file dialog for selecting a video.
- **Process Steps (1-4)**: Executes the video processing pipeline.
- **Play Processed Video**: Displays the output video after processing is complete.

## Results
![Screenshot of Output Video]([Group Assignment - Video 3D Pose Estimation/output.png])

### The project is based on the VideoPose3D:

```
@inproceedings{pavllo:videopose3d:2019,
  title={3D human pose estimation in video with temporal convolutions and semi-supervised training},
  author={Pavllo, Dario and Feichtenhofer, Christoph and Grangier, David and Auli, Michael},
  booktitle={Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2019}
}
```
