from network.interface import *
from network.listener import *
from network.nodediscovery import *
import sys


class NetworkManager:

	def __init__(self):
		self.macAddress = ""
		self.net = NetworkInterface()
		self.nodeList = set()
		self.isRunning = False
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
		self.nodeDiscovery = NodeDiscovery(self.nodeList, self.eventListener)
		self.nodeDiscovery.start()

	def disconnect(self):
		self.net.disconnectAdHoc()