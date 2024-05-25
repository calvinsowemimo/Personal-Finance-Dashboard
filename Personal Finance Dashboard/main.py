import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
import database
from ui.login import Login
from ui.dashboard import DashboardTab
from ui.transaction import TransactionTab
from ui.reports import ReportsTab
from ui.account import AccountTab
from ui.ledger import LedgerTab
from styles import duskStyle

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Econoscope v2.1')
        self.setGeometry(100, 100, 800, 600)  # Set the window size
        self.initUI()

    def initUI(self):
        # Initialize Tab Screen
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(True)

        # Create and add tabs
        self.dashboard_tab = DashboardTab()
        self.transaction_tab = TransactionTab()
        self.reports_tab = ReportsTab()
        self.account_tab = AccountTab()
        self.ledger_tab = LedgerTab()

        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.transaction_tab, "Transactions")
        self.tabs.addTab(self.ledger_tab, "Ledger")
        self.tabs.addTab(self.reports_tab, "Reports")
        self.tabs.addTab(self.account_tab, "Account")

        self.setCentralWidget(self.tabs)
        
        # Signals
        self.transaction_tab.transaction_added.connect(self.ledger_tab.load_transactions)
        self.ledger_tab.balance_updated.connect(self.dashboard_tab.update_balance_display)
        self.ledger_tab.balance_updated.connect(self.transaction_tab.update_balance_display)

        self.setStyleSheet(duskStyle)

if __name__ == '__main__':
    database.setup_database()
    database.setup_database2()
    app = QApplication(sys.argv)
    login = Login()
    main = MainWindow()
    login.authenticated.connect(main.show)
    login.show()
    sys.exit(app.exec_())
