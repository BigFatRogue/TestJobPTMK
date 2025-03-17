from datetime import datetime


date_of_birth = '2009-07-12'
date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
age = int((datetime.now() - date_of_birth).days // 365)
print(age)