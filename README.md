# foodorderingapp

[![Test](https://github.com/JonasBerx/foodorderingapp/actions/workflows/python-test.yml/badge.svg)](https://github.com/JonasBerx/foodorderingapp/actions/workflows/python-test.yml)

Team 0 ~ Food ordering and management application using Python

## Requirements chosen

1. [x] Place order -> Customer
2. Manage order -> Employee
3. [x] Start session -> Courier
4. [x] End session -> Courier
5. Accept order delivery -> courier
6. [x] Manage menu: Changing & Removing & Adding -> Partner
7. [x] Login & Logout 
8. [x] Profile update

## Tools

- VCS: GitHub
- Programming Language: Python
- Framework: Flask
- Unit Test Tool: unittest
- TDD protocol tracking: [GitHub Actions](https://github.com/JonasBerx/foodorderingapp/actions/workflows/python-test.yml)

## How to run the program

### Requirements

- Python: 3.6 or above

### Environment

```bash
git clone https://github.com/JonasBerx/foodorderingapp.git
cd foodorderingapp
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Setup

```bash
flask mock
```

Please reset the database if its structure changes:

```bash
flask mock --reset
```

### Run

```bash
flask run
```

### Test accounts

- Courier:
    - username: `cou`
    - password: `12345`
- Customer:
    - username: `cus`
    - password: `123456`
- Employee:
    - username: `emp`
    - password: `1234567`
- Partner:
    - username: `par`
    - password: `12345678`


### Unittest 

```bash
python -m unittest
```

### Coverage 

```bash
coverage run --source=dolt -m unittest
coverage report
coverage html
```
