#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from kobuki_msgs.msg import BumperEvent
from kobuki_msgs.msg import WheelDropEvent
rospy.init_node('kobuki')
vel_x = rospy.get_param('~vel_x', 0.2)
vel_rot = rospy.get_param('~vel_rot',0.5)
pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
global stopa
global bump
global count
count=0
bump=0
stopa=0
def callback(bumper):
    back_vel=Twist()
    back_vel.angular.z=vel_rot
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
    if bump==1 and stopa==0 and count<10:
        vel.angular.z=-0.5
        print vel
        count=count+1
    elif stopa==1:
        vel.linear.x=0
    else:
 	vel.linear.x = vel_x
    pub.publish(vel)
