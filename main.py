import json
from datetime import datetime

class PersonalFinanceTracker():

    def __init__(self, data_file = 'transactions.json'):
        self.data_file = data_file
        self.transactions = []
        self.load_data()
    
    def load_data(self):
        try:
            file = open(self.data_file, "r")
            self.transactions = json.load(file)
        except FileNotFoundError:
            self.transactions = []

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.transactions, file, indent=2)
    
    def add_transaction(self, amount, category, transaction_type, date=datetime.now().strftime('%Y-%m-%d')):
        t = {
            'amount' : amount,
            'category' : category,
            'transaction_type' : transaction_type,
            'date' : date}
        
        self.transactions.append(t)
        self.save_data()
    
    def view_transactions(self, category=None):
        if category:
            filtered = [t for t in self.transactions if t['category'] == category]
        else:
            filtered = self.transactions
        
        for t in filtered:
            print(f"{t['date']} - {t['category']} ({t['transaction_type']}): ${t['amount']}")

    def calculate_balance(self):

        balance = sum(t['amount'] if t['transaction_type'] == 'income' else -t['amount'] for t in self.transactions)
        return balance

    def generate_summary_report(self):
        
        total_income = sum(t['amount'] for t in self.transactions if t['transaction_type'] == 'income')
        total_expenses = sum(t['amount'] for t in self.transactions if t['transaction_type'] == 'expense')
        balance = self.calculate_balance()

        print(f"Total Income: ${total_income}")
        print(f"Total Expenses: ${total_expenses}")
        print(f"Balance: ${balance}")



def test_personal_finance_tracker():
    # Create an instance of PersonalFinanceTracker for testing
    finance_tracker = PersonalFinanceTracker(data_file="test_transactions.json")

    try:
        # Test Case 1: Add transactions
        print("Test Case 1: Adding transactions")
        finance_tracker.add_transaction(amount=1000.0, category="Salary", transaction_type="income")
        finance_tracker.add_transaction(amount=50.0, category="Groceries", transaction_type="expense")
        finance_tracker.add_transaction(amount=200.0, category="Freelance", transaction_type="income")
        finance_tracker.add_transaction(amount=30.0, category="Dining Out", transaction_type="expense")

        # Test Case 2: View all transactions
        print("\nTest Case 2: Viewing all transactions")
        finance_tracker.view_transactions()

        # Test Case 3: View transactions for a specific category
        print("\nTest Case 3: Viewing transactions for 'Groceries'")
        finance_tracker.view_transactions(category="Groceries")

        # Test Case 4: Calculate and display balance
        print("\nTest Case 4: Calculating and displaying balance")
        balance = finance_tracker.calculate_balance()
        print(f"Current Balance: ${balance}")

        # Test Case 5: Generate and print a summary report
        print("\nTest Case 5: Generating and printing a summary report")
        finance_tracker.generate_summary_report()

        # Test Case 6: Save data to file
        print("\nTest Case 6: Saving data to file")
        finance_tracker.save_data()

        # Test Case 7: Load data from file
        print("\nTest Case 7: Loading data from file")
        new_finance_tracker = PersonalFinanceTracker(data_file="test_transactions.json")
        new_finance_tracker.view_transactions()  # Check if data loaded correctly

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Cleanup: Delete the test data file
        import os
        os.remove("test_transactions.json")

# Run the test function
test_personal_finance_tracker()