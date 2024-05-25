from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QMessageBox, QComboBox, QDateEdit, QCheckBox)
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSignal
import sqlite3
from datetime import datetime
from financial_calculations import FinancialCalculations  # Assuming this module is in the same directory

class TransactionTab(QWidget):
    transaction_added = pyqtSignal()  # Notify Signal Here

    def __init__(self):
        super().__init__()
        self.fin_calculations = FinancialCalculations()
        self.initUI()
        self.initDB()  # Initialize the database table when the widget is created
        self.update_balance_display()

    def initUI(self):
        layout = QVBoxLayout()

        # Balance display
        self.balance_label = QLabel("Available Balance: £0.00")
        layout.addWidget(self.balance_label)

        form_layout = QFormLayout()

        self.transaction_type = QComboBox()
        self.transaction_type.addItems(["Income", "Expense", "Transfer"])

        self.category = QComboBox()
        self.category.addItems(["Utilities", "Rent/Mortgage", "Groceries", "Salary", "Investments"])

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Enter numerical value")
        self.amount.setValidator(QDoubleValidator(0.99, 9999999.99, 2))

        self.description = QLineEdit()
        self.date = QDateEdit()
        self.date.setCalendarPopup(True)
        self.date.setDate(datetime.now())

        self.recurring = QCheckBox("Recurring Transaction")
        self.frequency = QComboBox()
        self.frequency.addItems(["Monthly", "Weekly", "Annually"])
        self.frequency.setEnabled(False)

        self.recurring.toggled.connect(self.toggle_frequency_enabled)

        form_layout.addRow("Transaction Type:", self.transaction_type)
        form_layout.addRow("Category:", self.category)
        form_layout.addRow("Amount £:", self.amount)
        form_layout.addRow("Description:", self.description)
        form_layout.addRow("Date:", self.date)
        form_layout.addRow(self.recurring, self.frequency)

        self.submit_btn = QPushButton("Submit Transaction")
        self.submit_btn.clicked.connect(self.submit_transaction)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

    def initDB(self):
        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                transaction_type TEXT,
                category TEXT,
                amount REAL,
                description TEXT,
                date TEXT,
                recurring BOOLEAN,
                frequency TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def toggle_frequency_enabled(self, checked):
        self.frequency.setEnabled(checked)

    def submit_transaction(self):
        t_type = self.transaction_type.currentText()
        category = self.category.currentText()
        raw_amount = float(self.amount.text())
        amount = -raw_amount if t_type in ["Expense", "Transfer"] else raw_amount
        description = self.description.text()
        date = self.date.date().toString("yyyy-MM-dd")
        recurring = self.recurring.isChecked()
        frequency = self.frequency.currentText() if recurring else None

        try:
            conn = sqlite3.connect('finance.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO transactions (transaction_type, category, amount, description, date, recurring, frequency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (t_type, category, amount, description, date, recurring, frequency))
            conn.commit()
            conn.close()
            self.transaction_added.emit()  # Emit signal
            self.update_balance_display()
            QMessageBox.information(self, 'Success', 'Transaction saved successfully!')
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save transaction. Error: {e}')

    def clear_fields(self):
        self.amount.clear()
        self.description.clear()
        self.date.setDate(datetime.now())
        self.recurring.setChecked(False)
        self.frequency.setCurrentIndex(0)

    def update_balance_display(self):
        """Updates the balance label with the current balance from the database."""
        financial_calculations = FinancialCalculations()
        available_balance = self.fin_calculations.calculate_balance()
        self.balance_label.setText(f"Available Balance: £{available_balance:.2f}")
