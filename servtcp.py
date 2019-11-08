from socket import *
import time

def servicing(con):
	start = time.time()
	data = con.recv(4096)
	print(f"Receiving data: {data.decode('utf-8')}")
	print(f"This took {time.time() - start} seconds since connection starts")
	con.close()

s=socket(AF_INET,SOCK_STREAM)
s.bind(('',9999))
s.listen()
while True:
	con,addr = s.accept()
	print(f"Accept connection from {addr}; setting timer")
	servicing(con)