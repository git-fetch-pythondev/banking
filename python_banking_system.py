class Account:
    def __init__(self, account_id, customer_id, account_number, balance):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("amount should be > 0")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("invalid withdrawal amount or insufficient balance")

    def get_balance(self):
        return self.balance
    
    def get_account_id(self):
        return self.account_id
    
    def get_transactions(self):
        return [{'type' : 'Withdraw', 'amount' : 500}]


class Customer:
    def __init__(self, customer_id, name, email, phone_number):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def get_customer_id(self):
        return self.customer_id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_phone_number(self):
        return self.phone_number

    def set_name(self, new_name):
        self.name = new_name

    def set_email(self, new_email):
        self.email = new_email

    def set_phone_number(self, new_phone_number):
        self.phone_number = new_phone_number


class CreateAccountUseCase:
    def create_account(self, customer_id, name, email, phone_number):
        customer = Customer(customer_id, name, email, phone_number)
        
        # Generate a unique account ID (You can implement this as needed)
        account_id = self.generate_unique_account_id()  # Assume this method generates a unique account ID

        account_number = "ACC000123" # Unique (You can implement this as needed)
        
        # Create an Account with 0 balance
        new_account = Account(account_id, customer.get_customer_id(), account_number, 0)
        
        return new_account

    def generate_unique_account_id(self):
        # Implement your logic to generate a unique account ID here
        return "ACCOUNT123"
    

class TransactionUseCase:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def make_transaction(self, account_id, amount, transaction_type):
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            return "No account found"

        if transaction_type == 'deposit':
            account.deposit(amount)
        elif transaction_type == 'withdraw':
            account.withdraw(amount)
        else:
            return "Invalid transaction type"

        self.account_repository.save_account(account)
        return f"{transaction_type} of {amount} completed for account_id:  {account_id}"


class AccountStatementUseCase:
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def generate_account_statement(self, account_id):
        account = self.account_repository.find_account_by_id(account_id)
        if not account:
            return "No account found"
        
        account_statement = ''

        # Retrieve transaction details from the account
        transactions = account.get_transactions()

        if not transactions:
            account_statement += "No transactions found for this account"
        else:
            account_statement += "Transaction Details:"
            for transaction in transactions:
                transaction_type = transaction['type']
                amount = transaction['amount']
                transaction_info = f"{transaction_type} - Amount: {amount}\n"
                account_statement += transaction_info

        return account_statement


class AccountRepository:
    def __init__(self):
        self.accounts = {}  # Using a dictionary to save account_id as key and other details as value

    def save_account(self, account):
        self.accounts[account.account_id] = account

    def find_account_by_id(self, account_id):
        return self.accounts.get(account_id)

    def find_accounts_by_customer_id(self, customer_id):
        accounts_by_customer = []
        for account in self.accounts.values():
            print('Acount details', account.customer_id ,account.balance, customer_id)
            if account.customer_id == customer_id:
                accounts_by_customer.append(account)
        return accounts_by_customer


# Simple Tests

# Create a Customer
customer = Customer(customer_id="CUST123", name="Ranvijay", email="ranvijay@gmail.com", phone_number="1234567890")

# Create an Account for the Customer
create_account_usecase = CreateAccountUseCase()
new_account = create_account_usecase.create_account(
    customer_id=customer.get_customer_id(),
    name=customer.get_name(),
    email=customer.get_email(),
    phone_number=customer.get_phone_number()
)

# Initialize an AccountRepository
account_repository = AccountRepository()

# Save the created account to the repository
account_repository.save_account(new_account)

# Perform transactions on the account
transaction_usecase = TransactionUseCase(account_repository)
transaction_usecase.make_transaction(new_account, amount=500, transaction_type='deposit')
transaction_usecase.make_transaction(new_account, amount=200, transaction_type='withdraw')

# Generate an account statement for the account
account_statement_usecase = AccountStatementUseCase(account_repository)
statement = account_statement_usecase.generate_account_statement(new_account.get_account_id())

# Display the generated account statement
print(statement,"Statement details")

# Find account by ID from the repository
found_account = account_repository.find_account_by_id(new_account.get_account_id())
if found_account:
    print("account found by id", found_account.get_account_id())
else:
    print("No account found", found_account.get_account_id())

# Find accounts by customer ID from the repository
accounts_by_customer = account_repository.find_accounts_by_customer_id(customer.get_customer_id())
if accounts_by_customer:
    print("accounts found for customer_id:", customer.get_customer_id())
    for account in accounts_by_customer:
        print("account_id:", account.get_account_id())
else:
    print("No accounts found for customer_id:", customer.get_customer_id())
