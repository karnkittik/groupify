import threading, time, logging
import requests as rq

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
		

logger = logging.getLogger('NodeDiscovery')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

