#------------------------------------------# 
# Title: CDInventory.py 
# Desc: Script CDInventory with Structured Error Handling and Binary Data Storage
# Change Log: (Who, When, What) 
# DBiesinger, 2030-Jan-01, Created File #
# MYokus, 2021-Aug-22, Added Code 
#------------------------------------------#

import pickle
import os.path #Common pathname manipulation

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
read_FileName = ''  # data storage file to read from
save_FileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor: 
    """Processing the data in a 2D table (list of dicts)"""

    @staticmethod
    def add_to_table(inputs, table):
        """Function to add a list to a 2D table (list of dicts)
        
        Add user inputs (a list) to the main inventory table (list of dicts)
    
        Args:
            inputs (list): user inputs (ID, title, artist)
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None
        """
        try: 
            dicRow = {'ID': int(inputs[0]), 'Title': inputs[1], 'Artist': inputs[2]}
            table.append(dicRow)
        except ValueError as e:
            print('That is not an integer!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')

    @staticmethod
    def del_row(row_del, table):
        """ Function to delete a row in a 2D table

        Deletes an entry from the main inventory table (list of dicts)

        Args:
            row (int): the row number to be deleted
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == row_del:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from a binary file to a list of dictionaries

        Reads the data from a binary file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            data (list of dict): 2D data structure (list of dicts)
        """

        try:
            data = []
            with open(file_name, 'rb') as fileObj:
                data = pickle.load(fileObj)
            return data
        except FileNotFoundError as e:
            print('Binary file does not exist!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')

    @staticmethod
    def read_Textfile(file_name, table):
        """Function to manage data ingestion from a text file to a list of dictionaries

        Reads the data from a text file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """

        try:
            table.clear()  # this clears existing data and allows to load data from file
            objFile = open(file_name, 'r')
            for line in objFile:
                data = line.strip().split(',') # data type: list
                dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]} # data type: dictionary
                table.append(dicRow) # data type: list
            objFile.close()
        except FileNotFoundError as e:
            print('Text file does not exist!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')


    @staticmethod
    def write_file(file_name, table):
        """Function to save a 2D table (a list of dictionaries) to file via pickle

        Saves the data in a file identified by file_name into a .dat file

        Args:
            file_name (string): name of file used to save the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            with open(file_name, 'wb') as fileObj:
                pickle.dump(table, fileObj)
        except FileNotFoundError as e:
            print('Binary file does not exist!')
            print('Build in error info:')
            print(type(e), e, e.__doc__, sep='\n')


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']: # 'While not loop: executes the body of the loop until the condition for loop termination is met'
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def user_input():
        """ Ask user for new ID, CD Title, and Artist
        Args:
            None.

        Returns:
            a list of user inputs
        """
        
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return [strID, strTitle, stArtist]


# 1. When program starts, read in the currently saved Inventory
#FileProcessor.read_file(strFileName, lstTbl)
if os.path.isfile('CDInventory.dat'): # if "CDInventory.dat" exits, use function "read_file()"
    read_FileName = 'CDInventory.dat'
    lstTbl = FileProcessor.read_file(read_FileName)
else:                                 # if "CDInventory.txt" exits, use function "read_Textfile()"
    read_FileName = 'CDInventory.txt'
    FileProcessor.read_Textfile(read_FileName,lstTbl)


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled. ')
        if strYesNo.lower() == 'yes':
            print('\nreloading...')
            if os.path.isfile('CDInventory.dat'): # if "CDInventory.dat" exits, use function "read_file()"
                read_FileName = 'CDInventory.dat'
                lstTbl = FileProcessor.read_file(read_FileName)
            else:                                 # if "CDInventory.txt" exits, use function "read_Textfile()"
                read_FileName = 'CDInventory.txt'
                FileProcessor.read_Textfile(read_FileName,lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        inputs_list = IO.user_input() # a list of user inputs

        # 3.3.2 Add item to the table
        DataProcessor.add_to_table(inputs_list, lstTbl)
        print()
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl) 
        # 3.5.1.2 ask user which ID to remove
        intIDDel = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
        DataProcessor.del_row(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(save_FileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')

