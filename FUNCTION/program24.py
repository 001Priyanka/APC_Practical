# 24. Create functions for deposit, withdrawal, balance enquiry,
#     and transaction history. Prevent withdrawal when the balance
#     is insufficient and maintain a transaction record.

balance = 0
transactions = []

def deposit(amount):
    global balance
    balance += amount
    transactions.append("Deposited: " + str(amount))

def withdraw(amount):
    global balance

    if amount <= balance:
        balance -= amount
        transactions.append("Withdrawn: " + str(amount))
    else:
        print("Insufficient balance.")

def balance_enquiry():
    print("Balance =", balance)

def transaction_history():
    print("Transaction History:")
    for transaction in transactions:
        print(transaction)

deposit(5000)
withdraw(1500)
balance_enquiry()
transaction_history()