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
        uic.loadUi("login.ui", self) # loads login ui
        self.setWindowTitle("Login") # Set window title
        self.show()
       
        # Connecting button
        self.NextBtn.clicked.connect(self.Next)
        # Add users to combo box
        self.LoginBox.addItem("Ground Manager")
        self.LoginBox.addItem("Flight Manager")
        self.LoginBox.addItem("Airport Manager")
        self.LoginBox.addItem("Aircraft Manager")
        self.LoginBox.addItem("Admin")

        # Instances to store windows
        self.ground_manager_window = None
        self.flight_manager_window = None
        self.airport_manager_window=None
        self.aircraft_manager_window=None
        self.admin_window = None

    def Next(self):   #When the next button is clicked on the login screen
        
        Username = self.Username.text() # Getting username text
        Password = self.Password.text() # Getting password text
        login_as = self.LoginBox.currentText() # See which user is logging in

        if not Username:    # If no username is not typed, error message will apear
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Username")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()     
        elif not Password:    # If no password is not typed, error message will apear
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Password")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        if Username and Password and login_as:    # If username and passwords accepetd
            if login_as == "Ground Manager":
                self.open_ground_manager()  # calls the open_ground_manager func
            elif login_as == "Flight Manager":
                self.open_flight_manager()  # calls the open_flight_manager func
            elif login_as == "Admin":
                self.open_admin()
            elif login_as == "Airport Manager":
                self.open_airport_manager()
            elif login_as == "Aircraft Manager":
                self.open_aircraft_manager()

    def open_ground_manager(self):   # This function creates
        if not self.ground_manager_window:  # Check if the window instance exists
            self.ground_manager_window = GroundManagerWindow()  # Create if it doesn't exist
        self.hide()  # Hides the login window
        self.ground_manager_window.show()  # Show the new window

    def open_flight_manager(self): 
        if not self.flight_manager_window: 
            self.flight_manager_window = FlightManagerWindow() 
        self.hide() 
        self.flight_manager_window.show()  
 
    def open_admin(self):
        if not self.admin_window: 
            self.admin_window = AdminWindow() 
        self.hide() 
        self.admin_window.show()

    def open_airport_manager(self):
        if not self.flight_manager_window: 
            self.airport_manager_window = AirportManagerWindow() 
        self.hide() 
        self.airport_manager_window.show()  

    def open_aircraft_manager(self):
        if not self.aircraft_manager_window:
              self.aircraft_manager_window=AircraftManagerWindow()
        self.hide()
        self.aircraft_manager_window.show()  

class GroundManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GroundManagerWindow, self).__init__()
        uic.loadUi("GroundManager.ui", self)  # Opens the Groundmanager screen
        self.setWindowTitle("Ground Manager")
        self.show()
        self.TerminalBtn.clicked.connect(self.open_terminal)  #When Terminal button is clicked it opens the terminal
        self.RunwayBtn.clicked.connect(self.open_runway)
        self.GateBtn.clicked.connect(self.open_gate)
        self.GBackBtn.clicked.connect(self.open_main_window)  #Back button to go back to the login screen

    def open_terminal(self):  #Opens terminal screen
        self.hide()          #hides previous screen
        self.terminal_window = TerminalWindow() # creates terminal screen
        self.terminal_window.show() #shows the screen

    def open_runway(self):
        self.hide()
        self.runway_window = RunwayWindow()
        self.runway_window.show()

    def open_gate(self):
        self.hide()
        self.gate_window = GateWindow()
        self.gate_window.show()

    def open_main_window(self):  #called when back button is pressed
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()

class TerminalWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(TerminalWindow, self).__init__()
        uic.loadUi("terminal.ui", self)
        self.setWindowTitle("Terminal")
        self.show()
        self.TerminalNum.addItem("1")  #To test numbers were added in the combo box
        self.TerminalNum.addItem("2")
        self.TerminalNum.addItem("3")
        self.TerminalNum.addItem("4")
        self.TerminalNum.addItem("5")
        self.TAddBtn.clicked.connect(self.addTerminal)  #Add button is connected
        self.TBackBtn.clicked.connect(self.open_ground_manager)   #Back button is connected
        self.Terminal_ID = 1  #Shows terminal id in Table when pressed add button

    def open_ground_manager(self):  #called when back button pressed
        self.hide()
        self.ground_window = GroundManagerWindow()
        self.ground_window.show()

    def addTerminal(self):   #When add button pressed, information is stored in the table
        Terminal_num = self.TerminalNum.currentText()   #Stores Terminal Number
        row_count = self.TerminalTable.rowCount()   #Counts table rows
        self.TerminalTable.insertRow(row_count)   #insert rows
        item1 = QTableWidgetItem(str(self.Terminal_ID))  #sets TerminalID on auto increment as item
        item2 = QTableWidgetItem(Terminal_num)     #sets written Terminal Num as item
        self.TerminalTable.setItem(row_count, 0, item1 ) #inserts the data
        self.TerminalTable.setItem(row_count, 1, item2)
        self.Terminal_ID+=1  #increments Terminal id

class RunwayWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(RunwayWindow, self).__init__()
        uic.loadUi("Runway.ui", self)
        self.setWindowTitle("Runway")
        self.show()
        self.RAddBtn.clicked.connect(self.addRunway)
        self.RBackBtn.clicked.connect(self.open_ground_manager)
        self.Runway_ID = 1

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

    def open_ground_manager(self):
        self.hide()
        self.ground_window = GroundManagerWindow()
        self.ground_window.show()

class FlightManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FlightManagerWindow, self).__init__()
        uic.loadUi("FlightManager.ui", self)
        self.setWindowTitle("Flight Manager")
        self.show()
        self.FlightBtn.clicked.connect(self.open_flight)
        self.TypeBtn.clicked.connect(self.open_flightType)
        self.StatusBtn.clicked.connect(self.open_flightStatus)
        self.FMBackBtn.clicked.connect(self.open_main_window)

    def open_flight(self):
        self.hide()
        self.flight_window=FlightWindow()
        self.flight_window.show()
    def open_flightType(self):
        self.hide()
        self.flightType_window=flightTypeWindow()
        self.flightType_window.show()
    def open_flightStatus(self):
        self.hide()
        self.flightStatus_window=flightStatusWindow()
        self.flightStatus_window.show()
    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()

class FlightWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FlightWindow, self).__init__()
        uic.loadUi("flight .ui", self)
        self.setWindowTitle("Flight")
        self.show()


class flightTypeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(flightTypeWindow, self).__init__()
        uic.loadUi("flight type.ui", self)
        self.setWindowTitle("Flight Type")
        self.show()

class flightStatusWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(flightStatusWindow, self).__init__()
        uic.loadUi("flight status .ui", self)
        self.setWindowTitle("Flight Status")
        self.show()

class AircraftManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftManagerWindow, self).__init__()
        uic.loadUi("AircraftManager.ui", self)
        self.setWindowTitle("Aircraft Manager")
        self.show()
        self.aircraftBtn.clicked.connect(self.open_aircraft)
        self.aircraftTypebtn.clicked.connect(self.open_aircraftType)
    def open_aircraft(self):
         self.hide()
         self.aircraft_window=AircraftWindow()
         self.aircraft_window.show()
    def open_aircraftType(self):
         self.hide()
         self.aircraftType_window=AircraftTypeWindow()
         self.aircraftType_window.show()

class AircraftWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftWindow, self).__init__()
        uic.loadUi("aircraft .ui", self)
        self.setWindowTitle("Aircraft")
        self.show()
        
class AircraftTypeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftTypeWindow, self).__init__()
        uic.loadUi("aircraft type.ui", self)
        self.setWindowTitle("Aircraft Type")
        self.show()
        self.addType.clicked.connect(self.addType)
        
class AirportManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AirportManagerWindow, self).__init__()
        uic.loadUi("airportManager.ui", self)
        self.setWindowTitle("Airport Manager")
        self.show()

class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        uic.loadUi("admin.ui", self)
        self.setWindowTitle("Admin")
        self.show()
        self.AAddBtn.clicked.connect(self.addUser)
        self.ABackBtn.clicked.connect(self.open_main_window)
        # Add users to combo box
        self.Role.addItem("Ground Manager")
        self.Role.addItem("Flight Manager")
        self.Role.addItem("Airport Manager")
        self.Role.addItem("Aircraft Manager")
        self.Role.addItem("Admin")

    def addUser(self):
        username = self.Username.text()
        password = self.Password.text()
        confirm = self.ConfirmPassword.text()
        name = self.Name.text()
        role = self.Role.currentText()
        if not (username and password and confirm and name and role):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("You haven't entered all the details yet!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        elif password!=confirm:
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Passwords do not match")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        elif name and username and (password==confirm) and role:
            row_count = self.AdminTable.rowCount()
            self.AdminTable.insertRow(row_count)
            item1 = QTableWidgetItem(name)
            item2 = QTableWidgetItem(username)
            item3 = QTableWidgetItem(role)
            self.AdminTable.setItem(row_count, 0, item1 )
            self.AdminTable.setItem(row_count, 1, item2)
            self.AdminTable.setItem(row_count, 2, item3)

    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()

class GateWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(GateWindow, self).__init__()
        uic.loadUi("gate.ui", self)
        self.setWindowTitle("Gate")
        self.GAddBtn.clicked.connect(self.add_gate)
        self.show()
        self.GBackBtn.clicked.connect(self.open_ground_manager)

    def add_gate(self):
        GateNum = self.GateNum.text()
        if not(GateNum.isnumeric()):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Numeric values only")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:
            row_count = self.GateTable.rowCount()
            self.GateTable.insertRow(row_count)
            item1 = QTableWidgetItem(GateNum)
            self.GateTable.setItem(row_count, 0, item1)

    def open_ground_manager(self):
        self.hide()
        self.ground_window = GroundManagerWindow()
        self.ground_window.show()
        

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()