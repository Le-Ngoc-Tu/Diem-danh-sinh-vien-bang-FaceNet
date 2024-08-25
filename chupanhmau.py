import cv2
import os
import time
cap = cv2.VideoCapture(0)
count = 0
nameID = "K13THO0058"

path = 'train_img/'
path = path+nameID
# Kiểm tra thư mục hình ảnh đã tồn tại chưa
isExist = os.path.exists(path)

if isExist:
    print("Thư mục đã tồn tại")
else:
    os.makedirs(path)

while True:
    success, img = cap.read()
    count = count + 1
    name = os.path.join(path, f'{nameID}_{count}.jpg')
    print("Đang tạo hình ảnh..." + name)
    cv2.imwrite(name, img)
    cv2.imshow("Camera", img)
    cv2.waitKey(1)
    time.sleep(0.2)
    if count > 100:
        break

cap.release()
cv2.destroyAllWindows()