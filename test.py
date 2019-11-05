from network.NetworkManager import *
from services.EventHandler import EventHandler

net = NetworkManager()
ev = EventHandler()
net.addListener(ev)