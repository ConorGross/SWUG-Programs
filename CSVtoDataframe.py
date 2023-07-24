import datetime

# input date
date_string = '07.07.23'
date_format = '%m.%d.%y'

# using try-except blocks for handling the exceptions
try:
    datetime.datetime.strptime(date_string, date_format)
    print('good')
except ValueError:
    print("Incorrect data format")