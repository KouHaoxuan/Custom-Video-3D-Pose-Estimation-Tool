import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
import cv2
from PIL import Image, ImageTk


# Classe for displaying video
class VideoPlayer:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.video_source = None
        self.capture = None
        self.frame = None
        self.photo = None

    def open(self, video_path):
        """Open video file"""
        self.video_source = video_path
        self.capture = cv2.VideoCapture(video_path)
        self.play()

    def play(self):
        """Play the video"""
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                # Scaling video frames to fit the size of the Canvas
                frame_resized = cv2.resize(frame, (self.width, self.height))
                frame_resized = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(frame_resized)
                self.photo = ImageTk.PhotoImage(image)

                # If an image already exists, delete it first to avoid duplicate creation
                for item in self.canvas.find_all():
                    self.canvas.delete(item)

                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
                self.canvas.after(28, self.play)
            else:
                self.capture.release()

    def stop(self):
        """Stop Playing"""
        if self.capture:
            self.capture.release()


def read_output(process, output_text_widget):
    while True:
        for line in process.stdout:
            output_text_widget.insert(tk.END, line)
            output_text_widget.yview(tk.END)
        for line in process.stderr:
            output_text_widget.insert(tk.END, line)
            output_text_widget.yview(tk.END)

# Run command line tasks in a new thread to avoid UI freezes
def run_command(command, output_text_widget):
    try:
        output_text_widget.insert(tk.END, "running command: " + command + "\n" + "************" + "\n")
        output_text_widget.yview(tk.END)
        # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        #
        # # Creating threads for standard output and standard errors
        # stdout_thread = threading.Thread(target=read_output, args=(process, output_text_widget))
        # stdout_thread.start()
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Capture output and update the Text control in real time
        for line in process.stdout:
            output_text_widget.insert(tk.END, line)
            output_text_widget.yview(tk.END)
        for line in process.stderr:
            output_text_widget.insert(tk.END, line)
            output_text_widget.yview(tk.END)
        # process.wait()
    except Exception as e:
        output_text_widget.insert(tk.END, f"Error starting process: {e}\n")
        output_text_widget.yview(tk.END)



# UI
class VideoProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Video Processing Tool")
        self.root.geometry("1000x800")

        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Video display canvas
        self.canvas = tk.Canvas(main_frame, width=640, height=360, bg="lightgrey")
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Select video button (centered)
        self.select_button = tk.Button(main_frame, text="Select Video", command=self.select_video)
        self.select_button.grid(row=1, column=0, columnspan=2, pady=10, sticky="n")

        # Command output text box
        self.output_text = tk.Text(main_frame, height=10, width=80)
        self.output_text.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

        # Processing buttons frame (aligned vertically on the right)
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0, column=2, rowspan=3, padx=20, sticky="n")

        # Video processing steps buttons
        self.process_button1 = tk.Button(button_frame, text="Test", command=self.process_video1, width=30)
        self.process_button1.pack(pady=5)

        self.process_button2 = tk.Button(button_frame, text="Reason 2d Key Points", command=self.process_video2, width=30)
        self.process_button2.pack(pady=5)

        self.process_button3 = tk.Button(button_frame, text="Create Custom Data Sets", command=self.process_video3, width=30)
        self.process_button3.pack(pady=5)

        self.process_button4 = tk.Button(button_frame, text="Render custom videos", command=self.process_video4, width=30)
        self.process_button4.pack(pady=5)

        # Play processed video button
        self.play_processed_button = tk.Button(main_frame, text="Play the processed video", command=self.play_processed_video, state=tk.DISABLED)
        self.play_processed_button.grid(row=3, column=0, columnspan=2, pady=10, sticky="n")

        # Status bar
        self.status = tk.Label(self.root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Video player
        self.player = VideoPlayer(self.canvas, 640, 360)
        self.processed_video_path = "/pycharmproject/VideoPose3D-main/detecions/viz/output.mp4"

    def select_video(self):
        """Select the video file and play it"""
        video_path = filedialog.askopenfilename(title="Select the video file",
                                                filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if video_path:
            self.selected_video = video_path
            self.player.open(self.selected_video)
            self.play_processed_button.config(state=tk.DISABLED)  # Initially disable playback of processed video button

    def process_video1(self):
        # self.processed_video_path = self.selected_video.replace('.mp4', '_output.mp4')
        # Clear the command line output box
        self.output_text.delete(1.0, tk.END)
        command = """cd"""
        # Run the command in a background thread
        threading.Thread(target=run_command, args=(command, self.output_text), daemon=True).start()
        # Enable the Play Processed Video button (but it can't be clicked at this point because the video hasn't been processed yet)
        self.play_processed_button.config(state=tk.NORMAL)

    def process_video2(self):
        # self.processed_video_path = self.selected_video.replace('.mp4', '_output.mp4')
        # Clear the command line output box
        self.output_text.delete(1.0, tk.END)
        command = """cd D:/pycharmproject/VideoPose3D-main && python inference/infer_video_d2.py  --cfg COCO-Keypoints/keypoint_rcnn_R_101_FPN_3x.yaml   --output-dir D:/pycharmproject/VideoPose3D-main/detecions/output_directory  --image-ext mp4  D:/pycharmproject/VideoPose3D-main/detecions/input_directory"""  # 在后台线程运行命令
        threading.Thread(target=run_command, args=(command, self.output_text), daemon=True).start()
        # Enable the Play Processed Video button (but it can't be clicked at this point because the video hasn't been processed yet)
        self.play_processed_button.config(state=tk.NORMAL)

    def process_video3(self):
        # self.processed_video_path = self.selected_video.replace('.mp4', '_output.mp4')
        # Clear the command line output box
        self.output_text.delete(1.0, tk.END)
        command = """cd D:/pycharmproject/VideoPose3D-main/data &&  python prepare_data_2d_custom.py -i D:/pycharmproject/VideoPose3D-main/detecions/output_directory -o myvideos"""

        # Run the command in a background thread
        threading.Thread(target=run_command, args=(command, self.output_text), daemon=True).start()
        # Enable the Play Processed Video button (but it can't be clicked at this point because the video hasn't been processed yet)
        self.play_processed_button.config(state=tk.NORMAL)

    def process_video4(self):
        self.processed_video_path = f"/pycharmproject/VideoPose3D-main/detecions/viz/output.mp4"
        # Clear the command line output box
        self.output_text.delete(1.0, tk.END)
        command = """cd D:/pycharmproject/VideoPose3D-main/ && python run.py -d custom -k myvideos -arc 3,3,3,3,3 -c checkpoint --evaluate pretrained_h36m_detectron_coco.bin --render --viz-subject myvideo.mp4 --viz-action custom --viz-camera 0 --viz-video /pycharmproject/VideoPose3D-main/detecions/input_directory/myvideo.mp4 --viz-output /pycharmproject/VideoPose3D-main/detecions/viz/output.mp4 --viz-size 6"""
        # Run the command in a background thread
        threading.Thread(target=run_command, args=(command, self.output_text), daemon=True).start()
        # Enable the Play Processed Video button (but it can't be clicked at this point because the video hasn't been processed yet)
        self.play_processed_button.config(state=tk.NORMAL)

    def play_processed_video(self):
        """Play the processed video"""
        if self.processed_video_path and os.path.exists(self.processed_video_path):
            self.player.stop()  # Stop the currently playing video (if any)
            self.player.open(self.processed_video_path)  # Open and play the processed video
        else:
            messagebox.showerror("Error", "The processed video file does not exist, make sure the process is complete.")


# Main Program
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoProcessorApp(root)
    root.mainloop()
