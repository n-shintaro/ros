#!/usr/bin/env python
import rospy
import random
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import WheelDropEvent
class Kobuki():
    def __init__(self):
        self.vel_x = rospy.get_param('~vel_x', 0.2)
        self.vel_rot = rospy.get_param('~vel_rot',0.5)
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        rospy.init_node("kobuki3")
        self.sub_bumper = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.bumperevent_callback,queue_size=1)
        self.sub_wheel = rospy.Subscriber('/mobile_base/events/wheel_drop', WheelDropEvent,self.wheel_drop_callback,queue_size=1)
        self.bump=0
        self.stopa=0
        self.count=0
    def controller(self):
        r = rospy.Rate(10.0)
        ran=random.randrange(50, 100)
	print(ran)
	while not rospy.is_shutdown():
	    vel = Twist()
	    if self.bump==1 and self.stopa==0 and self.count<20:
	    		vel.linear.x=-0.1
	    		self.count=self.count+1
	    elif self.bump==1 and self.stopa==0 and self.count>=20 and self.count<ran:
	                vel.angular.z=0.5
	                self.count=self.count+1
	    elif self.stopa==1:
	    		vel.linear.x=0
	    		#print('wheel up')
	    elif self.count==ran:
	    		self.bump=0
	    		self.count=0
	    else:
 	    		vel.linear.x =self.vel_x
	        	# print('nothing')
	    self.pub.publish(vel)
	    r.sleep()
    #bumper ivent
    def bumperevent_callback(self,bumper):
        print(bumper)
        self.bump=1
        self.stopa=0
        self.count=0
                #print(vel)
    def wheel_drop_callback(self,wheel_drop):
        stop_vel= Twist()
        self.stopa=1
if __name__=="__main__":
    rospy.init_node('kobuki3')
    kobuki=Kobuki()
    kobuki.controller()
