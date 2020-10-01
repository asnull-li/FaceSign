import cv2  # 导入人脸检测库
import os  # 导入文件操作模块
from PIL import Image, ImageFont, ImageDraw
import numpy as np

# 录入人脸数据
''' 安装库  pip install opencv-python'''

cap = cv2.VideoCapture(0)  # 开启摄像头 0为电脑默认摄像头 1 2

face_id = input('\n 请输入采集ID:')

print('\n 等待开启摄像头 ...')

# 创建人脸数据保存文件夹
face_data = 'Face_data'
if os.path.exists(face_data) is False:
    # 创建一个文件夹
    os.mkdir(face_data)


count = 0
while True:
    ok, img = cap.read()  # 读取摄像头图像
    if ok is False:
        print('无法读取到摄像头！')
        break
    
    k = cv2.waitKey(10)  # 键盘值

    # 绘制矩形
    cv2.rectangle(img, (190, 110), (410, 360), (0, 0, 255), 3)  # 采集框
    cv2.rectangle(img, (188, 360), (412, 385), (0, 0, 255), cv2.FILLED)  # 文字框

    # 写入文字
    fontpath = "simsun.ttc"  # 宋体字体文件
    font_1 = ImageFont.truetype(fontpath, 19)  # 加载字体, 字体大小
    img_pil = Image.fromarray(img) # 图像
    draw = ImageDraw.Draw(img_pil)
    draw.text((190, 362), '人脸采集框', font=font_1, fill=(255, 255, 255))
    img = np.array(img_pil)

    if k == 32:  # 按空格健保存人脸
        # 保存图像(保存路径，图像)
        count += 1
        print(count)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(face_data+"/User." + str(face_id) + '.' + str(count) + '.jpg', gray[113: 358, 193: 408])
        cv2.imshow('face', gray[113: 358, 193: 408])  # y+h， x+w

    # 展示图像
    cv2.imshow('image', img)

    if k == 27:   # 通过esc键退出摄像
        break

    if count >= 250:  # 得到*个样本后退出摄像
        print('样本提取完毕！')
        break

# 关闭摄像头
cap.release()
cv2.destroyAllWindows()