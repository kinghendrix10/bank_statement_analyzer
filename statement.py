# store list as a DataFrame

statement = pd.DataFrame()

for row in rows:
    statement = pd.concat([statement, row], axis=0, ignore_index=True)