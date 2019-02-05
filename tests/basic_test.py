from lxml import etree
from xmlwriter import models
from xmlwriter import elements
from xmlwriter import attributes


class Employees(models.Model):
    name = attributes.StringAttribute()


class Employee(models.Model):

    pk = attributes.IntegerAttribute()
    first_name = elements.StringElement(default='')
    last_name = elements.StringElement(default='')
    salary = attributes.IntegerAttribute(default=100)

    class company(models.Model):
        name = elements.StringElement()
        country = elements.StringElement()

    class school(models.Model):
        name = elements.StringElement()
        country = elements.StringElement()


def test_employees():
    employees = Employees('werknemers')
    for i in range(5):
        employee = Employee(
            i,
            salary=i * 100,
            company=Employee.company(
                name='Google',
                country='US',
            ),
            school=dict(
                name='Spam',
                country='NL',
            ),
        )

        employees.append(employee)

    a = etree.tostring(employees, pretty_print=True).decode('utf-8').strip()
    b = \
        '''
<Employees name="werknemers">
  <Employee pk="0" salary="0">
    <company>
      <name>Google</name>
      <country>US</country>
    </company>
    <school>
      <name>Spam</name>
      <country>NL</country>
    </school>
  </Employee>
  <Employee pk="1" salary="100">
    <company>
      <name>Google</name>
      <country>US</country>
    </company>
    <school>
      <name>Spam</name>
      <country>NL</country>
    </school>
  </Employee>
  <Employee pk="2" salary="200">
    <company>
      <name>Google</name>
      <country>US</country>
    </company>
    <school>
      <name>Spam</name>
      <country>NL</country>
    </school>
  </Employee>
  <Employee pk="3" salary="300">
    <company>
      <name>Google</name>
      <country>US</country>
    </company>
    <school>
      <name>Spam</name>
      <country>NL</country>
    </school>
  </Employee>
  <Employee pk="4" salary="400">
    <company>
      <name>Google</name>
      <country>US</country>
    </company>
    <school>
      <name>Spam</name>
      <country>NL</country>
    </school>
  </Employee>
</Employees>
    '''.strip()

    a = str(a).split('\n')
    b = str(b).split('\n')
    for line_a, line_b in zip(a, b):
        # print((line_a, line_b))
        print('%-50s %-50s' % (line_a, line_b))
    #     print(tabulate.tabulate(line))

    # print(a)
    # print(b)

    # print(repr(a[-100:]))
    # print(repr(b[-100:]))
    assert a == b


def test_employee():
    employees = Employees('werknemers')
    for i in range(2):
        employee = Employee(
            123,
            first_name='Guido',
            last_name='van Rossum',
            salary=1000000,
            company=Employee.company(
                name='Google',
                country='US',
            ),
            school=dict(
                name='Spam',
                country='NL',
            ),
        )

        employees.append(employee)

    print('name: %s %s' % (employee.first_name, employee.last_name))
    print('company: %s %s' % (employee.company, employee.company.name))
    print('school: %s %s' % (employee.school, employee.school.name))
    print(etree.tostring(employees, pretty_print=True).decode('utf-8'))


if __name__ == '__main__':
    test_employees()

