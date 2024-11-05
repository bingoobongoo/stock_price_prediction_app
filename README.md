# Stock Price Prediction

This project is **UNDER DEVELOPMENT**. The final goal is to be able to predict stock price of a company based on OLHC chart and financial statements data.

**Platform:** WSL Ubuntu

## Installation

Here are all the steps to run the project on your computer.

Install `postgresql`:

```text
sudo apt update
sudo apt install postgresql postgresql-contrib
```

Confirm the installation:

```text
psql --version
```

Give `postgres` user a password:

```text
sudo passwd postgres
```

Close and reopen terminal, then type:

```text
sudo service postgresql start
```

Now, when postgreSQL is installed, clone this repository:

```text
git clone git@github.com:bingoobongoo/stock_price_prediction_app.git
cd ./stock_price_prediction
```

Install all required packages:

```text
pip install -r requirements.txt
```

## Creating database

Make sure you have stable network connection and run:

```text
python3 main.py postgres <password> <databaseName>
```

Additionally, you can also specify **port** on which postgreSQL is running (default is 5432):

```text
python3 main.py postgres <password> <databaseName> <port>
```

After this you can minimize the terminal window and wait until database is created.
> The whole process can take approximately 20 minutes.

## Database

Database schema is saved as a ***nasdaq_companies_backup.tar*** file. For more details about database (i.e entities, attributes and relationships) check the [***DATABASE.md***](DATABASE.md) file.

> Note that the ***nasdaq_companies_backup.tar*** file is just a schema for database. The actual data is downloaded using ***main.py*** script.

*Further information will be added.*
