from sqlite_automation import AutomateSql as asql
from os import system


system('clear')
print "\t\t\t\t--- Instructions For Using This Module ---"
print " \t1. Please insert a character value in ''."
print " \t2. Please input everything in just capital letters"
print " \t3. Please insert values as guided.\n\n"
raw_input("Press Enter to continue: ")
print "\n\n"

asqlobj = asql()
while True:
    print "\tWhat do you want to do? \n"
    print " 1. Create a table"
    print " 2. Insert a row in a table"
    print " 3. Update a value in table(Just one condition allowed)"
    print " 4. Drop a table"
    print " 5. Select all values from a table"
    choice = int(raw_input(
        " \tChoose the coresponding numbers else any number to quit(Just numbers allowed)"))
    print "\n"
    if choice == 1:
        name = raw_input("Enter the table name: ")
        columndetails = raw_input(
            "Enter column details with datatype and restrictions as you do in sqlite seprated by ', '\n").split(", ")
        asqlobj.createTable(name, columndetails)
    elif choice == 2:
        name = raw_input("Enter the table name: ")
        columns = raw_input(
            "Enter columns in which you want to add values seprated by ', '\n").split(", ")
        values = raw_input(
            "Enter values for those column seprated by ', '\n").split(", ")
        asqlobj.insertRow(name, columns, values)

    elif choice == 3:
        name = raw_input("Enter the table name: ")
        values = raw_input(
            "Enter column, value, column for search and its value in order seprated by whitespace\n").split()
        asqlobj.updateVal(name, values[0], values[1], values[2], values[3])
    elif choice == 4:
        name = raw_input("Enter the table name: ")
        asqlobj.dropTable(name)
    elif choice == 5:
        name = raw_input("Enter the table name: ")
        asqlobj.selectAll(name)
    else:
        asqlobj.quit()
        break
