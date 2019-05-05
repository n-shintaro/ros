#!/usr/bin/env python
import rospy
import random
from tf2_msgs.msg import TFMessage
from kobuki_msgs.msg import DockInfraRed
from kobuki_msgs.msg import WheelDropEvent
from geometry_msgs.msg import Twist
class Kobuki():
	def __init__(self):
                self.sub_wheel = rospy.Subscriber('/mobile_base/events/wheel_drop', WheelDropEvent,self.stop,queue_size=1)
		self.sub_dock_ir=rospy.Subscriber('/mobile_base/sensors/dock_ir',DockInfraRed,self.feel,queue_size=1)
		
		self.sub_tf=rospy.Subscriber('/tf',TFMssage,self.tf,queue_size=1)
                self.vel_x = rospy.get_param('~vel_x', 0.2)
        	self.vel_rot = rospy.get_param('~vel_rot',0.5)
		self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
		#rospy.init_node("dockir")	
	def stop(self,wheel_drop):
        	stop_vel= Twist()
        	self.stopa=1
	def feel(self,dockinfrared):
		receivedDataArray = [ord(n) for n in dockinfrared.data]
		vel = Twist()
	        print(receivedDataArray)
                if receivedDataArray[0]==0 and receivedDataArray[1]==0 and receivedDataArray[2]==0:
        	#print(dockinfrared)
                    vel.angular.z=self.vel_rot
            	    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                self.pub.publish(vel)        	
		#print("dockinfrared.data[0]=")
        	#print(dockinfrared.data[0])
        	#print("dockinfrared.data[1]=")i
        def tf(self,tf):
            print(tf)
if __name__=="__main__":
    rospy.init_node('kobuki3')
    kobuki=Kobuki()
    rospy.spin()
