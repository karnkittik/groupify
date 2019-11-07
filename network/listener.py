import sys, threading, logging
import socket
import selectors
import traceback
from  network.message import ListenerMessage

class Listener(threading.Thread):

	def __init__(self, eventHandler, networkManager):
		threading.Thread.__init__(self)
		self.sel = selectors.DefaultSelector()
		self.host = "0.0.0.0"
		self.port = 8421
		self.net = networkManager
		self.eventHandler = eventHandler
		self.lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
		self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.lsock.bind((self.host, self.port))


	def accept_wrapper(self, sock):
		conn, addr = sock.accept()  # Should be ready to read
		logger.info(f"accepted connection from {addr}")
		conn.setblocking(False)
		message = ListenerMessage(self.sel, conn, addr, self.eventHandler)
		self.sel.register(conn, selectors.EVENT_READ, data=message)


	def run(self):
		self.lsock.listen()
		logger.info(f"listening on {self.host} {self.port}")
		self.lsock.setblocking(False)
		self.sel.register(self.lsock, selectors.EVENT_READ, data=None)
		while True:
			logger.debug("Start new itteration...")
			if (self.net.isRunning == False):
				logger.info("Server stop...")
				self.sel.close()
				break
			logger.debug("Before select")
			events = self.sel.select(timeout=None)
			logger.debug("After select")
			for key, mask in events:
				if key.data is None:
					self.accept_wrapper(key.fileobj)
				else:
					message = key.data
					try:
						message.processEvents(mask)
					except Exception:
						print("main: error: exception for", f"{message.addr}:\n{traceback.format_exc()}")
						message.close()
		logger.info("Terminating listener thread")

logger = logging.getLogger('Listener')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

