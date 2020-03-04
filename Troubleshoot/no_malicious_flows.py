import paramiko
import argparse
from datetime import datetime
import time
import pytz    # $ pip install pytz
import tzlocal # $ pip install tzlocal


def datetime_from_utc_to_local(utc_datetime):
    local_time = "No time stamp"
    try:
        local_timezone = tzlocal.get_localzone() # get pytz tzinfo
        utc_time = datetime.strptime(utc_datetime, "%Y-%m-%d %H:%M:%S")
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    except Exception as e:
        raise e
    return local_time


def ask_user(question):
    check = str(input(question+" ? (Y/N): ")).lower().strip()
    try:
        if check[0] == 'y':
            return True
        elif check[0] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()


def ssh_conn(hostname,username,password,cmd):
    final_output = " No response from server "
    try:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname,username=username,password=password)
            print("Connected to %s" % hostname)
        except paramiko.AuthenticationException:
            print("Failed to connect to %s due to wrong username/password" %hostname)
            exit(1)
        except Exception as e:
            print(e)
            exit(2)

        try:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print (cmd)
        except Exception as e:
            print(e.message)

        err = ''.join(stderr.readlines())
        out = ''.join(stdout.readlines())
        final_output = str(out)+str(err)
        if "workingDirectory" in final_output:
            print("************************")
    except Exception as e:
        raise e
    return final_output


def start(hostname,username,password,lines,sid):
    try:
        first_cmd = "tail -"+lines+" /var/lib/pipeline/log/alerts.log | grep "+sid

        result = ssh_conn(hostname,username,password,first_cmd)
        print(result)
        last_rec_time = (result.strip().split("\n")[-1].split('|')[0])
        src_ip = (result.strip().split("\n")[-1].split('|')[5])
        dst_ip = (result.strip().split("\n")[-1].split('|')[4])
        spt = (result.strip().split("\n")[-1].split('|')[6])
        dpt = (result.strip().split("\n")[-1].split('|')[7])
        print("********************************************************** LAST UPDATED MALICIOUS FLOW DETAILS **************************************************************")
        print(last_rec_time)
        last_rec = datetime_from_utc_to_local(last_rec_time)
        print(str(last_rec) +"               Note : 2 to 3 mins variation negligible" )
        print (src_ip)
        print (dst_ip)
        print (spt)
        print (dpt)
        user_yes_or_no = ask_user("Do you want to know count of pending records")
        if user_yes_or_no == True:
            second_cmd = "cd /var/lib/pipeline/log \nls -l alerts.log \ncat alerts.log.*"
            log_count = ssh_conn(hostname,username,password,second_cmd)
            print (log_count)

        services_input = ask_user("Do you want to restart the services in master")
        if services_input == True:
            third_cmd = "service rwflowappend restart\nservice rwflowpack stop \nservice pipeline restart \nservice blu_pipeline restart"
            restart_out = ssh_conn(hostname,username,password,third_cmd)
            print (restart_out)
            print("\n")
            time.sleep(7)
            third_2 = "service rwflowpack start"
            restart_out_2 = ssh_conn(hostname,username,password,third_2)
            print(restart_out_2)
            print("\n")
            time.sleep(3)
            fouth_cmd = "service rwflowappend status\nservice rwflowpack status \nservice pipeline status \nservice blu_pipeline status"
            status_out = ssh_conn(hostname,username,password,fouth_cmd)
            for i in (status_out.strip().split("\n")):
                print(i+'\n\n')

    except Exception as e:
        raise e

def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-ip", help="ip address of remote server(MASTER)",type=str)
        parser.add_argument("-u", help="user name of remote server",type=str,default="root")
        parser.add_argument("-p", help="password of remote server",type=str, default="1844di@lG14Solutions")
        parser.add_argument("-l", help="number of lines",default="100",type=str)
        parser.add_argument("-sid", help="sensor id",default="S",type=str)

        args = parser.parse_args()
        if args.ip:
            hostname = args.ip
            print(args.ip)
        if args.u:
            username = args.u
            print(args.u)
        if args.p:
            password = args.p
            print (args.p)
        lines = args.l
        sid = args.sid
        start(hostname,username,password,lines,sid)
    except Exception as e:
        raise e


if __name__== "__main__":
  main()
