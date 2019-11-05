from network.utility import *
import re, time, logging

class NetworkInterface:
	def __init__(self):
		self.interface = self.autoFindInterface()
		self.interfaceMac = self.getInterfaceMac()
		logger.info(f"Mac address of interface: {self.interfaceMac}")
		self.oldChannel = "auto"
		self.oldEssid = "ChulaWiFi"
		self.oldMode = "Managed"

	def autoFindInterface(self):
		interfaces = self.getAvailableInterface()
		interface = interfaces[0][0]
		logger.info(f"Selecting {interface} as primary interface...")
		return interface

	def getAvailableInterface(self):
		result = run("iwconfig")
		match = re.findall(".+\s+IEEE\s+802.11", result)
		returnList = []
		for s in match:
			part = s.split()
			returnList.append((part[0], part[2]))
		return returnList

	def getIw(self, type, name=None):
		name = self.checkDefaultInterface(name)
		result = run(f"iwconfig {name}")
		match = re.findall(r"\S+:\s?\S+", result)
		if match is not None:
			keyDict = dict()
			for s in match:
				key, val = s.split(":", maxsplit=1)
				keyDict[key.lower()] = stripQuote(val.strip())
			if type in keyDict:
				return keyDict[type]
			elif type == "channel":
				return channelMap[keyDict["frequency"]]
			else:
				logger.error("Property not present error")
		else:
			logger.error("Interface not found error")

	def setInterfaceProperty(self, property, value, interface=None, validate=True):
		interface = self.checkDefaultInterface(interface)
		cmd = f"iwconfig {interface} {property} {value}"
		result=run(cmd)
		if not validate or checkAndWait(self.getIw, [property, interface], value, normalize=True):
			logger.info(f"Setting {property} property of interface {interface} to {value} is successful")
			return True
		else:
			logger.error(f"Setting {property} property of interface {interface} error")
			return False

	def setInterfaceEssid(self, essid="CUWIRELESS", name=None):
		if self.interfaceStatus(name) != "DOWN":
			logger.error("Cannot set interface property while the interface is active")
			return False
		name = self.checkDefaultInterface(name)
		return self.setInterfaceProperty("essid", essid, name)

	def setInterfaceMode(self, mode, name=None):
		if self.interfaceStatus(name) != "DOWN":
			logger.error("Cannot set interface property while the interface is active")
			return False
		name = self.checkDefaultInterface(name)
		return self.setInterfaceProperty("mode", mode, name)

	def setInterfaceChannel(self, channel="auto", name=None):
		if self.interfaceStatus(name) != "DOWN":
			logger.error("Cannot set interface property while the interface is active")
			return False
		name = self.checkDefaultInterface(name)
		validate = False if channel == "auto" else True
		return self.setInterfaceProperty("channel", channel, name, validate)

	def saveInterfaceSetting(self):
		logger.info("Saving interface setting...")
		self.oldMode = self.getIw("mode")
#		self.oldChannel = self.getIw("channel")
		self.oldEssid = self.getIw("essid")

	def getIp(self, type, name=None):
		name = self.checkDefaultInterface(name)
		result = run(f"ip a s {name}")
		match = re.search(f"{type} \S+", result)
		if match is not None:
			status = match.group(0).split()[1].strip()
			return status
		else:
			logger.error("Interface not found error")

	def getInterfaceMac(self, name=None):
		name = self.checkDefaultInterface(name)
		return self.getIp("link/ether", name)

	def interfaceStatus(self, name=None):
		return self.getIp("state", name)

	def interfaceIP4(self, name=None):
		result = self.getIp("inet", name)
		if result is None:
			logger.error("Fail in obtaining IPV4")
			return False
		ip, subnet = result.split("/")
		return ip, subnet

	def interfaceIP6(self, name=None):
		result = self.getIp("inet6", name)
		if result is None:
			logger.error("Fail in obtaining IPV6")
			return False
		ip, subnet = result.split("/")
		return ip, subnet

	def interfaceDown(self, name=None):
		name = self.checkDefaultInterface(name)
		cmd = f"ip link set {name} down"
		result=run(cmd)
		if checkAndWait(self.interfaceStatus, [name], "DOWN"):
			logger.info(f"Turned off interface {name} successfully")
			return True
		else:
			logger.error("Turning off interface error")
			return False

	def interfaceUp(self, name=None):
		name = self.checkDefaultInterface(name)
		cmd = f"ip link set {name} up"
		result=run(cmd)
		if checkAndWait(self.interfaceStatus, [name], "UP", tries=60, interval=1):
			logger.info(f"Turned on interface {name} successfully")
			return True
		else:
			logger.error("Turning on interface error")
			return False

	def checkDefaultInterface(self, name):
		if name is None:
			if self.interface is not None:
				return self.interface
			else:
				logger.error("Interface not specify; must throw exception in the future")
				return
		return name

	def turnNetworkManagerOff(self):
		run("systemctl stop NetworkManager.service")
		time.sleep(5)

	def turnNetworkManagerOn(self):
		run("systemctl start NetworkManager.service")
		time.sleep(5)

	def connectAdHoc(self):
		self.saveInterfaceSetting()
		self.turnNetworkManagerOff()
		self.interfaceDown()
		self.setInterfaceMode("ad-hoc")
		self.setInterfaceChannel("auto")
		self.setInterfaceEssid()
		self.interfaceUp()
		if waitUntilChange(self.getIw, ["cell"], ["Not-Associated"], tries=50, interval=0.5, normalize=True):
			cell = self.getIw("cell")
			logger.info(f"Successfully connected to ad-hoc network; cell:{cell}")
		else:
			logger.warning("Cannot obtain cell in the specified time")
		return cell

	def disconnectAdHoc(self):
		self.interfaceDown()
		self.setInterfaceMode(self.oldMode)
		self.setInterfaceChannel(self.oldChannel)
		self.setInterfaceEssid(self.oldEssid)
		self.interfaceUp()
		logger.info("Turning on network manager...")
		self.turnNetworkManagerOn()
		logger.info("Successfully disconnected from ad-hoc network")


logger = logging.getLogger('Interface')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

