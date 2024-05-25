from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate
import sqlite3
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db_path = 'finance.db'

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDisplayFormat("MMMM yyyy")
        self.dateEdit.setDate(QDate.currentDate())

        self.btnGeneratePDF = QPushButton("Generate PDF")
        self.btnGenerateCSV = QPushButton("Generate CSV")
        
        self.btnGeneratePDF.clicked.connect(self.generatePDF)
        self.btnGenerateCSV.clicked.connect(self.generateCSV)

        layoutH = QHBoxLayout()
        layoutH.addWidget(self.dateEdit)
        layoutH.addWidget(self.btnGeneratePDF)
        layoutH.addWidget(self.btnGenerateCSV)

        self.layout.addLayout(layoutH)
        self.setLayout(self.layout)

    def fetch_data(self, date):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT transaction_type, category, amount, description, date FROM transactions
            WHERE strftime('%Y-%m', date) = ?
        ''', (date,))
        data = cursor.fetchall()
        conn.close()
        return data

    def generatePDF(self):
        selected_date = self.dateEdit.date().toString("yyyy-MM")
        data = self.fetch_data(selected_date)
        if not data:
            QMessageBox.information(self, 'PDF Report', 'No data found for selected month.')
            return
        
        file_path = f'report_{selected_date}.pdf'
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, f'Report for {selected_date}')
        for index, (tran_type, category, amount, desc, date) in enumerate(data, start=1):
            y_position = height - 100 - (index * 20)
            line = f"{tran_type}, {category}, {amount}, {desc}, {date}"
            c.drawString(50, y_position, line)
        c.save()
        QMessageBox.information(self, 'PDF Report', f'PDF report for {selected_date} saved to {file_path}')

    def generateCSV(self):
        selected_date = self.dateEdit.date().toString("yyyy-MM")
        data = self.fetch_data(selected_date)
        if not data:
            QMessageBox.information(self, 'CSV Report', 'No data found for selected month.')
            return
        
        file_path = f'report_{selected_date}.csv'
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Transaction Type', 'Category', 'Amount', 'Description', 'Date'])
            for row in data:
                writer.writerow(row)
        QMessageBox.information(self, 'CSV Report', f'CSV report for {selected_date} saved to {file_path}')
