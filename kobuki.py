#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import WheelDropEvent
rospy.init_node('kobuki')
vel_x = rospy.get_param('~vel_x', 0.2)
vel_rot = rospy.get_param('~vel_rot',0.2)
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
global stopa
global bump
bump=0
stopa=0
def callback(bumper):
    global bump
    bump=1
    r = rospy.Rate(10.0)
    for i in range(5):
        pub.publish(back_vel)
        r.sleep()
def stop(wheel_drop):
    stop_vel= Twist()
    global stopa
    stopa=1
sub1 = rospy.Subscriber('/mobile_base/events/bumper', BumperEvent, callback,
                       queue_size=1)
sub2 = rospy.Subscriber('/mobile_base/events/wheel_drop', WheelDropEvent, stop,
                       queue_size=1)
while not rospy.is_shutdown():
    vel = Twist()
    #print(vel)
    #r = rospy.Rate(10.0)
    #for i in range(10):
    if bump==1 and stopa==0:
        vel.linear.x=-vel_x
	vel.angular.z=vel_rot
    elif stopa==1:
        vel.linear.x=0
    else:
 	vel.linear.x = vel_x
    pub.publish(vel)
