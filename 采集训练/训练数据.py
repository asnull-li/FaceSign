# 训练人脸数据
''' 安装库
  pip install opencv-python
  pip install pillow
  pip install opencv-contrib-python
'''

import numpy as np
from PIL import Image
import os
import cv2

# 人脸数据路径
path = 'Face_data'

# 创建训练数据保存文件夹
train_data = 'face_trainer'
if os.path.exists(train_data) is False:
    os.mkdir(train_data)

recognizer = cv2.face.LBPHFaceRecognizer_create()

# 加载分类器
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)] 
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')   # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(id)
    return faceSamples, ids

print('正在训练人脸数据，请稍后 ...')
faces, ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))

recognizer.write(r'face_trainer\trainer.yml')
print("{0} 个人脸数据".format(len(np.unique(ids))))