#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
#from math import pow, atan2, sqrt


class Robot:

    distance_tolerance = 1

    def __init__(self):
        # Creates a node with
        rospy.init_node('Robot', anonymous=True)

        # Publisher which will publish to the topic '/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

        # A subscriber to the topic '/base_scan'. self.update_pose is called
        # when a message of type Pose is received.
        self.pose_subscriber = rospy.Subscriber('/base_scan', LaserScan, self.update_pose)

        self.pose = LaserScan()
        for i in range(18):
            self.pose.ranges.append(0.001)
        self.rate = rospy.Rate(10)

    def update_pose(self, data):
        """Callback function which is called when a new message of type LaserScan is
        received by the subscriber."""
        self.pose = data
	#right=sum(self.pose.ranges[0:6])/len(self.pose.ranges[0:6])
	#forward=sum(self.pose.ranges[6:12])/len(self.pose.ranges[6:12])
	#left=sum(self.pose.ranges[12:18])/len(self.pose.ranges[12:18])
	right=min(self.pose.ranges[0:6])
	forward=min(self.pose.ranges[6:12])
	left=min(self.pose.ranges[12:18])
	self.pose.ranges = [right, forward, left]
	print (right, forward, left)

    def linear_vel(self, constant=1.5):

        return constant * self.pose.ranges[1]

    def move_forward(self):
	print("moving forward...")
 	#distance_tolerance = 1
	vel_msg = Twist()
        while self.pose.ranges[1] > self.distance_tolerance:

            # Linear velocity in the x-axis.
            vel_msg.linear.x = self.linear_vel()
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = 0

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)
	return

    def angular_vel(self, dist, constant=6):

	return dist * constant

    def rotate(self):
	print("rotating...")
	#distance_tolerance = 1
	vel_msg = Twist()
	dist=0.0
	if self.pose.ranges[0] < self.pose.ranges[2]:
		dist=self.pose.ranges[2]/self.pose.ranges[0]
		print("rotating right")
	else: 
		dist=-self.pose.ranges[0]/self.pose.ranges[2]
		print("rotating left")

        while self.pose.ranges[1] < self.distance_tolerance:
            vel_msg.linear.x = 0
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = self.angular_vel(dist)

            # Publishing our vel_msg
            self.velocity_publisher.publish(vel_msg)

            # Publish at the desired rate.
            self.rate.sleep()

        # Stopping our robot after the movement is over.
        vel_msg.angular.z = 0
        self.velocity_publisher.publish(vel_msg)
	return

        

    def move(self):

	while not rospy.is_shutdown():
		self.move_forward()
		self.rotate()


if __name__ == '__main__':
    try:
	#rospy.wait_for_message('/base_scan', 'sensor_msgs')???
	x = Robot()
	x.move()
    except rospy.ROSInterruptException:
        pass
