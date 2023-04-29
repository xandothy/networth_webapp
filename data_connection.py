import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime

class Connector:
    def __init__(self, host_name, user_name, password):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=password,
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: {err}")

        if len(self._read_query("SHOW DATABASES LIKE 'net_worth'")) == 0:
            print("First time initialization...")
            self.run_initial_setup()
            print("Done!")
        else:
            self.connection.database = "net_worth"

    def create_database(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            print("Database created successfully")
        except Error as err:
            print(f"Error: '{err}'")

    def _execute_query(self, query, data=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data)
            self.connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")

    def _read_query(self, query, data=None):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query, data)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: {err}")

    def run_initial_setup(self):
        self._execute_query("CREATE DATABASE net_worth;")
        self.connection.database = "net_worth"

        # What's in the account (stocks, crypto, real estate..?)
        create_account_content_table = """
        CREATE TABLE account_content (
          account_content_id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(40) NOT NULL,
          description VARCHAR(250)
          );
        """

        # REER, CELI, etc?
        create_account_types_table = """
        CREATE TABLE account_types (
          account_type_id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(40) NOT NULL,
          description VARCHAR(250)
          );
        """

        # Stocks, real estate, crypto?
        create_investment_types_table = """
        CREATE TABLE investment_types (
          investment_type_id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(40) NOT NULL,
          description VARCHAR(250)
          );
        """

        # Salary, tax return, birthday money?
        create_income_types_table = """
                CREATE TABLE income_types (
                  income_type_id INT PRIMARY KEY AUTO_INCREMENT,
                  name VARCHAR(40) NOT NULL,
                  description VARCHAR(250)
                  );
                """

        # Mortgage, line of credit, loan?
        create_debt_types_table = """
        CREATE TABLE debt_types (
          debt_type_id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(40) NOT NULL,
          description VARCHAR(250)
          );
        """

        # Utilities, groceries, restaurant?
        create_expense_tags_table = """
        CREATE TABLE expense_tags (
          expense_tag_id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(40) NOT NULL,
          description VARCHAR(250)
          );
        """

        # Account owner
        create_owners_table = """
        CREATE TABLE owners (
          owner_id INT PRIMARY KEY AUTO_INCREMENT,
          first_name VARCHAR(40) NOT NULL,
          last_name VARCHAR(40) NOT NULL
          );
        """

        # Account containing an investments, debts, etc
        create_accounts_table = """
        CREATE TABLE accounts (
          account_id INT PRIMARY KEY AUTO_INCREMENT,
          name VARCHAR(40) NOT NULL,
          type_id INT,
          content_id INT,
          owner1_id INT,
          owner2_id INT,
          CONSTRAINT fk_account_type FOREIGN KEY (type_id)
          REFERENCES account_types(account_type_id),
          CONSTRAINT fk_account_content FOREIGN KEY (content_id)
          REFERENCES account_content(account_content_id),
          CONSTRAINT fk_account_owner1 FOREIGN KEY (owner1_id)
          REFERENCES owners(owner_id),
          CONSTRAINT fk_account_owner2 FOREIGN KEY (owner2_id)
          REFERENCES owners(owner_id)
          );
         """

        # investment
        create_investments_table = """
        CREATE TABLE investments (
          investment_id INT PRIMARY KEY AUTO_INCREMENT,
          account_id INT,
          type_id INT,
          name VARCHAR(40),
          CONSTRAINT fk_account_investment FOREIGN KEY (account_id)
          REFERENCES accounts(account_id),
          CONSTRAINT fk_investment_type FOREIGN KEY (type_id)
          REFERENCES investment_types(investment_type_id)
          );
        """

        # debt
        create_debts_table = """
        CREATE TABLE debts (
          debt_id INT PRIMARY KEY AUTO_INCREMENT,
          account_id INT,
          type_id INT,
          name VARCHAR(40),
          CONSTRAINT fk_account_debts FOREIGN KEY (account_id)
          REFERENCES accounts(account_id),
          CONSTRAINT fk_debt_type FOREIGN KEY (type_id)
          REFERENCES debt_types(debt_type_id)
          );
        """

        # history for an investment
        create_investment_history = """
        CREATE TABLE investment_history (
          history_id INT PRIMARY KEY AUTO_INCREMENT,
          investment_id INT,
          date DATE,
          amount DECIMAL(38, 18),
          value DECIMAL(38, 18),
          CONSTRAINT fk_investment FOREIGN KEY (investment_id)
          REFERENCES investments(investment_id),
          UNIQUE (investment_id, date)
          );
        """

        # history for a debt
        create_debt_history = """
        CREATE TABLE debt_history (
          history_id INT PRIMARY KEY AUTO_INCREMENT,
          debt_id INT,
          date DATE,
          amount DECIMAL(38, 18),
          value DECIMAL(38, 18),
          CONSTRAINT fk_debt FOREIGN KEY (debt_id)
          REFERENCES debts(debt_id),
          UNIQUE (debt_id, date)
          );
        """

        # expense
        create_expenses_table = """
        CREATE TABLE expenses (
          expense_id INT PRIMARY KEY AUTO_INCREMENT,
          account_id INT,
          name VARCHAR(40),
          date DATE,
          value DECIMAL(38, 18),
          CONSTRAINT fk_account_expense FOREIGN KEY (account_id)
          REFERENCES accounts(account_id)
          );
        """

        # expense tags
        create_expense_tags_link_table = """
                CREATE TABLE expenses_tags_link (
                  expense_id INT,
                  tag_id INT,
                  CONSTRAINT fk_expense FOREIGN KEY (expense_id)
                  REFERENCES expenses(expense_id),
                  CONSTRAINT fk_tag FOREIGN KEY (tag_id)
                  REFERENCES expense_tags(expense_tag_id)
                  );
                """

        # investment
        create_income_table = """
                CREATE TABLE income (
                  income_id INT PRIMARY KEY AUTO_INCREMENT,
                  account_id INT,
                  type_id INT,
                  name VARCHAR(40),
                  date DATE,
                  value DECIMAL(38, 18),
                  CONSTRAINT fk_account_income FOREIGN KEY (account_id)
                  REFERENCES accounts(account_id),
                  CONSTRAINT fk_income_type FOREIGN KEY (type_id)
                  REFERENCES income_types(income_type_id)
                  );
                """

        # calculated net worth
        create_net_worth_table = """
                        CREATE TABLE net_worth (
                          net_worth_id INT PRIMARY KEY AUTO_INCREMENT,
                          date DATE UNIQUE,
                          value DECIMAL(38, 18)
                          );
                        """

        self._execute_query(create_account_content_table)
        self._execute_query(create_account_types_table)
        self._execute_query(create_investment_types_table)
        self._execute_query(create_debt_types_table)
        self._execute_query(create_expense_tags_table)
        self._execute_query(create_owners_table)
        self._execute_query(create_accounts_table)
        self._execute_query(create_investments_table)
        self._execute_query(create_debts_table)
        self._execute_query(create_investment_history)
        self._execute_query(create_debt_history)
        self._execute_query(create_expenses_table)
        self._execute_query(create_expense_tags_link_table)
        self._execute_query(create_income_types_table)
        self._execute_query(create_income_table)
        self._execute_query(create_net_worth_table)

    def get_net_worth(self):
        results = self._read_query("SELECT * FROM net_worth ORDER BY date ASC")
        l = [r for r in results]

        columns = ["ID", "date", "value"]
        return pd.DataFrame(l, columns=columns)

    def add_net_worth(self, date, value):
        self._execute_query("""INSERT INTO net_worth (date, value) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM net_worth
                                              WHERE date = %s
                                              AND value = %s)
                            ON DUPLICATE KEY UPDATE value=%s;""", (date, value, date, value, value))

    def get_owners(self):
        results = self._read_query("SELECT * FROM owners")
        l = [r for r in results]

        columns = ["ID", "first_name", "last_name"]
        return pd.DataFrame(l, columns=columns)

    def add_owner(self, first_name, last_name):
        self._execute_query("""INSERT INTO owners (first_name, last_name) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM owners
                                              WHERE first_name = %s
                                              AND last_name = %s);""", (first_name, last_name, first_name, last_name))

    def get_account_contents(self):
        results = self._read_query("SELECT * FROM account_content")
        l = [r for r in results]

        columns = ["ID", "name", "description"]
        return pd.DataFrame(l, columns=columns)

    def add_account_content(self, name, description):
        self._execute_query("""INSERT INTO account_content (name, description) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM account_content
                                              WHERE name = %s
                                              AND description = %s);""", (name, description, name, description))

    def get_account_types(self):
        results = self._read_query("SELECT * FROM account_types")
        l = [r for r in results]

        columns = ["ID", "name", "description"]
        return pd.DataFrame(l, columns=columns)

    def add_account_type(self, name, description):
        self._execute_query("""INSERT INTO account_types (name, description) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM account_types
                                              WHERE name = %s
                                              AND description = %s);""", (name, description, name, description))

    def get_income_types(self):
        results = self._read_query("SELECT * FROM income_types")
        l = [r for r in results]

        columns = ["ID", "name", "description"]
        return pd.DataFrame(l, columns=columns)

    def add_income_type(self, name, description):
        self._execute_query("""INSERT INTO income_types (name, description) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM income_types
                                              WHERE name = %s
                                              AND description = %s);""", (name, description, name, description))

    def get_accounts(self):
        results = self._read_query("""SELECT accounts.account_id, accounts.name, account_types.name, account_content.name, 
                                      O1.first_name, O2.first_name FROM accounts
                                      JOIN account_types ON accounts.type_id=account_types.account_type_id
                                      JOIN account_content ON accounts.content_id=account_content.account_content_id
                                      LEFT JOIN owners AS O1 ON accounts.owner1_id=O1.owner_id
                                      LEFT JOIN owners AS O2 ON accounts.owner2_id=O2.owner_id;""")
        l = [r for r in results]

        columns = ["ID", "name", "type", "content", "owner 1", "owner 2"]
        return pd.DataFrame(l, columns=columns)

    def add_account(self, name, account_type, account_content, owner1, owner2):
        self._execute_query("""INSERT INTO accounts (name, type_id, content_id, owner1_id, owner2_id) 
                            SELECT %s, (SELECT account_type_id FROM account_types WHERE name=%s),
                             (SELECT account_content_id FROM account_content WHERE name=%s),
                             (SELECT owner_id FROM owners WHERE first_name=%s),
                             (SELECT owner_id FROM owners WHERE first_name=%s) 
                            WHERE NOT EXISTS (SELECT * FROM accounts
                                              WHERE name = %s
                                              AND type_id = 
                                              (SELECT account_type_id FROM account_types WHERE name=%s)
                                              AND content_id = 
                                              (SELECT account_content_id FROM account_content WHERE name=%s)
                                              AND owner1_id = 
                                              (SELECT owner_id FROM owners WHERE first_name=%s)
                                              AND owner2_id = 
                                              (SELECT owner_id FROM owners WHERE first_name=%s));""",
                            (name, account_type, account_content, owner1, owner2,
                             name, account_type, account_content, owner1, owner2))

    def get_debt_types(self):
        results = self._read_query("SELECT * FROM debt_types")
        l = [r for r in results]

        columns = ["ID", "name", "description"]
        return pd.DataFrame(l, columns=columns)

    def add_debt_type(self, name, description):
        self._execute_query("""INSERT INTO debt_types (name, description) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM debt_types
                                              WHERE name = %s
                                              AND description = %s);""", (name, description, name, description))

    def get_investment_types(self):
        results = self._read_query("SELECT * FROM investment_types")
        l = [r for r in results]

        columns = ["ID", "name", "description"]
        return pd.DataFrame(l, columns=columns)

    def add_investment_type(self, name, description):
        self._execute_query("""INSERT INTO investment_types (name, description) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM investment_types
                                              WHERE name = %s
                                              AND description = %s);""", (name, description, name, description))

    def get_expense_tags(self):
        results = self._read_query("SELECT * FROM expense_tags")
        l = [r for r in results]

        columns = ["ID", "name", "description"]
        return pd.DataFrame(l, columns=columns)

    def add_expense_tag(self, name, description):
        self._execute_query("""INSERT INTO expense_tags (name, description) 
                            SELECT %s, %s 
                            WHERE NOT EXISTS (SELECT * FROM expense_tags
                                              WHERE name = %s
                                              AND description = %s);""", (name, description, name, description))

    def get_debts(self):
        results = self._read_query("""select debt.debt_id, debt.name, a.name account, t.name type,
                                        hist.amount amount, hist.value value
                                        from debts debt
                                        join (select debt_id, max(date) as latestDate
                                              from debt_history
                                              group by debt_id)
                                              debt_hist ON debt.debt_id = debt_hist.debt_id
                                        join debt_history hist on debt_hist.debt_id = hist.debt_id
                                        and debt_hist.latestDate = hist.date
                                        join accounts a on a.account_id = debt.account_id
                                        join debt_types t on t.debt_type_id = debt.type_id;""")
        l = [r for r in results]

        columns = ["ID", "name", "account", "type", "amount", "value"]
        return pd.DataFrame(l, columns=columns)

    def get_investments(self):
        results = self._read_query("""select inv.investment_id, inv.name, a.name account, t.name type,
                                        hist.amount amount, hist.value value
                                        from investments inv
                                        join (select investment_id, max(date) as latestDate
                                              from investment_history
                                              group by investment_id)
                                              inv_hist ON inv.investment_id = inv_hist.investment_id
                                        join investment_history hist on inv_hist.investment_id = hist.investment_id
                                        and inv_hist.latestDate = hist.date
                                        join accounts a on a.account_id = inv.account_id
                                        join investment_types t on t.investment_type_id = inv.type_id;""")
        l = [r for r in results]

        columns = ["ID", "name", "account", "type", "amount", "value"]
        return pd.DataFrame(l, columns=columns)

    def add_debt(self, name, account, type):
        self._execute_query("""INSERT INTO debts (name, account_id, type_id) 
                            SELECT %s, (SELECT account_id FROM accounts WHERE name=%s),
                            (SELECT debt_type_id FROM debt_types WHERE name=%s)
                            WHERE NOT EXISTS (SELECT * FROM debts
                                              WHERE name = %s
                                              AND account_id = 
                                              (SELECT account_id FROM accounts WHERE name=%s)
                                              AND type_id = 
                                              (SELECT debt_type_id FROM debt_types WHERE name=%s));""",
                            (name, account, type, name, account, type))

        results = self._read_query("""SELECT MAX(debt_id) FROM debts;""")
        l = [r[0] for r in results]

        return l[0]

    def get_expenses(self):
        results = self._read_query("""SELECT expenses.expense_id, expenses.name, accounts.account_id, expenses.date,
                                      expenses.value FROM expenses
                                      JOIN accounts ON expenses.account_id=accounts.account_id
                                      ORDER BY expenses.date DESC;""")
        l = [r for r in results]

        columns = ["ID", "name", "account", "date", "value"]
        return pd.DataFrame(l, columns=columns)

    def add_expense(self, name, account, date, value):
        self._execute_query("""INSERT INTO expenses (name, account_id, date, value) 
                            SELECT %s, (SELECT account_id FROM accounts WHERE name=%s), %s, %s
                            WHERE NOT EXISTS (SELECT * FROM expenses
                                              WHERE name = %s
                                              AND account_id = (SELECT account_id FROM accounts WHERE name=%s)
                                              AND date = %s
                                              AND value = %s);""",
                            (name, account, date, value, name, account, date, value))

        results = self._read_query("""SELECT MAX(expense_id) FROM expenses;""")
        l = [r[0] for r in results]

        return l[0]

    def add_investment(self, name, account, type):
        self._execute_query("""INSERT INTO investments (name, account_id, type_id) 
                            SELECT %s, (SELECT account_id FROM accounts WHERE name=%s),
                            (SELECT investment_type_id FROM investment_types WHERE name=%s)
                            WHERE NOT EXISTS (SELECT * FROM investments
                                              WHERE name = %s
                                              AND account_id = 
                                              (SELECT account_id FROM accounts WHERE name=%s)
                                              AND type_id = 
                                              (SELECT investment_type_id FROM investment_types WHERE name=%s));""",
                            (name, account, type, name, account, type))

        results = self._read_query("""SELECT MAX(investment_id) FROM investments;""")
        l = [r[0] for r in results]

        return l[0]

    def get_incomes(self):
        results = self._read_query("""SELECT income.income_id, income.name, income.date, accounts.account_id,
                                      income_types.income_type_id, income.value FROM income
                                      JOIN accounts ON income.account_id=accounts.account_id
                                      JOIN income_types ON income.type_id=income_types.income_type_id
                                      ORDER BY income.date DESC;""")
        l = [r for r in results]

        columns = ["ID", "name", "date", "account", "type", "value"]
        return pd.DataFrame(l, columns=columns)

    def get_incomes_filtered(self, month):
        year = datetime.datetime.today().year
        results = self._read_query("""SELECT income.income_id, income.name, income.date, accounts.account_id,
                                      income_types.income_type_id, income.value FROM income
                                      JOIN accounts ON income.account_id=accounts.account_id
                                      JOIN income_types ON income.type_id=income_types.income_type_id
                                      WHERE MONTH(income.date) = %s AND YEAR(income.date) = %s
                                      ORDER BY income.date DESC;""", (month, year))
        l = [r for r in results]

        columns = ["ID", "name", "date", "account", "type", "value"]
        return pd.DataFrame(l, columns=columns)

    def get_expenses_filtered(self, month):
        year = datetime.datetime.today().year
        results = self._read_query("""SELECT expenses.expense_id, expenses.name, accounts.account_id, expenses.date,
                                      expenses.value FROM expenses
                                      JOIN accounts ON expenses.account_id=accounts.account_id
                                      WHERE MONTH(expenses.date) = %s AND YEAR(expenses.date) = %s
                                      ORDER BY expenses.date DESC;""", (month, year))
        l = [r for r in results]

        columns = ["ID", "name", "account", "date", "value"]
        return pd.DataFrame(l, columns=columns)

    def add_income(self, account, type, name, date, value):
        self._execute_query("""INSERT INTO income (name, account_id, type_id, date, value) 
                            SELECT %s, (SELECT account_id FROM accounts WHERE name=%s),
                            (SELECT income_type_id FROM income_types WHERE name=%s), %s, %s
                            WHERE NOT EXISTS (SELECT * FROM income
                                              WHERE name = %s
                                              AND account_id = 
                                              (SELECT account_id FROM accounts WHERE name=%s)
                                              AND type_id = 
                                              (SELECT income_type_id FROM income_types WHERE name=%s)
                                              AND date=%s
                                              AND value=%s);""",
                            (name, account, type, date, value, name, account, type, date, value))

    def get_debt_history(self, debt_id):
        results = self._read_query("""SELECT debt_history.history_id, debts.name, debt_history.date,
                                      debt_history.amount, debt_history.value FROM debt_history
                                      JOIN debts ON debt_history.debt_id=debts.debt_id
                                      WHERE debt_history.debt_id=%s
                                      ORDER BY debt_history.date ASC;""", (debt_id,))
        l = [r for r in results]

        columns = ["ID", "debt", "date", "amount", "value"]
        return pd.DataFrame(l, columns=columns)

    def get_investment_history(self, investment_id):
        results = self._read_query("""SELECT investment_history.history_id, investments.name, investment_history.date,
                                      investment_history.amount, investment_history.value FROM investment_history
                                      JOIN investments ON investment_history.investment_id=investments.investment_id
                                      WHERE investment_history.investment_id=%s
                                      ORDER BY investment_history.date ASC;""", (investment_id,))
        l = [r for r in results]

        columns = ["ID", "investment", "date", "amount", "value"]
        return pd.DataFrame(l, columns=columns)

    def add_debt_history(self, debt, date, amount, value):
        self._execute_query("""INSERT INTO debt_history (debt_id, date, amount, value) 
                            SELECT %s, %s, %s, %s
                            WHERE NOT EXISTS (SELECT * FROM debt_history
                                              WHERE debt_id = %s
                                              AND date = %s
                                              AND amount = %s
                                              AND value=%s)
                              ON DUPLICATE KEY UPDATE amount=%s, value=%s;""",
                            (debt, date, amount, value, debt, date, amount, value, amount, value))

    def add_investment_history(self, investment, date, amount, value):
        self._execute_query("""INSERT INTO investment_history (investment_id, date, amount, value) 
                            SELECT %s, %s, %s, %s
                            WHERE NOT EXISTS (SELECT * FROM investment_history
                                              WHERE investment_id = %s
                                              AND date = %s
                                              AND amount = %s
                                              AND value=%s)
                            ON DUPLICATE KEY UPDATE amount=%s, value=%s;""",
                            (investment, date, amount, value, investment, date, amount, value, amount, value))

    def add_expense_tag_link(self, expense_id, tag):
        self._execute_query("""INSERT INTO expenses_tags_link (expense_id, tag_id) 
                            SELECT %s, (SELECT expense_tag_id FROM expense_tags WHERE name=%s)
                            WHERE NOT EXISTS (SELECT * FROM expenses_tags_link
                                              WHERE expense_id = %s
                                              AND tag_id = 
                                              (SELECT expense_tag_id FROM expense_tags WHERE name=%s));""",
                            (expense_id, tag, expense_id, tag))

    def get_expense_associated_tags(self, expense):
        results = self._read_query("""SELECT expense_tags.name FROM expenses_tags_link
                                      WHERE expenses_tags_link.expense_id = (SELECT expenses.expense_id FROM expenses
                                                                             WHERE expenses.name = %s)
                                              JOIN expense_tags ON expenses_tags_link.tag_id=expense_tags.tag_id;""", expense)
        l = [r for r in results]

        columns = ["ID", "name"]
        return pd.DataFrame(l, columns=columns)

