#!/usr/bin/env python

import rospy
import re
import sys
from rtk_emlid_reach.msg import rtklibLLH
from TcpGate import TcpSerialDataGateway

class rtk_node(object):
    def __init__(self):
        self._rtk_pub = rospy.Publisher('rtk',rtklibLLH,queue_size=20)
        rospy.init_node('rtk_node')
        host = rospy.get_param("~host","172.16.55.124")
        port = rospy.get_param("~port",9001)

        self._tcpGate = TcpSerialDataGateway(host,port,self._inDataHandler)
        
    def Start(self):
        self._tcpGate.start()
    def Stop(self):
        self._tcpGate.stop()
    def _inDataHandler(self,inData):
        try:
            splitData = re.split('\s+',inData)
            if (len(splitData) == 15):
                rtkmsg = rtklibLLH()
                rtkmsg.header.stamp = rospy.Time.now()
                rtkmsg.header.frame_id = 'rtk_base'
                rtkmsg.fixDate = splitData[0]
                rtkmsg.fixTime = splitData[1]
                rtkmsg.latitude = float(splitData[2])
                rtkmsg.longitude = float(splitData[3])
                rtkmsg.altitude = float(splitData[4])
                rtkmsg.fixQuality = int(splitData[5])
                rtkmsg.satellites = int(splitData[6])
                rtkmsg.standarDevs = [float(x) for x in splitData[7:13] ]
                rospy.loginfo("cp")
                rtkmsg.age = float(splitData[13])
                rtkmsg.ratio = float(splitData[14])
                
                self._rtk_pub.publish(rtkmsg)
        except:
            rospy.logwarn("Unexpected error:" + str(sys.exc_info()[0]))

if __name__ == '__main__':
    rtkNode = rtk_node()
    try:
        rtkNode.Start()
        rospy.spin()
    except rospy.ROSInterrupException:
        rtkNode.Stop()