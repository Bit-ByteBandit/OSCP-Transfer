#!/usr/bin/env python3
import argparse
import os
import threading
import http.server
import psutil
import socket
import socketserver
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from impacket import smbserver

class FileUploadHandler(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        file_path = self.path[1:]
        with open(file_path, 'wb') as file:
            file.write(self.rfile.read(content_length))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File uploaded successfully via HTTP')


def interface_check(protocol,port):
    network_interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in network_interfaces.items():
        if interface_name != 'lo':
            for address in interface_addresses:
                if address.family == socket.AF_INET:
                    print(f"{protocol} is Listening On {interface_name} {address.address} on port {port}")

#  http put request server to upload files from target to you
def listen_put(port):
    try:
        server_address = ('', port)
        httpd = http.server.HTTPServer(server_address, FileUploadHandler)
        interface_check('HTTP PUT',port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping HTTP Server")

# http get request server to download files
def listen_get(port):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as server:
        interface_check('HTTP GET',port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


def listen_ftp(port, directory, username, password):
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, directory, perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    interface_check('FTP',port)
    server = FTPServer(("0.0.0.0", port), handler)
    server.serve_forever()


def listen_smb(directory):
    try:
            server = smbserver.SimpleSMBServer()
            server.addShare('share', directory)
            interface_check('SMB','445')
            server.setSMB2Support(True)
            server.setSMBChallenge('')
            server.start()

    except KeyboardInterrupt:
        print("\nStopping SMB Server")

def main():
    parser = argparse.ArgumentParser(
        description='File Transfer Listener',
        usage='%(prog)s -m [METHOD] -p [PORT] -d [DIRECTORY] -u [USERNAME] -p [PASSWORD]',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-m', '--method', choices=['PUT', 'put', 'ftp', 'FTP', 'SMB', 'smb', 'get', 'GET'], help='Transfer method')
    parser.add_argument('-l', '--port', type=int, help='Port to listen on - FTP 21 by Default')
    parser.add_argument('-d', '--directory', default='.', help='FTP or SMB - #specify working directory or `.` by Default - Directory for file storage')
    parser.add_argument('-u', '--username', default='ftp', help='FTP Only - #specify Username or by Default `ftp`')
    parser.add_argument('-p', '--password', default='ftp', help='FTP Only - #Default `ftp`')
    example_text = '''
examples:
    %(prog)s -m GET -l 80

    %(prog)s -m PUT -l 80

    %(prog)s -m ftp -l 21 -d /path/to/directory -u username -p password

    %(prog)s -m smb -d /path/to/directory

'''

    parser.epilog = example_text
    args = parser.parse_args()

    if args.method == 'PUT' or args.method == 'put':
        if args.port is None:
            args.port = 80
            
        listen_put(args.port)
        
    elif args.method == 'ftp' or args.method == 'FTP':
        if args.port is None:
            args.port = 21
        if args.username is None:
            args.username = 'ftp'
        if args.password is None:
            args.password = 'ftp'
        listen_ftp(args.port, args.directory, args.username, args.password)
    elif args.method == 'smb' or args.method == 'SMB':
        if args.directory:
            listen_smb(args.directory)
        else:
            print('Please provide directory for the SMB server.')
    if args.method == 'get' or args.method == 'GET':
        if args.port is None:
            args.port = 80
        listen_get(args.port)
    else:
         print('Invalid transfer method. Please choose one of the available options.')


if __name__ == '__main__':
    main()
