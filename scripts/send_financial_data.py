import pandas as pd
import numpy as np
import sqlalchemy
import os
from functools import reduce
from scripts.create_db import run_comnmand

def get_csv_paths(directory) -> list[list[str]]:
    path_list = []
    for company_ticker in sorted(os.listdir(directory)):
        company_path = os.path.join(directory, company_ticker)
        if os.path.isdir(company_path) and not company_path.endswith(".ipynb_checkpoints"):
            assert len(os.listdir(company_path)) == 4, f"Missing a CSV data in {company_path}. Expected 4 CSV files, found {len(os.listdir(company_path))}."
            company_csvs = []
            for csv_file in os.listdir(company_path):
                csv_path = os.path.join(company_path, csv_file)
                assert csv_path.endswith(".csv"), f"{csv_path} not a CSV file."
                company_csvs.append(csv_path)
            path_list.append(company_csvs)
    return path_list

def get_formated_df_from_csv_path(csv_path) -> pd.DataFrame:
    df = pd.read_csv(csv_path, na_values=["-"])
    df = df.transpose()
    df.reset_index(inplace=True)
    df.columns = df.iloc[0,:]
    df.drop(labels=0, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    if df.iloc[0]["Quarter Ending"] == "Current":
        df.drop(labels=0, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df

def merge_dfs(data_frames) -> pd.DataFrame:   
    n_rows = [df.shape[0] for df in data_frames]
    assert all(i == n_rows[0] for i in n_rows), f"Different cardinality of input DataFrames: {n_rows}"

    df_merged = reduce(lambda left, right: pd.merge(left, right, on=["Quarter Ending"], how="outer", suffixes=("", "_y")), data_frames)
    assert df_merged.shape[0] == n_rows[0], f"Cardinality of merged DataFrame is different than its components: {df_merged.shape[0]} != {n_rows[0]}"

    df_merged.drop(df_merged.filter(regex="_y$").columns, axis=1, inplace=True)
    return df_merged

def create_column_translation() -> dict[str, str]:
    translation_dict = {
        "quarter_ending": "Quarter Ending",
        "market_cap": "Market Capitalization",
        "enterprise_value": "Enterprise Value",
        "revenue": "Revenue",
        "gross_profit": "Gross Profit",
        "operating_income": "Operating Income",
        "net_income": "Net Income",
        "ebt": "Pretax Income",
        "ebitda": "EBITDA",
        "ebit": "EBIT",
        "eps_diluted": "EPS (Diluted)",
        "gross_margin": "Gross Margin",
        "operating_margin": "Operating Margin",
        "profit_margin": "Profit Margin",
        "cash_flow_margin": "Free Cash Flow Margin",
        "operating_cash_flow": "Operating Cash Flow",
        "investing_cash_flow": "Investing Cash Flow",
        "financing_cash_flow": "Financing Cash Flow",
        "net_cash_flow": "Net Cash Flow",
        "free_cash_flow": "Free Cash Flow",
        "cash_and_short_term_investments": "Cash & Cash Equivalents",
        "net_cash_per_share": "Net Cash Per Share",
        "free_cash_flow_per_share": "Free Cash Flow Per Share", 
        "receivables": "Receivables",
        "inventory": "Inventory",
        "current_assets": "Total Current Assets",
        "total_assets": "Total Assets",
        "accounts_payable": "Accounts Payable",
        "total_debt": "Total Debt",
        "current_liabilities": "Total Current Liabilities",
        "total_liabilities": "Total Liabilities",
        "shareholders_equity": "Shareholders Equity",
        "shares_outstanding": "Shares Outstanding (Basic)",
        "price_to_earnings": "PE Ratio",
        "price_to_sales": "PS Ratio",
        "price_to_book": "PB Ratio",
        "price_to_fcf": "P/FCF Ratio",
        "ev_to_ebit": "EV/EBIT Ratio",
        "ev_to_ebitda": "EV/EBITDA Ratio",
        "debt_to_equity": "Debt / Equity Ratio",
        "debt_to_ebitda": "Debt / EBITDA Ratio",
        "quick_ratio": "Quick Ratio",
        "current_ratio": "Current Ratio",
        "asset_turnover": "Asset Turnover",
        "roe": "Return on Equity (ROE)",
        "roa": "Return on Assets (ROA)",
        "roic": "Return on Capital (ROIC)",
        "shareholder_return": "Total Shareholder Return"
    }

    return translation_dict

def create_columns_per_type_dict() -> dict[str, list[str]]:
    integer_columns = ["market_cap", "enterprise_value", "revenue", "gross_profit", "operating_income", "net_income", "ebt",
                       "ebitda", "ebit", "operating_cash_flow", "investing_cash_flow", "financing_cash_flow",
                       "net_cash_flow", "free_cash_flow", "cash_and_short_term_investments", "receivables",
                       "inventory", "current_assets", "total_assets", "accounts_payable", "total_debt", "current_liabilities",
                       "total_liabilities", "shareholders_equity", "shares_outstanding"]
    
    float_columns = ["eps_diluted", "net_cash_per_share", "price_to_earnings", "price_to_sales", "price_to_book", "price_to_fcf", 
                     "ev_to_ebit", "ev_to_ebitda", "debt_to_equity", "debt_to_ebitda", "quick_ratio", "current_ratio", "asset_turnover",
                     "free_cash_flow_per_share"]

    float_per_cent_columns = ["gross_margin", "operating_margin", "profit_margin", "cash_flow_margin", "roe", 
                                "roa", "roic", "shareholder_return"]
    
    other_columns = ["quarter_ending"]
    
    columns_per_type = {
        "integer": integer_columns,
        "float": float_columns,
        "float_per_cent": float_per_cent_columns,
        "other": other_columns
    }
    
    return columns_per_type

def clean_data_frame(df: pd.DataFrame, columns_per_type: dict) -> pd.DataFrame:
    n_cols = sum([len(columns_per_type[key]) for key in columns_per_type.keys()])
    assert n_cols == df.shape[1], f"Number of columns do not match: {n_cols} != {df.shape[1]}"
    
    for column in columns_per_type["integer"]:
        series = df[column]
        new_list = []
        for num in series:
            string = str(num)
            if string == "nan":
                new_list.append(np.nan)
            elif "." in string:
                idx = string.find(".")
                string = string[:idx]
                new_list.append(int(string))
            else:
                new_list.append(int(num))
        df[column] = pd.Series(new_list)
        
    for column in columns_per_type["float"]:
        series = df[column]
        new_list = []
        for num in series:
            string = str(num)
            if string == "nan":
                new_list.append(np.nan)
            elif string.endswith("%"):
                string = string.rstrip("%")
                new_list.append(float(string))
            else:
                new_list.append(num)
        df[column] = pd.Series(new_list)

    for column in columns_per_type["float_per_cent"]:
        series = df[column]
        new_list = []
        for num in series:
            string = str(num)
            if string == "nan":
                new_list.append(np.nan)
            else:
                string = string.rstrip("%")
                fl = float(string)
                fl /= 100.0;
                new_list.append(fl)
        df[column] = pd.Series(new_list)
        
    return df

def add_missing_columns(db_df: pd.DataFrame, company_id: int) -> pd.DataFrame:
    db_df["company_id"] = company_id
    db_df["debt_to_equity"] = db_df["total_debt"] / db_df["shareholders_equity"]
    db_df["debt_to_ebitda"] = db_df["total_debt"] / db_df["ebitda"]
    db_df["roe"] = db_df["net_income"].rolling(window=4, min_periods=4).sum() / db_df["shareholders_equity"].rolling(window=4, min_periods=2).mean()
    db_df["roa"] = db_df["net_income"].rolling(window=4, min_periods=4).sum() / db_df["total_assets"].rolling(window=4, min_periods=2).mean()
    db_df["asset_turnover"] = db_df["revenue"].rolling(window=4, min_periods=4).sum() / db_df["total_assets"].rolling(window=4, min_periods=2).mean()
    db_df["ev_to_ebit"] = db_df["enterprise_value"] / db_df["ebit"].rolling(window=4, min_periods=4).sum()
    db_df["ev_to_ebitda"] = db_df["enterprise_value"] / db_df["ebitda"].rolling(window=4, min_periods=4).sum()
    
    return db_df

def create_database_df(merged_df: pd.DataFrame, translation_dict: dict, columns_per_type: dict, company_id: int):
    nan_series = pd.Series([np.nan] * merged_df.shape[0])
    fin_stmt_dict = {k: merged_df.get(v, nan_series) for (k, v) in translation_dict.items()}
    db_df = pd.DataFrame(fin_stmt_dict)
    db_df = clean_data_frame(db_df, columns_per_type)
    db_df = add_missing_columns(db_df, company_id)
    
    return db_df

def get_table_columns(table_name, engine) -> pd.Series:
    query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}'"
    result = pd.read_sql(query, engine)["column_name"]
    return result

def send_table_data_to_db(db_df, table_name, engine):
    company_id = db_df["company_id"].iloc[0]
    table_cols = get_table_columns(table_name, engine)
    table_cols.drop(table_cols[table_cols == "financial_statement_id"].index, inplace=True)
    table_df = db_df.loc[:, table_cols]
    
    stmt_id_query = f"SELECT financial_statement_id FROM financial_statement WHERE company_id = {company_id} ORDER BY quarter_ending ASC"
    fin_stmt_id = pd.read_sql(stmt_id_query, engine).loc[:, "financial_statement_id"]
    
    table_df.loc[:, "financial_statement_id"] = fin_stmt_id
    table_df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

def send_data_to_db(db_df, engine):
    financial_stmt_cols = get_table_columns("financial_statement", engine)
    financial_stmt_cols.drop(financial_stmt_cols[financial_stmt_cols == "financial_statement_id"].index, inplace=True)
    financial_stmt_df = db_df[financial_stmt_cols]
    financial_stmt_df.to_sql(name="financial_statement", con=engine, if_exists="append", index=False)
    
    df_tables = ["income", "balance_sheet", "cash_flow", "ratio"]
    [send_table_data_to_db(db_df, table, engine) for table in df_tables]
    
def run(username, password, database, port):
    print("Unzipping financial data...")
    unzip_command = "tar -xvzf financial_data.tar.gz"
    run_comnmand(unzip_command)
    print("Data extracted successfully!")

    engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@localhost:{port}/{database}")
    paths = get_csv_paths('financial_data/')
    csv_types = ['income-statement-quarterly.csv', 'ratios-quarterly.csv', 'balance-sheet-quarterly.csv', 'cash-flow-statement-quarterly.csv']

    for company_csv_paths in paths:
        company_ticker = company_csv_paths[0].split('/')[1].upper()
        company_id_query = f"SELECT company_id FROM company WHERE ticker = '{company_ticker}'"
        company_id = pd.read_sql(company_id_query, engine)["company_id"].iloc[0]
        income_df = None
        ratios_df = None
        balance_sheet_df = None
        cash_flow_df = None
        
        for csv_path in company_csv_paths:
            csv_name = csv_path.split('/')[2]
            if csv_name.endswith(csv_types[0]):
                income_df = get_formated_df_from_csv_path(csv_path)
            elif csv_name.endswith(csv_types[1]):
                ratios_df = get_formated_df_from_csv_path(csv_path)
            elif csv_name.endswith(csv_types[2]):
                balance_sheet_df = get_formated_df_from_csv_path(csv_path)
            elif csv_name.endswith(csv_types[3]):
                cash_flow_df = get_formated_df_from_csv_path(csv_path)
        
        try:
            data_frames = [income_df, ratios_df, balance_sheet_df, cash_flow_df]
            merged_df = merge_dfs(data_frames)
            
        except AssertionError as e:
            print(f"There was an error while merging DataFrames for {company_ticker.upper()}:")
            print(e)
            raise
        
        columns_per_type = create_columns_per_type_dict()
        translation_dict = create_column_translation()
        db_df = create_database_df(merged_df, translation_dict, columns_per_type, company_id)
        send_data_to_db(db_df, engine)
        print(f"{company_ticker.upper()} financial data successfully sent to '{database}' database!")
    print("Fincancial data loaded successfully!\n")