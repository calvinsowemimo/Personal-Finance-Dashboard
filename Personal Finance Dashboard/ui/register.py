from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QDateEdit)
from PyQt5.QtCore import QDate
import sqlite3
import database  # Ensure database.py is set up correctly

class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.fname = QLineEdit()
        self.lname = QLineEdit()
        self.birthday = QDateEdit()
        self.birthday.setCalendarPopup(True)
        self.birthday.setDateRange(QDate(1900, 1, 1), QDate.currentDate())
        self.email = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.create_btn = QPushButton('Create Account')

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
        layout.addWidget(self.create_btn)

        self.setLayout(layout)
        self.setWindowTitle('Create Account')
        self.create_btn.clicked.connect(self.create_account)

    def create_account(self):
        fname = self.fname.text().strip()
        lname = self.lname.text().strip()
        birthday = self.birthday.date().toString("yyyy-MM-dd")
        email = self.email.text().strip()
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not all([fname, lname, birthday, email, username, password]):
            QMessageBox.warning(self, 'Registration Failed', 'All fields are required.')
            return

        conn = database.create_connection()
        try:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO users (first_name, last_name, birthday, email, username, password) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (fname, lname, birthday, email, username, password))
            conn.commit()
            QMessageBox.information(self, 'Registration Success', 'Account successfully created.')
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, 'Registration Failed', 'This username or email is already taken.')
        except Exception as e:
            QMessageBox.critical(self, 'Registration Failed', str(e))
        finally:
            conn.close()
