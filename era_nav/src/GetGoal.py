#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, PoseWithCovarianceStamped
from nav_msgs.msg import OccupancyGrid 
from move_base_msgs.msg import MoveBaseActionGoal
#from sensor_msgs.msg import LaserScan
import threading # Needed for Timer
from std_msgs.msg import String

PI = 3.1415926535897

class GetGoal:

    

    def __init__(self):

        # Creates a node with
        rospy.init_node('GetGoal', anonymous=True)

        # Publisher which will publish to the topic 'Goal'.
        self.goal_publisher = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)

        # A subscriber to the topics 'cmd_vel'.
	self.velocity_subscriber=rospy.Subscriber("/cmd_vel",Twist, self.timer_callback) # When receiving a message, call timer_callback()
	timer = threading.Timer(1, self.PublishGoal) # If 5 seconds elapse, call timeout()
	timer.start()
 
	# A subscriber to the topics '/amcl_Pose'
        self.pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.update_pose)
	#Initial pose
	self.pose_stamped=PoseWithCovarianceStamped()
	self.pose_stamped.pose.pose.position.x=5
	self.pose_stamped.pose.pose.position.y=5
	self.pose_stamped.pose.pose.orientation.z=0

	# A subscriber to the topics '/map'
        self.pose_subscriber = rospy.Subscriber('/map', OccupancyGrid, self.update_map)
	self.map=OccupancyGrid()


    def timer_callback(self, msg):
  	global timer
	#print("Velocity message received")
	timer.cancel()
	timer = threading.Timer(1,PublishGoal)
	timer.start()

    def update_pose(self, msg):
        
	self.pose_stamped=msg
	#self.pose_stamped.pose.pose.position.x
	#self.pose_stamped.pose.pose.position.y
	#self.pose_stamped.pose.pose.orientation.z

    def update_map(self, msg):
	self.map=msg
	print(self.map.info.resolution)
	print(self.map.info.width)
	print(self.map.info.height)


    def PublishGoal(self):
	x=self.pose_stamped.pose.pose.position.x
	y=self.pose_stamped.pose.pose.position.y
	theta=self.pose_stamped.pose.pose.orientation.z*PI
	res=self.map.info.resolution
	w=self.map.info.width
	h=self.map.info.width
	#here suppose to be map analysys and publishing
	#pose_msg=MoveBaseActionGoal
	#self.goal_publisher.publish(pose_msg)

if __name__ == '__main__':
    try:
	x = GetGoal()
    except rospy.ROSInterruptException:
        pass
