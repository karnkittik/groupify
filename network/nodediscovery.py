from entities.node import Node
import threading
import time
import logging
import requests as rq
import socket
import json
from network.utility import *
from services.EventHandler import *
from services.user import UserService


class NodeDiscovery (threading.Thread):

    def __init__(self, nodeList, nodeMap, reverseMap, eventListener, sender, info):
        threading.Thread.__init__(self)
        self.nodeList = nodeList
        self.nodeMap = nodeMap
        self.reverseMap = reverseMap
        self.sender = sender
        self.eventListener = eventListener
        self.info = info

    def getAllNode(self):
        logger.info("Retreaving nodes...")
        url = "http://localhost:1980/telnet/olsrv2info node"
        res = rq.get(url)
        if res.status_code != 200:
            print("Error in getting node from OLSR")
        text = res.content.decode("utf-8").strip()
        nodes = [[x for x in y.split("\t")] for y in text.split("\n")]
        res = [x[0] for x in nodes if (x[0] != '' and ':' not in x[0])]
        logger.info(f"Found following node: {res}")
        return set(res)

    def run(self):
        while True:
            nodes = self.getAllNode()
            addedNode, deletedNode = self.diffNode(nodes)
            self.nodeList = nodes
#			logger.debug(f"Add node: {addedNode}, deleted node: {deletedNode}")
#			logger.debug(f"Len node {len(nodes)}, add node {len(addedNode)}, deleted node {len(deletedNode)}")
            nodeInfo = self.probeNode(addedNode)
            for (ip, info) in nodeInfo:
                # createdNode = Node(ip, info["username"], info["firstname"], info["lastname"],
                #                    info["faculty"], info["year"], info["groupID"], info)
                createdNode = Node(ip, info)
                self.eventListener.nodeJoin(createdNode)
                self.nodeMap[ip] = info
                self.reverseMap[info["username"]] = ip
            for ip in deletedNode:
                if ip in self.nodeMap:
                    info = self.nodeMap.get(ip)
                    # createdNode = Node(ip,info["username"],info["firstname"],info["lastname"],info["faculty"],info["year"],info["group_id"],info)
                    createdNode = Node(ip, info)
                    self.eventListener.nodeLeave(createdNode)
                    self.nodeMap.pop(ip)
                    self.reverseMap.pop(info["username"])
            self.info = UserService.infoBroadcast()
            self.sender.sendGroupBroadcast()
            time.sleep(10)

    def probeNode(self, nodeList):
        num = len(nodeList)
        threadList = [None]*num
        result = [None]*num
        for i, j in enumerate(nodeList):
            threadList[i] = NodeWorker(j, result, i, self.info)
            threadList[i].start()

        for thread in threadList:
            thread.join()
        return result

    def diffNode(self, nodeList):
        oldNode = set(self.nodeList)
        processNode = set(self.nodeList)
        newNode = set(nodeList)
        for node in processNode:
            if node in newNode:
                oldNode.remove(node)
                newNode.remove(node)
        # oldNode contains node seen previously, but can't be seen now = leave node
        # newNode contains node haven't seen previously, but is being seen now = enter node
        return (newNode, oldNode)


class NodeWorker(threading.Thread):

    def __init__(self, addr, resultList, index, info):
        threading.Thread.__init__(self)
        self.addr = addr
        self.resultList = resultList
        self.index = index
        self.sock = None
        self.info = info

    def createNodeRequest(self):
        header = {
            "srcUsername": self.info.get("username", ""),
            "srcGroup": self.info.get("groupID", ""),
            "desGroup": "",
            "admin": self.info.get("isAdmin", ""),
            "member": self.info.get("isMember", ""),
            "broadcast": False,
            "groupBroadcast": False,
            "memberRq": False,
            "ackRq": False,
            "denyRq": False,
            "leaveRq": False,
            "nodeRq": True,
            "big": False,
            "nodeRep": False,
            "contentLength": 0,
        }
        return packHeader(header)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sendMsg = self.createNodeRequest()
        iAttempt = 1
        while True:
            logger.debug(
                f"On thread #{threading.get_ident()}, connection attempt #{iAttempt}")
            try:
                self.sock.connect((self.addr, 8421))
            except OSError as e:
                iAttempt += 1
                continue
            break
        self.sock.sendall(sendMsg)
        logger.debug("Send complete")
        headerByte = self.sock.recv(26)
        header = unpackHeader(headerByte)
        msgLength = header["contentLength"]
        recvByte = b""
        recvLength = 0
        while recvLength < msgLength:
            tempByte = self.sock.recv(4096)
            recvLength += len(tempByte)
            recvByte += tempByte
        data = json.loads(recvByte.decode("utf-8"))
        logger.info(f"Recieve node reply {data}")
        self.resultList[self.index] = (self.addr, data)
        self.sock.close()


logger = logging.getLogger('NodeDiscovery')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
