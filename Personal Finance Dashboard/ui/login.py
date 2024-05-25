from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QHBoxLayout, QMessageBox, QDateEdit)
from PyQt5.QtCore import pyqtSignal
import sqlite3
import database

class Login(QWidget):
    authenticated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.register_form = None
        self.forgot_password_form = None
        self.initUI()
        self.check_user_existence()

    def initUI(self):
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.login_btn = QPushButton('Login', self)
        self.register_btn = QPushButton('Register', self)
        self.forgot_password_btn = QPushButton('Forgot Password', self)

        self.login_btn.clicked.connect(self.login)
        self.register_btn.clicked.connect(self.show_register_form)

        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.register_btn)
        layout.addWidget(self.forgot_password_btn)

        self.setLayout(layout)
        self.setWindowTitle('Login or Register')
        self.forgot_password_btn.clicked.connect(self.show_forgot_password_form)
        
    def show_forgot_password_form(self):
        try:
            if self.forgot_password_form is None:
                self.forgot_password_form = ForgotPasswordForm()
            self.forgot_password_form.show()
        except Exception as e:
            print(f"Error showing Forgot Password form: {e}")

    def check_user_existence(self):
        if not database.user_exists():
            self.login_btn.setEnabled(False)
        else:
            self.login_btn.setEnabled(True)
            self.register_btn.setEnabled(False)

    def show_register_form(self):
        if not self.register_form:
            self.register_form = RegisterForm()
            self.register_form.registration_successful.connect(self.on_registration_success)
            self.register_form.show()

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.warning(self, 'Login Failed', 'Please enter both username and password.')
            return

        if database.authenticate_user(username, password):
            QMessageBox.information(self, 'Login Success', 'You have successfully logged in.')
            self.authenticated.emit()
            self.close()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')

    def on_registration_success(self):
        self.login_btn.setEnabled(True)
        self.register_btn.setEnabled(False)
        if self.register_form:
            self.register_form.close()

class RegisterForm(QWidget):
    registration_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.fname = QLineEdit()
        self.lname = QLineEdit()
        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.email = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.security_question = QComboBox()
        self.security_question.addItems([
            "What is your mother's maiden name?",
            "What was the name of your first pet?",
            "What was your first car?",
            "What elementary school did you attend?",
            "What is the city of your birth?"
        ])
        self.security_answer = QLineEdit()

        self.create_btn = QPushButton('Create Account', self)
        self.create_btn.clicked.connect(self.create_account)

        layout.addWidget(QLabel('First Name:'))
        layout.addWidget(self.fname)
        layout.addWidget(QLabel('Last Name:'))
        layout.addWidget(self.lname)
        layout.addWidget(QLabel('Birthday:'))
        layout.addWidget(self.birthday)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email)
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(QLabel('Security Question:'))
        layout.addWidget(self.security_question)
        layout.addWidget(QLabel('Answer:'))
        layout.addWidget(self.security_answer)
        layout.addWidget(self.create_btn)

        self.setLayout(layout)
        self.setWindowTitle('Create Account')

    def create_account(self):
        if not all([self.fname.text(), self.lname.text(), self.email.text(), self.username.text(), self.password.text(), self.security_answer.text()]):
            QMessageBox.warning(self, 'Registration Failed', 'All fields are required.')
            return

        if database.register_user(
            self.fname.text(), self.lname.text(), self.birthday.date().toString("yyyy-MM-dd"), 
            self.email.text(), self.username.text(), self.password.text(),
            self.security_question.currentText(), self.security_answer.text()):
            QMessageBox.information(self, 'Registration Success', 'Account successfully created.')
            self.registration_successful.emit()
        else:
            QMessageBox.warning(self, 'Registration Failed', 'Registration failed due to a database error or duplicate username/email.')

class ForgotPasswordForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.last_name = QLineEdit()
        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.security_question = QLabel()  # Display the user's security question
        self.security_answer = QLineEdit()
        self.submit_btn = QPushButton('Submit', self)
        self.submit_btn.clicked.connect(self.verify_user)

        layout.addWidget(QLabel('Last Name:'))
        layout.addWidget(self.last_name)
        layout.addWidget(QLabel('Birthday:'))
        layout.addWidget(self.birthday)
        layout.addWidget(self.security_question)
        layout.addWidget(QLabel('Security Answer:'))
        layout.addWidget(self.security_answer)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)
        self.setWindowTitle('Forgot Password')

    def verify_user(self):
        last_name = self.last_name.text().strip()
        birthday = self.birthday.date().toString("yyyy-MM-dd")
        answer = self.security_answer.text().strip().lower()  # Normalize input
        if database.verify_user_details(last_name, birthday, answer):
            user_info = database.get_user_info(last_name, birthday, answer)
            QMessageBox.information(self, "User Details", f"Username: {user_info['username']}\nPassword: {user_info['password']}")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "No matching details found.")
            self.close()
