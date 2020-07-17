transaction_type = []
for ind, row in statement1.iterrows():
    if row['Deposit(CR)'] == 0:
        transaction_type.append('debit')
    else: transaction_type.append('credit')
        
statement['transaction_type'] = transaction_type
statement['amount'] = statement['Deposit(CR)'] - statement['Withdrawal(DR)']

plot = sns.relplot(x='Trans Date', y='amount', hue ='transaction_type', kind='line', data=statement,
                   ci=None, height=40, aspect=10)
plot.fig.set_size_inches(30,8)
sns.despine()