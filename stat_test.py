import socket
import time
import fcntl
import struct
import psutil
from  subprocess import PIPE, Popen

def get_ip(interface):
	temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(temp.fileno(), 0x8915, struct.pack('256s', interface[:15]))[20:24])

def get_temp():
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
	output, _error = process.communicate()
	return float(output[output.index('=') + 1:output.rindex("'")])

host_name = socket.gethostname()
CPU_temp = get_temp()
CPU_usage = psutil.cpu_percent()

print(host_name)
print(get_ip('eth0'))
print("{:.1f}C").format(CPU_temp)
print("{:.1f}%").format(CPU_usage)
