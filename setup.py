from GUI_ALL.data_class import *
from GUI_ALL.data_class_eiei import *

from database.database import DB

from entities.message import *
from entities.node import *
from entities.group import *
from entities.request import *
from network.NetworkManager import *
from services.EventHandler import EventHandler

DB.destroy_table()
DB.init_table()

net = NetworkManager()
# net.connect()
mac = net.getMacAddress()
ev = EventHandler(net)
net.addListener(ev)
# start listener
net.startListener()
# start node discovery service
net.startNodeDiscovery()

current_user = user()
all_group = all_group()
