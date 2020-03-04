import subprocess
import pexpect
import socket
import os


known_connections = ["G14_Group24", "G14 BGroup", "G14_Link", "em1"]


def is_connected():
    REMOTE_SERVER = "www.google.com"
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        s = socket.create_connection((REMOTE_SERVER, 80), 2)
        s.close()
        return True
    except:
        pass
    return False
  
  
def connect_vpn():
    output = subprocess.check_output("nmcli -t -f NAME connection show --active", shell=True)
    if output:
        output = output.split('\n')
    output = list(filter(None, output))    # Filter is fastest to do this work.
    if set(output) & set(known_connections):
        print("You are using office networks no need to connect to vpn.")
    else:
        print("Connecting to VPN, Please wait....")
        child = pexpect.spawn ('sudo openvpn /home/rpandey/Downloads/G14Sense-udp-1194-Rpandey-config.ovpn')
        child.expect ('.*Enter Auth Username:')
        child.sendline ('Rpandey')
        child.expect('Enter Auth Password:')
        child.sendline('VSL5uww!M&$%C@L9')
        print("Connection Established.")
    

def main():
    conn = is_connected()
    if conn:
        connect_vpn()
    else:
        print("You are not connected to internet.")


if __name__ == '__main__':
    main()
