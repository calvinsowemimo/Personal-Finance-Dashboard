from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from financial_calculations import FinancialCalculations  # Ensure this is correctly imported

class DashboardTab(QWidget):
    def __init__(self):
        super().__init__()
        self.fin_calculations = FinancialCalculations()  # Create an instance of the financial calculations class
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Create and configure the balance label
        self.balance_label = QLabel("Available Balance: £0.00")
        self.balance_label.setStyleSheet("font-size: 24px; color: white;")  # Styling the balance label
        self.layout.addWidget(self.balance_label)

        self.update_balance_display()  # Call this function to update the balance display when the tab is initialized

    def update_balance_display(self):
        """Updates the balance label with the current balance from the database."""
        financial_calculations = FinancialCalculations()
        available_balance = self.fin_calculations.calculate_balance()
        self.balance_label.setText(f"Available Balance: £{available_balance:.2f}")  # Format the balance to two decimal places
