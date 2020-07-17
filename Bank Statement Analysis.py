#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import tabula


# In[2]:


import sys
np.set_printoptions(threshold=sys.maxsize)
pd.set_option('display.max_rows', None)


# In[3]:


BANK_DETAILS = {
    'Column Headers': {
        'Trans Date': 0,    # index of date column
        'Ref. Number': 1,     # index of reference number column
        'Transaction Details': 2,        # index of transaction column
        'Value Date': 3,        # index of value date column
        'Withdrawal(DR)': 4,           # index of debit column
        'Deposit(CR)': 5,            # index of credit no. column
        'Balance': 6      # index of balance column
   },

}


# In[4]:


filepath= input('Enter folder path: ')
assert os.path.exists(filepath), 'Files not found at '+str(filepath)

# reading table using tabula
rows = tabula.read_pdf(filepath,
                       pages='all',
                       silent=True,
                       stream=True
#                        pandas_options={
#                            'header': None,
#                            'error_bad_lines': False,
#                            'warn_bad_lines': False
                       })
# converting to list
# rows = rows.values.tolist()


# In[ ]:


rows


# In[ ]:


len(rows)


# In[7]:


rows = rows[1:198] #code to get data without the summary header


# In[14]:


statement = pd.DataFrame()

for row in rows:
    statement = pd.concat([statement, row], axis=0, ignore_index=True)


# In[15]:


statement = statement.drop(index=0, axis=0)
statement = statement.drop(index=8089, axis=0)
# statement = statement[7500:]


# In[17]:


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


# In[18]:


statement['Trans Date'] = pd.to_datetime(statement['Trans Date'], format='%d-%b-%Y')
statement['Value Date'] = pd.to_datetime(statement['Value Date'], format='%d-%b-%Y')


# In[19]:


statement['Ref. Number'] = statement['Ref. Number'].fillna('None')
statement = statement.reset_index()


# In[20]:


p_i = statement['Transaction Details']


# In[21]:


from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords


import re, string

def remove_noise(transaction):
    stop_words = stopwords.words('english')
    my_stopwords = set({'online', 'payment', 'fip', 'nip', 'fcm', 'dia', 'uba',
                        'trsf', 'frm', 'trf', 'ifo', 'trn', 'trns', 'mr', 'mrs',
                        'txn', 'txns', 'fr', 'mobile', 'ltd' ,'funds', 'dep', 'web',
                        'fcmb', 'fbn', 'union', 'from', 'gtb', 'zib', 'bank', 'ft',
                       'fid', 'ib', 'ubn', 'fbnmobile', 'fbn mobile', 'withdrawal',
                       'credit', 'debit', 'bo', 'deb', 'cred', 'trnf',
                        'trfr', 'ussd', 'neft', 'via', 'eco', 'tud', 'intl', 'int',
                       'intnl', 'atm', 'pos', 'user', 'scb', 'cash', '3rd', 'party'})
    cleaned_transaction = []
    for token, tag in pos_tag(transaction):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        token = re.sub(r'(?<=\d)[,\.]',"", token) #remove decimals
        token = re.sub(r'\d+\/\d+\/\d+',"", token) #remove dates
#         token = re.sub("\d+","", token) #remove numbers
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words and token.lower() not in my_stopwords:
               cleaned_transaction.append(token.lower())
    return cleaned_transaction


# In[22]:


from nltk.tokenize import word_tokenize

tokenized_trans = []
for trans in p_i:
    tokenized_trans.append(word_tokenize(trans))


# In[23]:


cleaned_tokens_list = []
for tokens in tokenized_trans:
    cleaned_tokens_list.append(remove_noise(tokens))


# In[24]:


statement['Clean Txn'] = pd.Series(cleaned_tokens_list)

statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace('[', '')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace(']', '')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace(',', ' ')
statement['Clean Txn'] = statement['Clean Txn'].astype(str).str.replace(r"[\"\',]", '')


# In[25]:


import textdistance as td
# from fuzzywuzzy import process, fuzz

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
                    
#     similairity.append(process.extract(string1, string2.split(), scorer=fuzz.ratio)[0][1])          
#     print (table[i], ':', score[i])
#     for index in range(0, nr_matches):
        
    
    i += 1
    
matching_table = pd.DataFrame({'trans_date': date, 'left_side': left_side, 'similarity': similarity,
                               'right_side': right_side, 'credit': credit, 'debit': debit})

graph_table = pd.DataFrame({'trans_date': date, 'row_data': row_data, 'similarity': similarity,
                               'right_side': right_side, 'credit': credit, 'debit': debit})


# In[26]:


matching_table = pd.DataFrame({'trans_date': date, 'left_side': left_side, 'similarity': similarity,
                               'right_side': right_side, 'credit': credit, 'debit': debit})

matching_table


# In[92]:


graph_table = pd.DataFrame({'trans_date': date, 'row_data': row_data, 'similarity': similarity,
                               'right_side': right_side, 'credit': credit, 'debit': debit})

graph_table


# In[28]:


graph_table.groupby('row_data')[['credit', 'debit']].sum()


# In[100]:


graph_data = pd.DataFrame(graph_table.groupby('row_data')[['credit', 'debit']].sum())

transaction_type = []
for ind, row in graph_data.iterrows():
    if row['credit'] == 0:
        transaction_type.append('debit')
    else: transaction_type.append('credit')
        
graph_data['transaction_type'] = transaction_type
graph_data['amount'] = graph_data['credit'] + graph_data['debit']

graph_data[['credit', 'debit']].plot(kind='bar', figsize=(20,10))


# In[93]:


transaction_type = []
for ind, row in graph_table.iterrows():
    if row['credit'] == 0:
        transaction_type.append('debit')
    else: transaction_type.append('credit')
        
graph_table['transaction_type'] = transaction_type
graph_table['amount'] = graph_table['credit'] - graph_table['debit']
graph_table


# In[94]:


import seaborn as sns

plot = sns.factorplot(x='trans_date', y='amount', hue ='transaction_type', kind='bar', data=graph_table, aspect=10)
plot.fig.set_size_inches(30,8)
sns.despine()


# In[90]:


transaction_type = []
for ind, row in statement.iterrows():
    if row['Deposit(CR)'] == 0:
        transaction_type.append('debit')
    else: transaction_type.append('credit')
        
statement['transaction_type'] = transaction_type
statement['amount'] = statement['Deposit(CR)'] - statement['Withdrawal(DR)']


# In[91]:


plot = sns.relplot(x='Trans Date', y='amount', hue ='transaction_type', kind='line', data=statement,
                   ci=None, height=40, aspect=10)
plot.fig.set_size_inches(30,8)
sns.despine()


# In[97]:


statement.sort_values('Deposit(CR)', ascending=False)



