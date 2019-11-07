from network.interface import *
from network.sender import *
from network.listener import *
from network.nodediscovery import *
import sys


class NetworkManager:

	def __init__(self):
		self.macAddress = ""
		self.net = NetworkInterface()
		self.nodeList = set()
		self.selfInfo = mocSelf()
		self.nodeMap = dict()
		self.reverseMap = dict()
		self.isRunning = False
		self.sender = Sender(self.reverseMap, self.info)
		self.eventListener = None

	def connect(self):
		self.net.connectAdHoc()
		self.macAddress = self.net.getInterfaceMac()
		return self.macAddress

	def addListener(self, eventListener):
		self.eventListener = eventListener

	def startListener(self):
		self.listener = Listener(self.eventListener, self)
		self.isRunning = True
		self.listener.start()

	def startNodeDiscovery(self):
		self.nodeDiscovery = NodeDiscovery(self.nodeList, self.nodeMap, self.reverseMap, self.eventListener, self.sender, self.selfInfo)
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

	def disconnect(self):
		self.net.disconnectAdHoc()
