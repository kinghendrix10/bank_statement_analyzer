# drop 'opening' and 'closing' entries
statement = statement.drop(index=0, axis=0)
statement = statement.drop(index=-1, axis=0)