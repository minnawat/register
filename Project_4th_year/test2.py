import socket

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
local_ip = local_ip+":5000"

print(hostname)
print(local_ip)