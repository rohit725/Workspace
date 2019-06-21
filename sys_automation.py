import os
import logging


class AutomateSys:
    def firstTest(self):
        # Saving a log file in a new dierectory using library os.
        os.mkdir("Files")
        os.chdir("/home/charan/Rohit/Files")
        logging.basicConfig(filename="logfile.log",
                            format="%(asctime)s%(message)s", filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.info("This file is created using logger.")
        logger.debug("os library is used to create a directory Rohit")
        os.chdir("/home/charan/Rohit")
        logger.warning("Directory changed back to /home/charan/Rohit")

    def secondTest(self):
        # Running a command using os.system() method.
        os.chdir("/home/charan/Rohit/Files")
        os.system("ls -lrth > result.txt")
        with open('result.txt', 'r') as result:
            print result.read()

    def thirdTest(self):
        # running some more os methods
        os.chdir("/home/charan/")
        for dirpath, dirnames, filenames in os.walk("Rohit"):
            print "Files in %s are: " % dirpath
            for filen in filenames:
                print "\t" + filen
            print "Directories in %s are: " % dirpath
            for dire in dirnames:
                print "\t" + dire


if __name__ == '__main__':
    atmsysobj = AutomateSys()
    # atmsysobj.firstTest()
    # atmsysobj.secondTest()
    atmsysobj.thirdTest()
