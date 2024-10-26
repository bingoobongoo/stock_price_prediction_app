# Stock Price Prediction

This project is under development. The final goal is to be able to predict stock price of a company based on some data.

## Database

Database schema is saved as a ***stock_price.tar*** file. For more details about database (i.e entities, attributes and relationships) check the ***DATABASE.md*** file.

> Note that the ***stock_price.tar*** file is just a schema for database. The actual data is downloaded using scripts.

## Data Extraction

First step is to aquire all the data required to train an AI model:

* **Companies** data - the first thing we have to extract is basic information about companies we will be training our model on. The ***company_data.ipynb*** script uses ***companies_data.csv*** to create a table which then is transferred to database as a table ***company***.
* **OLHC** data - after we create table with companies, we can start downloading OLHC (close, open, low, high, volume) values for every company and store them in seperate table called ***stock_price***. The ***olhc_data.ipynb*** script do just that.
* **Indicator** data - third step is to run ***indicator_data.ipynb*** script which will calculate basic technical analysis indicators. The result will be saved as a ***indicator*** table.

*Further steps will be added.*
