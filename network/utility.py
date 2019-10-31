import subprocess, time, logging


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