# Functional Tests

## Setup

We use `selenium` as the testing tool, please install it.

```bash
pip install chromedriver-binary selenium
```

We also use [Selenium IDE](https://www.selenium.dev/selenium-ide/) to automatically save and run the tests, please install the corresponding extension in the browser.

Quick guide:

```bash
git clone https://github.com/JonasBerx/foodorderingapp.git
cd foodorderingapp
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
flask mock --reset
flask run
```

Then open another terminal in this path.

```bash
cd risks_based_tests/functional
```

## AFT01 - AFT07

Since the first 7 parts do not need to artificially simulate POST requests, we use [Selenium IDE](https://www.selenium.dev/selenium-ide/). 

Please use this file: [aft01-07.side](./aft01-07.side)

Result: All tests passed.

## AFT08 

```bash
python aft08.py
```

Result: All tests passed.

## AFT09

```bash
python aft09.py
```

Result: All tests passed.

## AFT10

```bash
python aft10.py
```

Result: All tests passed.

## AFT11

```bash
python aft11.py
```

Result: All tests passed.

## AFT12

```bash
python aft12.py
```

Result: All tests passed.
