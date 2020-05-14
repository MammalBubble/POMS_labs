Для корректной работы скрипта catkin_ws должен быть прописан в переменную ROS_PACKAGE_PATH

После сбора пакета:
* запускаем roscore
* rosrun stage_ros stageros $(rospack find lab_4)/src/name_fam.world
* rosrun lab_4 robot.py

![result](https://github.com/MammalBubble/POMS_labs/blob/master/lab_4/stage.png)

