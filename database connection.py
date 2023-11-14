# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView, QMessageBox, QLineEdit
import sys
import pyodbc


# Replace these with your own database connection details
server = 'LAPTOP-CDQ2932B'
database = 'AirportManagementSystem'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication

# Main Window Class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("airport.ui", self)
        self.setWindowTitle("Airport")
        self.show()
        
        self.Add.clicked.connect(self.addAirport)
        self.Delete.clicked.connect(self.deleteAirport)
    
    def deleteAirport(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        AirportID = self.clicked.AirportID.currentText()

        sql_query = """
        DELETE FROM Airports
        WHERE AirportID = ?
        """

        if not AirportID:
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("No Airport ID selected")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            button = output.exec()
        else:
            cursor.execute(sql_query, (AirportID,))
            connection.commit()
            connection.close()
            
            
            output = QMessageBox(self)              
            output.setWindowTitle("Message") 
            output.setText("Airport added successfully!")
            output.setStandardButtons(QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Information)
            button = output.exec()
            
    def addAirport(self):
        connection = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        )
        cursor = connection.cursor()
        
        sql_query = """
        INSERT INTO Airports
        ([AirportID], [AirportName], [Country], [City])
        VALUES (?, ?, ?, ?)
        """
        
        AirportID = self.AirportID.text()
        AirportName = self.AirportName.text()
        Country = self.Country.currentText()
        City = self.City.currentText()
        
        if not AirportName:
            output = QMessageBox(self)              
            output.setWindowTitle("ERROR") 
            output.setText("No Airport Name")
            output.setStandardButtons( QMessageBox.StandardButton.Ok)
            output.setIcon(QMessageBox.Icon.Warning) 
            button = output.exec()
        
        cursor.execute(sql_query, (AirportID, AirportName, Country, City))
        connection.commit()
        connection.close()
        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()