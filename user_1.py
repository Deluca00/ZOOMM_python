from vidstream import AudioSender, AudioReceiver, ScreenShareClient, CameraClient, StreamingServer
import tkinter as tk
import socket
import threading
from PIL import Image, ImageTk
import numpy as np

# Biến toàn cục để lưu trữ các client
camera_clients = {}
screen_clients = {}
audio_senders = {}
audio_receivers = {}

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

def toggle_audio_stream():
    if text_user_name.get(1.0, 'end-1c') and text_target_ip.get(1.0, 'end-1c'):
        user_name = text_user_name.get(1.0, 'end-1c').strip()
        target_ip = text_target_ip.get(1.0, 'end-1c').strip()

        if user_name not in audio_senders:
            audio_sender = AudioSender(target_ip, 8888)
            audio_senders[user_name] = audio_sender
            t = threading.Thread(target=start_audio_stream, args=(user_name,))
            t.start()
            print(f"Audio stream started for {user_name}")
        else:
            audio_senders[user_name].stop_stream()
            del audio_senders[user_name]
            print(f"Audio stream stopped for {user_name}")

def start_audio_stream(user_name):
    audio_sender = audio_senders[user_name]
    audio_sender.start_stream()
    while user_name in audio_senders:
        pass  # Logic for continuous audio streaming can be added here if needed

def toggle_camera_stream():
    if text_user_name.get(1.0, 'end-1c') and text_target_ip.get(1.0, 'end-1c'):
        user_name = text_user_name.get(1.0, 'end-1c').strip()
        target_ip = text_target_ip.get(1.0, 'end-1c').strip()

        if user_name not in camera_clients:
            camera_client = CameraClient(target_ip, 9999)
            camera_clients[user_name] = camera_client
            t = threading.Thread(target=start_camera_stream, args=(user_name,))
            t.start()
            print(f"Camera stream started for {user_name}")
        else:
            camera_clients[user_name].stop_stream()
            del camera_clients[user_name]
            print(f"Camera stream stopped for {user_name}")

def start_camera_stream(user_name):
    camera_client = camera_clients[user_name]
    while user_name in camera_clients:
        frame = camera_client._get_frame()
        if frame is not None:
            image = Image.fromarray(frame)
            image = image.resize((160, 120))  # Kích thước video nhỏ hơn cho hiển thị
            photo = ImageTk.PhotoImage(image)
            # Cập nhật giao diện với video của người dùng
            update_video_display(user_name, photo, "camera")
        else:
            break

def toggle_screen_sharing():
    if text_user_name.get(1.0, 'end-1c') and text_target_ip.get(1.0, 'end-1c'):
        user_name = text_user_name.get(1.0, 'end-1c').strip()
        target_ip = text_target_ip.get(1.0, 'end-1c').strip()

        if user_name not in screen_clients:
            stream_client = ScreenShareClient(target_ip, 9999)
            screen_clients[user_name] = stream_client
            t = threading.Thread(target=start_screen_sharing, args=(user_name,))
            t.start()
            print(f"Screen sharing started for {user_name}")
        else:
            screen_clients[user_name].stop_stream()
            del screen_clients[user_name]
            print(f"Screen sharing stopped for {user_name}")

def start_screen_sharing(user_name):
    stream_client = screen_clients[user_name]
    while user_name in screen_clients:
        frame = stream_client._get_frame()
        if frame is not None:
            image = Image.fromarray(frame)
            image = image.resize((160, 120))  # Kích thước video nhỏ hơn cho hiển thị
            photo = ImageTk.PhotoImage(image)
            # Cập nhật giao diện với màn hình chia sẻ của người dùng
            update_video_display(user_name, photo, "screen")
        else:
            break

def update_video_display(user_name, photo, stream_type):
    # Cập nhật video camera hoặc màn hình chia sẻ cho người dùng
    if stream_type == "camera":
        label = labels_camera.get(user_name)
    else:
        label = labels_screen.get(user_name)

    if label is not None:
        label.config(image=photo)
        label.image = photo

def create_user_video_display(user_name):
    # Tạo không gian hiển thị cho camera và màn hình chia sẻ của người dùng
    frame_user = tk.Frame(window, bg="black")
    frame_user.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    label_camera = tk.Label(frame_user, bg="black", text=f"{user_name}'s Camera", fg="white")
    label_camera.pack(expand=True, fill=tk.BOTH)
    labels_camera[user_name] = label_camera

    label_screen = tk.Label(frame_user, bg="black", text=f"{user_name}'s Screen", fg="white")
    label_screen.pack(expand=True, fill=tk.BOTH)
    labels_screen[user_name] = label_screen

# GUI
window = tk.Tk()
window.title("Meeting Calls v0.1.7 BETA")
window.geometry('800x800')

labels_camera = {}
labels_screen = {}

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
btn_camera = tk.Button(window, text="Start/Stop Camera Stream", width=50, bg="red", fg="white", command=toggle_camera_stream)
btn_camera.pack(anchor=tk.CENTER, expand=True)

# Nút điều khiển chia sẻ màn hình
btn_screen = tk.Button(window, text="Start/Stop Screen Sharing", width=50, bg="red", fg="white", command=toggle_screen_sharing)
btn_screen.pack(anchor=tk.CENTER, expand=True)

# Nút điều khiển âm thanh
btn_audio = tk.Button(window, text="Start/Stop Audio Stream", width=50, bg="red", fg="white", command=toggle_audio_stream)
btn_audio.pack(anchor=tk.CENTER, expand=True)

window.mainloop()
