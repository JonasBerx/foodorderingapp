import click

from dolt import app, db
from dolt.models import Courier, Customer, Employee, Food, Order, Partner


@app.cli.command()
@click.option("--reset", is_flag=True, help="Please reset the database when structure changes")
def mock(reset):
    # Generate the local test data
    reset and db.drop_all()
    db.create_all()  # noqa

    courier = Courier(name="Homer Simpson", username="cou")  # noqa
    courier.set_password("12345")
    customer = Customer(name="Bart Simpson", username="cus", address="Earth, the Solar System")  # noqa
    customer.set_password("123456")
    employee = Employee(name="Lisa Simpson", username="emp")  # noqa
    employee.set_password("1234567")
    partner1 = Partner(name="Marge's", username="par")  # noqa
    partner1.set_password("12345678")
    partner2 = Partner(name="Maggie's", username="par2")  # noqa
    partner2.set_password("12345678")

    food_1 = Food(name="Garlic Bread", restaurant=partner1, price=6.99)
    food_2 = Food(name="Cheese Balls", restaurant=partner1, price=7.99)
    food_a = Food(name="Onion Rings", restaurant=partner2, price=10.99)
    food_b = Food(name="Vegetable Soup", restaurant=partner2, price=12.99)
    food_burger = Food(
        name="Burgers and Pancakes",
        restaurant=partner2,
        price=12.99
    )

    order = Order(
        status="finished",
        foods=[food_1],
        customer=customer,
        restaurant=food_1.restaurant
    )
    order.courier = courier

    order2 = Order(
        status="ongoing",
        foods=[food_burger],
        customer=customer,
        restaurant=food_burger.restaurant
    )
    courier2 = Courier(name="Homer Simpson 2", username="cou2")  # noqa
    courier2.set_password("12345")
    order2.courier = courier2

    db.session.add_all(
        [courier, customer, employee, partner1, partner2,
         food_1, food_2, food_a, food_b, food_burger,
         order, order2, courier2]
    )
    db.session.commit()

    click.echo("Mock done" if not reset else "Reset done")
