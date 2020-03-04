#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  no_scanned_files.py
#
#  Copyright 2019 Unknown <rpandey@dev-master>
#
#


from paramiko_expect import SSHClientInteraction
import traceback
import paramiko
import argparse
import getpass
import socket
import time


MS_PROMPT = "\[root@.*\s~\]#\s+"
SENS_PROMPT = "root@.*:~\s#\s+"
lines = ""


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def restart_services(channel, service_list):
    try:
        result = []
        for service in service_list:
            cmd = "service %s stop" % service
            channel.send(cmd)
            channel.expect(SENS_PROMPT)
        time.sleep(30)
        for service in service_list:
            cmd = "service %s status" % service
            channel.send(cmd)
            channel.expect(SENS_PROMPT)
            res = channel.current_output_clean
            result.append(res)
    except Exception as err:
        print("Error in restart_services: " + str(err))
    return result


def print_details(result):
    global lines
    if result.get("Blu_session_logs", ""):
        file_lst = [i for i in result["Blu_session_logs"].strip().split(
            '\n') if "Filename:" in i]
        if not file_lst:
            print(bcolors.FAIL + "The last %s lines in blu_session.log does not contains any file logs" % (lines) + bcolors.ENDC)
            return
        last_file = file_lst[-1]
        timestamp = last_file.split(',')[0]
        filename = last_file.split(',')[1].split(':')[-1].strip()
        print(bcolors.HEADER + "\n\t\t***************************************************** " + bcolors.ENDC + bcolors.BOLD +
            "Last Scanned File" + bcolors.ENDC + bcolors.HEADER + " *****************************************************\n" + bcolors.ENDC)
        print(bcolors.OKBLUE + "Timestamp: " + bcolors.ENDC + timestamp +
            "\t\t" + bcolors.OKBLUE + "Filename: " + bcolors.ENDC + filename)
        print(bcolors.OKBLUE + "Log Line: " + bcolors.ENDC + last_file)
        print(bcolors.OKBLUE + "\n\n\tLast %s lines from logs:\n" % lines + bcolors.ENDC)
        print(result["Blu_session_logs"])
    if result.get("Port_47760", ""):
        print(bcolors.HEADER + "\n\t\t***************************************************** " + bcolors.ENDC + bcolors.BOLD +
            "Port 47760 stats" + bcolors.ENDC + bcolors.HEADER + " ******************************************************\n" + bcolors.ENDC)
        result["Port_47760"] = result["Port_47760"].replace("47760", bcolors.WARNING + "47760" + bcolors.ENDC)
        print(result["Port_47760"])
    if result.get("Service_status", ""):
        print(bcolors.HEADER + "\n\t\t****************************************************** " + bcolors.ENDC + bcolors.BOLD +
            "Services Status" + bcolors.ENDC + bcolors.HEADER + " ******************************************************\n" + bcolors.ENDC)
        for key, value in result["Service_status"].items():
            if "running" in value:
                value = bcolors.OKGREEN + value + bcolors.ENDC
            else:
                value = bcolors.FAIL + value + bcolors.ENDC
            key = bcolors.BOLD + key + bcolors.ENDC
            print("%s:\n%s" % (key, value))
    print(bcolors.HEADER + "\n\t\t*****************************************************************************************************************************" + bcolors.ENDC)
    return


def ssh_conn(hostname, username, password, lines, sid):
    res = {}
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        print(bcolors.OKGREEN + "Connection established to host: %s" %
              hostname + bcolors.ENDC)
        with SSHClientInteraction(ssh, timeout=10) as interact:     # display=True
            res = {}
            port = str(int(sid) + 8000)
            cmd = 'netstat -na | grep %s' % port
            interact.send(cmd)
            time.sleep(2)
            interact.expect(MS_PROMPT)
            cmd_out = interact.current_output_clean
            res["sensor_grep"] = cmd_out.replace(port[1:], port)
            interact.send('ssh blusapphire@localhost -p %s' % port)
            interact.expect(".*Password for.*")
            interact.send(getpass.getpass(
                prompt="Please enter sensor password:\t", stream=None))
            interact.expect("\$\s+")
            interact.send('sudo su -')
            interact.expect(SENS_PROMPT)
            interact.send('tail -n %s /var/log/blu_session.log' % lines)
            interact.expect(SENS_PROMPT)
            res["Blu_session_logs"] = interact.current_output_clean
            interact.send('netstat -na | grep 47760')
            interact.expect(SENS_PROMPT)
            res["Port_47760"] = interact.current_output_clean
            services = ["blu_naf", "blu_paf", "blu_ipfix", "blu_session", "blu_sync"]
            result = []
            for service in services:
                cmd = "service %s status" % service
                interact.send(cmd)
                time.sleep(3)
                interact.expect(SENS_PROMPT)
                result.append(interact.current_output_clean)
            res["Service_status"] = dict(list(zip(services, result)))
            print_details(res)
            choice = input(bcolors.WARNING + "Do you want to restart the services in sensor? [y/n]" + bcolors.ENDC)
            if choice.lower() == "y" or choice.lower() == "yes":
                lst = list(input("Please enter the services you want to restart seprated by a space.\n").strip().split(" "))
                print(lst)
                pass    # Invoke services function here
            interact.send("logout")
            interact.expect("\$\s+")
            interact.send('\x04')
            interact.expect(MS_PROMPT)
    except paramiko.AuthenticationException as err:
        print_details(res)
        print(bcolors.FAIL + str(err) + bcolors.ENDC)
    except socket.timeout as err:
        print_details(res)
        res["err"] = str(err)
        print(bcolors.FAIL + "Socket timeout.")
        print(traceback.format_exc() + bcolors.ENDC)
    except Exception as err:
        print_details(res)
        res["err"] = str(err)
        print(bcolors.FAIL + traceback.format_exc() + bcolors.ENDC)
    finally:
        if ssh:
            print(bcolors.OKGREEN + "\nClosing the Connection." + bcolors.ENDC)
            ssh.close()
    return res


def start(hostname, username, password, lines, sid):
    result = ssh_conn(hostname, username, password, lines, sid)
    # print(result)


def main():
    try:
        global lines
        parser = argparse.ArgumentParser(prog="Scanned Files Troubleshoot")
        parser.add_argument(
            "-ip", help="IP address of remote server(master)", type=str)
        parser.add_argument(
            "-u", "--user", help="User name of remote server", type=str, default="root")
        parser.add_argument("-p", "--password", help="Password of remote server",
                            type=str, default="1844di@lG14Solutions")
        parser.add_argument(
            "-l", "--lines", help="Number of lines to print in logs", default="10", type=str)
        parser.add_argument("-sid", help="sensor id", type=str)

        args = parser.parse_args()
        if not (args.ip and args.lines and args.sid):
            raise Exception("Please provide necessary parameters.")
        hostname = args.ip
        username = args.user
        password = args.password
        lines = args.lines
        sid = args.sid
        start(hostname, username, password, lines, sid)
    except Exception as err:
        print(err)
        print(traceback.format_exc())


if __name__ == '__main__':
    import sys
    main()
    sys.exit(0)
