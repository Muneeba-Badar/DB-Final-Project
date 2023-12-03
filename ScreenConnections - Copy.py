# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox, QLineEdit, QComboBox
import sys
import pyodbc
from datetime import datetime


# Replace these with your own database connection details
server = 'LAPTOP-CDQ2932B'
database = 'AMS'  # Name of your database
use_windows_authentication = True  # Set to True to use Windows Authentication

# Main Window Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("login.ui", self) # loads login ui
        self.setWindowTitle("Login") # Set window title
        self.setFixedSize(self.size()) #fixed size of screen
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
        self.TAddBtn.clicked.connect(self.addTerminal)  #Add button is connected
        self.TBackBtn.clicked.connect(self.open_ground_manager)   #Back button is connected
        self.DeleteBtn.clicked.connect(self.deleteTerminal)
        self.TViewBtn.clicked.connect(self.viewTerminal)

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
        
        if(TerminalNum_2.isnumeric() == False):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Numeric values only")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:
            cursor.execute(sql_query, (TerminalNum_2))
            connection.commit()
            
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
        
        DelTerminalNum = self.DelTerminalNum.text()
        
        sql_query = """
        DELETE FROM Termial
        WHERE TerminalNumber = ?
        """
        cursor.execute(sql_query, (DelTerminalNum))
        connection.commit()
        
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
        output.setText("Terminal Deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def viewTerminal(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
        self.RBackBtn.clicked.connect(self.deleteRunway)
        self.RViewBtn.clicked.connect(self.viewRunway)

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
        if not(RunwayNum.isnumeric() and RunwayLen.isnumeric()):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Please enter Numeric values only")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:
            cursor.execute(sql_query, (RunwayNum, RunwayLen))
            connection.commit()
            
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
        
        DelRunwayNum = self.DelRunwayNum.text()
        
        sql_query = """
        DELETE FROM Runway
        WHERE RunwayNumber = ?
        """
        cursor.execute(sql_query, (DelRunwayNum))
        connection.commit()
        
        cursor.execute("select * from Runway")
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.RunwayTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.RunwayTable.setItem(row_index, col_index, item)
        connection.commit()
        connection.close()
        
        output = QMessageBox(self)              
        output.setWindowTitle("Success") 
        output.setText("Runway Deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
    def viewRunway(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
        self.flightView.clicked.connect(self.viewFlight)
    def open_flight_manager(self):
        self.hide()
        self.ground_window = FlightManagerWindow()
        self.ground_window.show()
    def open_main_window(self):
        self.hide()
        self.main_window = MainWindow()
        self.main_window.show()
    def addFlight(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Flights
        ([FlightNo], [Date], [Time], [TailNumber], [FlightStatus], [RumwayID], [TerminalID], [DestinationTo], [ArrivalFrom], [FlightTypeID], [GateID], [IsDomestic])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
        """
        
        FlightNo = self.FlightNo.text()
        Date = self.Date.text()
        Date = datetime.strptime(Date, '%Y-%m-%d')
        Time = self.Time.text()
        Time = datetime.strptime(Time, '%H:%M')
        TailNumber = self.TailNumber.text()
        FlightStatus = self.FlightStatus.currentText()
        RunwayNumber = self.RunwayNumber.currentText()
        TerminalNumber = self.TerminalNumber.currentText()
        DestinationTo = self.DestinationTo.currentText()
        ArrivalFrom = self.ArrivalFrom.currentText()
        FlightType = self.FlightType.currentText()
        GateNumber = self.GateID.currentText()
        IsDomestic = self.IsDomestic.currentText()
        
        if not (FlightNo, Date, Time, TailNumber, FlightStatus, RunwayNumber, TerminalNumber, DestinationTo, ArrivalFrom, FlightType, GateNumber, IsDomestic):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("You haven't entered all the details yet!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        
        else:
            cursor.execute(sql_query, (FlightNo, Date, Time, TailNumber, FlightStatus, RunwayNumber, TerminalNumber, DestinationTo, ArrivalFrom, FlightType, GateNumber, IsDomestic))
            connection.commit()
            
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
            
    def viewFlight(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
        self.flightTypeView.clicked.connect(self.viewFT)
        self.show()
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
        
        delFTline = self.delFTline.text()
        
        sql_query = """
        DELETE FROM FlightType
        WHERE TypeName = ?
        """
        cursor.execute(sql_query, (delFTline))
        connection.commit()
        
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
        output.setText("Flight Type deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def viewFT(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
        self.flightStatusView.clicked.connect(self.viewFS)
        self.show()
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
        
        deleteFS = self.deleteFS.text()
        
        sql_query = """
        DELETE FROM FlightStatusTable
        WHERE FlightStatus = ?
        """
        cursor.execute(sql_query, (deleteFS))
        connection.commit()
        
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
        output.setText("Flight Status deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def viewFS(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
         
class AircraftWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(AircraftWindow, self).__init__()
        uic.loadUi("aircraft .ui", self)
        self.setWindowTitle("Aircraft")
        self.aircraftBack.clicked.connect(self.open_aircraftManager)
        self.ADadd.clicked.connect(self.addAircraft)
        self.ADdel.clicked.connect(self.deleteAircraft)
        self.aircraftView.clicked.connect(self.viewAircraft)
        self.show()
    def open_aircraftManager(self):
        self.hide()
        self.ground_window=AircraftManagerWindow()
        self.ground_window.show()
    def addAircraft(self):
        #####################################################################################################################################
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Aircraft
        ([TailNumber],[Name],[AircraftTypeID],[Capacity],[AirlineId])
        VALUES (?,?,?,?,?)
        """
        
        TailNumber = self.TailNumber.text()
        Name = self.Name.text()
        AircraftTypeID = self.AircraftTypeID.currentText()
        Capacity = self.Capacity.text()
        AirlineId = self.AirlineId.currentText()
        
        if not (Capacity.isnumeric() and TailNumber.isnumeric()):
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("Capacity can only be a numeric value")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            output.exec()
        else:    
            cursor.execute(sql_query, (TailNumber, Name, AircraftTypeID, Capacity, AirlineId))
            connection.commit()
            connection.close()
            
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
        
        delTailNum = self.delTailNum.text()
        
        sql_query = """
        DELETE FROM Aircraft
        WHERE TerminalNumber = ?
        """
        cursor.execute(sql_query, (delTailNum))
        connection.commit()
        
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
        output.setText("Aircraft deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def viewAircraft(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
        self.show()
    def open_aircraftManager(self):
        self.hide()
        self.ground_window=AircraftManagerWindow()
        self.ground_window.show()

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
        self.show()
        
        self.country_cities = {
            'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'San Francisco'],
            'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Edinburgh'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'Germany': ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt'],
            'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
            'Japan': ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama', 'Sapporo'],
            'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
            'India': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
            'Pakistan': ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 'Faisalabad'],
        }

        # Create and populate the country combo box
        self.Country = QComboBox()
        self.Country.addItems(self.country_cities.keys())
        self.Country.currentIndexChanged.connect(self.update_city_combo_box)

        # Create the city combo box
        self.City = QComboBox()
        
    def update_city_combo_box(self, index):
        # Update the city combo box based on the selected country
        selected_country = self.Country.currentText()
        cities = self.country_cities.get(selected_country, [])
        self.City.clear()
        self.City.addItems(cities)
        
    def open_airportManager(self):
        self.hide()
        self.ground_window=AirportManagerWindow()
        self.ground_window.show()
    def addAirport(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Airports
        ([AirportName],[City],[Country])
        VALUES (?,?,?)
        """
        
        AirportName = self.AirportName.text()
        Country = self.Country.currentText()
        City = self.City.currentText()
        
        cursor.execute(sql_query, (AirportName, Country, City))
        connection.commit()
        
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
        
        delAirportName = self.delAirportName.text()
        
        sql_query = """
        DELETE FROM Airports
        WHERE AirportName = ?
        """
        cursor.execute(sql_query, (delAirportName))
        connection.commit()
        
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
        output.setText("Airport deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def viewAirport(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
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
        self.show()
    def open_airportManager(self):
        self.hide()
        self.ground_window=AirportManagerWindow()
        self.ground_window.show()
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
        
        cursor.execute(sql_query, (AirlineName, ContactP, Phone, Email, City, Country))
        connection.commit()
        
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
        
        delAirline = self.delAirline.text()
        
        sql_query = """
        DELETE FROM Airline
        WHERE AirlineName = ?
        """
        cursor.execute(sql_query, (delAirline))
        connection.commit()
        
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
        output.setText("Airline deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def view_airline(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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
        # Add users to combo box
        self.Role.addItem("Ground Manager")
        self.Role.addItem("Flight Manager")
        self.Role.addItem("Airport Manager")
        self.Role.addItem("Aircraft Manager")
        self.Role.addItem("Admin")

    def addUser(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Airports
        ([AirportID], [AirportName], [Country], [City])
        VALUES (?, ?, ?, ?)
        """
        
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
            
        # cursor.execute(sql_query, (RunwayNum, RunwayLen))
        # connection.commit()
        # connection.close()

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
        self.GViewBtn.clicked.connect(self.viewGate)

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
        
        cursor.execute(sql_query, (GateNum))
        connection.commit()
        
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
        
        DelGateNum = self.DelGateNum.text()
        
        sql_query = """
        DELETE FROM Gate
        WHERE GateName = ?
        """
        cursor.execute(sql_query, (DelGateNum))
        connection.commit()
        
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
        output.setText("Gate deleted successfully!")
        output.setStandardButtons(QMessageBox.StandardButton.Ok)
        output.setIcon(QMessageBox.Icon.Information)
        output.exec()
        
    def viewGate(self):
        connection = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
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