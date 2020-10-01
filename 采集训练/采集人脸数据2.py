import cv2
import os

# 开启摄像头
cap = cv2.VideoCapture(0)
minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4)

# 加载「分类器」
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

face_id = input('\n 请输入采集ID:')

print('\n 等待开启摄像头 ...')

# 创建人脸数据保存文件夹
face_data = './Face_data'
if os.path.exists(face_data) is False:
    # 创建一个文件夹
    os.mkdir(face_data)

count = 0
while True:

    # 从摄像头读取图片
    sucess, img = cap.read()

    # 转为灰度图片
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH))
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+w), (0, 0, 255), 2)
        count += 1

        # 保存图像
        cv2.imwrite(face_data+"/User." + str(face_id) + '.' + str(count) + '.jpg', gray[y: y + h, x: x + w])
        print(count)

    cv2.imshow('image', img)  # 保持画面的持续。

    k = cv2.waitKey(1)
    if k == 27:   # 通过esc键退出摄像
        break

    elif count >= 250:  # 得到*个样本后退出摄像
        print('样本提取完毕！')
        break

# 关闭摄像头
cap.release()
cv2.destroyAllWindows()