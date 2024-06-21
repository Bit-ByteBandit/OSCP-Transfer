
<div align="center">

# **`OSCP File Transfer Tool`**

<p align="center">
  <b>A Streamlined Solution for File Transfers During the OSCP Exam Using <br><code>FTP,HTTP(PUT,GET),SMB</code></b>
</p>

</div>

<p align="center" width="50px">
  <img alt="Static Badge" src="https://img.shields.io/badge/ALL_Transfers_Methods_In_One_Tool-%23FF5733">
</p>

<p align="center">
  <a href="https://github.com/Bit-ByteBandit/OSCP-Transfer/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg"></a>
  <a href="https://github.com/Bit-ByteBandit/OSCP-Transfer"><img src="https://img.shields.io/github/languages/top/Bit-ByteBandit/OSCP-Transfer"></a>
  <a href="https://github.com/Bit-ByteBandit/OSCP-Transfer"><img src="https://img.shields.io/github/last-commit/Bit-ByteBandit/OSCP-Transfer.svg"></a>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#running-servers">Running Servers</a> •
  <a href="#examples">Examples</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>


## Table of Contents

- [Key Features](#key-features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Running Servers](#running-servers)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Key Features

- **Multi-protocol support**: FTP, HTTP (PUT/GET), and SMB
- **Easy-to-use command-line interface**
- **Flexible configuration options**
- **Automatic server setup** for quick file transfers
- **OSCP exam-friendly**: Designed with the OSCP exam environment in mind
- **Minimal dependencies**: Relies primarily on Python standard libraries

## Requirements

- Python 3.6 or higher
- Git (for cloning the repository)
- Additional dependencies will be installed by the `install.sh` script

## Installation

1. Clone the Repository:
```bash
git clone https://github.com/Bit-ByteBandit/OSCP-Transfer.git
```

2. Navigate to the Directory:
```bash
cd OSCP-Transfer
```

3. Install Dependencies:
```bash
chmod +x ./install.sh && ./install.sh
```

## Usage

The tool offers flexible transfer methods and customizable options:

```
oscp-transfer -m {METHOD} [options]
```

### Options:

- `-h, --help`: Display the help message and exit.
- `-m {PUT, FTP, SMB, GET}`: Choose the transfer method.
- `-l PORT`: Specify the listening port (default: 21 for FTP).
- `-d DIRECTORY`: For FTP or SMB, set the working directory.
- `-sh SHARE`: Name for SMB share (default: SHARE).
- `-u USERNAME`: Provide the FTP or SMB username (default for FTP only: user).
- `-p PASSWORD`: Provide the FTP or SMB password (default for FTP only: user).
- `-smb2`: Use SMB2 protocol (for SMB transfers only).

## Running Servers

Start different types of servers easily:

```bash
# Start GET-HTTP Server
oscp-transfer -m GET

# Start SMB Server
oscp-transfer -m SMB

# Start FTP Server
oscp-transfer -m FTP

# Start PUT-HTTP Server
oscp-transfer -m PUT
```

## Examples

1. Initiate a GET server on port 80:
```bash
oscp-transfer -m GET -l 80
```

2. Initiate a PUT server on port 80:
```bash
oscp-transfer -m PUT -l 80
```

3. Use FTP with custom options:
```bash
oscp-transfer -m ftp -l 21 -d /path/to/directory -u username -p password
```

4. Use SMB with a username and a password:
```bash
oscp-transfer -m smb -u foo -p foo -sh MySharefoo -smb2
```

5. Upload a file using PUT request:
```bash
curl http://[IP] -T [File]
```

## Contributing

We welcome contributions to improve the OSCP File Transfer Tool! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made  by <a href="https://github.com/Bit-ByteBandit">Bit-ByteBandit</a>
</p>
