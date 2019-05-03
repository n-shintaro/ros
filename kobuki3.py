#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import WheelDropEvent
class Kobuki():
    def __init__(self):
        self.vel_x = rospy.get_param('~vel_x', 0.2)
        self.vel_rot = rospy.get_param('~vel_rot',0.5)
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
        rospy.init_node("kobuki3")
        self.sub_bumper = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, self.callback,queue_size=1)
        self.sub_wheel = rospy.Subscriber('/mobile_base/events/wheel_drop', WheelDropEvent,self.stop,queue_size=1)
        self.bump=0
        self.stopa=0
        self.count=0
    #bumper ivent
    def callback(self,bumper):
        print(self.bump)
        self.bump=0
        self.stopa=0
        self.count=0
        while not rospy.is_shutdown(): 
		vel = Twist()
        	#print(vel)
        	#r = rospy.Rate(10.0)
        	#for i in range(10):
        	if self.bump==0 and self.stopa==0 and self.count<10000:
            		vel.angular.z=-0.5
            		self.count=self.count+1
        	elif self.stopa==1:
            		vel.linear.x=0
            		#print('wheel up')
        	elif self.count==10000:
            		self.bump=1
            		self.count=0
                elif self.bump==1:
 	    		vel.linear.x =self.vel_x
                	# print('nothing')
                self.pub.publish(vel)
    def stop(self,heel_drop):
        stop_vel= Twist()
        self.stopa=1
if __name__=="__main__":
    rospy.init_node('kobuki3')
    kobuki=Kobuki()
    rospy.spin()
