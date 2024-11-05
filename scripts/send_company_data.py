import pandas as pd
import sqlalchemy

def run(username, password, database, port):
    engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@localhost:{port}/{database}")
    companies_df = pd.read_csv("companies_data/companies_data.csv")

    tickers = companies_df["Symbol"]
    names = companies_df["Name"]
    sectors = companies_df["Sector"]
    sub_industries = companies_df["Industry"]
    countries = companies_df["Country"]

    companies_dict = {
        "name":names,
        "country":countries,
        "ticker":tickers,
        "sector":sectors,
        "industry":sub_industries
    }

    companies_df = pd.DataFrame(companies_dict)
    companies_df.dropna(inplace=True)

    companies_df.to_sql(
        name="company",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Company data successfully sent to '{database}'\n")