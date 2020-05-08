#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen
speed=2
PI = 3.1415926535897

#strting a new node for publisher
velocity_publisher = rospy.Publisher("turtle1/cmd_vel", Twist, queue_size=10)
rospy.init_node('velocity_publisher', anonymous = False)

rospy.wait_for_service("turtle1/set_pen")
setpen = rospy.ServiceProxy("turtle1/set_pen", SetPen)
#res = setpen(255, 255, 255, 4, switch)
vel_msg = Twist()

def pu():
	setpen(255, 255, 255, 3, 1)
#	rospy.spin()
	return

def pd():
	setpen(255, 255, 255, 3, 0)
#	rospy.spin()
	return

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
	while(current_distance < distance-0.1):
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
	return 

def r(angle):
	print('rotating on '+ str(angle))
	#Converting from angles to radians
	angular_speed = speed*2*PI/72
	relative_angle = abs(angle*2*PI/360)

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
	current_angle = 1*2*PI/360

	while(current_angle < relative_angle):
		velocity_publisher.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)

	#Forcing our robot to stop
	vel_msg.angular.z = 0
	velocity_publisher.publish(vel_msg)
	#rospy.spin()
	return 

def zero():
	print('drawing zero...')
	r(-90); f(2); r(90); f(1)
	r(90); f(2); r(90); f(1)
	r(180);	pu(); f(1.2); pd()
	return

def one():
	print('drawing one...')
	pu(); f(1); r(-90); pd()
	f(2); pu(); r(90); f(0.2)
	r(90); f(2); r(-90); pd()
	return

def two():
	print('drawing two...')
	r(-90); f(1); r(90); f(1)
	r(-90); f(1); r(-90); f(1)
	r(-90); pu(); f(2); r(-90)
	pd(); f(1); pu(); f(0.2); pd()
	return


def three():
	print('drawing three...')	
	for i in range(3):
		f(1); pu(); r(180); f(1)
		r(90); f(1); r(90); pd()
	pu(); f(1); r(90); f(1)
	pd(); f(2); r(-90); pu()
	f(0.2); pd()
	return


def four():
	print('drawing four...')
	pu(); r(-90); f(2); r(180)
	pd(); f(1); r(-90); f(1)
	r(-90); f(1); r(180); f(2)
	pu(); r(-90); f(0.2); pd()
	return


def five():
	print('drawing five...')
	f(1); r(-90); f(1); r(-90)
	f(1); r(90); f(1); r(90)
	f(1); pu(); r(90); f(2)
	r(-90); f(0.2); pd()
	return


def six():
	print('drawing six...')
	f(1); r(-90); f(1); r(-90)
	f(1); r(90); f(1); r(90)
	f(1); r(180); f(1); r(-90)
	f(2); pu(); r(-90); f(1.2);
	pd()
	return


def seven():
	print('drawing seven...')	
	pu(); r(-90); f(2); r(90)
	pd(); f(1); r(90); f(2);
	pu(); r(-90); f(0.2); pd()
	return


def eight():
	print('drawing eight...')
	for i in range(2):
		f(1); r(-90); f(1); r(-90);
		f(1); r(-90); f(1); r(180);
		f(1); r(90)
	pu(); f(1.2); r(90); f(2)
	r(-90); pd()
	return

def nine():
	print('drawing nine...')
	f(1); r(-90); f(2); r(-90)
	f(1); r(-90); f(1); r(-90)
	f(1); pu(); f(0.2); r(90)
	f(1); r(-90); pd()
	return

def draw_number(i):
	print('starting draw number...')
	switcher={
		0: zero,
		1: one,
		2: two,
		3: three,
		4: four,
		5: five,
		6: six,
		7: seven,
		8: eight,
		9: nine
		}
	switcher[i]()
	return

def velocity_publisher_f(string):
        
	while not rospy.is_shutdown():
		for number in string:	
			number=int(number)
			draw_number(number)
			#rospy.spin()
		break
	return

if __name__ == '__main__':
	try:
		#Testing our function
		print('welcome to draw_numbers programm!')
		#r(15);r(-15)
		string=input("Write your number ")
		velocity_publisher_f(string)
	except rospy.ROSInterruptException: pass
