import sqlite3

class FinancialCalculations:
    def __init__(self, db_path='finance.db'):
        """Initialize with the path to the SQLite database."""
        self.db_path = db_path

    def calculate_balance(self):
        """Calculate the available balance based on transactions."""
        # Connect to the database
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # Calculate the sum of all transaction amounts
        cur.execute("SELECT SUM(amount) FROM transactions")
        result = cur.fetchone()
        balance = result[0] if result[0] is not None else 0

        # Close the database connection
        conn.close()

        return balance

    def fetch_transactions(self, start_date=None, end_date=None):
        """Fetch transactions within a specific date range (optional)."""
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        query = "SELECT id, transaction_type, category, amount, description, date FROM transactions"
        params = ()

        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params = (start_date, end_date)

        cur.execute(query, params)
        transactions = cur.fetchall()

        conn.close()
        return transactions
