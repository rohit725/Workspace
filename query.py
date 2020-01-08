import os
import json
import logging
import zipfile
import argparse
import requests
import traceback
import subprocess
import configparser


##############################################
config_file = "C:\\responder\\responder.ini"
execute_api = "/restapi/responder/job_progress_update"
upload_api = "/restapi/responder/log_upload"
log_file = "C:\\responder\\responder.log"
##############################################


class ExecuteCmd():
    def __init__(self, logger):
        self.logger = logger
        self.read_config()
        self.logger.info("Initialisation complete.")

    def read_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(config_file)
            self.server = config.get("RESPONDER", "res_server")
            self.api_token = config.get("RESPONDER", "api_token")
            self.org_code = config.get("RESPONDER", "org_code")
            self.res_id = config.get("RESPONDER", "responderid")
        except Exception as err:
            self.logger.warning(str(err))

    def run_commands(self, filepath):
        try:
            # print(filepath)
            if not os.path.isfile(filepath):
                raise Exception("Invalid path for the json file: \t %s" % (filepath))
            with open(filepath, "r") as jsonfile:
                dct = json.load(jsonfile)
                api_url = self.server + execute_api
                jobid = str(dct.get("jobid", "-"))
                body = {}
                body["api_token"] = self.api_token
                body["params"] = {}
                body["params"]["job_id"] = int(jobid)
                body["params"]["org_code"] = self.org_code
                body["params"]["data"] = {}
                tmp = {}
                if dct and "commands" in dct:
                    commands = dct.get("commands", [])
                    self.logger.info("%s, starting command execution" % (jobid))
                    for command in commands:
                        self.logger.debug("%s, command - %s" % (jobid, command))
                        cmd = list(command.split(" "))
                        proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        outs, errs = proc.communicate()
                        if outs and not errs:
                            tmp[command + "_out"] = outs.decode()
                        elif errs and outs:
                            tmp[command + "_out"] = outs.decode()
                            tmp[command + "_err"] = errs.decode()
                        elif errs and not outs:
                            tmp[command + "_err"] = errs.decode()
                            break
                        else:
                            tmp[command + "_out"] = "Successfully executed."
                        proc.kill()
                body["params"]["data"]["cmd_out"] = tmp
                self.logger.info("%s, sending the data back to master %s" % (jobid, self.server))
                response = requests.post(url=api_url, data=json.dumps(body))
                if response.status_code != 200:
                    raise Exception("%s, Failed to send request to master %s, status_code: %s" % (jobid, self.server, response.status_code))
                self.logger.info("%s, Successfully sent data to master" % (jobid))
        except Exception as err:
            self.logger.warning(str(err))
            self.logger.debug(traceback.format_exc())

    def upload(self, path):
        try:
            if os.path.exists(path):
                zip_file = ""
                api_url = self.server + upload_api
                if os.path.isfile(path):
                    basename = os.path.basename(path).split(".")[0]
                    zip_file = basename + ".zip"
                    zipf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
                    if path.endswith(".log"):
                        last_1000 = self.file_read_from_tail(path, 1000)
                        with open(basename + "_1000.log", "w") as fp:
                            fp.write(last_1000)
                        zipf.write(basename + "_1000.log")
                        os.remove(basename + "_1000.log")
                    else:
                        zipf.write(path)
                    zipf.close()
                if os.path.isdir(path):
                    zip_file = os.path.basename(path) + ".zip"
                    zipf = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
                    self.zipdir(path, zipf)
                    zipf.close()
                files = {'file': open(zip_file, 'rb')}
                response = requests.post(url=api_url, files=files)
                os.remove(zip_file)
                if response.status_code != 200:
                    raise Exception("%s, Failed to send request to master %s, status_code: %s" % (zip_file, self.server, response.status_code))
                self.logger.info("%s, Successfully sent data to master" % (zip_file))
            else:
                raise Exception("Given path is not valid.")
        except Exception as err:
            self.logger.warning(str(err))
            self.logger.debug(traceback.format_exc())

    def file_read_from_tail(self, fname, lines):
        try:
            bufsize = 8192
            fsize = os.stat(fname).st_size
            iter = 0
            with open(fname) as f:
                if bufsize > fsize:
                    bufsize = fsize-1
                    data = []
                    while True:
                        iter +=1
                        f.seek(fsize-bufsize*iter)
                        data.extend(f.readlines())
                        if len(data) >= lines or f.tell() == 0:
                            return ''.join(data[-lines:])
        except Exception as err:
            self.logger.warning(str(err))
            self.logger.debug(traceback.format_exc())
        return ''

    def zipdir(self, path, ziph):
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    ziph.write(os.path.join(root, file))
        except Exception as err:
            self.logger.warning(str(err))
            self.logger.debug(traceback.format_exc())


def main(args):
    logging.basicConfig(filename=log_file, format="%(asctime)s - %(levelname)s - %(module)s - %(name)s - %(funcName)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S", level=logging.DEBUG)
    logger = logging.getLogger("Query")
    parser = argparse.ArgumentParser(description="Update blusapphire services")
    parser.add_argument("--execute", type=str, default="", help="take's a jsonfile and executes commands in it.")
    parser.add_argument("--upload", type=str, default="", help="takes a directory or file path and zips it and sends back to master.")
    args = parser.parse_args()
    obj = ExecuteCmd(logger)
    if args.execute:
        obj.run_commands(args.execute)
        return 0
    elif args.upload:
        obj.upload(args.upload)
        return 0
    else:
        logger.warning("No arguments provided.")
        return -1


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
