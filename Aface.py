# 广东省人工智能应用比赛作品
# Create by 小A

# 模块
from PIL import Image, ImageFont, ImageDraw
import cv2
import numpy as np  # numpy在opencv库中自带
import requests
import os
import datetime
import serial
from playsound import playsound
import threading


def Face_check(host):
    """用于开启人脸识别（后端api）"""

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_trainer/trainer.yml')  # 训练模型数据
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  # 分类器
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 开启摄像头
    cam = cv2.VideoCapture(0)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

    # 发起http请求获取名字
    name = requests.post(host+'/api.php', data={'type': 'preson'})
    names = eval(name.text)  # 将列表样式字符串转列表

    # 写入一个空的临时数据文件,清除上次运行的数据
    filename = 'preson.txt'  # 保存临时数据的文件
    with open(filename, 'w') as file_object:
        file_object.write('')

    # 加载中文字体包
    fontpath = "simsun.ttc"  # 宋体字体文件
    font_1 = ImageFont.truetype(fontpath, 17)  # 加载字体, 字体大小

    idnum = 0
    while True:

        # 判断是否正在执行上传指令
        if os.path.exists('status.txt') is True:
            continue  # 跳过这个循环

        # 读取图像
        ok, img = cam.read()
        if ok is False:
            print('无法读取到摄像头！')
            break  # 跳出循环

        # 人脸检测
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图  
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH))
        )

        # print(len(faces))  # 人脸个数

        for (x, y, w, h) in faces:

            # 绘制矩形
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.rectangle(img, (x-2, y-25), (x+w+2, y), (0, 0, 255), cv2.FILLED)  # 文字框

            # 相似度计算
            idnum, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < 100:
                # 相识
                idnum = names[idnum]
                confidence = "{0}%".format(round(100 - confidence))
                cv2.putText(img, str(confidence), (x+w-35, y-8), font, 0.5, (0, 255, 0), 1) # 相似度文本
                # user_face = imgs[y+2:y+h-2, x+2:x+w-2]
                WritePerson(idnum, filename, img)  # 写入信息
            else:
                idnum = "未知"

            # 写入中文
            img_pil = Image.fromarray(img)  # 图像
            draw = ImageDraw.Draw(img_pil)
            draw.text((x+5, y-20), str(idnum), font=font_1, fill=(255, 255, 255))  # 坐标，文字，颜色
            img = np.array(img_pil)

        cv2.imshow('Camera', img)
        k = cv2.waitKey(10)

        if k == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


def WritePerson(name, filename, user_face):
    """用于保存识别到的人姓名"""

    with open(filename, "r", encoding='UTF-8') as file_object:
        content = file_object.read()  # 读取数据

    date = datetime.datetime.now()  # 获取当前时间
    if content == '':
        msg = {name: ['1', str(date)]}  # 写入的数据
        with open(filename, 'w', encoding='UTF-8') as file_object:
            file_object.write(str(msg))
    else:
        msg = eval(content)  # 转换为字典
        if name in msg.keys():
            # 如果名字在字典里
            list = msg[name]
            time = list[0]  # 获取识别到的次数
            da = list[1]  # 获取首次识别到的时间
            print(time)
            first_date = datetime.datetime.strptime(da, "%Y-%m-%d %H:%M:%S.%f") # 转化为时间数据
            time_difference = (date - first_date).seconds  # 获取秒数差
            if time_difference > 5:
                # 时差大于5s，写入新的数据
                msg = {name: ['1', str(date)]}  # 写入的数据
                with open(filename, 'w', encoding='UTF-8') as file_object:
                    file_object.write(str(msg))
            else:
                if time == 15:
                    # 判断已识别次数是否16次
                    cv2.imwrite('user_face.jpg', user_face)  # 保存人脸图片
                    filename_1 = 'status.txt'  # 识别状态文件
                    with open(filename_1, 'w', encoding='UTF-8') as file_object:
                        file_object.write(str(name))
                else:
                    msg = {name: [int(time) + 1, str(date)]}  # 写入的数据
                    with open(filename, 'w', encoding='UTF-8') as file_object:
                        file_object.write(str(msg))
        else:
            # 若不在
            msg = {name: ['1', str(date)]}  # 写入的数据
            with open(filename, 'w', encoding='UTF-8') as file_object:
                file_object.write(str(msg))


def face_success(host):
    '''用于人脸经过验证后的数据上传'''

    # 写入一个空的临时数据文件,清除上次运行的数据
    with open('already.txt', 'w') as file_object:
        file_object.write('')

    while True:

        # 判断是否执行上传指令    
        if os.path.exists('status.txt') is True:

            date = datetime.datetime.now()  # 获取当前时间
            with open('status.txt', "r", encoding='UTF-8') as file_object:
                name = file_object.read()  # 读取数据
            
            # 30s内不重复识别同一人
            with open('already.txt', "r", encoding='UTF-8') as file_object:
                content = file_object.read()  # 读取数据
            if content != '':
                msg = eval(content)  # 转换为字典
                if name in msg.keys():
                    # 如果名字在字典里
                    da = msg[name]
                    first_date = datetime.datetime.strptime(da, "%Y-%m-%d %H:%M:%S.%f") # 转化为时间数据
                    time_difference = (date - first_date).seconds  # 获取秒数差
                    if time_difference < 30:
                        os.remove('status.txt')  # 删除文件
                        os.remove('user_face.jpg')  # 删除文件
                        # 清空识别数据
                        with open('preson.txt', 'w') as file_object:
                            file_object.write('')
                        print('重复识别！')
                        continue

            # 一切通过后执行

            # 调用上传文件函数
            data = {'name': str(name), 'type': 'upData'}
            r = UpFile(host+'/api.php', 'user_face.jpg', data)
            print(r.text)
            if r.text == '上传成功':

                # 丢给新线程播报语音
                t1 = threading.Thread(target=playm, args=('file/face_successful.mp3',))
                t1.start()

                # 写入一个防止重复识别的文件
                msg = {name: str(date)}  # 写入的数据
                with open('already.txt', 'w', encoding='UTF-8') as file_object:
                    file_object.write(str(msg))
                
                # 正确后执行的事件-----
				# 例如可加一个开启舵机的函数
				
				
				# ------
				
                os.remove('status.txt')  # 删除文件
                os.remove('user_face.jpg')  # 删除文件

                    # 写入一个空的临时数据文件,清除上次运行的数据
                    with open('preson.txt', 'w') as file_object:
                        file_object.write('')
            else:
                os.remove('status.txt')  # 删除文件
                os.remove('user_face.jpg')  # 删除文件


def UpFile(Url, FilePath, data):
    '''
    用于POST上传文件以及提交参数
    @ Url 上传接口
    @ FilePath 文件路径
    @ data 提交参数 {'key':'value', 'key2':'value2'}
    '''
    files = {'file': open(FilePath, 'rb')}
    result = requests.post(Url, files=files, data=data)
    return result


def ckCall(send, Port, baudRate):
    '''与arduino进行串口通信(发送的数据,串口, 波特率)'''

    ser = serial.Serial(Port, baudRate, timeout=1)
    while True:
        ser.write(send.encode())
        str = ser.readline().decode()  # 获取arduino发送的数据
        if(str != ""):
            print(str)
            if(str == 'ok\r\n'):  # 发送一次便退出
                return True
                ser.close()
                break


def playm(file):
    '''用于播放音频'''
    playsound(file)