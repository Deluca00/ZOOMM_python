from vidstream import ScreenShareClient
from mss import mss
import threading

# def start_screen_sharing():
#     with mss() as sct:
#         while True:
#             sct.shot(output="screenshot.png")
#
# # Sử dụng luồng để chạy chia sẻ màn hình
# t = threading.Thread(target=start_screen_sharing)
# t.start()


# Địa chỉ IP và cổng của máy nhận
sender = ScreenShareClient('192.168.111.111', 9999)

# Khởi tạo và bắt đầu luồng chia sẻ màn hình
t = threading.Thread(target=sender.start_stream)
t.start()

try:
    # Lặp lại cho đến khi nhận được "STOP"
    while input("Nhập 'STOP' để dừng: ") != 'STOP':
        continue
finally:
    # Đảm bảo ngắt kết nối
    sender.stop_stream()
    print("Đã dừng chia sẻ màn hình.")

