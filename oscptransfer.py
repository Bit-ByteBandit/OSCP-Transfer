import argparse
import os
import threading
import http.server
import psutil
import socket
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


def interface_check(protocol):
    network_interfaces = psutil.net_if_addrs()
    for interface_name, interface_addresses in network_interfaces.items():
        if interface_name != 'lo':
            for address in interface_addresses:
                if address.family == socket.AF_INET:
                    print(f"{protocol} Server is Listening On {interface_name} {address.address}")


def listen_http(port):
    try:
        server_address = ('', port)
        httpd = http.server.HTTPServer(server_address, FileUploadHandler)
        interface_check('HTTP PUT')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping HTTP Server")


def listen_ftp(port, directory, username, password):
    authorizer = DummyAuthorizer()
    authorizer.add_user(username, password, directory, perm="elradfmw")
    handler = FTPHandler
    handler.authorizer = authorizer
    interface_check('FTP')
    server = FTPServer(("0.0.0.0", port), handler)
    server.serve_forever()


def listen_smb(directory):
    try:
            server = smbserver.SimpleSMBServer()
            server.addShare('share', directory)
            interface_check('SMB')
            server.setSMB2Support(True)
            server.setSMBChallenge('')
            server.start()

    except KeyboardInterrupt:
        print("\nStopping SMB Server")

def main():
    parser = argparse.ArgumentParser(
        description='File Transfer Listener',
        usage='%(prog)s -m [METHOD] -p [PORT] -d [DIRECTORY] -u [USERNAME] -pw [PASSWORD]',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-m', '--method', choices=['PUT', 'put', 'ftp', 'FTP', 'SMB', 'smb'], help='Transfer method')
    parser.add_argument('-l', '--port', type=int, help='Port to listen on - FTP 21 by Default')
    parser.add_argument('-d', '--directory', default='.', help='FTP or SMB - #specify working directory or `.` by Default - Directory for file storage')
    parser.add_argument('-u', '--username', default='user', help='FTP Only - #specify Username or by Default `user`')
    parser.add_argument('-p', '--password', default='', help='FTP Only - #Default blank')
    example_text = '''
examples:

    %(prog)s -m PUT -l 80

    %(prog)s -m ftp -l 21 -d /path/to/directory -u username -p password

    %(prog)s -m smb -d /path/to/directory

'''

    parser.epilog = example_text
    args = parser.parse_args()

    if args.method == 'PUT' or args.method == 'put':
        if args.port:
            listen_http(args.port)
        else:
            print('Please provide the port number for the HTTP server.')
    elif args.method == 'ftp' or args.method == 'FTP':
        if args.port is None:
            args.port = 21
        listen_ftp(args.port, args.directory, args.username, args.password)
    elif args.method == 'smb' or args.method == 'SMB':
        if args.directory:
            listen_smb(args.directory)
        else:
            print('Please provide directory for the SMB server.')
    else:
        print('Invalid transfer method. Please choose one of the available options.')


if __name__ == '__main__':
    main()
