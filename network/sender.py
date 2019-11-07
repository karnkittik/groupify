from network.utility import *
from entities.message import *
from entities.node import *
from entities.group import *
from entities.request import *
import sys
import threading, time, logging
import json
import io
import struct
import socket

class Sender:

	def __init__(self, reverseMap, info):
		self.reverseMap = reverseMap
		self.info = info

	def sendMessage(self, message):
		data = {"timestamp":message.timestamp, "message":message.message}
		body = json.dumps(data).encode('utf-8')
		header = {
		"srcUsername":message.fromUsername,
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
		"nodeRq":False,
		"big":False,
		"nodeRep":False,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		addr = self.reverseMap.get(message.toUsername)
		worker = SenderWorker(addr, msg)
		worker.start()

	def sendMessageBroadcast(self, message):
		data = {"timestamp":message.timestamp, "message":message.message}
		body = json.dumps(data).encode('utf-8')
		header = {
		"srcUsername":message.fromUsername,
		"srcGroup":self.info.get("groupID",""),
		"desGroup":"",
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":True,
		"groupBroadcast":False,
		"memberRq":False,
		"ackRq":False,
		"denyRq":False,
		"leaveRq":False,
		"nodeRq":False,
		"big":False,
		"nodeRep":False,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		for addr in self.reverseMap.values():
			worker = SenderWorker(addr, msg)
			worker.start()

	def sendMessageGroup(self, message):
		data = {"timestamp":message.timestamp, "message":message.message}
		body = json.dumps(data).encode('utf-8')
		header = {
		"srcUsername":message.fromUsername,
		"srcGroup":message.groupID,
		"desGroup":"",
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":True,
		"groupBroadcast":True,
		"memberRq":False,
		"ackRq":False,
		"denyRq":False,
		"leaveRq":False,
		"nodeRq":False,
		"big":False,
		"nodeRep":False,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		for addr in self.reverseMap.values():
			worker = SenderWorker(addr, msg)
			worker.start()

	def sendGroupJoinRequest(self, request):
		data = {"message":request.message}
		body = json.dumps(data).encode('utf-8')
		header = {
		"srcUsername":request.fromUsername,
		"srcGroup":self.info["groupID"],
		"desGroup":request.groupID,
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":Ttrue,
		"groupBroadcast":False,
		"memberRq":True,
		"ackRq":False,
		"denyRq":False,
		"leaveRq":False,
		"nodeRq":False,
		"big":False,
		"nodeRep":False,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		for addr in self.reverseMap.values():
			worker = SenderWorker(addr, msg)
			worker.start()

	def sendGroupAcknowledgeRequest(self, request):
		body = b""
		header = {
		"srcUsername":self.info["username"],
		"srcGroup":self.info["groupID"],
		"desGroup":"",
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":False,
		"groupBroadcast":False,
		"memberRq":False,
		"ackRq":True,
		"denyRq":False,
		"leaveRq":False,
		"nodeRq":False,
		"big":False,
		"nodeRep":False,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		addr = self.reverseMap.get(request.fromUsername)
		worker = SenderWorker(addr, msg)
		worker.start()

	def sendGroupDenyRequest(self, request):
		body = b""
		header = {
		"srcUsername":self.info["username"],
		"srcGroup":self.info["groupID"],
		"desGroup":"",
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":False,
		"groupBroadcast":False,
		"memberRq":False,
		"ackRq":False,
		"denyRq":True,
		"leaveRq":False,
		"nodeRq":False,
		"big":False,
		"nodeRep":False,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		addr = self.reverseMap.get(request.fromUsername)
		worker = SenderWorker(addr, msg)
		worker.start()

	def sendGroupBroadcast(self):
		data = self.info
		body = json.dumps(data).encode('utf-8')
		header = {
		"srcUsername":self.info["username"],
		"srcGroup":self.info["groupID"],
		"desGroup":"",
		"admin":self.info.get("isAdmin",""),
		"member":self.info.get("isMember",""),
		"broadcast":True,
		"groupBroadcast":False,
		"memberRq":False,
		"ackRq":False,
		"denyRq":False,
		"leaveRq":False,
		"nodeRq":False,
		"big":False,
		"nodeRep":True,
		"contentLength": len(body),
		}
		packedHeader = packHeader(header)
		msg = packedHeader + body
		for addr in self.reverseMap.values():
			worker = SenderWorker(addr, msg)
			worker.start()



class SenderWorker(threading.Thread):

	def __init__(self, addr, msg):
		threading.Thread.__init__(self)
		self.addr = addr
		self.msg = msg
		self.sock = None

	def run(self):
		self.sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		iAttempt = 1
		while True:
			logger.debug(f"On thread #{threading.get_ident()}, connection attempt #{iAttempt}")
			try:
				self.sock.connect((self.addr, 8421))
			except OSError as e:
				iAttempt += 1
				continue
			break
		self.sock.sendall(sendMsg)
		logger.debug("Send complete")
		self.sock.close()