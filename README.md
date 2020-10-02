# 前言
本项目为我代表学校参加广东省中小学劳动教育暨学生信息素养提升实践活动 - 人工智能项目 主题作品。
![1][1]

人工智能是这个赛事首次举行的项目，在比赛前我们连比什么如何比都是处于未知状态，直到比赛前一晚才确定了比赛的主题为Ai防疫，所以只能勉强使用这个项目作为比赛作品了，记录人员行踪也挺符合这次智能防疫主题的。

也许这个项目使用的算法或逻辑或命名规则或语法规则都运用的不正确或处于不成熟的状态，但也请给位大神见谅或是请求未来的我不要为此感到丢人，毕竟人都是处于一个不断进步的过程。

核心算法使用了opencv开源库

我将用此文档来大概说下使用流程以及可能需要安装的库。

若此项目对你有帮助，顺便给个Star咯~

# 可能需要安装的库

    pip install opencv-python
    pip install pillow
    pip install opencv-contrib-python
    pip install playsound 用于播放音频

# 文件结构说明

**1，文件夹**
- face_trainer (训练模型文件储存文件夹)
- file （一个识别成功后播放的音频文件）
- 后端 （需要上传到服务器的文件）
- 采集训练 （采集训练图片的一些程序）

**2，文件**
- main.py (主运行程序)
- Aface.py (主要函数模块)

# 使用步骤

**1，安装所需库并能正常import**

**2，搭建服务器环境**

（1）这个服务器环境可以是本地局域网环境或是云端云服务器。

（2）这个服务器环境需要能正常运行PHP程序和使用数据库MySQL，若不能请自行百度相关环境搭建教程。这里推荐[宝塔][2]一键集成化环境。

（3）你需要一个ip或域名，作为访问服务器的地址，若是本地服务器记得手机与你的程序连接在同一个局域网下，这样才能正常进行数据传输。

**2，信息配置**

（1）导入数据库数据
将此文件导入到你的MySQL数据库中

![2020-10-02 100945.png][3]


![2020-10-02 101458.png][4]

数据库结构：

![2020-10-02 101305.png][5]

（2）修改数据库账号密码

修改api.php中的数据库信息，若没有正常修改将导致数据无法上传到服务器

![2020-10-02 101927.png][6]

（3）修改主机地址

在python主程序main.py中修改主机地址为你的域名或局域网IP

![2020-10-02 102443.png][7]

（4）下载使用App源码

这里App源码请移步到另一个仓库下载，具体使用方法请看那里的描述文档。

![20201002104117.jpg][8]

# 现场演示视频
[B站：FaceSign 演示视频][9]

# 注意
这里将返回一个人名列表并给变量names

![2020-10-02 114831.png][10]

在采集数据时输入人脸ID：0 对应列表中的第一个名字，以此类推

    ['张三','李四','李华']
    ID =0 对应张三

# 联系我
Authon：小A

QQ：2253162533


  [1]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/1010757683.jpg
  [2]: https://www.bt.cn/
  [3]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/1072375587.png
  [4]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/1654160804.png
  [5]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/2011270633.png
  [6]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/2215194851.png
  [7]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/1323135802.png
  [8]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/3668382161.jpg
  [9]: https://b23.tv/QM6PAR
  [10]: https://cdn.jsdelivr.net/gh/Xiao-A1/fasv/usr/uploads/2020/10/1505172136.png
