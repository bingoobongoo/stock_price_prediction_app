# Database

Below you can find basic information about used database.

## Entities

List of entities in a database:

* ***company*** table
* ***stock_price*** table
* ***indicator*** table
* ***financial_statement*** table
* ***income*** table
* ***balance_sheet*** table
* ***cash_flow*** table
* ***ratio*** table

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

### financial_statement

* ***financial_statement_id*** *uuid* **DEFAULT gen_random_uuid()** [PK]
* ***quarter_ending*** *date*
* ***company_id*** *integer* **NOT NULL** [FK]

**FOREIGN KEY** ***company_id*** **REFERENCES** ***company(company_id)***

### income

* ***financial_statement_id*** *uuid* **NOT NULL** [PK] [FK]
* ***revenue*** *bigint*
* ***gross_profit*** *bigint*
* ***operating_income*** *bigint*
* ***net_income*** *bigint*
* ***ebt*** *bigint*
* ***ebitda*** *bigint*
* ***ebit*** *bigint*
* ***eps_diluted*** *real*
* ***gross_margin*** *real*
* ***operating_margin*** *real*
* ***profit_margin*** *real*
* ***shares_outstanding*** *bigint*

**FOREIGN KEY** ***financial_statement_id*** **REFERENCES** ***financial_statement(financial_statement_id)***

### balance_sheet

* ***financial_statement_id*** *uuid* **NOT NULL** [PK] [FK]
* ***cash_and_short_term_investments*** *bigint*
* ***net_cash_per_share*** *bigint*
* ***receivables*** *bigint*
* ***inventory*** *bigint*
* ***current_assets*** *bigint*
* ***total_assets*** *bigint*
* ***accounts_payable*** *bigint*
* ***total_debt*** *bigint*
* ***current_liabilities*** *bigint*
* ***total_liabilities*** *bigint*
* ***shareholders_equity*** *bigint*

**FOREIGN KEY** ***financial_statement_id*** **REFERENCES** ***financial_statement(financial_statement_id)***

### cash_flow

* ***financial_statement_id*** *uuid* **NOT NULL** [PK] [FK]
* ***cash_flow_margin*** *real*
* ***operating_cash_flow*** *bigint*
* ***investing_cash_flow*** *bigint*
* ***financing_cash_flow*** *bigint*
* ***net_cash_flow*** *bigint*
* ***free_cash_flow*** *bigint*
* ***free_cash_flow_per_share*** *real*

**FOREIGN KEY** ***financial_statement_id*** **REFERENCES** ***financial_statement(financial_statement_id)***

### ratio

* ***financial_statement_id*** *uuid* **NOT NULL** [PK] [FK]
* ***market_cap*** *bigint*
* ***enterprise_value*** *bigint*
* ***price_to_earnings*** *real*
* ***price_to_sales*** *real*
* ***price_to_book*** *real*
* ***price_to_fcf*** *real*
* ***ev_to_ebit*** *real*
* ***ev_to_ebitda*** *real*
* ***debt_to_equity*** *real*
* ***debt_to_ebitda*** *real*
* ***quick_ratio*** *real*
* ***current_ratio*** *real*
* ***asset_turnover*** *real*
* ***roe*** *real*
* ***roa*** *real*
* ***roic*** *real*
* ***shareholder_return*** *real*

**FOREIGN KEY** ***financial_statement_id*** **REFERENCES** ***financial_statement(financial_statement_id)***

*More attributes and relationships will be added.*
