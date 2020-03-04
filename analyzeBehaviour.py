from stat import S_ISDIR
import os, sys, paramiko
import traceback
import socket
import time


LOGDBIP      = '192.168.122.1'
LOGDBPASSWD  = '1844di@lG14Solutions'
ftp_server   = '192.168.122.121'
ftp_username = 'Blues'
ftp_password = 'bs98'
local_path   = '/home/rpandey/Downloads'
logs_path    = 'C:\\blues\\logs'
file_name    = '34d0636684f0577cb9c2c3f701c0e8f8.bin'


def scanCmdSend_toVM(file_type, file_name):
    # Create a UDP socket
    try:
        inj_service_port = 9876
        print ('ScanCMDSend_toVM Started:: ')
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (ftp_server, inj_service_port)
        message = ""
        file_id = 1315069557 # fileid for the file
        message = str(file_type) + "," + str(file_id)+ "," + LOGDBIP + "," + LOGDBPASSWD + "," + file_name
        print ('ScanCMDSend_toVM :message: ' + str(message))
        sock.settimeout(180)
        sent = sock.sendto(str.encode(message), server_address)
        # Receive response
        data, server = sock.recvfrom(4096)
        sock.close()
        print ('ScanCMDSend_toVM :: ', data, server)
    except Exception as e:
        print ('ScanCMDSend_toVM: ' + str(e))
    return

##############################################################################
def sftp_walk(socket, remotepath):
    remotepath = remotepath.replace('\\', '/')
    path = remotepath
    files = []
    folders = []
    for f in socket.listdir_attr(remotepath.replace('\\', '/')):
        if S_ISDIR(f.st_mode):
            folders.append(f.filename)
        else:
            files.append(f.filename)
    print(path, folders, files)
    yield path, folders, files
    for folder in folders:
        new_path = os.path.join(remotepath.replace('\\', '/'), folder)
        for x in sftp_walk(socket, new_path):
            yield x

##############################################################################
def get_all(socket, remotepath, localpath):
    remotepath = remotepath.replace('\\', '/')
    socket.chdir(os.path.split(remotepath)[0])
    parent = os.path.split(remotepath)[1]
    try:
        os.mkdir(localpath)
    except:
        pass
    for walker in sftp_walk(socket, parent):
        try:
            os.mkdir(os.path.join(localpath, walker[0]).replace('\\', '/'))
        except:
            pass
        for file in walker[2]:
            socket.get(os.path.join(walker[0], file).replace('\\', '/'), os.path.join(localpath, walker[0], file).replace('\\', '/'))

##############################################################################
def main():
    paramiko.util.log_to_file("Behaviour_analysis.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ftp_server,22,username=ftp_username,password=ftp_password,timeout=4)
    sftp = s.open_sftp()
    sftp.put(local_path+'/'+file_name,'C:/blues/'+file_name)
    scanCmdSend_toVM(6, file_name)    # change file type here.
    get_all(sftp, logs_path, local_path)
    print("Done")
    s.close()

################################################################################
def getfiles():
    paramiko.util.log_to_file("Behaviour_analysis.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ftp_server,22,username=ftp_username,password=ftp_password,timeout=4)
    sftp = s.open_sftp()
    get_all(sftp, logs_path, local_path)
    print("Done")


if __name__ == "__main__":
    main()
