import subprocess, time, logging, struct
from bitarray import bitarray


logger = logging.getLogger('adhoc.utility')
channelMap = {
"2.412":"1",
"2.417":"2",
"2.422":"3",
"2.427":"4",
"2.432":"5",
"2.437":"6",
"2.442":"7",
"2.447":"8",
"2.452":"9",
"2.457":"10",
"2.462":"11",
"2.467":"12",
"2.472":"13",
"2.484":"14"}

def run(cmd):
	result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
	return result.stdout.decode("utf-8")

def checkAndWait(function, argument, expected, tries=10, interval=0.3, normalize=False):
	while tries > 0:
		result = function(*argument)
		if normalize == True:
			result = result.lower()
			expected = expected.lower()
		if result == expected:
			return True
		else:
			time.sleep(interval)
			logger.debug(f"tries={tries}")
			tries -= 1
	return False

def waitUntilChange(function, argument, waitFor, tries=10, interval=0.3, normalize=False):
	while tries > 0:
		result = function(*argument)
		if normalize == True:
			result = result.lower()
			waitFor = [x.lower() for x in waitFor]
		if result not in waitFor:
			return True
		else:
			time.sleep(interval)
			logger.debug(f"tries={tries}")
			tries -= 1
	return False

def stripQuote(input):
	first = input[0]
	last = input[-1]
	quote = ["'", "\""]
	if first == last and first in quote:
		return input[1:-1]
	else:
		return input

def macToUserId(mac):
	mac = mac.replace(":")
	return mac.upper()

def unpackHeader(data):
	header = dict()
	pattern = "6x8x8xH2x"
	contentLength = struct.unpack(pattern, data)
	header["srcUsername"] = data[4:10].hex()
	header["srcGroup"] = data[10:18].hex()
	header["desGroup"] = data[18:26].hex()
	header["contentLength"] = contentLength
	flags = data[28:]
	bit = bitarray()
	bit.frombytes(flags)
	header["admin"] = bit[0]
	header["member"] = bit[1]
	header["broadcast"] = bit[2]
	header["groupBroadcast"] = bit[3]
	header["memberRq"] = bit[4]
	header["leaveRq"] = bit[5]
	header["ackRq"] = bit[6]
	header["denyRq"] = bit[7]
	header["big"] = bit[8]
	header["nodeRq"] = bit[9]
	header["nodeRep"] = bit[10]
	return header

def packHeader(header):
	data = bytes()
	data += bytes.fromhex(header["srcUsername"].zfill(12))
	data += bytes.fromhex(header["srcGroup"].zfill(16))
	data += bytes.fromhex(header["desGroup"].zfill(16))
	data += struct.pack("H", header["contentLength"])
	bit = bitarray(16)
	bit.setall(0)
	bit[0] = header["admin"]
	bit[1] = header["member"]
	bit[2] = header["broadcast"]
	bit[3] = header["groupBroadcast"]
	bit[4] = header["memberRq"]
	bit[5] = header["leaveRq"]
	bit[6] = header["ackRq"]
	bit[7] = header["denyRq"]
	bit[8] = header["big"]
	bit[9] = header["nodeRq"]
	bit[10] = header["nodeRep"]
	data += bit.tobytes()
	return data


def mocSelf():
	d = {"username":"AABBCCDDEEFF",
"groupID":"FFFFAABBCCDDEEFF",
"role":"admin",
"isAdmin":True,
"isMember":True,
"firstname":"Pawin",
"lastname":"Piemthai",
"faculty":"Engineering",
"year":4}
	return d