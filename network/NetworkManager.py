from network.interface import *
from network.sender import *
from network.udpListener import *
from network.listener import *
from network.nodediscovery import *
import sys

from services.user import UserService


class NetworkManager:

    def __init__(self):
        self.net = NetworkInterface()
        UserService.initMe(self.net.getInterfaceMac(), '', '', '', 1)
        self.macAddress = self.net.getInterfaceMac()
        self.nodeList = set()
        # self.selfInfo = mocSelf()
        self.selfInfo = UserService.infoBroadcast()
        self.nodeMap = dict()
        self.packetSet = set()
        self.reverseMap = dict()
        self.isRunning = False
        self.sender = Sender(self.reverseMap, self.selfInfo)
        self.eventListener = None

    def getMacAddress(self):
        return self.macAddress

    def connect(self):
        self.net.connectAdHoc()
        self.macAddress = self.net.getInterfaceMac()
        return self.macAddress

    def addListener(self, eventListener):
        self.eventListener = eventListener

    def startListener(self):
        self.listener = Listener(self.eventListener, self)
        self.udpListener = UDPListener(self.eventListener, self)
        self.isRunning = True
        self.listener.start()
        self.udpListener.start()

    def startNodeDiscovery(self):
        self.nodeDiscovery = NodeDiscovery(
            self.nodeList, self.nodeMap, self.reverseMap, self.eventListener, self.sender, self.selfInfo)
        self.nodeDiscovery.start()

    def sendMessage(self, message):
        self.sender.sendMessage(message)

    def sendMessageBroadcast(self, message):
        self.sender.sendMessageBroadcast(message)

    def sendMessageGroup(self, message):
        self.sender.sendMessageGroup(message)

    def sendGroupJoinRequest(self, request):
        self.sender.sendGroupJoinRequest(request)

    def sendGroupAcknowledgeRequest(self, request):
        self.sender.sendGroupAcknowledgeRequest(request)

    def sendGroupDenyRequest(self, request):
        self.sender.sendGroupDenyRequest(request)

    def stop(self):
        self.isRunning = False
        self.listener.join()
        self.udpListener.join()
        logger.info("Gracefully stop")

    def disconnect(self):
        self.net.disconnectAdHoc()
