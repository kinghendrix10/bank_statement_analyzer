statement['Withdrawal(DR)'] = statement['Withdrawal(DR)'].str.replace(',', '')
statement['Deposit(CR)'] = statement['Deposit(CR)'].str.replace(',', '')
statement['Balance'] = statement['Balance'].str.replace(',', '')

statement['Withdrawal(DR)'] = statement['Withdrawal(DR)'].astype(float).round(2)
statement['Deposit(CR)'] = statement['Deposit(CR)'].astype(float).round(2)
statement['Balance'] = statement['Balance'].astype(float).round(2)

statement['Transaction Details'] = statement['Transaction Details'].astype(str).str.replace('/', ' ')
statement['Transaction Details'] = statement['Transaction Details'].astype(str).str.replace('\\', ' ')
statement['Transaction Details'] = statement['Transaction Details'].astype(str).str.replace(':', ' ')
statement['Transaction Details'] = statement['Transaction Details'].astype(str).str.replace('-', ' ')
statement['Transaction Details'] = statement['Transaction Details'].astype(str).str.replace('\\r', ' ')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace('[', '')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace(']', '')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace(',', ' ')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace(r"[\"\',]", '')

statement['Trans Date'] = pd.to_datetime(statement['Trans Date'], format='%d-%b-%Y')
statement['Value Date'] = pd.to_datetime(statement['Value Date'], format='%d-%b-%Y')

statement['Ref. Number'] = statement['Ref. Number'].fillna('None')
statement = statement.reset_index()