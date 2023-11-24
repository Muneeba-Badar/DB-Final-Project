# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox, QLineEdit
import sys
import pyodbc


# Replace these with your own database connection details
server = 'AMNAH'
database = 'AirportManagementSystem'  # Name of your database
use_windows_authentication = True  # Set to True to use Windows Authentication

# Main Window Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("login.ui", self)
        self.setWindowTitle("Login")
        self.show()
        # self.setStyleSheet("background-image: url('background.jpg');") 

        # Connecting button
        self.NextBtn.clicked.connect(self.Next)
        # Add items to combo box
        self.LoginBox.addItem("Ground Manager")
        self.LoginBox.addItem("Flight Manager")
        self.LoginBox.addItem("Airport Manager")
        self.LoginBox.addItem("Aircraft Manager")
        self.LoginBox.addItem("Admin")

        # Instances to store windows
        self.ground_manager_window = None
        self.flight_manager_window = None

    def Next(self):
        
        Username = self.Username.text()
        Password = self.Password.text()
        login_as = self.LoginBox.currentText()

        if not Username:
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Username")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec() 
        elif not Password:
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Password")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        if Username and Password and login_as:
            if login_as == "Ground Manager":
                        self.open_ground_manager()  # calls the open_ground_manager func
            elif login_as == "Flight Manager":
                        self.open_flight_manager()


    def open_ground_manager(self):
        if not self.ground_manager_window:  # Check if the window instance exists
            self.ground_manager_window = GroundManagerWindow()  # Create if it doesn't exist
        self.hide()  # Hides the login window
        self.ground_manager_window.show()  # Show the new window

    def open_flight_manager(self):
        if not self.flight_manager_window: 
            self.flight_manager_window = FlightManagerWindow() 
        self.hide() 
        self.flight_manager_window.show()  
 

class GroundManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GroundManagerWindow, self).__init__()
        uic.loadUi("GroundManager.ui", self)
        self.setWindowTitle("Ground Manager")
        self.show()
        self.TerminalBtn.clicked.connect(self.open_terminal)
        self.RunwayBtn.clicked.connect(self.open_runway)
        self.GateBtn.clicked.connect(self.open_gate)

    def open_terminal(self):
        self.hide() 
        self.terminal_window = TerminalWindow() 
        self.terminal_window.show() 

    def open_runway(self):
        self.hide()
        self.runway_window = RunwayWindow()
        self.runway_window.show()

    def open_gate(self):
        self.hide()
        self.gate_window = GateWindow()
        self.gate_window.show()

class FlightManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FlightManagerWindow, self).__init__()
        uic.loadUi("FlightManager.ui", self)
        self.setWindowTitle("Flight Manager")
        self.show()

class TerminalWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TerminalWindow, self).__init__()
        uic.loadUi("terminal.ui", self)
        self.setWindowTitle("Terminal")
        self.show()
        self.TerminalNum.addItem("1")
        self.TerminalNum.addItem("2")
        self.TerminalNum.addItem("3")
        self.TerminalNum.addItem("4")
        self.TerminalNum.addItem("5")
        self.TAddBtn.clicked.connect(self.addTerminal)
        self.Terminal_ID = 1
    
    def populate_terminal(self):
        server = 'AMNAH'
        database = 'AirportManagemnetSystem'  # Name of your Northwind database
        use_windows_authentication = False  # Set to True to use Windows Authentication
        username = 'sa'  # Specify a username if not using Windows Authentication
        password = 'Project_db23'  # Specify a password if not using Windows Authentication
        
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("select * from TerminalTable")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.orderTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.TerminalTable.setItem(row_index, col_index, item)
        connection.close()
        # Adjust content display
        header = self.orderTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    def addTerminal(self):
        Terminal_num = self.TerminalNum.currentText()
        row_count = self.TerminalTable.rowCount()
        self.TerminalTable.insertRow(row_count)
        item1 = QTableWidgetItem(str(self.Terminal_ID))
        item2 = QTableWidgetItem(Terminal_num)
        self.TerminalTable.setItem(row_count, 0, item1 )
        self.TerminalTable.setItem(row_count, 1, item2)
        self.Terminal_ID+=1
class RunwayWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(RunwayWindow, self).__init__()
        uic.loadUi("Runway.ui", self)
        self.setWindowTitle("Runway")
        self.show()
        self.RAddBtn.clicked.connect(self.addRunway)
        self.Runway_ID = 1
    def populate_runway(self):
        server = 'AMNAH'
        database = 'AirportManagemnetSystem'  # Name of your Northwind database
        use_windows_authentication = False  # Set to True to use Windows Authentication
        username = 'sa'  # Specify a username if not using Windows Authentication
        password = 'Project_db23'  # Specify a password if not using Windows Authentication
        
        if use_windows_authentication:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        else:
            connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("select * from RunwayTable")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.orderTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.TerminalTable.setItem(row_index, col_index, item)
        connection.close()
        # Adjust content display
        header = self.orderTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

    def addRunway(self):
        RunwayNum = self.RunwayNum.text()
        RunwayLen = self.RunwayLen.text()
        if not(RunwayNum.isnumeric() and RunwayLen.isnumeric()):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Numeric values only")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:
            row_count = self.RunwayTable.rowCount()
            self.RunwayTable.insertRow(row_count)
            item1 = QTableWidgetItem(str(self.Runway_ID))
            item2 = QTableWidgetItem(RunwayNum)
            item3 = QTableWidgetItem(RunwayLen)
            self.RunwayTable.setItem(row_count, 0, item1)
            self.RunwayTable.setItem(row_count, 1, item2)
            self.RunwayTable.setItem(row_count, 2, item3)

class GateWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GateWindow, self).__init__()
        uic.loadUi("gate.ui", self)
        self.setWindowTitle("Gate")
        self.show()
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()