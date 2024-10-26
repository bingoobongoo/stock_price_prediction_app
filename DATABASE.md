# Database

Below you can find basic information about used database.

## Entities

List of entities in a database:

* ***company*** table
* ***stock_price*** table
* ***indicator*** table

*More entities will be added.*

## Attributes and Relationships

List of columns for each table:

### company

* ***company_id*** *integer* **SERIAL** [PK]
* ***name*** *varchar(255)* **NOT NULL**
* ***country*** *varchar(255)* **NOT NULL**
* ***ticker*** *varchar(16)* **NOT NULL**
* ***sector*** *varchar(255)* **NOT NULL**
* ***industry*** *varchar(255)* **NOT NULL**
* ***market_cap*** *bigint* **NOT NULL**

### stock_price

* ***stock_price_id*** *uuid* **DEFAULT gen_random_uuid()** [PK]
* ***company_id*** *integer* **NOT NULL** [FK]
* ***date*** *date* **NOT NULL**
* ***close*** *real* **NOT NULL**
* ***open*** *real* **NOT NULL**
* ***low*** *real* **NOT NULL**
* ***high*** *real* **NOT NULL**
* ***volume*** *bigint* **NOT NULL**

**FOREIGN KEY** ***company_id*** **REFERENCES** ***company(company_id)***

### indicator

* ***stock_price_id*** *uuid* **NOT NULL** [PK] [FK]
* ***rsi*** *double precison*
* ***obv*** *bigint*
* ***roc*** *double precison*
* ***uo*** *double precison*
* ***ppo*** *double precison*
* ***adi*** *double precison*
* ***atr*** *double precison*
* ***bollinger_lband*** *double precison*
* ***bollinger_mband*** *double precison*
* ***bollinger_hband*** *double precison*
* ***adx*** *double precison*
* ***aroon_down*** *double precison*
* ***aroon_up*** *double precison*
* ***macd*** *double precison*
* ***so*** *double precison*
* ***minus_di*** *double precison*
* ***plus_di*** *double precison*

**FOREIGN KEY** ***stock_price_id*** **REFERENCES** ***stock_price(stock_price_id)***

*More attributes and relationships will be added.*
