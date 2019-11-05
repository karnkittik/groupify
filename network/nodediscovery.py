import threading, time, logging
import requests as rq
import socket, json
from network.utility import *

class NodeDiscovery (threading.Thread):

	def __init__(self, nodeList, eventListener):
		threading.Thread.__init__(self)
		self.nodeList = nodeList
		self.eventListener = eventListener

	def getAllNode(self):
		logger.info("Retreaving nodes...")
		url = "http://localhost:1980/telnet/olsrv2info node"
		res = rq.get(url)
		if res.status_code != 200:
			print("Error in getting node from OLSR")
		text = res.content.decode("utf-8").strip()
		nodes = [[x for x in y.split("\t")] for y in text.split("\n")]
		res = [x[0] for x in nodes]
		logger.info(f"Found following node: {res}")
		return set(res)

	def run(self):
		while True:
			nodes = self.getAllNode()
			addedNode, deletedNode = self.diffNode(nodes)
			self.nodeList = nodes
			logger.debug(f"Add node: {addedNode}, deleted node: {deletedNode}")
			time.sleep(10)

	def diffNode(self, nodeList):
		oldNode = set(self.nodeList)
		newNode = set(nodeList)
		for node in oldNode:
			if node in newNode:
				newNode.remove(node)
		#oldNode contains node seen previously, but can't be seen now = leave node
		#newNode contains node haven't seen previously, but is being seen now = enter node
		return newNode, oldNode
		
class NodeWorker(threading.Thread):

	def __init__(self, addr, resultList, index, info):
		threading.Thread.__init__(self)
		self.addr = addr
		self.resultList = resultList
		self.index = index
		self.sock = None	
		self.ip = socket.gethostbyname(socket.gethostname())
		self.info = info

	def createNodeRequest(self):
		header = {
		"srcIP":self.ip,
		"srcUsername":self.info.get("username", ""),
		"srcGroup":self.info.get("groupID",""),
		"desGroup":"",
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":False,
		"groupBroadcast":False,
		"memberRq":False,
		"ackRq":False,
		"denyRq":False,
		"leaveRq":False,
		"nodeRq":True,
		"big":False,
		"nodeRep":False,
		"contentLength": 0,
		}
		return packHeader(header)

	def run(self):
		self.sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.addr, 8421))
		sendMsg = self.createNodeRequest()
		self.sock.sendall(sendMsg)
		headerByte = self.sock.recv(30)
		header = unpackHeader(headerByte)
		msgLength = header["contentLength"]
		recvByte = b""
		recvLength = 0
		while recvLength < msgLength:
			tempByte = self.sock.recv(2096)
			recvLength += len(tempByte)
			recvByte += tempByte
		data = json.loads(recvByte.decode("utf-8"))
		self.resultList[self.index] = data
		self.sock.close()


logger = logging.getLogger('NodeDiscovery')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

