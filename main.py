# 广东省人工智能应用比赛作品
# Create by 小A

import threading
import Aface  # 自制模块

host = 'http://facesign.fasv.top/'  # 后端服务器地址

# 开新线程运行（检测上传数据）
t2 = threading.Thread(target=Aface.face_success, args=(host,))
t2.start()

# 开启人脸识别  
Aface.Face_check(host)
