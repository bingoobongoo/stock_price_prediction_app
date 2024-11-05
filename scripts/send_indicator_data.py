import pandas as pd
import sqlalchemy
import ta

def run(username, password, database, port):
    engine = sqlalchemy.create_engine(f"postgresql://{username}:{password}@localhost:{port}/{database}")
    tickers = pd.read_sql("SELECT ticker FROM company", engine).loc[:, 'ticker']
    
    for ticker in tickers:
        try:
            query = f"""SELECT s.stock_price_id, c.company_id, s.date, s.close, s.open, s.low, s.high, s.volume 
                        FROM company as c 
                        JOIN stock_price as s USING(company_id) 
                        WHERE c.ticker = '{ticker}' 
                        ORDER BY s.date"""
            company_data = pd.read_sql(query, engine)

            rsi = ta.momentum.RSIIndicator(close=company_data['close'], window=14).rsi()
            
            obv = ta.volume.OnBalanceVolumeIndicator(close=company_data['close'], volume=company_data['volume']).on_balance_volume()
            
            roc = ta.momentum.ROCIndicator(close=company_data['close'], window=12).roc()
            
            uo = ta.momentum.UltimateOscillator(
                high=company_data['high'],
                low=company_data['low'],
                close=company_data['close'],
                window1=7,
                window2=14,
                window3=28,
                weight1=4.0,
                weight2=2.0,
                weight3=1.0
            ).ultimate_oscillator()
            
            ppo = ta.momentum.PercentagePriceOscillator(
                close=company_data['close'],
                window_slow=26,
                window_fast=12,
                window_sign=9
            ).ppo()
            
            adi = ta.volume.AccDistIndexIndicator(
                high=company_data['high'],
                low=company_data['low'],
                close=company_data['close'],
                volume=company_data['volume']
            ).acc_dist_index()
            
            atr = ta.volatility.AverageTrueRange(
                high=company_data['high'],
                low=company_data['low'],
                close=company_data['close'],
                window=14
            ).average_true_range()
            
            bollinger_obj = ta.volatility.BollingerBands(
                close=company_data['close'],
                window=20,
                window_dev=2
            )
            bollinger_lband = bollinger_obj.bollinger_lband()
            bollinger_mband = bollinger_obj.bollinger_mavg()
            bollinger_hband = bollinger_obj.bollinger_hband()
        
            adx_obj = ta.trend.ADXIndicator(
                high=company_data['high'],
                low=company_data['low'],
                close=company_data['close'],
                window=14
            )
            adx = adx_obj.adx()
            minus_di = adx_obj.adx_neg()
            plus_di = adx_obj.adx_pos()
        
            aroon_obj = ta.trend.AroonIndicator(
                high=company_data['high'],
                low=company_data['low'],
                window=25
            )
            aroon_down = aroon_obj.aroon_down()
            aroon_up = aroon_obj.aroon_up()
        
            macd = ta.trend.MACD(
                close=company_data['close'],
                window_slow=26,
                window_fast=12,
                window_sign=9    
            ).macd()
        
            so = ta.momentum.StochasticOscillator(
                high=company_data['high'],
                low=company_data['low'],
                close=company_data['close'],
                window=14,
                smooth_window=3
            ).stoch()
        
            indicator_dict = {
                'stock_price_id':company_data['stock_price_id'],
                'rsi':rsi,
                'obv':obv,
                'roc':roc,
                'uo':uo,
                'ppo':ppo,
                'adi':adi,
                'atr':atr,
                'bollinger_lband':bollinger_lband,
                'bollinger_mband':bollinger_mband,
                'bollinger_hband':bollinger_hband,
                'adx':adx,
                'aroon_down':aroon_down,
                'aroon_up':aroon_up,
                'macd':macd,
                'so':so,
                'minus_di':minus_di,
                'plus_di':plus_di
            }
        
            indicator_data = pd.DataFrame(indicator_dict)
            indicator_data.to_sql(
                name='indicator',
                con=engine,
                if_exists='append',
                index=False
            )

            print(f"Successfully sent {ticker} indicator data to '{database}'!")
        except:
            print(f"Failed to send {ticker} indicator data.")

    print("Sending indicator data completed!\n")