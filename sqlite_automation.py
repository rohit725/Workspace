import sqlite3
import logging


class AutomateSql:
    def __init__(self):
        # Constructor which create's database and connect's to it and also initializes the logger.
        logging.basicConfig(filename="Files/dbentry.log",
                            format='%(asctime)s %(message)s', filemode='a')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.db = sqlite3.connect('Files/mydb')
        self.cursor = self.db.cursor()
        self.logger.info("Database Initialised.")
        print "You are now connected to mydb.\n"

    def createTable(self, tablename, columndetails):
        # Method to create a table in database.
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {}({})'''.format(
            tablename, ", ".join(columndetails)))
        self.db.commit()
        self.logger.info("New table created: {}".format(tablename))

    def insertRow(self, tablename, columns, values):
        # Method for inserting new rows in database.
        self.cursor.execute('''INSERT INTO {}({}) VALUES({})'''.format(
            tablename, ", ".join(columns), ", ".join(values)))
        self.db.commit()
        self.logger.info("New row inserted into table {}.".format(tablename))

    def updateVal(self, tablename, column, value, scolumn, svalue):
        # Method for updating value of provided column based on id.
        self.cursor.execute("UPDATE {} SET {} = {} WHERE {} = {}".format(
            tablename, column, value, scolumn, svalue))
        self.db.commit()
        self.logger.info("Value updated in table {}.".format(tablename))

    def dropTable(self, tablename):
        # Method for deleting a table.
        self.cursor.execute("DROP TABLE IF EXISTS {}".format(tablename))
        self.db.commit()
        self.logger.info("Table deleted: {}".format(tablename))

    def selectAll(self, tablename):
        # Method for fetching all the rows of a table and printing it on the screen.
        self.cursor.execute("SELECT * FROM {}".format(tablename))
        rows = self.cursor.fetchall()
        for row in rows:
            print "\t".join(map(str, row))

    def quit(self):
        # Disconnect to database.
        self.db.close()
