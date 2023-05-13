'''
PC 安裝
pip install opencv-python
pip install opencv-python-headless # 若您需要在沒有GUI的環境中使用 opencv
pip install pillow
樹梅派安裝
sudo apt update
sudo apt install python3-opencv
pip install pillow
sudo apt-get install python3-pil.imagetk
'''
import cv2
import tkinter as tk
from PIL import Image, ImageTk

# 初始化攝像頭
cap = cv2.VideoCapture(0)

# 攝像頭開啟失敗的話，結束程式
if not cap.isOpened():
    print("無法開啟攝像頭")
    exit(0)

# 建立一個 tkinter 視窗
window = tk.Tk()
window.title("USB Camera")

# 建立一個 tkinter 的 Label 來顯示影像
label = tk.Label(window)
label.pack()

# 更新視窗，顯示攝像頭影像
def update_image():
    ret, frame = cap.read()

    if not ret:
        print("無法讀取攝像頭影像")
        return

    # 將 OpenCV 讀取的 BGR 影像轉換為 RGB 影像，以便 Pillow 使用
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 將 OpenCV 影像轉換建立 PIL 影像
    pil_img = Image.fromarray(frame)

    # 將 PIL 影像轉換建立 tkinter 適用的 PhotoImage
    photo = ImageTk.PhotoImage(pil_img)

    # 在視窗上顯示攝像頭影像
    label.config(image=photo)
    label.image = photo

    # 進行下一次更新
    window.after(10, update_image)

# 開始更新視窗
update_image()

# 進入 tkinter 主迴圈
window.mainloop()

# 釋放攝像頭資源
cap.release()
cv2.destroyAllWindows()
