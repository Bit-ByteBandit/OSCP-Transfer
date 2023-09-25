# OSCP File Transfer Tool

  

This repository provides a streamlined solution for file transfers during the OSCP exam using various protocols, including FTP, PUT, GET and SMB.

  

## Installation

  

1. Clone the Repository:

```
$ git clone https://github.com/Bit-ByteBandit/OSCP-FIleTransfer.git
```

2. Navigate to the Directory:

```
$ cd OSCP-FIleTransfer
```

3. Install Dependencies:

```
$ chmod +x ./install.sh; ./install.sh
```

## Usage

  

The tool offers flexible transfer methods and customizable options:

```
oscp-transfer -m {METHOD} [options]
```

Options:

  

- -h, --help: Display the help message and exit.

- -m {PUT, FTP, SMB, GET}: Choose the transfer method.

- -l PORT: Specify the listening port (default: 21 for FTP).

- -d DIRECTORY: For FTP or SMB, set the working directory
  
- -sh SHARE name for SMB (default: SHARE)

- -u USERNAME: Provide the FTP or smb username (default for ftp only: user).

- -p PASSWORD: Provide the FTP or smb password (default for ftp only: user).

  

Examples:

  

- Initiate a GET server on port 80:

```
oscp-transfer -m GET -l 80
```

- Initiate a PUT server on port 80:

```
oscp-transfer -m PUT -l 80
```

- Use FTP with custom options:

```
oscp-transfer -m ftp -l 21 -d /path/to/directory -u username -p password
```

- Use SMB with a username and a password:

```
oscp-transfer -m smb -u foo -p foo -sh MySharefoo -smb2
```

## Running Servers

  

Start GET-HTTP Server:

```
oscp-transfer -m GET
```

Start SMB Server:

```
oscp-transfer -m SMB
```

Start FTP Server:

```
oscp-transfer -m FTP
```

Start PUT-HTTP Server:

```
oscp-transfer -m PUT
```
Upload a file using **PUT** request:

```
curl http://[IP] -T [File]
```
