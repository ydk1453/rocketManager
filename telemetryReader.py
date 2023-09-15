'''
Created on 13 Eyl 2023

@author: yusuf
'''

from threading import Thread
from queue import Queue
import socket


class telemetryReader(Thread):
    queue:Queue
    '''
    classdocs
    '''


    def __init__(self, portNo, ip):
        super(telemetryReader, self).__init__()
        '''
        Constructor
        '''
        self.portNo = portNo
        self.ip = '127.0.0.1'
        self.queue = Queue()
        self.readerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.readerSocket.connect((self.ip, self.portNo))
        
    def run(self):
        
        while True:
            data = self.readerSocket.recv(1024)
            self.queue.put(data) 
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        True