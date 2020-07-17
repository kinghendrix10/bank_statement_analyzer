graph_data = pd.DataFrame(graph_table.groupby('row_data')[['credit', 'debit']].sum())

transaction_type = []
for ind, row in graph_data.iterrows():
    if row['credit'] == 0:
        transaction_type.append('debit')
    else: transaction_type.append('credit')
        
graph_data['transaction_type'] = transaction_type
graph_data['amount'] = graph_data['credit'] + graph_data['debit']

graph_data[['credit', 'debit']].plot(kind='bar', figsize=(20,10))