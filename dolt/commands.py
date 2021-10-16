import click

from dolt import app, db
from dolt.models import Courier, Customer, Employee, Partner


@app.cli.command()
def mock():
    # Generate the local test data
    db.create_all()

    courier = Courier(name="COU", username="cou") # noqa
    courier.set_password("12345")
    customer = Customer(name="CUS", username="cus") # noqa
    customer.set_password("123456")
    employee = Employee(name="EMP", username="emp") # noqa
    employee.set_password("1234567")
    partner = Partner(name="PAR", username="par") # noqa
    partner.set_password("12345678")

    db.session.add_all([courier, customer, employee, partner])
    db.session.commit()

    click.echo("Mock done")
