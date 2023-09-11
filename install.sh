
#!/usr/bin/bash
echo "[+] installing requirements"
pip3 install -r requirements.txt
echo "[+] copy to environement /usr/bin"
sudo cp oscp-transfer.py /usr/bin/oscp-transfer
sudo chmod +x /usr/bin/oscp-transfer
echo "[+] refresh the terminal"
. ~/.bashrc
echo "[+] Done"
