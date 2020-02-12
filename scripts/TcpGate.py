#!/usr/bin/env/ python
import socket
import threading
import time
import re
from cStringIO import StringIO

def printData(line):
    #parsed = re.split('\s+',line)
    print line

class TcpSerialDataGateway(object):
    def __init__(self,ip4 = '172.16.55.124',port = 9001, dataHandler = printData):
        self._ip = ip4
        self._port = port
        self._dataHandler = dataHandler
        self._bytesReceived = 0
        self._keepRunning = False

    def start(self):
        try:
            self._sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self._sock.connect((self._ip,self._port))
            print "Connected to %s" % self._ip

            self._keepRunning = True
            self._receiverThread = threading.Thread(target=self._Listen)
            self._receiverThread.setDaemon(True)
            self._receiverThread.start()
        except:
            if self._keepRunning:
                self._sock.close()
            print "Unnable to connect"

    def stop(self):
        if self._keepRunning:
            print "closing connection"
            self._keepRunning = False
            time.sleep(0.1)
            self._sock.close()

    def _Listen(self):
        stringIO = StringIO()
        while self._keepRunning:
            data = self._sock.recv(1)
            if data == '\r' or data == '':
                pass
            if data == '\n' and self._bytesReceived > 0:
                self._dataHandler(stringIO.getvalue())
                stringIO.close()
                stringIO = StringIO()
                self._bytesReceived = 0
            if data == '\n' and self._bytesReceived == 0:
                stringIO.close()
                stringIO = StringIO()
            else:
                stringIO.write(data)
                self._bytesReceived += 1

if __name__ == '__main__':
    dataReceiver = TcpSerialDataGateway(ip4='172.16.55.124',port=9001)
    dataReceiver.start()
    raw_input("Hit <Enter to end")
    dataReceiver.stop()
