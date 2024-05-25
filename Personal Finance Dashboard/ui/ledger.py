from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QHeaderView)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import sqlite3

class LedgerTab(QWidget):
    balance_updated = pyqtSignal()  # Signal to notify balance update needed

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Assuming columns for ID, Type, Amount, Description, Date
        self.table.setHorizontalHeaderLabels(['ID', 'Type', 'Amount', 'Description', 'Date'])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
                    QTableWidget {
                        background-color: #282a36;
                        color: #bd93f9; /* Setting the font color to purple */
                        gridline-color: #bd93f9; /* Optional: if you want grid lines to be purple as well */
                    }
                    QTableWidget QHeaderView::section {
                        background-color: #44475a;
                        color: #bd93f9;
                        border: 1px solid #bd93f9;
                    }
                    QTableWidget::item:selected {
                        background-color: #6272a4; /* Change selection color if needed */
                        color: #f8f8f2;
                    }
                """)        
        self.table.setFont(QFont('Arial', 10))
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.doubleClicked.connect(self.edit_transaction)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.load_transactions()

        # Buttons for operations
        self.btnDelete = QPushButton('Delete Selected')
        self.btnDelete.setIcon(QIcon('delete_icon.png'))  # Ensure you have an icon file at the correct path
        self.btnDelete.clicked.connect(self.delete_transaction)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btnDelete)
        
        self.layout.addWidget(self.table)
        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def load_transactions(self):
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, transaction_type, amount, description, date FROM transactions")
        records = cursor.fetchall()

        self.table.setRowCount(len(records))
        for i, row in enumerate(records):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        if not records:
            self.table.setRowCount(0)
        conn.close()

    def edit_transaction(self, index):
        row = index.row()
        transaction_id = self.table.item(row, 0).text()
        QMessageBox.information(self, 'Edit', f'Edit transaction {transaction_id}')

    def delete_transaction(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            transaction_id = self.table.item(selected_row, 0).text()
            reply = QMessageBox.question(self, 'Delete', f'Are you sure you want to delete transaction {transaction_id}?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                conn = sqlite3.connect('finance.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
                conn.commit()
                conn.close()
                self.table.removeRow(selected_row)
                QMessageBox.information(self, 'Deleted', f'Transaction {transaction_id} deleted successfully')
                self.balance_updated.emit()  # Emit signal when a transaction is deleted
        else:
            QMessageBox.warning(self, 'Selection', 'Please select a transaction to delete')
