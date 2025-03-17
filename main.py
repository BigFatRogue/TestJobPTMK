from sys import argv
from db import DataBaseAfterOptimization, Employee, EmployeeRandomGenerator


_, *mode = argv


class App:
    def __init__(self, mode: int):
        self.mode = mode

    def run(self):        
        if len(self.mode) == 1:
            getattr(self, f'mode_{self.mode[0]}')()
        else:
            mode, *paremters = self.mode
            getattr(self, f'mode_{mode}')(paremters)
    
    def mode_1(self):
        DataBaseAfterOptimization().create_db()
        print('База данных создана')
        
    def mode_2(self, parameters):
        db = DataBaseAfterOptimization()
        db.add_employee(Employee(*parameters))
        print(F'Пользователь {parameters} добавлен')

    def mode_3(self):
        DataBaseAfterOptimization().get_unuque()
    
    def mode_4(self):
        gen = EmployeeRandomGenerator()
        lst = gen.generate_epmployees(count_radnom=1_000_000, count_special=100)
        DataBaseAfterOptimization().add_employees(lst)
        print('Добавлено 1_000_000 случайных пользователей и 100 специальных')

    def mode_5(self):
        db = DataBaseAfterOptimization()
        query = """SELECT *
                    FROM employee
                    WHERE fullname LIKE 'F%' AND gender = 'Male'
                    """
        db.query(query)


if __name__ == '__main__':
    app = App(mode)
    app.run()
