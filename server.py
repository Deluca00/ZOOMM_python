import socket
import threading
import random
from vidstream import StreamingServer
import tkinter as tk
from tkinter import messagebox


class MeetingServer:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.rooms = {}  # Dictionary to manage rooms and their ports

    def create_room(self):
        # Generate a random port number between 10000 and 60000
        room_port = random.randint(10000, 60000)

        # Ensure the port is not already in use
        while room_port in self.rooms:
            room_port = random.randint(10000, 60000)

        # Start a video server on the generated port
        video_server = StreamingServer(self.server_ip, room_port)
        threading.Thread(target=video_server.start_server).start()

        # Register the room with its port
        self.rooms[room_port] = video_server
        print(f"Room created with video port: {room_port}")

        return room_port  # Return the port to display in the interface


class MeetingApp:
    def __init__(self, root, server):
        self.server = server
        self.root = root
        self.root.title("Meeting Server")
        self.root.geometry("400x300")

        # Create UI elements
        self.create_room_button = tk.Button(root, text="Create New Room", command=self.create_room)
        self.create_room_button.pack(pady=20)

        self.room_list_label = tk.Label(root, text="Active Rooms:", font=("Arial", 12, "bold"))
        self.room_list_label.pack(pady=5)

        # Frame to display active rooms
        self.room_list_frame = tk.Frame(root)
        self.room_list_frame.pack(fill="both", expand=True)
        self.update_room_list()  # Update room list initially

    def create_room(self):
        # Create a new room and get the random port number
        room_port = self.server.create_room()
        messagebox.showinfo("New Room Created", f"Room created with port: {room_port}")
        self.update_room_list()  # Refresh the room list display

    def update_room_list(self):
        # Clear the previous room list display
        for widget in self.room_list_frame.winfo_children():
            widget.destroy()

        # Display each room with its port
        for port in self.server.rooms.keys():
            room_label = tk.Label(self.room_list_frame, text=f"Room Port: {port}")
            room_label.pack(anchor="w")


# Set the server's IP address here
server_ip= socket.gethostbyname(socket.gethostname())
# server_ip = 'YOUR_SERVER_IP'
server = MeetingServer(server_ip)

# Start the main application window
root = tk.Tk()
app = MeetingApp(root, server)
root.mainloop()
