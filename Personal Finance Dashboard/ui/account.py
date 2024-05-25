from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import database

class AccountTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # User detail fields
        self.username = QLineEdit()
        self.email = QLineEdit()
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.birthday = QLineEdit()  # Consider QDateEdit for actual implementations
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        # Buttons for editing and updating information
        self.change_info_btn = QPushButton("Change Info")
        self.update_info_btn = QPushButton("Update Info")

        self.change_info_btn.clicked.connect(self.enable_editing)
        self.update_info_btn.clicked.connect(self.update_user_info)

        # Add widgets to layout
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email)
        layout.addWidget(QLabel('First Name:'))
        layout.addWidget(self.first_name)
        layout.addWidget(QLabel('Last Name:'))
        layout.addWidget(self.last_name)
        layout.addWidget(QLabel('Birthday:'))
        layout.addWidget(self.birthday)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(self.change_info_btn)
        layout.addWidget(self.update_info_btn)

        self.setLayout(layout)
        self.load_user_info()
        self.toggle_editing(False)  # Start with fields in read-only mode

    def load_user_info(self):
        user_info = database.get_current_user_info()
        if user_info:
            self.username.setText(user_info['username'])
            self.email.setText(user_info['email'])
            self.first_name.setText(user_info['first_name'])
            self.last_name.setText(user_info['last_name'])
            self.birthday.setText(user_info['birthday'])
            self.password.setText("")  # Do not load password for security reasons
        else:
            QMessageBox.warning(self, "Error", "Failed to load user details.")

    def enable_editing(self):
        self.toggle_editing(True)

    def update_user_info(self):
        updated_info = {
            'username': self.username.text(),
            'email': self.email.text(),
            'first_name': self.first_name.text(),
            'last_name': self.last_name.text(),
            'birthday': self.birthday.text(),
            'password': self.password.text()  # Ensure password handling is secure
        }
        if database.update_user_info(updated_info):
            QMessageBox.information(self, "Success", "User details updated successfully.")
            self.toggle_editing(False)
        else:
            QMessageBox.warning(self, "Error", "Failed to update details.")

    def toggle_editing(self, editable):
        # Toggle read-only state of fields
        self.username.setReadOnly(not editable)
        self.email.setReadOnly(not editable)
        self.first_name.setReadOnly(not editable)
        self.last_name.setReadOnly(not editable)
        self.birthday.setReadOnly(not editable)
        self.password.setReadOnly(not editable)
        # Toggle visibility of buttons
        self.update_info_btn.setVisible(editable)
        self.change_info_btn.setVisible(not editable)
