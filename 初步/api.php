<?php
/**  
 * 人脸识别后端PHP程序
 * 2020-6-26
*/

//配置
$host = 'localhost'; // 服务器地址
$sqluser = 'facesign_fasv_to'; // 数据库名
$sqlpass = 'wehNSKzEWeFZKxDD'; // 数据库密码
$dbname = 'facesign_fasv_to'; //数据库名

//获取提交参数
$type = $_POST['type'];
$name = $_POST['name'];

//连接数据库
$con = mysqli_connect($host, $sqluser, $sqlpass, $dbname);
if(!$con){
    exit('数据库连接错误！');
}

//获取人
if($type == 'preson'){
    $preson ='';
    $result = mysqli_query($con, "select `name` from `user`");
    while($row = mysqli_fetch_array($result)){
        $name = $row['name'];
        $preson = $preson . "'" . $name . "'" . ",";
    }

    //输出python列表
    echo "[" . $preson . "]";
}

//上传数据
if($type == 'upData'){

    if($name == null){
        die('Name空！');
    }
    
    // 创建人脸数据保存文件夹
    $dir = 'user_face';
    if(!is_dir($dir)){
        $dir = iconv("UTF-8", "GBK", $dir);
        mkdir ($dir,0777,true);
    }

    $temp = explode(".", $_FILES["file"]["name"]);
    $extension = end($temp);     // 获取文件后缀名
    if($extension == 'jpg'){
        if (isset($_FILES['file'])){
            //将文件传到服务器根目录中
            $Up_Path = $dir.'/'.time().'.jpg';
            $tmpname = $_FILES['file']['tmp_name'];
            //转移临时文件
            $time = time();
            $date = date("Y-m-d H:i:s");
            if(move_uploaded_file($tmpname,$Up_Path)){
                $begin_date = date("Y-m-d ").'00:00:00';
                $result1 = mysqli_query($con, "select `id` from `sign` where name='{$name}' and date > '{$begin_date}'");
                if(mysqli_num_rows($result1) == 0){
                    // 签到进入
                    mysqli_query($con, "update `user` set `newdate`='{$date}'  where name='{$name}'");
                    mysqli_query($con, "update `user` set times=times+1  where name='{$name}'");
                    $status = '1';
                }else{
                    //普通进入
                    $status = '0';
                }
                $sql = "insert into `sign`(`name`,`file`,`status`,`date`) values ('{$name}','{$time}','{$status}','{$date}')";
                $result = mysqli_query($con, $sql);
                if($result){
                    echo "上传成功";
                }
            }else{
                echo "上传失败";
            }
        }
    }else{
        echo '格式不被允许！';
    }
}

//获取今日签到人数
if($type == 'sign_num'){
    $today = date("Y-m-d ").'00:00:00';
    $sql = "select `id` from `sign` where date > '{$today}'";
    $result = mysqli_query($con, $sql);
    $num = mysqli_num_rows($result);
    echo $num;
    
}

//获取人app
if($type == 'app_preson'){
    $result = mysqli_query($con, "select * from `user`");
    while($row = mysqli_fetch_array($result)){
        $name = $row['name'];  //名字
        $age = $row['age'];  //年龄
        $time = $row['times'];  //总签到次数
        $newdate = $row['newdate'];  //最近签到时间
        $today = date("Y-m-d ").'00:00:00';
        if($newdate > $today) $today_sign = 'yes'; else $today_sign = 'no';
        $arr = array(
            'name' => $name,
            'age' => $age,
            'today_sign' => $today_sign,
            'time' => $time
        );
        $list = json_encode($arr) . ',' . $list;
    }
    //输出json数据
    echo '{"list":[' . substr($list, 0, -1) . ']}';
}

//增加人
if($type == 'add'){
    $age = $_POST['age'];
    $res = mysqli_query($con ,"select `id` from `user` where name = '{$name}'");
    if(mysqli_num_rows($res) > 0){
        die('名字不能重复！');
    }
    $date = date("Y-m-d H:i:s");
    $sql = "insert into `user` (`name`, `age`, `newdate`) values ('{$name}','{$age}','{$date}')";
    $result = mysqli_query($con,$sql);
    if($result){
        echo '新人添加成功，请重新训练模型！';
    }
}

//删除
if($type == 'delete')
{
    $sql = "delete from `user` where name ='{$name}' ";
    mysqli_query($con,$sql);
    echo '人员删除成功，请重新训练模型！';
}

//获取单人签到记录
if($type == 'person_sign'){
    $result = mysqli_query($con, "select * from `sign` where name ='{$name}' order by id desc");
    if(mysqli_num_rows($result) == 0){
        die('empty');
    }
    while($row = mysqli_fetch_array($result)){
        $status = $row['status'];  //状态 1签到 0普通入
        $date = $row['date'];  //签到时间
        $file = $row['file'];  //文件
        $arr = array(
            'status' => $status,
            'file' => $file,
            'date' => $date
        );
        $list = json_encode($arr) . ',' . $list;
    }
    //输出json数据
    echo '{"list":[' . substr($list, 0, -1) . ']}';

}

//进记录
if($type == 'into'){
    $result = mysqli_query($con, "select * from `sign` where status ='0' order by id desc");
    while($row = mysqli_fetch_array($result)){
        $status = $row['status'];  //状态 1签到 0普通入
        $name = $row['name'];  //名字
        $date = $row['date'];  //签到时间
        $file = $row['file'];  //文件
        $arr = array(
            'name' => $name,
            'status' => $status,
            'file' => $file,
            'date' => $date
        );
        $list = json_encode($arr) . ',' . $list;
    }
    //输出json数据
    echo '{"list":[' . substr($list, 0, -1) . ']}';
}

//签到记录
if($type == 'signD'){
    $result = mysqli_query($con, "select * from `sign` where status ='1' order by id desc");
    while($row = mysqli_fetch_array($result)){
        $status = $row['status'];  //状态 1签到 0普通入
        $name = $row['name'];  //名字
        $date = $row['date'];  //签到时间
        $file = $row['file'];  //文件
        $arr = array(
            'name' => $name,
            'status' => $status,
            'file' => $file,
            'date' => $date
        );
        $list = json_encode($arr) . ',' . $list;
    }
    //输出json数据
    echo '{"list":[' . substr($list, 0, -1) . ']}';
}
