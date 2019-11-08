from entities.message import *
from entities.node import *
from entities.group import *
from entities.request import *
from network.NetworkManager import *
from services.MocHandler import MocHandler

net = NetworkManager()
mac = net.getMacAddress()
ev = MocHandler()
net.addListener(ev)
# start listener
#net.startListener()
# start node discovery service
#net.startNodeDiscovery()

msg = Message("FFEEDDCCBBAA", "AABBCCDDEEFF", {
              "timestamp": "2019-11-07 10:10:10", "message": "Hello test test"})
groupMsg = GroupMessage("FFEEDDCCBBAA", "FFFFAABBCCDDEEFF", {
                        "timestamp": "2019-11-07 10:10:10", "message": "Hello test test"})
broadcastMsg = GroupMessage("FFEEDDCCBBAA", {
                            "timestamp": "2019-11-07 10:10:10", "message": "Hello test test"})
req = Request("FFEEDDCCBBAA", "FFFFAABBCCDDEEFF",
              {"message": "Hello test test"})
