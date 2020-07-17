filepath= input('Enter folder path: ')
assert os.path.exists(filepath), 'Files not found at '+str(filepath)

# reading table using tabula
rows = tabula.read_pdf(filepath, pages='all', silent=True)