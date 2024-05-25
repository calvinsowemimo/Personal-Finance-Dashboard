# Personal Finance Dashboard

## Project Overview
This Personal Finance Dashboard is an application designed to help users manage and track their financial activities. It provides a secure and user-friendly interface for monitoring and analyzing personal financial data, including income, expenses, and investments, using interactive visualizations.

## Features
- **Secure Login and Registration**: Manage access with a secure authentication system.
- **Interactive Financial Dashboard**: Visualize financial data through interactive charts and graphs.
- **Transaction Management**: Add, edit, and delete income and expense transactions.
- **Automated Financial Reports**: Generate and view monthly financial reports.
- **Data Management**: Robust SQLite database integration for reliable data storage and retrieval.

## Technologies Used
- **Python**: Primary programming language.
- **PyQt5**: Used for building the graphical user interface.
- **SQLite**: Database for storing user data and transactions.
- **Matplotlib**: For generating static, interactive, and animated visualizations in Python.

## Project Structure
- `main.py`: Entry point of the application. Launches the GUI.
- `login.py`: Handles user authentication.
- `register.py`: Manages new user registration.
- `dashboard.py`: Core script for displaying the dashboard interface.
- `transaction.py`: Manages transaction data operations.
- `financial_calculations.py`: Contains logic for financial calculations and metrics.
- `reports.py`: Automates the generation of financial reports.
- `database.py`: Manages database connections and queries.
- `ledger.py`: Handles the logging of transaction data.
- `styles.py`: Contains PyQt5 styles for the GUI.
- `account.py`: Defines the user account functionalities.

## Installation
Ensure you have Python and pip installed on your system. Then follow these steps:
```bash
git clone https://github.com/yourgithubusername/finance-dashboard
cd finance-dashboard
pip install -r requirements.txt
