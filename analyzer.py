statement['Clean Txn'] = pd.Series(cleaned_tokens_list)

table = []
left_side = []
right_side = []
similarity = []
date = []
credit = []
debit = []
row_data = []
        
i = 0
for ind, row in statement.iloc[:].iterrows():
    string1 = row['Clean Txn']
    for ind_copy, row_copy in statement.iloc[i:].iterrows():
        string2 = row_copy['Clean Txn']
        if (string1 + string2) not in table and (string2 + string1) not in table:
            table.append(string1 + string2)
            trans_date = row_copy['Trans Date']
            cred = row_copy['Deposit(CR)']
            deb = row_copy['Withdrawal(DR)']
            if deb > 5000 or deb == 0:
                score = td.ratcliff_obershelp(string1, string2)
                if score >= 0.7 and string2 not in right_side:
                    date.append(trans_date)
                    row_data.append(string1)
                    similarity.append(score)
                    right_side.append(string2)
                    credit.append(cred)
                    debit.append(deb)
                    if string1 not in left_side: left_side.append(string1)
                    else: left_side.append('-')       
    
    i += 1
    
matching_table = pd.DataFrame({'trans_date': date, 'left_side': left_side, 'similarity': similarity,
                               'right_side': right_side, 'credit': credit, 'debit': debit})

graph_table = pd.DataFrame({'trans_date': date, 'row_data': row_data, 'similarity': similarity,
                               'right_side': right_side, 'credit': credit, 'debit': debit})