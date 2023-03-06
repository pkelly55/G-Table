"""Client Gui with pyqt5 and CRUD operations"""

import csv
import sys
import os 
import datetime
import time

from PyQt5 import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(700, 700, 300, 200)

        # Create the labels and text boxes for username and password
        self.username_label = QLabel('Username:', self)
        self.username_label.move(50, 50)
        self.username = QLineEdit(self)
        self.username.move(120, 50)
        self.username.resize(150, 20)

        self.password_label = QLabel('Password:', self)
        self.password_label.move(50, 80)
        self.password = QLineEdit(self)
        self.password.move(120, 80)
        self.password.resize(150, 20)
        self.password.setEchoMode(QLineEdit.Password)

        # Create the login button
        self.login_button = QPushButton('Login', self)
        self.login_button.move(120, 120)
        self.login_button.clicked.connect(self.login)

        self.show()

    def login(self):
        # Check if the username and password are correct
        # Here, you would need to write your own authentication code
        # This is just an example
        if self.username.text() == 'admin' and self.password.text() == 'password':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.undo_stack = []

    def initUI(self):
    # Create the red frame
        self.red_frame = QLabel(self)
        self.red_frame.setGeometry(100, 100, 200, 200)
        self.red_frame.setStyleSheet("background-color: blue;") 
        
        # Create the horizontal layout for the buttons
        self.hbox = QHBoxLayout()

        # Create the buttons for CRUD functions
        self.create_button = QPushButton('Create', self)
        self.read_button = QPushButton('Read', self)
        self.update_button = QPushButton('Update', self)
        self.delete_button = QPushButton('Delete', self)

        # Add the buttons to the horizontal layout
        self.hbox.addWidget(self.create_button)
        self.hbox.addWidget(self.read_button)
        self.hbox.addWidget(self.update_button)
        self.hbox.addWidget(self.delete_button)


        # Create the vertical layout for the red frame and buttons
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.red_frame)
        self.vbox.addLayout(self.hbox)

        # Set the layout of the main window to the vertical layout
        self.setLayout(self.vbox)
        # Window resize False
        self.setFixedSize(self.size())
        # Set the window title and size
        self.setWindowTitle('Client Manager')
        self.setGeometry(700, 550, 700, 550)

    # Text boxs for client information
        self.client_name = QLineEdit(self)
        self.client_name.move(20, 20)
        self.client_name.resize(280, 40)
    # Address
        self.client_address = QLineEdit(self)
        self.client_address.move(20, 60)
        self.client_address.resize(280, 40)
    # Phone
        self.client_phone = QLineEdit(self)
        self.client_phone.move(20, 100)
        self.client_phone.resize(280, 40)
    # Email
        self.client_email = QLineEdit(self)
        self.client_email.move(20, 140)
        self.client_email.resize(280, 40)
    #placeholder text
        self.client_name.setPlaceholderText("Client Name")
        self.client_address.setPlaceholderText("Client Address")
        self.client_phone.setPlaceholderText("Client Phone")
        self.client_email.setPlaceholderText("Client Email")
       
        # Drop down menu for client information
        self.client_name_drop = QComboBox(self)
        self.client_name_drop.move(300, 20)
        self.client_name_drop.resize(150, 40)

        # Add items to drop down menu
        self.client_name_drop.addItem("Client Name")
        self.client_name_drop.addItem("Client Address")
        self.client_name_drop.addItem("Client Phone")
        self.client_name_drop.addItem("Client Email")

        # Search button
        self.search_button = QPushButton('Search by #', self)
        self.search_button.move(300, 60)
        self.search_button.resize(150, 40)

        # Undo button
        self.undo_button = QPushButton('Undo', self)
        self.undo_button.move(300, 140)
        self.undo_button.resize(150, 40)

        # Sort button
        self.sort_button = QPushButton('Sort', self)
        self.sort_button.move(300, 100)
        self.sort_button.resize(150, 40)

        # Save button top Right
        self.save_button = QPushButton('Save', self)
        self.save_button.move(500, 20)
        self.save_button.resize(100, 40)
        # Load button top Right 
        self.load_button = QPushButton('Load', self)
        self.load_button.move(500, 60)
        self.load_button.resize(100, 40)


        # Create table to store client information
        self.table = QTableWidget(self)
        self.table.move(20, 180)
        self.table.resize(400, 200)
        # make table expandable
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Client Name", "Client Address", "Client Phone", "Client Email"))

        self.create_button.clicked.connect(self.add_client_info)
        self.read_button.clicked.connect(self.read_client_info)
        self.update_button.clicked.connect(self.update_client_info)
        self.delete_button.clicked.connect(self.delete_client_info)
        self.save_button.clicked.connect(self.save_data_to_file)
        self.load_button.clicked.connect(self.load_file)
        self.search_button.clicked.connect(self.search_client_info)
        self.undo_button.clicked.connect(self.undo_last_action)
        self.sort_button.clicked.connect(self.sort_client_info)
        # Add a box to display the client information when searched for using read button
        self.client_info = QTextEdit(self)
        self.client_info.move(450, 180)
        self.client_info.resize(150, 200)
        self.client_info.setReadOnly(True)

        self.show()
    def add_client_info(self):
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(self.client_name.text()))
        self.table.setItem(0, 1, QTableWidgetItem(self.client_address.text()))
        self.table.setItem(0, 2, QTableWidgetItem(self.client_phone.text()))
        self.table.setItem(0, 3, QTableWidgetItem(self.client_email.text()))
        self.show()
# View Client Information in Right Box
    def read_client_info(self):
        # Client name is the primary key
        client_name = self.client_name.text()
        # Search for client name in table
        
        for i in range(self.table.rowCount()):
            # If client name is found, display client information in client_info box
            if self.table.item(i, 0).text() == client_name:
                self.client_info.setText("Client Found")
                time.sleep(1)
                self.client_info.setText("Client Name: " + self.table.item(i, 0).text() + "\nClient Address: " + self.table.item(i, 1).text() + "\nClient Phone: " + self.table.item(i, 2).text() + "\nClient Email: " + self.table.item(i, 3).text())
    def update_client_info(self):
        # Client name is the primary key
        client_name = self.client_name.text()
        # Search for client name in table
        for i in range(self.table.rowCount()):
            # If client name is found, update client information
            if self.table.item(i, 0).text() == client_name:
                self.table.setItem(i, 0, QTableWidgetItem(self.client_name.text()))
                self.table.setItem(i, 1, QTableWidgetItem(self.client_address.text()))
                self.table.setItem(i, 2, QTableWidgetItem(self.client_phone.text()))
                self.table.setItem(i, 3, QTableWidgetItem(self.client_email.text()))
                self.client_info.setText("Client Name: " + self.table.item(i, 0).text() + "\nClient Address: " + self.table.item(i, 1).text() + "\nClient Phone: " + self.table.item(i, 2).text() + "\nClient Email: " + self.table.item(i, 3).text())
        self.show() 
    def delete_client_info(self):
        # Client name is the primary key
        client_name = self.client_name.text()
        # Search for client name in client names list
        print("pressed")
        for i in range(self.table.rowCount()):
            # If client name is found, delete client information
            if self.table.item(i, 0) is not None and self.table.item(i, 0).text() == client_name:

                print("found")
                
                self.table.removeRow(i)
                self.client_info.setText("Client Removed")                    
        self.show()

    def search_client_info(self):
        # Client phone number is the primary key
        client_phone = self.client_phone.text()
        # Search for client name in table
        for i in range(self.table.rowCount()):
            # If client name is found, display client information in client_info box
            if self.table.item(i, 2).text() == client_phone:
                self.client_info.setText("Client Found")
                time.sleep(1)
                self.client_info.setText("Client Name: " + self.table.item(i, 0).text() + "\nClient Address: " + self.table.item(i, 1).text() + "\nClient Phone: " + self.table.item(i, 2).text() + "\nClient Email: " + self.table.item(i, 3).text())

    # Sort the table by client name
    def sort_client_info(self):
    # get the column to sort by
        column = self.client_name_drop.currentIndex()
        # get the current sort order
        order = self.table.horizontalHeader().sortIndicatorOrder()
        # if the table is already sorted by that column, reverse the sort
        if self.table.horizontalHeader().sortIndicatorSection() == column:
            if order == Qt.AscendingOrder:
                order = Qt.DescendingOrder
            else:
                order = Qt.AscendingOrder
        # sort the table
        self.table.sortByColumn(column, order)
    # Undo the last action
    def undo_last_action(self):
        # Check if there is an action to undo
        if not self.undo_stack:
            return
        
        # Pop the last action from the undo stack
        last_action = self.undo_stack.pop()
        
        # Undo the action based on its type
        if last_action[0] == 'add_client':
            # Delete the row from the table
            self.table.removeRow(last_action[3])
        elif last_action[0] == 'delete_client':
            # Add the row back to the table
            client_name = last_action[1]
            row_index = last_action[2]
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, client_name)
    
    # Save the client information for next time the program is run
    
   

    def save_data_to_file(self):
        def save_data(filename, data):
            with open(filename, 'w') as file:
                writer = csv.writer(file)
                writer.writerows(data)
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            data.append(row_data)

        filename, _ = QFileDialog.getSaveFileName(self, "Save Data", "", "CSV Files (*.csv)")
        if filename:
            save_data(filename, data)

    
    

    # Load the client information from the file
   
    # Load data from table.csv to go back into table.
    # Pick file to load
    def load_file(self):
        # Load data from table.csv to go back into table.
        # Pick file to load
        filename, _ = QFileDialog.getOpenFileName(self, "Load Data", "", "CSV Files (*.csv)")
        if filename:
            # Open the file to read from
            with open(filename, 'r') as file:
                # Read the client information from the file
                rows = []
                for line in file:
                    # Strip any whitespace or newline characters
                    line = line.strip()
                    # Split the line into values using commas as the delimiter
                    values = line.split(',')
                    # Add the row of values to the list of rows
                    rows.append(values)

                # Set the number of rows and columns in the table
                num_rows = len(rows)
                num_columns = len(rows[0])
                self.table.setRowCount(num_rows)
                self.table.setColumnCount(num_columns)

                # Populate the table with the data from the file
                for i in range(num_rows):
                    for j in range(num_columns):
                        self.table.setItem(i, j, QTableWidgetItem(rows[i][j]))

        self.show()

    # When exit button is clicked, save the client information to a file
    def exit_button_clicked(self):
        self.save_data_to_file()
        self.close()

    # When the window is closed, save the client information to a file
    def closeEvent(self, event):
        self.save_data_to_file()
        event.accept()

    # When the window is opened, read the client information from the file
    def read_file(self):
        # Open the file to read from
        with open('client_info.txt', 'r') as file:
            # Read the number of rows and columns from the file
            rows, columns = file.readline().split()
            # Set the number of rows and columns in the table
            self.table.setRowCount(int(rows))
            self.table.setColumnCount(int(columns))
            # Read the client information from the file
            for i in range(int(rows)):
                for j in range(int(columns)):
                    self.table.setItem(i, j, QTableWidgetItem(file.readline().strip()))

    # When the window is opened, read the client information from the file
    def showEvent(self, event):
        self.read_file()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
