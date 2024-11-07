import threading
import tkinter as tk
from vidstream.streaming import CameraClient, ScreenShareClient, VideoClient, StreamingServer
from vidstream.audio import AudioSender, AudioReceiver
from tkinter import messagebox
import time
from PIL import Image, ImageTk

class MeetingClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoom-like Meeting App")
        self.root.geometry("800x600")

        # Variables to track button states
        self.mic_on = True
        self.screen_share_on = False
        self.camera_on = True

        # Top frame for controls
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        # User name input
        tk.Label(control_frame, text="Your Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(control_frame)
        self.name_entry.grid(row=0, column=1)

        # Server IP and Room Port inputs
        tk.Label(control_frame, text="Server IP:").grid(row=1, column=0)
        self.server_ip_entry = tk.Entry(control_frame)
        self.server_ip_entry.grid(row=1, column=1)

        tk.Label(control_frame, text="Room Port:").grid(row=2, column=0)
        self.room_port_entry = tk.Entry(control_frame)
        self.room_port_entry.grid(row=2, column=1)

        # Start/Stop buttons
        self.start_button = tk.Button(control_frame, text="Join Room", command=self.start_video)
        self.start_button.grid(row=3, column=0, pady=10)

        self.stop_button = tk.Button(control_frame, text="Leave Room", command=self.stop_video)
        self.stop_button.grid(row=3, column=1, pady=10)

        # Control buttons for mic, camera, and screen share
        self.mic_button = tk.Button(root, text="Mic On", command=self.toggle_mic)
        self.mic_button.pack(side="left", padx=10, pady=10)

        self.screen_share_button = tk.Button(root, text="Share Screen", command=self.toggle_screen_share)
        self.screen_share_button.pack(side="left", padx=10, pady=10)

        self.camera_button = tk.Button(root, text="Camera On", command=self.toggle_camera)
        self.camera_button.pack(side="left", padx=10, pady=10)

        # Container for video frames
        self.video_frames = tk.Frame(root)
        self.video_frames.pack(fill=tk.BOTH, expand=True)

        # Audio control button
        self.audio_button = tk.Button(root, text="Mic On", command=self.toggle_audio)
        self.audio_button.pack(side="left", padx=10, pady=10)

        self.video_client = None
        self.screen_share_client = None
        self.streaming_server = None
        self.audio_sender = None
        self.audio_receiver = None
        self.user_name = ""

    def toggle_mic(self):
        self.mic_on = not self.mic_on
        self.mic_button.config(text="Mic On" if self.mic_on else "Mic Off")
        messagebox.showinfo("Mic Status", "Mic turned on." if self.mic_on else "Mic turned off.")

    def toggle_screen_share(self):
        self.screen_share_on = not self.screen_share_on
        self.screen_share_button.config(text="Stop Sharing" if self.screen_share_on else "Share Screen")
        if self.screen_share_on:
            messagebox.showinfo("Screen Share", "Screen sharing started.")
            self.start_screen_share()
        else:
            messagebox.showinfo("Screen Share", "Screen sharing stopped.")
            self.stop_screen_share()

    def toggle_camera(self):
        self.camera_on = not self.camera_on
        self.camera_button.config(text="Camera On" if self.camera_on else "Camera Off")
        if not self.camera_on and self.capture:
            self.video_frame.config(image="")  # Clear the display when camera is off

    def toggle_audio(self):
        self.mic_on = not self.mic_on
        self.audio_button.config(text="Mic On" if self.mic_on else "Mic Off")
        if not self.mic_on:
            self.stop_audio()
        else:
            self.start_audio()

    def start_video(self):
        self.user_name = self.name_entry.get()
        server_ip = self.server_ip_entry.get()
        room_port = int(self.room_port_entry.get())

        # Initialize the video, audio sender and receiver clients
        self.streaming_server = StreamingServer(server_ip, room_port)
        self.video_client = VideoClient(server_ip, room_port)
        self.audio_sender = AudioSender(server_ip, room_port)
        self.audio_receiver = AudioReceiver(server_ip, room_port)

        threading.Thread(target=self.streaming_server.start_stream).start()
        threading.Thread(target=self.video_client.start_stream).start()
        threading.Thread(target=self.audio_sender.start_stream).start()
        threading.Thread(target=self.audio_receiver.start_stream).start()

        # Create video frame to show
        self.create_video_frame(self.user_name)

    def stop_video(self):
        if self.video_client:
            self.video_client.stop_stream()
        if self.streaming_server:
            self.streaming_server.stop_stream()
        if self.audio_sender:
            self.audio_sender.stop_stream()
        if self.audio_receiver:
            self.audio_receiver.stop_stream()
        self.clear_video_frames()

    def start_screen_share(self):
        server_ip = self.server_ip_entry.get()
        room_port = int(self.room_port_entry.get())
        self.screen_share_client = ScreenShareClient(server_ip, room_port)
        threading.Thread(target=self.screen_share_client.start_stream).start()

    def stop_screen_share(self):
        if self.screen_share_client:
            self.screen_share_client.stop_stream()

    def start_audio(self):
        if self.audio_sender:
            self.audio_sender.start_stream()

    def stop_audio(self):
        if self.audio_sender:
            self.audio_sender.stop_stream()

    def create_video_frame(self, name):
        # Create a new frame for the video feed with the user's name
        frame = tk.Frame(self.video_frames, borderwidth=2, relief="groove")
        frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Label for the user's name
        label = tk.Label(frame, text=name)
        label.pack()

        # Placeholder canvas for video (replace with actual video feed)
        canvas = tk.Canvas(frame, width=200, height=150, bg="black")
        canvas.pack()

        # This example displays a simple placeholder, as rendering video in tkinter requires custom setup
        # To actually display video, use an external library like OpenCV or a tkinter-compatible video solution
        self.update_placeholder_video(canvas)

    def clear_video_frames(self):
        for widget in self.video_frames.winfo_children():
            widget.destroy()

    def update_placeholder_video(self, canvas):
        # Placeholder function to simulate video frame updates
        def update_frame():
            if self.video_client:  # Check if video is running
                # Simple color change to simulate video feed
                color = "#%06x" % (int(time.time() * 100) % 0xFFFFFF)
                canvas.configure(bg=color)
                self.root.after(100, update_frame)

        update_frame()

# Run the app
root = tk.Tk()
app = MeetingClientApp(root)
root.mainloop()
