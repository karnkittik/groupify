import sys, threading, logging
import socket
import selectors
import traceback
from  network.message import *

class UDPListener(threading.Thread):

	def __init__(self, eventHandler, networkManager):
		threading.Thread.__init__(self)
		self.host = "0.0.0.0"
		self.port = 8421
		self.net = networkManager
		self.eventHandler = eventHandler
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.sock.bind((self.host, self.port))


	def run(self):
		logger.info(f"listening on {self.host} {self.port} UDP")
		while True:
			if (self.net.isRunning == False):
				logger.info("Server stop...")
				self.sock.close()
				break
			data, addr = self.sock.recvfrom(2048)
			if data:
				udpProcess = UDPListenerMessage(data, addr, self.eventHandler, self.net.selfInfo, self.net.packetSet)
				udpProcess.start()

logger = logging.getLogger('UDPListener')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

