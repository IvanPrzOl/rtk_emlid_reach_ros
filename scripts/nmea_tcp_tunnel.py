#!/usr/bin/env python

import rospy
import re
import sys
from nmea_msgs.msg import Sentence
from TcpGate import TcpSerialDataGateway

class nmea_tunnel(object):
    def __init__(self):
        self._tunnel_pub = rospy.Publisher('nmea_sentence',Sentence,queue_size=20)
        rospy.init_node('nmea_tcp_tunnel')
        host = rospy.get_param("~host","192.168.42.1")
        port = rospy.get_param("~port",9001)

        self._tcpGate = TcpSerialDataGateway(host,port,self._inDataHandler)
        
    def Start(self):
        self._tcpGate.start()
    def Stop(self):
        self._tcpGate.stop()
    def _inDataHandler(self,inData):
        try:
            # to do: contruct and send nmea sentences
            sentence = Sentence()
            sentence.header.stamp = rospy.Time.now()
            sentence.sentence = inData
            self._tunnel_pub.publish(sentence)
        except:
            rospy.logwarn("Unexpected error:" + str(sys.exc_info()[0]))

if __name__ == '__main__':
    tunnel_node = nmea_tunnel()
    try:
        tunnel_node.Start()
        rospy.spin()
    except rospy.ROSInterrupException:
        tunnel_node.Stop()
