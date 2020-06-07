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
	doc_path =  '/var/www' # os.getcwd()+'/'
	def header(self):
		mime_ext = {
		"pdf" : "application/pdf",
		"txt" : "text/plain",
		"htm" : "text/html",
		"exe" : "application/octet-stream",
		"zip" : "application/zip",
		"doc" : "application/msword",
		"xls" : "application/vnd.ms-excel",
		"ppt" : "application/vnd.ms-powerpoint",
		"gif" : "image/gif",
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
		index_file = ['index.html', 'index.htm', 'index.php']
		for mime in mime_ext:
			try:
				self.response_mime = mime_ext[self.response_file.split('.')[-1]]
			except KeyError:
				self.response_mime = "text/html"
		try:
			if self.response_file != '/':
				try:
					if self.doc_path[-1] == '/':
						f = open(self.doc_path[:-1] + self.response_file, "rb")
					else:
						f = open(self.doc_path + self.response_file, "rb")
					self.response_status = 200
					self.response_status_set = "OK"
					self.response_data = f.read()
				except IsADirectoryError:
					self.response_status = 403
					self.response_status_set = "Forbidden"
					self.response_data = b"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<title>403 Forbidden</title>
</head>
<body>
<h1>Forbidden</h1>
<p>You don't have permission to access this resource.</p>
</body>
</html>"""
			else:
				for index in index_file:
					try:
						if self.doc_path[-1] == '/':
							f = open(self.doc_path+index, 'rb')
						else:
							f = open(self.doc_path+'/'+index, 'rb')
						self.response_status = 200
						self.response_status_set = "OK"
						self.response_data = f.read()
						break
					except FileNotFoundError:
						pass
		except FileNotFoundError:
			self.response_status = 404
			self.response_status_set = "Not Found"
			self.response_data = b"""<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<title>404 Not Found</title>
</head>
<body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
</body>
</html>
"""
		self.response_header = "HTTP/1.1 %d %s\n" % (self.response_status, self.response_status_set)
		self.response_header += "Date: %s\n" % time.strftime("%a, %d %b %Y %H:%M:%S GMT")
		self.response_header += "Server: 4Setter Server\n"
		self.response_header += "Content-Length: %d\n" % int(len(self.response_data))
		self.response_header += "Vary: Accept-Encoding\n"
		self.response_header += "Connection: Close\n"
		self.response_header += "Content-Type: %s\n\n" % self.response_mime
		
	def server(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		s.bind((self.lhost, self.lport))
		s.listen(5)
		print(f"[{b}*{n}] Server binding started at {g}{self.lhost}{n}:{g}{self.lport}{n}")
		while True:
			try:
				conn, addr = s.accept()
			except KeyboardInterrupt:
				print(f"[{r}!{n}] Shutting down the server... ", end='')
				s.close()
				print("OK")
				sys.exit(0)
			self.response_client = conn.recv(1024).decode()
			self.response_file = re.split(' ', self.response_client.splitlines()[0])[1].replace("%20", " ")
			self.header()
			print(f'{g}%s{n} - - [{b}%s{n}] \"%s\" %d -' % (addr[0], time.strftime("%d/%m/%Y %H:%M:%S"), self.response_client.splitlines()[0], self.response_status))
			conn.sendall(self.response_header.encode() + self.response_data)
if __name__ == '__main__':
	r = '\033[031m'
	g = '\033[032m'
	b = '\033[036m'
	k = '\033[030m'
	n = '\033[00m'
	banner = """
  {r}____ {g}____    __  {b}__{n}         
 {r}/ / /{g}/ __/__ / /_{b}/ /____ ____{n}
{r}/_  _/{g}\ \/ -_) __/{b} __/ -_) __/{n}
 {r}/_/{g}/___/\__/\__/{b}\__/\__/_/{n} 
 {r}MSF{n}{b}: http://www.{n}mmsecurity.n{g}et/forum/member.php?action=register&referrer=9450{n}
		                 		{r}v1.0{n} 
	""".format(r=r, g=g, b=b, n=n)
	print(banner)
	asetter().server()