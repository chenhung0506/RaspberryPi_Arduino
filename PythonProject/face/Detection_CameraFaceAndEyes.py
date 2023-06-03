# 辨識人臉
# noinspection PyUnresolvedReferences
import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

# 人臉特徵檔
face_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
# 眼睛特徵檔
eyes_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_eye.xml")
#eyes_cascade = cv2.CascadeClassifier("./haarcascade/haarcascade_eye_tree_eyeglasses.xml")

while True:
    ret, frame = cap.read() # 捕捉影像資料
    print(ret, frame)

    if ret == True:
        # 偵測人臉
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 偵測臉部並得到臉部的座標(x, y, w, h)
        faces = face_cascade.detectMultiScale(
            gray,  # 待檢測圖片
            scaleFactor=1.1,  # 檢測粒度(數字越小越精準(速度慢), 反之數字越大越模糊(速度快))
            minNeighbors=15,  # 檢測次數(每個目標至少要檢測通過幾次才算成功，才被認定是 face)
            minSize=(30, 30),  # 搜尋比對最小尺寸
            flags=cv2.CASCADE_SCALE_IMAGE  # 比對物類型
        )
        # 在人臉的周圍上畫上矩形
        for (x, y, w, h) in faces:
            # 參數：frame, 坐上角座標, 右下角座標, BGR 色碼, 框線的寬度
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # 在臉內部進行眼睛偵測
            roi_color = frame[y:y + h, x:x + w]  # 人臉區域-彩色
            roi_gray = gray[y:y + h, x:x + w]  # 人臉區域-灰階
            eyes = eyes_cascade.detectMultiScale(
                roi_gray,  # 待檢測圖片
                scaleFactor=1.1,  # 檢測粒度(數字越小越精準(速度慢), 反之數字越大越模糊(速度快))
                minNeighbors=5,  # 檢測次數(每個目標至少要檢測通過幾次才算成功，才被認定是 face)
                minSize=(30, 30),  # 搜尋比對最小尺寸
                flags=cv2.CASCADE_SCALE_IMAGE  # 比對物類型
            )
            # 在眼睛的周圍上畫上矩形
            for (ex, ey, ew, eh) in eyes:
                # 參數：frame, 坐上角座標, 右下角座標, BGR 色碼, 框線的寬度
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    # 顯示影像
    cv2.imshow('MyCam', frame)
    # 按下 q 離開
    # cv2.waitKey(1) 一個等待鍵盤輸入的涵式
    # 0xFF == ord('q') 獲取 q 的 ASCII
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
