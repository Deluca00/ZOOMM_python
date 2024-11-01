from vidstream import AudioSender, AudioReceiver, ScreenShareClient, CameraClient, StreamingServer
import tkinter as tk
import socket
import threading
from PIL import Image, ImageTk
import numpy as np

# Biến toàn cục để lưu trữ các client
camera_client = None
stream_client = None
audio_sender = None

local_ip_address = socket.gethostbyname(socket.gethostname())
print("Local IP Address:", local_ip_address)
server = StreamingServer(local_ip_address, 7777)
receiver = AudioReceiver(local_ip_address, 6666)

def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()
    print("Server started")

def toggle_camera_stream():
    global camera_client
    if camera_client is None:
        camera_client = CameraClient(text_target_ip.get(1.0, 'end-1c'), 9999)
        t3 = threading.Thread(target=start_camera_stream)
        t3.start()
        btn_camera.config(text="Stop Camera Stream", bg="green", fg="white")
        print("Camera stream started")
    else:
        camera_client.stop_stream()
        camera_client = None
        btn_camera.config(text="Start Camera Stream", bg="red", fg="white")
        stop_video_display()  # Đưa đến hàm để dừng hiển thị video
        print("Camera stream stopped")

def start_camera_stream():
    global camera_client
    while camera_client is not None:
        frame = camera_client._get_frame()  # Sử dụng phương thức _get_frame() trực tiếp
        if frame is not None:
            # Chuyển đổi frame thành hình ảnh có thể hiển thị
            image = Image.fromarray(frame)
            image = image.resize((640, 480))
            photo = ImageTk.PhotoImage(image)

            # Cập nhật label video
            label_video.config(image=photo)
            label_video.image = photo  # Giữ tham chiếu đến hình ảnh để không bị Garbage Collection
        else:
            break
        window.update_idletasks()  # Cập nhật giao diện

def toggle_screen_sharing():
    global stream_client
    if stream_client is None:
        stream_client = ScreenShareClient(text_target_ip.get(1.0, 'end-1c'), 9999)
        t4 = threading.Thread(target=start_screen_sharing)
        t4.start()
        btn_screen.config(text="Stop Screen Sharing", bg="green", fg="white")
        print("Screen sharing started")
    else:
        stream_client.stop_stream()
        stream_client = None
        btn_screen.config(text="Start Screen Sharing", bg="red", fg="white")
        stop_video_display()  # Đưa đến hàm để dừng hiển thị video
        print("Screen sharing stopped")

def start_screen_sharing():
    global stream_client
    while stream_client is not None:
        frame = stream_client._get_frame()  # Sử dụng phương thức _get_frame() trực tiếp
        if frame is not None:
            # Chuyển đổi frame thành hình ảnh có thể hiển thị
            image = Image.fromarray(frame)
            image = image.resize((640, 480))
            photo = ImageTk.PhotoImage(image)

            # Cập nhật label video
            label_video.config(image=photo)
            label_video.image = photo  # Giữ tham chiếu đến hình ảnh để không bị Garbage Collection
        else:
            break
        window.update_idletasks()  # Cập nhật giao diện

def toggle_audio_stream():
    global audio_sender
    if audio_sender is None:
        audio_sender = AudioSender(text_target_ip.get(1.0, 'end-1c'), 8888)
        t5 = threading.Thread(target=audio_sender.start_stream)
        t5.start()
        btn_audio.config(text="Stop Audio Stream", bg="green", fg="white")
        print("Audio stream started")
    else:
        audio_sender.stop_stream()
        audio_sender = None
        btn_audio.config(text="Start Audio Stream", bg="red", fg="white")
        print("Audio stream stopped")

def stop_video_display():
    # Đặt màu nền thành đen và hiển thị tên người dùng
    label_video.config(image='', bg='black')  # Đặt hình ảnh là trống
    label_video.text = "Account: " + text_user_name.get(1.0, 'end-1c')  # Hiển thị tên người dùng
    label_video.pack(expand=True, fill=tk.BOTH)
    label_name.config(text=label_video.text)

# GUI
window = tk.Tk()
window.title("Meeting Calls v0.1.7 BETA")
window.geometry('800x800')

label_target_ip = tk.Label(window, text="Target IP:")
label_target_ip.pack()

text_target_ip = tk.Text(window, height=1)
text_target_ip.pack()

label_user_name = tk.Label(window, text="User Name:")
label_user_name.pack()

text_user_name = tk.Text(window, height=1)
text_user_name.pack()

btn_listen = tk.Button(window, text="Start Listening", width=50, command=start_listening)
btn_listen.pack(anchor=tk.CENTER, expand=True)

# Nút điều khiển camera
btn_camera = tk.Button(window, text="Start Camera Stream", width=50, bg="red", fg="white", command=toggle_camera_stream)
btn_camera.pack(anchor=tk.CENTER, expand=True)

# Nút điều khiển chia sẻ màn hình
btn_screen = tk.Button(window, text="Start Screen Sharing", width=50, bg="red", fg="white",
                       command=toggle_screen_sharing)
btn_screen.pack(anchor=tk.CENTER, expand=True)

# Nút điều khiển âm thanh
btn_audio = tk.Button(window, text="Start Audio Stream", width=50, bg="red", fg="white", command=toggle_audio_stream)
btn_audio.pack(anchor=tk.CENTER, expand=True)

# Khung hiển thị video hoặc màn hình
frame_video = tk.Frame(window, bg="black", width=640, height=480)
frame_video.pack(padx=10, pady=10)

# Label để hiển thị video hoặc màn hình
label_video = tk.Label(frame_video, bg="black", text="No active video", fg="white")
label_video.pack(expand=True, fill=tk.BOTH)

# Label để hiển thị tên người dùng
label_name = tk.Label(window, bg="black", fg="white", text="")
label_name.pack()

window.mainloop()
