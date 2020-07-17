trans = statement['Transaction Details']
tokenized_trans = []
for trans in trans:
    tokenized_trans.append(word_tokenize(trans))
    
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
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
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
    
  cleaned_tokens_list = []
for tokens in tokenized_trans:
    cleaned_tokens_list.append(remove_noise(tokens))