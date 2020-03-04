import paramiko
import traceback


ftp_server   = '192.168.122.121'    # Virtual Machine IP in which you want to copy the file.
ftp_username = 'blusapphire'
ftp_password = 'bs98'
source = "/home/rpandey/Downloads/responder.ini"
destination = "C:/Users/Blues/Desktop/responder.ini"


def main(args):
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(ftp_server,22,username=ftp_username,password=ftp_password,timeout=4)
        sftp = s.open_sftp()
        sftp.put(source, destination)
        print("Done")
    except Exception as err:
        print(err)
        print(traceback.format_exc())
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
