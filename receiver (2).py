from vidstream import StreamingServer
import threading 

receiver = StreamingServer('192.168.111.111', 9999)

t = threading.Thread(target=receiver.start_server)
t.start()

while input("") != 'STOP':
    continue 

receiver.stop_server()
