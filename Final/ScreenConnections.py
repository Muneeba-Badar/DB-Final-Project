# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox, QLineEdit, QComboBox
import sys
import pyodbc
from datetime import datetime


# Replace these with your own database connection details
server = 'DESKTOP-V9ACGIC'
database = 'ACM'  # Name of your database
use_windows_authentication = True  # Set to True to use Windows Authentication

# Main Window Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("login.ui", self) # loads login ui
        self.setWindowTitle("Login") # Set window title
        self.setFixedSize(self.size()) #fixed size of screen
        self.show()
        self.populateComboBox(self.LoginBox)
    
    def populateComboBox(self, LoginBox):
        trying=f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

        connection = pyodbc.connect(trying)
        

        cursor = connection.cursor()
        cursor.execute("SELECT Type FROM UserType")
        data = cursor.fetchall()
        for row in data:
            self.LoginBox.addItem(row[0])
            
        connection.commit()
        connection.close()
       
        # Connecting button
        self.NextBtn.clicked.connect(self.Next)
        
        

        # Instances to store windows
        self.ground_manager_window = None
        self.flight_manager_window = None
        self.airport_manager_window=None
        self.aircraft_manager_window=None
        self.admin_window = None
    
    def Next(self):
        Username = self.Username.text()
        Password = self.Password.text()
        login_as = self.LoginBox.currentText()
        

        if not Username:
            self.showErrorMessage("Please enter a username.")
        elif not Password:
            self.showErrorMessage("Please enter a password.")
        elif Username and Password and login_as:
            if login_as == "Admin":
                print(login_as)
                if self.verifyAdminCredentials(Username, Password):
                    self.open_admin()
                    self.admin_window.viewAdmin()

                else:
                    self.showErrorMessage("Invalid Admin credentials.")
            elif login_as == "Ground Manager":
                if self.verifyGMCredentials(Username, Password):
                    self.open_ground_manager()
                else:
                    self.showErrorMessage("Invalid Ground Manager credentials.")
            elif login_as == "Flight Manager":
                if self.verifyFMCredentials(Username, Password):
                    self.open_flight_manager()
                else:
                    self.showErrorMessage("Invalid Flight Manager credentials.")
            elif login_as == "Airport Manager":
                if self.verifyAMCredentials(Username, Password):
                    self.open_airport_manager()
                else:
                    self.showErrorMessage("Invalid Airport Manager credentials.")
            elif login_as == "Aircraft Manager":
                if self.verifyAIRMCredentials(Username, Password):
                    self.open_aircraft_manager()
                else:
                    self.showErrorMessage("Invalid Aircraft Manager credentials.")
        

    def verifyAdminCredentials(self, username, password):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()

        # Check if provided credentials match Admin's records
        cursor.execute("""
            SELECT * FROM [User]
            WHERE Username = ? AND Password = ? AND UserTypeId = 1
        """, (username, password))
        admin_record = cursor.fetchone()

        if admin_record is not None:
            # Admin credentials are correct, now check if a special user exists
            special_user = 'special_user'
            special_password = 'special_password'
            cursor.execute("""
                SELECT * FROM [User]
                WHERE Username = ? AND Password = ?
            """, (special_user, special_password))

            # If the special user doesn't exist, create it
            if cursor.fetchone() is None:
                # Assuming 'Admin' is a role in your UserType table
                cursor.execute("""
                    INSERT INTO [User] (Username, Password, UserTypeId)
                    VALUES (?, ?, 1)
                """, (special_user, special_password))
                connection.commit()

        connection.close()
        return admin_record is not None

    
    def verifyGMCredentials(self, username, password):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        # Check if provided credentials match Admin's records
        cursor.execute("""
            SELECT * FROM [User]
            WHERE Username = ? AND Password = ? AND UserTypeId = 2
        """, (username, password))
        
        return cursor.fetchone() is not None
    
    def verifyAMCredentials(self, username, password):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        # Check if provided credentials match Admin's records
        cursor.execute("""
            SELECT * FROM [User]
            WHERE Username = ? AND Password = ? AND UserTypeId = 3
        """, (username, password))
        return cursor.fetchone() is not None
    def verifyAIRMCredentials(self, username, password):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        # Check if provided credentials match Admin's records
        cursor.execute("""
            SELECT * FROM [User]
            WHERE Username = ? AND Password = ? AND UserTypeId = 4
        """, (username, password))
        return cursor.fetchone() is not None
    def verifyFMCredentials(self, username, password):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        # Check if provided credentials match Admin's records
        cursor.execute("""
            SELECT * FROM [User]
            WHERE Username = ? AND Password = ? AND UserTypeId = 5
        """, (username, password))
        return cursor.fetchone() is not None

    def showErrorMessage(self, message):
        output = QMessageBox(self)
        output.setWindowTitle("ERROR")
        output.setText(message)
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Warning)
        output.exec()

    def open_ground_manager(self):   # This function creates
        if not self.ground_manager_window:  # Check if the window instance exists
            self.ground_manager_window = GroundManagerWindow()  # Create if it doesn't exist
        self.hide()  # Hides the login window
        self.setFixedSize(self.size()) #fixed size of screen
        self.ground_manager_window.show()  # Show the new window

    def open_flight_manager(self): 
        if not self.flight_manager_window: 
            self.flight_manager_window = FlightManagerWindow() 
        self.hide() 
        self.setFixedSize(self.size()) #fixed size of screen
        self.flight_manager_window.show()  
 
    def open_admin(self):
        if not self.admin_window: 
            self.admin_window = AdminWindow() 
        self.hide() 
        self.setFixedSize(self.size()) #fixed size of screen
        self.admin_window.show()

    def open_airport_manager(self):
        if not self.flight_manager_window: 
            self.airport_manager_window = AirportManagerWindow() 
        self.hide() 
        self.setFixedSize(self.size()) #fixed size of screen
        self.airport_manager_window.show()  

    def open_aircraft_manager(self):
        if not self.aircraft_manager_window:
              self.aircraft_manager_window = AircraftManagerWindow()
        self.hide()
        self.setFixedSize(self.size()) #fixed size of screen
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
        self.TAddBtn.clicked.connect(self.addTerminal)
        self.TBackBtn.clicked.connect(self.open_ground_manager)
        self.DeleteBtn.clicked.connect(self.deleteTerminal)
        self.viewTerminal()  # Fetch and display data when the window is initialized

    def open_ground_manager(self):  #called when back button pressed
        self.hide()
        self.ground_window = GroundManagerWindow()
        self.ground_window.show()

    def addTerminal(self):   #When add button pressed, information is stored in the table
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Termial
        ([TerminalNumber])
        VALUES (?)
        """
        TerminalNum_2 = self.TerminalNum_2.text()  #Stores Terminal Number
        sql_query_check_existing = "SELECT COUNT(*) FROM Termial WHERE TerminalNumber = ?"
        # Check if the terminal with the same number already exists
        cursor.execute(sql_query_check_existing, (TerminalNum_2,))
        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("Terminal with the given number already exists.")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning)
            output.exec()
        else:
            cursor.execute(sql_query, (TerminalNum_2))
            connection.commit()
            self.TerminalTable.clearContents()
            cursor.execute("select * from Termial")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.TerminalTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.TerminalTable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
            
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Terminal added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
            
    def deleteTerminal(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.TerminalTable.currentRow()
        
        if DelRow > -1:
            currentterminalid = (self.TerminalTable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM Termial
            WHERE TerminalId = ?
            """
            cursor.execute(sql_query, (currentterminalid[0],))
            connection.commit()
            self.TerminalTable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Terminal Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
            
        elif DelRow < 0:
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()

        
    def viewTerminal(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.TerminalTable.clearContents()
        cursor.execute("select * from Termial")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.TerminalTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.TerminalTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()

class RunwayWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(RunwayWindow, self).__init__()
        uic.loadUi("Runway.ui", self)
        self.setWindowTitle("Runway")
        self.show()
        self.RAddBtn.clicked.connect(self.addRunway)
        self.RBackBtn.clicked.connect(self.open_ground_manager)
        self.RDeleteBtn.clicked.connect(self.deleteRunway)
        self.viewRunway()  # Fetch and display data when the window is initialized

    def addRunway(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Runway
        ([RunwayNumber], [RunwayLength])
        VALUES (?, ?)
        """
                
        RunwayNum = self.RunwayNum.text()
        RunwayLen = self.RunwayLen.text()
        sql_query_check_existing = "SELECT COUNT(*) FROM Runway WHERE RunwayNumber = ?"
         # Check if the runway with the same number already exists
        cursor.execute(sql_query_check_existing, (RunwayNum,))
        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("Runway with the given number already exists.")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning)
            output.exec()
        elif not(RunwayNum.isnumeric() and RunwayLen.isnumeric()):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Numeric values only")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:
            cursor.execute(sql_query, (RunwayNum, RunwayLen))
            connection.commit()
            self.RunwayTable.clearContents()
            cursor.execute("select * from Runway")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.RunwayTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.RunwayTable.setItem(row_index, col_index, item)
            connection.commit()
                
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Runway added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()

    def open_ground_manager(self):
        self.hide()
        self.ground_window = GroundManagerWindow()
        self.ground_window.show()
        
    def deleteRunway(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.RunwayTable.currentRow()
        if DelRow > -1:
            currentrunwayid = (self.RunwayTable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM Runway
            WHERE RunwayNumber = ?
            """
            cursor.execute(sql_query, (currentrunwayid[0],))
            connection.commit()
            self.RunwayTable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Runway Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
    def viewRunway(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.RunwayTable.clearContents()
        cursor.execute("select * from Runway")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.RunwayTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.RunwayTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        

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
        self.flightStatus_window = flightStatusWindow()
        self.flightStatus_window.show()
    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
        


class FlightWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(FlightWindow, self).__init__()
        uic.loadUi("flight.ui", self)
        self.setWindowTitle("Flight")
        self.flightBack.clicked.connect(self.open_flight_manager)
        self.flightAddBtn.clicked.connect(self.addFlight)
        # self.flightView.clicked.connect(self.viewFlight)
        self.populate_combobox(self.RunwayNumber)
        self.populateDestination(self.DestinationTo)
        self.populateArrival(self.ArrivalFrom)
        self.populateTerminal(self.TerminalNumber)
        self.populateGate(self.GateNumber)
        self.populateFlightStatus(self.FlightStatus)
        self.populateFlightType(self.FlightType)
        self.populateAicraftName(self.AircraftName)
        self.show()
        self.viewFlight()


    def open_flight_manager(self):
        self.hide()
        self.ground_window = FlightManagerWindow()
        self.ground_window.show()

    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()

    def populate_combobox(self, RunwayNumber):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.RunwayNumber.clear()
        cursor=connection.cursor()
        cursor.execute("Select RunwayNumber from Runway")
        data=cursor.fetchall()
        for row in data:
            self.RunwayNumber.addItem(str(row[0]))
        connection.commit()
        connection.close()
    ##POPULATING DEPARTURE:
    def populateDestination(self, DestinationTo):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.DestinationTo.clear()
        cursor=connection.cursor()
        cursor.execute("Select City from Airports")
        data=cursor.fetchall()
        for row in data:
            self.DestinationTo.addItem(str(row[0]))
        connection.commit()
        connection.close()

    ## POPULATE ARRIVAL
    def populateArrival(self, ArrivalFrom):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.ArrivalFrom.clear()
        cursor=connection.cursor()
        cursor.execute("Select City from Airports")
        data=cursor.fetchall()
        for row in data:
            self.ArrivalFrom.addItem(str(row[0]))
        connection.commit()
        connection.close()

    ## POPULATE TERMINAL NUMBER
    def populateTerminal(self, TerminalNumber):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.TerminalNumber.clear()
        cursor=connection.cursor()
        cursor.execute("Select TerminalNumber from Termial")
        data=cursor.fetchall()
        for row in data:
            self.TerminalNumber.addItem(str(row[0]))
        connection.commit()
        connection.close()

    ## POPULATE GATE:
    def populateGate(self,GateNumber):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.GateNumber.clear()
        cursor=connection.cursor()
        cursor.execute("Select GateName from Gate")
        data=cursor.fetchall()
        for row in data:
            self.GateNumber.addItem(str(row[0]))
        connection.commit()
        connection.close()

    ## populate flight type 
    def populateFlightStatus(self,FlightStatus):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.FlightStatus.clear()
        cursor=connection.cursor()
        cursor.execute("Select FlightStatus from FlightStatusTable")
        data=cursor.fetchall()
        for row in data:
            self.FlightStatus.addItem(str(row[0]))
        connection.commit()
        connection.close()
    
    def populateFlightType(self,FlightType):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.FlightType.clear()
        cursor=connection.cursor()
        cursor.execute("Select TypeName from FlightType")
        data=cursor.fetchall()
        for row in data:
            self.FlightType.addItem(str(row[0]))
        connection.commit()
        connection.close()

    def populateAicraftName(self,AircraftName):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.AircraftName.clear()
        cursor=connection.cursor()
        cursor.execute("Select Name from Aircraft")
        data=cursor.fetchall()
        for row in data:
            self.AircraftName.addItem(str(row[0]))
        connection.commit()
        connection.close()
    
    def addFlight(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
 
        sqlquery = """
            INSERT INTO Flights (
                [FlightNo], [Date], [Time], [TailNumber], [FlightStatusId],
                [RumwayID], [TerminalID], [DestinationTo], [ArrivalFrom],
                [FlightTypeID], [GateID], [IsDomestic]
            )
            VALUES (
                ?, ?, ?, 
                (SELECT TOP 1 TailNumber FROM Aircraft WHERE Name = ? COLLATE SQL_Latin1_General_CP1_CS_AS),

                (SELECT TOP 1 FlightStatudID FROM FlightStatusTable WHERE FlightStatus = ?),
                (SELECT TOP 1 RunwayId FROM Runway WHERE RunwayNumber = ?),
                (SELECT TOP 1 TerminalId FROM Termial WHERE TerminalNumber = ?),
                (SELECT TOP 1 AirportID FROM Airports WHERE City = ?),
                (SELECT TOP 1 AirportID FROM Airports WHERE City = ?),
                (SELECT TOP 1 TypeID FROM FlightType WHERE TypeName = ?),
                (SELECT TOP 1 GateID FROM Gate WHERE GateName = ?),

                ?
            )
        """
       
        flightNo=self.FlightNo.text()
        date=self.Date.text()
        time=self.Time.text()
        flightto=self.DestinationTo.currentText()
        arrival=self.ArrivalFrom.currentText()
        tailno=self.AircraftName.currentText()
        flightStatus=self.FlightStatus.currentText()
        runwayno=self.RunwayNumber.currentText()
        terminalno=self.TerminalNumber.currentText()
        flightType=self.FlightType.currentText()
        gateno=self.GateNumber.currentText()
        isDomestic=self.yes.isChecked()
        cursor.execute("SELECT * FROM Flights WHERE flightNo = ?", (flightNo,))
        existing_airport = cursor.fetchone()

        if existing_airport:
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("Flight with the same number already exists!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
            return
       
        if not (flightNo, date, time, tailno, flightStatus, runwayno, terminalno, flightto, arrival, flightType, gateno, isDomestic):
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("You haven't entered all the details yet!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning)
            output.exec()


        ##Flight no cannot be anything other than int

        if not flightNo.isdigit():
            self.showValidationError("Flight number should be an integer.")
            return
        
        ## arrival and destination cannot be same
        if flightto==arrival:
            self.showValidationError("Arrival and Destination cannot be same.")
            return 
        
        if not(self.yes.isChecked() or self.no.isChecked()):
            self.showValidationError("Is flight Domestic?")
            return

        if not (flightNo, date, time, tailno, flightStatus, runwayno, terminalno, flightto, arrival, flightType, gateno, isDomestic):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("You haven't entered all the details yet!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()    
        else:
            cursor.execute(sqlquery, (flightNo, date, time, tailno, flightStatus, runwayno, terminalno, flightto, arrival, flightType, gateno, isDomestic))
            connection.commit()
            row_index = self.FDtable.rowCount()
            self.FDtable.insertRow(row_index)
            # item1 = QTableWidgetItem(flightNo)
            # item2 = QTableWidgetItem(date)
            # item3 = QTableWidgetItem(time)
            # item4 = QTableWidgetItem(tailno)
            # item5 = QTableWidgetItem(flightStatus)
            # item6 = QTableWidgetItem(runwayno)
            # item7 = QTableWidgetItem(terminalno)
            # item8 = QTableWidgetItem(flightto)
            # item9 = QTableWidgetItem(arrival)
            # item10 = QTableWidgetItem(flightType)
            # item11 = QTableWidgetItem(gateno)
            
    
            # self.FDtable.setItem(row_index, 1, item1) 
            # self.FDtable.setItem(row_index, 2, item2) 
            # self.FDtable.setItem(row_index, 3, item3) 
            # self.FDtable.setItem(row_index, 4, item4) 
            # self.FDtable.setItem(row_index, 5, item5) 
            # self.FDtable.setItem(row_index, 6, item6) 
            # self.FDtable.setItem(row_index, 7, item7) 
            # self.FDtable.setItem(row_index, 8, item8) 
            # self.FDtable.setItem(row_index, 9, item9) 
            # self.FDtable.setItem(row_index, 10, item10) 
            # self.FDtable.setItem(row_index, 11, item11) 
            # if isDomestic:
            #     domestic_item = QTableWidgetItem('yes')
            #     self.FDtable.setItem(row_index, 12, domestic_item)
            # else:
            #     international_item = QTableWidgetItem('no')
            #     self.FDtable.setItem(row_index, 12, international_item)
            self.FDtable.clearContents()
            cursor.execute("select * from Flights")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.FDtable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.FDtable.setItem(row_index, col_index, item)

            connection.commit()
            connection.close()
            
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Flight added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
        



    def showValidationError(self, message):
        output = QMessageBox(self)
        output.setWindowTitle("Validation Error")
        output.setText(message)
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Warning)
        output.exec()
    

    def viewFlight(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.FDtable.clearContents()
        cursor.execute("select * from Flights")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.FDtable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.FDtable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()

        
    
class flightTypeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(flightTypeWindow, self).__init__()
        uic.loadUi("flight type.ui", self)
        self.setWindowTitle("Flight Type")
        self.flightTypeBack.clicked.connect(self.open_flight_manager)
        self.FlightTypeAdd.clicked.connect(self.add_flightType)
        self.FTdel.clicked.connect(self.deleteFT)
        self.show()
        self.viewFT()
    def open_flight_manager(self):
        self.hide()
        self.ground_window=FlightManagerWindow()
        self.ground_window.show()
    def add_flightType(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO FlightType
        ([TypeName])
        VALUES (?)
        """
        
        FlightType = self.FlightType.text()
        
        if not (FlightType):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("You haven't entered all the details yet!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
            
        else:
            cursor.execute(sql_query, (FlightType))
            connection.commit()
            self.FTtable.clearContents()
            cursor.execute("select * from FlightType")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.FTtable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.FTtable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
            
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Flight Type added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()

    def deleteFT(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.FTtable.currentRow()
        if DelRow > -1:
            currentflighttypeid = (self.FTtable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM FlightType
            WHERE TypeName = ?
            """
            cursor.execute(sql_query, (currentflighttypeid[0],))
            connection.commit()
            self.FTtable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Flight Type Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def viewFT(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.FTtable.clearContents()
        cursor.execute("select * from FlightType")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.FTtable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.FTtable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        
class flightStatusWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(flightStatusWindow, self).__init__()
        uic.loadUi("flight status .ui", self)
        self.setWindowTitle("Flight Status")
        self.flightStatusBack.clicked.connect(self.open_flight_manager)
        self.FlightStatusAdd.clicked.connect(self.add_flightStatus)
        self.DelFlightS.clicked.connect(self.del_flightStatus)
        # self.flightStatusView.clicked.connect(self.viewFS)
        self.show()
        self.viewFS()
    def open_flight_manager(self):
        self.hide()
        self.ground_window=FlightManagerWindow()
        self.ground_window.show()
    def add_flightStatus(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO FlightStatusTable
        ([FlightStatus])
        VALUES (?)
        """
        
        FlightStatus = self.FlightStatus.text()
        
        if not (FlightStatus):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("You haven't entered all the details yet!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:    
            cursor.execute(sql_query, (FlightStatus))
            connection.commit()
            self.FStable.clearContents()
            cursor.execute("select * from FlightStatusTable")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.FStable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.FStable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
            
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Flight Status added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
            
    def del_flightStatus(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.FStable.currentRow()
        if DelRow > -1:
            currentflightstatid = (self.FStable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM FlightStatusTable
            WHERE FlightStatus = ?
            """
            cursor.execute(sql_query, (currentflightstatid[0],))
            connection.commit()
            self.FStable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Flight Status Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def viewFS(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.FStable.clearContents()
        cursor.execute("select * from FlightStatusTable")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.FStable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.FStable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        

class AircraftManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftManagerWindow, self).__init__()
        uic.loadUi("AircraftManager.ui", self)
        self.setWindowTitle("Aircraft Manager")
        self.aircraftBtn.clicked.connect(self.open_aircraft)
        self.amBack.clicked.connect(self.open_main_window)
        self.aircraftTypebtn.clicked.connect(self.open_aircraftType)
        self.aircraftReport.clicked.connect(self.open_report)
        # self.show()
    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
    def open_aircraft(self):
        self.hide()
        self.aircraft_window=AircraftWindow()
        self.aircraft_window.show()
    def open_aircraftType(self):
        self.hide()
        self.aircraftType_window=AircraftTypeWindow()
        self.aircraftType_window.show()
    def open_report(self):
        self.hide()
        self.report_window=AircraftReportWindow()
        self.report_window.show()
class AircraftReportWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftReportWindow, self).__init__()
        uic.loadUi("aircraftReport.ui", self)
        self.setWindowTitle("Aircraft Report")
        self.AirBack.clicked.connect(self.open_aircraftManager)
        self.AirView.clicked.connect(self.viewReport)
        self.populate_combobox(self.AirName)
        self.show()
    def populate_combobox(self, AirName):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.AirName.clear()
        cursor = connection.cursor()
        cursor.execute("SELECT Name FROM Aircraft group by Name")
        data = cursor.fetchall()
        for row in data:
            self.AirName.addItem(row[0])
            
        connection.commit()
        connection.close()
        
    def viewReport(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        AircraftName =  self.AirName.currentText()
        self.AirTable.clearContents()
        sql_query1 = """
        SELECT TailNumber, Name FROM Aircraft WHERE Name = ?
        """
        
        cursor.execute(sql_query1, (AircraftName))
        data1 = cursor.fetchall()

        for row_index, row_data in enumerate(data1):
            self.AirTable.insertRow(row_index)
            for col_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.AirTable.setItem(row_index, col_index, item)
        connection.close()
        
    def open_aircraftManager(self):
        self.hide()
        self.ground_window=AircraftManagerWindow()
        self.ground_window.show()
class AircraftWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftWindow, self).__init__()
        uic.loadUi("aircraft .ui", self)
        self.setWindowTitle("Aircraft")
        self.aircraftBack.clicked.connect(self.open_aircraftManager)
        self.ADadd.clicked.connect(self.addAircraft)
        self.ADdel.clicked.connect(self.deleteAircraft)
        # self.aircraftView.clicked.connect(self.viewAircraft)
        self.populateComboBoxAT(self.ATcb)
        self.populateComboBoxAN(self.ANcb)
        self.show()
        self.viewAircraft()
        
    def populateComboBoxAT(self, ATcb):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.ATcb.clear()
        cursor = connection.cursor()
        cursor.execute("select NameOfAircraft from AircraftType")
        data = cursor.fetchall()
        for row in data:
            self.ATcb.addItem(row[0])
            
        connection.commit()
        connection.close()
    def populateComboBoxAN(self, ANcb):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()

        cursor.execute("select AirlineName from Airline")
        data = cursor.fetchall()
        for row in data:
            self.ANcb.addItem(row[0])
            
        connection.commit()
        connection.close()
        self.show()
        
    def open_aircraftManager(self):
        self.hide()
        self.ground_window=AircraftManagerWindow()
        self.ground_window.show()
    def addAircraft(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        # TailNumber = self.TailNumber.text()
        Name = self.Name.text()
        AircraftTypeID = self.ATcb.currentText()
        Capacity = self.Capacity.text()
        AirlineId = self.ANcb.currentText()
        
        air_cursor = connection.cursor()
        air_cursor.execute("SELECT AirlineId FROM Airline WHERE AirlineName = ?", (AirlineId,))
        air = air_cursor.fetchone()
        
        atype_cursor = connection.cursor()
        atype_cursor.execute("SELECT AircraftTypeID FROM AircraftType WHERE NameOfAircraft = ?", (AircraftTypeID,))
        atype = atype_cursor.fetchone()
        
        # cursor.execute("SELECT COUNT(*) FROM Aircraft WHERE TailNumber = ?", (TailNumber,))
        # existing_count = cursor.fetchone()[0]

        # if existing_count > 0:
        #     output = QMessageBox(self)
        #     output.setWindowTitle("ERROR")
        #     output.setText("Aircraft with the given TailNumber already exists.")
        #     output.setStandardButtons(QMessageBox.StandardButton.Ok)
        #     output.setIcon(QMessageBox.Icon.Warning)
        #     output.exec()
        if not (Capacity.isnumeric()):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Capacity can only be a numeric value")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:   
            sql_query = """
            INSERT INTO Aircraft
            ([Name],[AircraftTypeID],[Capacity],[AirlineId])
            VALUES (?,?,?,?)
            """ 
            cursor.execute(sql_query, (Name, atype[0], Capacity, air[0]))
            connection.commit()
            self.ADtable.clearContents()
            cursor.execute("select * from Aircraft")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.ADtable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.ADtable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
        
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Aircraft added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def deleteAircraft(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.ADtable.currentRow()
        if DelRow > -1:
            currentaircraftid = (self.ADtable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM Aircraft
            WHERE TailNumber = ?
            """
            cursor.execute(sql_query, (currentaircraftid[0],))
            connection.commit()
            self.ADtable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Aircraft Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def viewAircraft(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.ADtable.clearContents()
        cursor.execute("select * from Aircraft")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ADtable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ADtable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        

class AircraftTypeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftTypeWindow, self).__init__()
        uic.loadUi("aircraft type.ui", self)
        self.setWindowTitle("Aircraft Type")
        self.aircraftTypeBack.clicked.connect(self.open_aircraftManager)
        self.ATadd.clicked.connect(self.addAircraftType)
        self.ATdel.clicked.connect(self.deleteAircraftType)
        self.show()
        self.viewAircraftType()
    
    def open_aircraftManager(self):
        self.hide()
        self.ground_window=AircraftManagerWindow()
        self.ground_window.show()
    def addAircraftType(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO AircraftType
        ([NameOfAircraft])
        VALUES (?)
        """
        Type = self.AircraftType.text()
        cursor.execute(sql_query, (Type,))
        connection.commit()
        self.ATtable.clearContents()
        cursor.execute("select * from AircraftType")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ATtable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ATtable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        
        output = QMessageBox(self)              
        output.setWindowTitle("Success") 
        output.setText("Aircraft added successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def deleteAircraftType(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.ATtable.currentRow()
        if DelRow > -1:
            currentaircrafttypeid = (self.ATtable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM AircraftType
            WHERE AircraftTypeId = ?
            """
            cursor.execute(sql_query, (currentaircrafttypeid[0],))
            connection.commit()
            self.ATtable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Aircraft Type Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
    def viewAircraftType(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.ATtable.clearContents()
        cursor.execute("select * from AircraftType")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.ATtable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.ATtable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()

class AirportManagerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AirportManagerWindow, self).__init__()
        uic.loadUi("airportManager.ui", self)
        self.setWindowTitle("Flight Manager")
        self.airportManagerBack.clicked.connect(self.open_main_window)
        self.airportBtn.clicked.connect(self.open_airport)
        self.airlineBtn.clicked.connect(self.open_airline)

        # self.show()
    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
    def open_airport(self):
        self.hide()
        self.ground_window=airportWindow()
        self.ground_window.show()
    def open_airline(self):
        self.hide()
        self.ground_window=airlineWindow()
        self.ground_window.show()

class airportWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(airportWindow, self).__init__()
        uic.loadUi("airport.ui", self)
        self.setWindowTitle("Airport")
        self.airportBack.clicked.connect(self.open_airportManager)
        self.Add.clicked.connect(self.addAirport)
        self.Delete.clicked.connect(self.deleteAirport)
        self.airportView.clicked.connect(self.viewAirport)
        self.populateComboBoxCo(self.CountryCB)
        self.CountryCB.currentIndexChanged.connect(self.populateComboBoxCi)
        self.populateComboBoxCi(self.CityCB)
        self.show()
        self.viewAirport()
    
    def populateComboBoxCo(self, CountryCB):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.CountryCB.clear()
        cursor = connection.cursor()
        cursor.execute("SELECT  CountryName FROM Country")
        data = cursor.fetchall()
        for row in data:
            self.CountryCB.addItem(row[0])
            
        connection.commit()
        connection.close()
    def populateComboBoxCi(self, CityCB):
        selected_country = self.CountryCB.currentText()
        self.CityCB.clear()
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()

        cursor.execute("""select CountryID from Country where CountryName = ?""", (selected_country,))
        CountryID = cursor.fetchone()

        cursor.execute("SELECT CityName FROM City WHERE CountryID = ?", (CountryID[0],))
        data = cursor.fetchall()
        for row in data:
            self.CityCB.addItem(row[0])
            
        connection.commit()
        connection.close()
        
    def open_airportManager(self):
        self.hide()
        self.ground_window=AirportManagerWindow()
        self.ground_window.show()
    def addAirport(self):
        AirportName = self.AirportName.text()
        Country = self.CountryCB.currentText()
        City = self.CityCB.currentText()
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
         # Check if the airport with the same name already exists
        cursor.execute("SELECT * FROM Airports WHERE AirportName = ?", (AirportName,))
        existing_airport = cursor.fetchone()

        if existing_airport:
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("Airport with the same name already exists!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        else:
            sql_query = """
            INSERT INTO Airports
            ([AirportName],[City],[Country])
            VALUES (?,?,?)
            """
            
            cursor.execute(sql_query, (AirportName, Country, City))
            connection.commit()
            self.AirportTable.clearContents()
            cursor.execute("select * from Airports")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.AirportTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.AirportTable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
            
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Airport added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
    
    def deleteAirport(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.AirportTable.currentRow()
        if DelRow > -1:
            currentairportid = (self.AirportTable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM Airports
            WHERE AirportName = ?
            """
            cursor.execute(sql_query, (currentairportid[0],))
            connection.commit()
            self.AirportTable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Airport Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def viewAirport(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.AirportTable.clearContents()
        cursor.execute("select * from Airports")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.AirportTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.AirportTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        
class airlineWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(airlineWindow, self).__init__()
        uic.loadUi("airline.ui", self)
        self.setWindowTitle("Airline")
        self.addAircraft_2.clicked.connect(self.open_airportManager)
        self.addAirline.clicked.connect(self.add_airline)
        self.deleteAirline.clicked.connect(self.delete_airline)
        self.viewAircraftBtn.clicked.connect(self.view_airline)
        self.populateComboBoxCo(self.HQCountry)
        self.HQCountry.currentIndexChanged.connect(self.populateComboBoxCi)
        self.populateComboBoxCi(self.HQCity)
        self.show()
        self.view_airline()
    def open_airportManager(self):
        self.hide()
        self.ground_window=AirportManagerWindow()
        self.ground_window.show()
#####################################################################   
    def populateComboBoxCo(self, HQCountry):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        self.HQCountry.clear()
        cursor = connection.cursor()
        cursor.execute("SELECT  CountryName FROM Country")
        data = cursor.fetchall()
        for row in data:
            self.HQCountry.addItem(row[0])
            
        connection.commit()
        connection.close()
##################################################################
    def populateComboBoxCi(self, HQCity):
        selected_country = self.HQCountry.currentText()
        self.HQCity.clear()
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()

        cursor.execute("""select CountryID from Country where CountryName = ?""", (selected_country,))
        CountryID = cursor.fetchone()

        cursor.execute("SELECT CityName FROM City WHERE CountryID = ?", (CountryID[0],))
        data = cursor.fetchall()
        for row in data:
            self.HQCity.addItem(row[0])
            
        connection.commit()
        connection.close()
        
    def add_airline(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Airline
        ([AirlineName],[ContactPerson],[Phone], [Email], [HeadquarterCity], [HeadquarterCountry])
        VALUES (?,?,?,?,?,?)
        """
        
        AirlineName = self.AirlineName.text()
        ContactP = self.ContactPerson.text()
        Phone = self.Phone.text()
        Email = self.Email.text()
        Country = self.HQCountry.currentText()
        City = self.HQCity.currentText()
        
        # Check if the airline with the same name already exists
        cursor.execute("SELECT * FROM Airline WHERE AirlineName = ?", (AirlineName,))
        existing_airline = cursor.fetchone()

        if existing_airline:
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("Airline with the same name already exists!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif not (AirlineName and ContactP and Phone and Email and Country and City):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Kindly fill all attributes!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        else:
            cursor.execute(sql_query, (AirlineName, ContactP, Phone, Email, City, Country))
            connection.commit()
            self.AirlineTable.clearContents()
            cursor.execute("select * from Airline")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.AirlineTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.AirlineTable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
            
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Airline added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def delete_airline(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.AirlineTable.currentRow()
        if DelRow > -1:
            currentairlineid = (self.AirlineTable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM Airline
            WHERE AirlineId = ?
            """
            cursor.execute(sql_query, (currentairlineid[0],))
            connection.commit()
            self.AirlineTable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Airline Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def view_airline(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.AirlineTable.clearContents()
        cursor.execute("select * from Airline")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.AirlineTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.AirlineTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AdminWindow, self).__init__()
        uic.loadUi("admin.ui", self)
        self.setWindowTitle("Admin")
        self.show()
        self.AAddBtn.clicked.connect(self.addUser)
        self.ABackBtn.clicked.connect(self.open_main_window)
        # self.AViewBtn.clicked.connect(self.viewAdmin)
        self.populateComboBox(self.Role)
        self.ADelBtn.clicked.connect(self.deleteUser)
    
    def populateComboBox(self, Role):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT Type FROM UserType")
        data = cursor.fetchall()
        for row in data:
            self.Role.addItem(row[0])
            
        connection.commit()
        connection.close()
        
    def addUser(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()

        username = self.Username.text()
        password = self.Password.text()
        confirm = self.ConfirmPassword.text()
        role = self.Role.currentText()

        if not (username and password and confirm and role):
            self.showErrorMessage("Please fill in all details.")
        elif password != confirm:
            self.showErrorMessage("Passwords do not match.")
        else:
            # Fetch the UserTypeId based on the selected role
            cursor.execute("""SELECT UserTypeId FROM UserType WHERE Type = ?""", (role,))
            roleID = cursor.fetchone()

            if roleID is not None:
                # Insert the new user into the database with the retrieved UserTypeId
                cursor.execute("""
                    INSERT INTO [User] (username, password, UserTypeId)
                    VALUES (?, ?, ?)
                """, (username, password, roleID[0]))
                print("User added successfully!")

                connection.commit()

                self.showSuccessMessage("User added successfully!")

                # Automatically refresh the table after adding a user
                self.viewAdmin()
            else:
                self.showErrorMessage("Invalid role. User not added.")

        connection.close()


    def showErrorMessage(self, message):
        output = QMessageBox(self)
        output.setWindowTitle("ERROR")
        output.setText(message)
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Warning)
        output.exec()

    def showSuccessMessage(self, message):
        output = QMessageBox(self)
        output.setWindowTitle("Success")
        output.setText(message)
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()

    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
    
    def viewAdmin(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.AdminTable.clearContents()
        cursor.execute("select * from [User]")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.AdminTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.AdminTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        
    def deleteUser(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.AdminTable.currentRow()
        if DelRow > -1:
            currentadminid = (self.AdminTable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM [User]
            WHERE id = ?
            """
            cursor.execute(sql_query, (currentadminid[0],))
            connection.commit()
            self.AdminTable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("User Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()

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
        self.GDeleteBtn.clicked.connect(self.deleteGate)
        self.viewGate()  # Fetch and display data when the window is initialized

    def add_gate(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Gate
        ([GateName])
        VALUES (?)
        """
        
        GateNum = self.GateNum.text()
        sql_query_check_existing = "SELECT COUNT(*) FROM Gate WHERE GateName = ?"

        # Check if the gate with the same name already exists
        cursor.execute(sql_query_check_existing, (GateNum,))
        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            output = QMessageBox(self)
            output.setWindowTitle("ERROR")
            output.setText("Gate with the given name already exists.")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning)
            output.exec()
        else:
            cursor.execute(sql_query, (GateNum))
            connection.commit()
            self.GateTable.clearContents()
            cursor.execute("select * from Gate")
            # Fetch all rows and populate the table
            for row_index, row_data in enumerate(cursor.fetchall()):
                self.GateTable.insertRow(row_index)
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.GateTable.setItem(row_index, col_index, item)
            connection.commit()
            connection.close()
        
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Gate added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()

    def open_ground_manager(self):
        self.hide()
        self.ground_window = GroundManagerWindow()
        self.ground_window.show()
        
    def deleteGate(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        DelRow = self.GateTable.currentRow()
        if DelRow > -1:
            currentgateid = (self.GateTable.item(DelRow, 0).text(), )
            sql_query = """
            DELETE FROM Gate
            WHERE GateName = ?
            """
            cursor.execute(sql_query, (currentgateid[0],))
            connection.commit()
            self.GateTable.removeRow(DelRow)
            connection.close()
            output = QMessageBox(self)              
            output.setWindowTitle("Success") 
            output.setText("Gate Deleted successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        elif DelRow < 0 :
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR!") 
            output.setText("Please select a row to delete")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            output.exec()
        
    def viewGate(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        self.GateTable.clearContents()
        cursor.execute("select * from Gate")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.GateTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.GateTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        
        
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()