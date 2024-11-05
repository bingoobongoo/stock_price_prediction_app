import pandas as pd
import sqlalchemy
import yfinance as yf

def run(username, password, database, port):
    engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@localhost:{port}/{database}")
    company_data = pd.read_sql("SELECT company_id, ticker FROM company", con=engine, index_col="company_id")
    n_companies = company_data.shape[0]
    counter = 1
    for ticker in company_data["ticker"]:
        company_id = company_data.index[company_data["ticker"] == ticker].tolist().pop(0)

        try:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(period="max").reset_index()
        except:
            print(f"No data available for {ticker} company. Skipping...")
            continue
        
        stock_data["company_id"] = company_id
        stock_data_dict = {
            "company_id":stock_data["company_id"],
            "date":stock_data["Date"],
            "close":stock_data["Close"],
            "open":stock_data["Open"],
            "low":stock_data["Low"],
            "high":stock_data["High"],
            "volume":stock_data["Volume"]
        }
        stock_data = pd.DataFrame(stock_data_dict)
        stock_data.dropna(inplace=True)
        stock_data.to_sql(
            name="stock_price",
            con=engine,
            if_exists="append",
            index=False
        )

        print(f"Successfully downloaded {ticker} stock data to '{database}'! [{counter}/{n_companies}]")
        counter += 1
    print(f"Downloading stock data completed!\n")