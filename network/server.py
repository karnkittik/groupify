import sys
import selectors
import json
import io
import struct

class Server:
	def __init__(self, selector, sock, addr, eventListener):
		self.selector = selector
		self.sock = sock
		self.addr = addr
		self.eventListener = eventListener
		self._recv_buffer = b""
		self._send_buffer = b""
		self.header = None
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

	def _json_encode(self, obj, encoding):
		return json.dumps(obj, ensure_ascii=False).encode(encoding)

	def _json_decode(self, json_bytes, encoding):
		tiow = io.TextIOWrapper(
			io.BytesIO(json_bytes), encoding=encoding, newline=""
		)
		obj = json.load(tiow)
		tiow.close()
		return obj

	def _create_message(
		self, *, content_bytes, content_type, content_encoding
	):
		header = {
			"byteorder": sys.byteorder,
			"content-type": content_type,
			"content-encoding": content_encoding,
			"content-length": len(content_bytes),
		}
		header_bytes = self._json_encode(header, "utf-8")
		message_hdr = struct.pack(">H", len(header_bytes))
		message = message_hdr + header_bytes + content_bytes
		return message

	def _create_response_json_content(self):
		action = self.request.get("action")
		if action == "search":
			query = self.request.get("value")
			answer = request_search.get(query) or f'No match for "{query}".'
			content = {"result": answer}
		else:
			content = {"result": f'Error: invalid action "{action}".'}
		content_encoding = "utf-8"
		response = {
			"content_bytes": self._json_encode(content, content_encoding),
			"content_type": "text/json",
			"content_encoding": content_encoding,
		}
		return response

	def _create_response_binary_content(self):
		response = {
			"content_bytes": b"First 10 bytes of request: "
			+ self.request[:10],
			"content_type": "binary/custom-server-binary-type",
			"content_encoding": "binary",
		}
		return response

	def process_events(self, mask):
		if mask & selectors.EVENT_READ:
			self.read()
		if mask & selectors.EVENT_WRITE:
			self.write()

	def read(self):
		self._read()

		if self._content_len is None:
			self.process_header()

		if self.header:
			if self.request is None:
				self.process_request()

	def write(self):
		if self.request:
			if not self.response_created:
				self.create_response()

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

	def process_header(self):
		hdrlen = 30
		if len(self._recv_buffer) >= hdrlen:
			self.header = unpackHeader(self._recv_buffer[:hdrlen])
			self._recv_buffer = self._recv_buffer[hdrlen:]
			for reqhdr in (
				"srcIP",
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

	def process_request(self):
		contentLength = self.header["contentLength"]
		if not len(self._recv_buffer) >= contentLength:
			return
		data = self._recv_buffer[:contentLength]
		self._recv_buffer = self._recv_buffer[contentLength:]
		if self.header["content-type"] == "text/json":
			encoding = self.header["content-encoding"]
			self.request = self._json_decode(data, encoding)
			print("received request", repr(self.request), "from", self.addr)
		else:
			# Binary or unknown content-type
			self.request = data
			print(
				f'received {self.header["content-type"]} request from',
				self.addr,
			)
		# Set selector to listen for write events, we're done reading.
		self._set_selector_events_mask("w")

	def create_response(self):
		if self.header["content-type"] == "text/json":
			response = self._create_response_json_content()
		else:
			# Binary or unknown content-type
			response = self._create_response_binary_content()
		message = self._create_message(**response)
		self.response_created = True
		self._send_buffer += message
