#!/bin/env python3
import socket, sys, os, re, time

class asetter(object):
	response_status = 200
	response_status_set = "OK"
	response_header = ""
	response_mime = "text/html"
	response_client = "GET / HTTP/1.1" if False else ""
	response_data = ""
	lhost = "0.0.0.0"
	lport = 40
	response_file = "index.html"
	def header(self):
		mime_ext = {
	     'php': 'text/plain',
	     'py': 'text/plain',
	     'html': 'text/html',
	     'js': 'application/javascript',
	     'css': 'text/css',
	     'jpeg': 'image/jpeg',
	     'jpg': 'image/jpeg',
	     'png': 'image/png',
	     'mp4': 'video/mp4',
	     'mp3': 'audio/mpeg'
	 	}
		for mime in mime_ext:
			try:
				self.response_mime = mime_ext[self.response_file.split('.')[-1]]
			except KeyError:
				self.response_mime = "text/html"
		try:
			if self.response_file != '/':
				try:
					f = open(os.getcwd() + self.response_file, "rb")
					self.response_status = 200
					self.response_status_set = "OK"
				except IsADirectoryError:
					f = open("403.html", "rb")
					self.response_status = 403
					self.response_status_set = "Forbidden"
			else:
				f = open('index.html', 'rb')
				self.response_status = 200
				self.response_status_set = "OK"
			self.response_data = f.read()
			f.close()
		except FileNotFoundError:
			f = open("404.html", "rb")
			self.response_status = 404
			self.response_status_set = "Not Found"
			self.response_data = f.read()
		self.response_header = "HTTP/1.1 %d %s\n" % (self.response_status, self.response_status_set)
		self.response_header += "Date: %s\n" % time.strftime("%a, %d %b %Y %H:%M:%S GMT")
		self.response_header += "Server: 4setter Server\n"
		self.response_header += "Content-Length: %d\n" % int(len(self.response_data))
		self.response_header += "Vary: Accept-Encoding\n"
		self.response_header += "Connection: Close\n"
		self.response_header += "Content-Type: %s\n\n" % self.response_mime
		
	def server(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		s.bind((self.lhost, self.lport))
		s.listen(5)
		print("[*] Server binding started at \033[032m{}\033[00m:\033[036m{}\033[00m".format(self.lhost, self.lport))
		while True:
			try:
				conn, addr = s.accept()
			except KeyboardInterrupt:
				print("[!] Shutting down the server... ", end='')
				s.close()
				print("OK")
				sys.exit(0)
			self.response_client = conn.recv(1024).decode()
			self.response_file = re.split(' ', self.response_client.splitlines()[0])[1].replace("%20", " ")
			self.header()
			print('%s - - [%s] \"%s\" %d -' % (addr[0], time.strftime("%d/%m/%Y %H:%M:%S"), self.response_client.splitlines()[0], self.response_status))
			conn.sendall(self.response_header.encode() + self.response_data)
if __name__ == '__main__':
	r = '\033[031m'
	g = '\033[032m'
	b = '\033[036m'
	k = '\033[030m'
	n = '\033[00m'
	banner = """
  {r}____ {b}____    __  {n}__{n}         
 {r}/ / /{b}/ __/__ / /_{n}/ /____ ____{n}
{r}/_  _/{b}\ \/ -_) __/{n} __/ -_) __/{n}
 {r}/_/{b}/___/\__/\__/{n}\__/\__/_/{n} 
 {r}MSF{n}{b}: http://www.{n}mmsecurity.n{g}et/forum/member.php?action=register&referrer=9450{n}
		                 		{r}v1.0{n} 
	""".format(r=r, g=g, b=b, n=n)
	print(banner)
	asetter().server()