import click

from dolt import app, db
from dolt.models import Courier, Customer, Employee, Food, Order, Partner


@app.cli.command()
@click.option("--reset", is_flag=True, help="Please reset the database when structure changes")
def mock(reset):
    # Generate the local test data
    reset and db.drop_all()
    db.create_all()

    courier = Courier(name="COU", username="cou")  # noqa
    courier.set_password("12345")
    customer = Customer(name="CUS", username="cus")  # noqa
    customer.set_password("123456")
    employee = Employee(name="EMP", username="emp")  # noqa
    employee.set_password("1234567")
    partner1 = Partner(name="Restaurant 1", username="par")  # noqa
    partner1.set_password("12345678")
    partner2 = Partner(name="Restaurant 2", username="par2")  # noqa
    partner2.set_password("12345678")

    food_1 = Food(name="Food 1", restaurant=partner1)
    food_2 = Food(name="Food 2", restaurant=partner1)
    food_a = Food(name="Food A", restaurant=partner2)
    food_b = Food(name="Food B", restaurant=partner2)

    order = Order(
        status="finished",
        foods=[food_1],
        customer=customer,
        restaurant=food_1.restaurant
    )
    order.courier = courier

    db.session.add_all(
        [courier, customer, employee, partner1, partner2,
         food_1, food_2, food_a, food_b,
         order]
    )
    db.session.commit()

    click.echo("Mock done" if not reset else "Reset done")
