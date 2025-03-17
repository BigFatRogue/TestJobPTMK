import sqlite3
from datetime import datetime   
import string
import random
from time import time
import timeit
from siiting import *


class Employee:
    def __init__(self, fullname: str, date_of_birth: str, gender: str):
        self.fullname = fullname
        self.date_of_birth = date_of_birth
        self.gender = gender

    def full_age(self) -> int:
        date_of_birth = datetime.strptime(self.date_of_birth, '%Y-%m-%d')
        now = datetime.now()
        return now.year - date_of_birth.year - ((now.month, now.day) < (date_of_birth.month, date_of_birth.day))
    
    def to_tuple(self) -> tuple:
        return self.fullname, self.date_of_birth, self.gender

    def __str__(self):
        return f'{self.fullname}, {self.date_of_birth}, {self.gender}, {self.full_age()}'

    def __repr__(self):
        return self.__str__()


class EmployeeRandomGenerator:
    def __init__(self):
        self.gender = ('Male', 'Female')
        self.first_letters = string.ascii_uppercase

    def _generate_special_epmployee(self) -> str:
        first_name = 'F' + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 6)))
        last_name = ''.join(random.choices(self.first_letters)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(7, 10)))
        patronymic = ''.join(random.choices(self.first_letters)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 12)))
        fullname = f'{first_name} {last_name} {patronymic}'

        date_of_birth = f'{random.randint(1950, 2006)}-{random.randint(1, 12)}-{random.randint(1, 28)}'

        return Employee(fullname, date_of_birth, 'Female')
        

    def _generate_epmployee(self) -> Employee:
        first_name = ''.join(random.choices(self.first_letters)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 6)))
        last_name = ''.join(random.choices(self.first_letters)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(7, 10)))
        patronymic = ''.join(random.choices(self.first_letters)) + ''.join(random.choices(string.ascii_lowercase, k=random.randint(8, 12)))
        fullname = f'{first_name} {last_name} {patronymic}'

        date_of_birth = f'{random.randint(1950, 2006)}-{random.randint(1, 12)}-{random.randint(1, 28)}'

        return Employee(fullname, date_of_birth, random.choice(self.gender))
    
    def generate_epmployees(self, count_radnom: int, count_special: int) -> list:
        lst = [self._generate_epmployee() for _ in range(count_radnom)]
        lst += [self._generate_special_epmployee() for _ in range(count_special)]
        return lst


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()
    
    def query(self, query: str) -> None:
        self.cursor.execute(query)
    
    def create_db() -> None:
        ...
    
    def add_employee(self, employee: Employee) -> None:
        ...
    
    def add_employees(self, employees: list) -> None:
        ...
    
    def get_unuque(self) -> None:
        ...

    def query(self, query: str) -> None:
        ...
 

class DataBaseBeforeOptimization(Database):    
    def create_db(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            fullname TEXT NOT NULL, 
                            date_of_birth TEXT NOT NULL, 
                            gender TEXT NOT NULL
                            )
                            ''')
        self.close()

    def add_employee(self, employee: Employee) -> None:
        self.cursor.execute(f'INSERT INTO employee (fullname, date_of_birth, gender) VALUES (?, ?, ?)', (employee.to_tuple()))
        self.close()
    
    def add_employees(self, employees: list) -> None:
        lst = [emp.to_tuple() for emp in employees]
        self.cursor.executemany('INSERT INTO employee (fullname, date_of_birth, gender) VALUES (?, ?, ?)', lst)
        self.close()

    def get_unuque(self) -> None:
        self.cursor.execute("""
                            SELECT DISTINCT fullname, date_of_birth, gender 
                            FROM employee
                            WHERE (fullname, date_of_birth) IN (
                                SELECT fullname, date_of_birth
                                FROM employee
                                GROUP BY fullname, date_of_birth
                                HAVING COUNT(*) = 1
                            )
                            """)
        
        for item in self.cursor.fetchall():
            emp = Employee(*item)
            print(emp)
        self.close() 


class DataBaseAfterOptimization(Database):    
    def create_db(self) -> None:
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employee_male (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            fullname TEXT NOT NULL, 
                            date_of_birth TEXT NOT NULL, 
                            gender TEXT NOT NULL
                            )
                            ''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employee_female (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            fullname TEXT NOT NULL, 
                            date_of_birth TEXT NOT NULL, 
                            gender TEXT NOT NULL
                            )
                            ''')
        self.close()
    
    def add_employee(self, employee: Employee) -> None:
        table = 'employee_male' if  employee.gender == 'male' else 'employee_female'
        self.cursor.execute(f'INSERT INTO {table} (fullname, date_of_birth, gender) VALUES (?, ?, ?)', (employee.to_tuple()))
        self.close()
    
    def add_employees(self, employees: list) -> None:
        lst_male = []
        lst_female = []
        for emp in employees:
            if emp.gender == 'Male':
                lst_male.append(emp.to_tuple())
            else:
                lst_female.append(emp.to_tuple())

        self.cursor.executemany('INSERT INTO employee_male (fullname, date_of_birth, gender) VALUES (?, ?, ?)', lst_male)
        self.cursor.executemany('INSERT INTO employee_female (fullname, date_of_birth, gender) VALUES (?, ?, ?)', lst_female)
        self.close()

    def get_unuque(self) -> None:
        self.cursor.execute("""
                            WITH fg AS (SELECT * FROM employee_male UNION ALL SELECT * FROM employee_female) 
                            SELECT DISTINCT fullname, date_of_birth, gender 
                            FROM fg
                            WHERE (fullname, date_of_birth) IN (
                                SELECT fullname, date_of_birth
                                FROM fg
                                GROUP BY fullname, date_of_birth
                                HAVING COUNT(*) = 1
                            )
                            """)
        for item in self.cursor.fetchall():
            emp = Employee(*item)
            print(emp)
        self.close()       


if __name__ == '__main__':
    db_after = DataBaseAfterOptimization()
    db_before = DataBaseBeforeOptimization()
    
    # db_before.create_db()
    # db_after.create_db()

    # mode 4
    gen = EmployeeRandomGenerator()
    lst = gen.generate_epmployees(1_000_000, 200)
    db_after.add_employees(lst)
    db_before.add_employees(lst)

    # mode 5
    # def mode5():
    #         query = """SELECT *
    #         FROM employee_male
    #         WHERE fullname LIKE 'F%' AND gender = 'Male'
    #         """
    #         db_before.query(query)

    # execution_time = timeit.timeit(mode5, number=1)
    # print(f"Время выполнения запроса: {execution_time:.4f} секунд")
    # db_after.close()
    



    

    


