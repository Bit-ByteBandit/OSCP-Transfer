# OSCP-FIleTransfer
This repo for making it easy to transfer files on the OSCP exam using FTP,PUT,SMB

## Instaltion
```python
# clone the repo
$ git clonehttps://github.com/Bit-ByteBandit/OSCP-FIleTransfer.git

# change the working directory to OSCP-FIleTransfer
$ cd OSCP-FIleTransfer

# install the requirements
$ pip install argparse pyftpdlib impacket
```
## Usage

```python
options:
  -h, --help            show this help message and exit
  -m {PUT,put,ftp,FTP,SMB,smb}, --method {PUT,put,ftp,FTP,SMB,smb}
                        Transfer method
  -l PORT, --port PORT  Port to listen on - FTP 21 by Default
  -d DIRECTORY, --directory DIRECTORY
                        FTP or SMB - #specify working directory or `.` by Default - Directory
                        for file storage
  -u USERNAME, --username USERNAME
                        FTP Only - #specify Username or by Default `user`
  -p PASSWORD, --password PASSWORD
                        FTP Only - #Default blank

examples:

    oscptransfer.py -m PUT -l 80

    oscptransfer.py -m ftp -l 21 -d /path/to/directory -u username -p password

    oscptransfer.py -m smb -d /path/to/directory


```

SMB-Server
```python
python3 oscptransfer.py -m SMB

```
FTP-Server
```python
python3 oscptransfer.py -m FTP 

```
PUT-HTTP Server
```python
python3 oscptransfer.py -m PUT -p 80

```
