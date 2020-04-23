#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
speed=1
PI = 3.1415926535897

#strting a new node for publisher
velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
rospy.init_node('velocity_publisher', anonymous = False)

#rospy.wait_for_service('/turtle1/set_pen')
#setpen=rospy.ServiceProxy('/turtle1/set_pen', turtlesim/SetPen)
vel_msg = Twist()

def f(distance):
	print('going on '+ str(distance))
	if(distance>0):
		vel_msg.linear.x = abs(speed)
	else:
		vel_msg.linear.x = -abs(speed)
	#Since we are moving just in x-axis
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0

	#Setting the current time for distance calculus
	t0 = float(rospy.Time.now().to_sec())
        current_distance = 0

        #Loop to move the turtle in an specified distance
        while(current_distance < distance):
            #Publish the velocity
            velocity_publisher.publish(vel_msg)
            #Takes actual time to velocity calculus
            t1=float(rospy.Time.now().to_sec())
            #Calculates distancePoseStamped
            current_distance= speed*(t1-t0)
        #After the loop, stops the robot
        vel_msg.linear.x = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)
	return 0

def r(angle):
	print('rotating on '+ str(angle))
   #Converting from angles to radians
	angular_speed = speed*2*PI/360
	relative_angle = angle*2*PI/360

    #We wont use linear components
	vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
	if (angle > 0):
		vel_msg.angular.z = -abs(angular_speed)
	else:
		vel_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
	t0 = rospy.Time.now().to_sec()
	current_angle = 0

	while(current_angle < relative_angle):
		velocity_publisher.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)

    #Forcing our robot to stop
	vel_msg.angular.z = 0
	velocity_publisher.publish(vel_msg)
#	rospy.spin()
	return 0

def zero():
	print('drawing zero..')
	r(-90);f(2);r(-90);f(1);r(-90);f(2);r(-90);r(-90);f(1)
	return 0

def one():
	r(90)

def two():
	f(2)


def draw_number(i):
	print('starting draw numbers...')
	switcher={
		0: zero(),
		1: one(),
		2: two()
#		3: three,
#		4: four,
#		5: five,
#		6: six,
#		7: seven,
#		8: eight,
#		9: nine
		}
	return 0


def velocity_publisher_f(string):

	while not rospy.is_shutdown():
		for number in string:
			number=int(number)
			draw_number(number)
			rospy.spin()
	return 0

if __name__ == '__main__':
    try:
        #Testing our function
	print('welcome to draw_numbers programm!')
	string=input("Write your number ")
        velocity_publisher_f(string)
    except rospy.ROSInterruptException: pass
