from xmlwriter import models
from xmlwriter import fields


class Employee(fields.Element):
    pk = fields.IntegerNode()
    first_name = fields.StringNode()
    last_name = fields.StringNode()
    salary = fields.IntegerNode()


def test_employee():
    employee = Employee(
        123,
        first_name='Guido',
        last_name='van Rossum',
        salary=1000000,
    )

    print(employee)


if __name__ == '__main__':
    test_employee()
