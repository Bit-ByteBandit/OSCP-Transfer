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
    except Exception as e:
        print("Exception:", e)
# http get request server to download files
def listen_get(port):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("0.0.0.0", port), handler) as server:
        interface_check('HTTP GET',port)
        try:
            server.serve_forever()

        except KeyboardInterrupt:
            print("\nServer stopped.")
        except Exception as e:
            print("Exception:", e)


def listen_ftp(port, directory, username, password):
    try:
            authorizer = DummyAuthorizer()
            authorizer.add_user(username, password, directory, perm="elradfmw")
            handler = FTPHandler
            handler.authorizer = authorizer
            interface_check('FTP',port)
            server = FTPServer(("0.0.0.0", port), handler)
            server.serve_forever()
    except KeyboardInterrupt:
         print("\nKeyboard interrupt received. Stopping the SMB server.")
    except Exception as e:
         print("Exception:", e)


def listen_smb(directory,port,sharename):
    try:
        
            server = smbserver.SimpleSMBServer(listenAddress='0.0.0.0', listenPort=int(port))
            server.addShare(sharename, directory)
            interface_check('SMB',port)
            print('\n')
            server.setSMB2Support(True)
            server.setSMBChallenge('')
            server.setLogFile('')
            # Start the SMB server
            server.start()
            

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Stopping the SMB server.")

    except Exception as e:
        print("Exception:", e)


def main():
    parser = argparse.ArgumentParser(
        description='File Transfer Listener',
        usage='%(prog)s -m [METHOD] -p [PORT] -d [DIRECTORY] -u [USERNAME] -p [PASSWORD]',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-m', '--method', choices=['PUT', 'put', 'ftp', 'FTP', 'SMB', 'smb', 'get', 'GET'], help='Transfer method')
    parser.add_argument('-l', '--port', type=int, help='Port to listen on - #FTP 21 by Default - #SMB 445 By Default')
    parser.add_argument('-d', '--directory', default='.', help='FTP or SMB - #specify working directory or `.` by Default - Directory for file storage')
    parser.add_argument('-u', '--username', default='FTP', help='FTP Only #specify Username or by Default `ftp`')
    parser.add_argument('-p', '--password', default='FTP', help='FTP Only #Default `ftp`')
    parser.add_argument('-sh', '--sharename', default='share', help='SMB Share-name By #Default `share`')
    example_text = '''
examples:
    %(prog)s -m GET -l 80

    %(prog)s -m PUT -l 80

    %(prog)s -m ftp -l 21 -d /path/to/directory -u username -p password

    %(prog)s -m smb 

'''

    parser.epilog = example_text
    args = parser.parse_args()

    allowed_methods = ['SMB', 'GET', 'PUT', 'FTP']

    if args.method.upper() in allowed_methods:
        
        if args.method.upper() == 'PUT':

            if args.port is None:
                args.port = 80
                
            listen_put(args.port)
            
        elif args.method.upper() == 'FTP':

            if args.port is None:
                args.port = 21
            if args.username is None:
                args.username = 'ftp'
            if args.password is None:
                args.password = 'ftp'
            listen_ftp(args.port, args.directory, args.username, args.password)

        elif args.method.upper() == 'SMB':
            if args.port is None:
                args.port = 445

            listen_smb(args.directory, args.port, args.sharename)

        if args.method.upper() == 'GET':

            if args.port is None:
                args.port = 80
                
            listen_get(args.port)
    else:
        print('Invalid transfer method. Please choose one of the available options.')


if __name__ == '__main__':
    main()
