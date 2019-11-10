from network.utility import *
from entities.message import *
from entities.node import *
from entities.group import *
from entities.request import *
import threading
import selectors
import json
import io
import struct
import socket

from services.user import UserService


class ListenerMessage:
    def __init__(self, selector, sock, addr, eventListener, info):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.eventListener = eventListener
        self._recv_buffer = b""
        self._send_buffer = b""
        self.header = None
        self.info = info
        self.request = None
        self.response_created = False

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
#				logger.debug(f"Add {data} to buffer")
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def createNodeReplyMessage(self):
        self.info = UserService.infoBroadcast()
        contentJson = json.dumps(self.info)
        contentByte = contentJson.encode("utf-8")
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
            "nodeRq": False,
            "big": False,
            "nodeRep": True,
            "contentLength": len(contentByte),
        }
        messageHeader = packHeader(header)
        message = messageHeader + contentByte
        return message

    def processEvents(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self.header is None:
            self.processHeader()

        if self.header:
            if self.request is None and self.header["contentLength"] > 0:
                self.processRequest()

        self.processData()

    def write(self):
        if self.request:
            if not self.response_created:
                self.createNodeReply()

        self._write()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def processHeader(self):
        hdrlen = 26
        logger.debug(f"Processing header")
        if len(self._recv_buffer) >= hdrlen:
            self.header = unpackHeader(self._recv_buffer[:hdrlen])
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                    "srcUsername",
                    "srcGroup",
                    "desGroup",
                    "contentLength",
                    "admin",
                    "member",
                    "broadcast",
                    "groupBroadcast",
                    "memberRq",
                    "leaveRq",
                    "ackRq",
                    "denyRq",
                    "big",
                    "nodeRq",
                    "nodeRep",
            ):
                if reqhdr not in self.header:
                    raise ValueError(f'Missing required header "{reqhdr}".')
        logger.info(f"Got header {self.header}")

    def processRequest(self):
        contentLength = self.header["contentLength"]
        if not len(self._recv_buffer) >= contentLength:
            return
        data = self._recv_buffer[:contentLength]
        self._recv_buffer = self._recv_buffer[contentLength:]
        self.request = json.loads(data.decode("utf-8"))
        print("received request", repr(self.request), "from", self.addr)

    def processData(self):
        print("processing request...")
        if self.header["nodeRq"]:
            self._set_selector_events_mask("w")
            self.createNodeReply()
        else:
            self.close()

    def createNodeReply(self):
        message = self.createNodeReplyMessage()
        self.response_created = True
        self._send_buffer += message


logger = logging.getLogger('MessageProcessor')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class UDPListenerMessage (threading.Thread):
    def __init__(self, data, addr, eventListener, info, packetSet, networkManager):
        threading.Thread.__init__(self)
        self.addr = addr
        self.eventListener = eventListener
        self._recv_buffer = data
        self.header = None
        self.request = None
        self.info = info
        self.packetSet = packetSet
        self.nodeMap = networkManager.nodeMap
        self.reverseMap = networkManager.reverseMap

    def processHeader(self):
        hdrlen = 26
        logger.debug(f"Processing header")
        if len(self._recv_buffer) >= hdrlen:
            self.header = unpackHeader(self._recv_buffer[:hdrlen])
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                    "srcUsername",
                    "srcGroup",
                    "desGroup",
                    "contentLength",
                    "admin",
                    "member",
                    "broadcast",
                    "groupBroadcast",
                    "memberRq",
                    "leaveRq",
                    "ackRq",
                    "denyRq",
                    "big",
                    "nodeRq",
                    "nodeRep",
            ):
                if reqhdr not in self.header:
                    raise ValueError(f'Missing required header "{reqhdr}".')
        logger.info(f"Got header {self.header}")

    def processRequest(self):
        contentLength = self.header["contentLength"]
        if not len(self._recv_buffer) >= contentLength:
            return
        data = self._recv_buffer[:contentLength]
        self._recv_buffer = self._recv_buffer[contentLength:]
        self.request = json.loads(data.decode("utf-8"))
        logger.debug(f"received request {self.request} from {self.addr}")

    def processData(self):
        print("processing request...")
        # handling broadcast message
        self.info = UserService.infoBroadcast()
        if self.header["broadcast"]:
            if self.header["groupBroadcast"]:
                if self.info.get("groupID", "") == self.header["srcGroup"][4:]:
                    msg = GroupMessage(
                        self.header["srcUsername"], self.header["srcGroup"][4:], self.request)
                    self.eventListener.receiveMessageGroup(msg)
                else:
                    print(
                        f"The sender is from group {self.header['srcGroup']}, but this node is in group {self.info.get('groupID','')}")
                    print("Drop request; not from the same group")
            elif self.header["memberRq"]:
                if self.header["desGroup"][4:] == self.info.get("groupID", "") and self.info.get("role", "") == "admin":
                    req = Request(
                        self.header["srcUsername"], self.header["desGroup"][4:])
                    self.eventListener.receiveGroupJoinRequest(req)
                print(self.header['desGroup'][4:], self.info.get(
                    'groupID', ''), self.info.get('role', ''))
            elif self.header["nodeRep"]:
                groupInfo = GroupBroadcast(self.request)
                if self.addr not in self.nodeMap:
                    # This is new node
                    createdNode = Node(self.addr, self.request)
                    self.eventListener.nodeJoin(createdNode)
                    self.nodeMap[self.addr] = self.request
                    self.reverseMap[self.request["username"]] = self.addr
                self.eventListener.receiveGroupBroadcast(groupInfo)
            else:
                msg = BroadcastMessage(
                    self.header["srcUsername"], self.request)
                self.eventListener.receiveMessageBroadcast(msg)
        elif self.header["ackRq"]:
            self.eventListener.receiveJoinOK(self.header["srcGroup"][4:])
        elif self.header["denyRq"]:
            self.eventListener.receiveJoinDeny(self.header["srcGroup"][4:])
        else:
            # personal message
            msg = Message(self.header["srcUsername"], self.info.get(
                "username", ""), self.request)
            self.eventListener.receiveMessage(msg)

    def run(self):
        packetHash = self._recv_buffer[:32]
        if packetHash in self.packetSet:
            return
        self.packetSet.add(packetHash)
        self._recv_buffer = self._recv_buffer[32:]
        if self.header is None:
            self.processHeader()

        if self.header:
            if self.request is None and self.header["contentLength"] > 0:
                self.processRequest()

        self.processData()
