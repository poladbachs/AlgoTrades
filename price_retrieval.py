from __future__ import print_function
import datetime
import warnings
import MySQLdb as mdb
import yfinance as yf

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'polad2003'
db_name = 'securities_master'

def obtain_list_of_db_tickers():
    """Obtains a list of the ticker symbols in the database."""
    con = mdb.connect(db_host, db_user, db_pass, db_name)
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
    return [(d[0], d[1]) for d in data]

def get_daily_historic_data_yahoo(ticker, start_date=(2024,8,17), end_date=datetime.date.today().timetuple()[0:3]):
    """
    Obtains data from Yahoo Finance and returns a list of tuples.
    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format
    """
    start_date_str = f"{start_date[0]}-{start_date[1]:02d}-{start_date[2]:02d}"
    end_date_str = f"{end_date[0]}-{end_date[1]:02d}-{end_date[2]:02d}"

    try:
        data = yf.download(ticker, start=start_date_str, end=end_date_str)
        prices = [
            (
                date, row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume']
            )
            for date, row in data.iterrows()
        ]
    except Exception as e:
        print(f"Could not download Yahoo data for {ticker}: {e}")
        prices = []
    return prices

def insert_daily_data_into_db(data_vendor_id, symbol_id, daily_data):
    """
    Takes a list of tuples of daily data and adds it to the MySQL database.
    Appends the vendor ID and symbol ID to the data.
    daily_data: List of tuples of the OHLC data (with adj_close and volume)
    """
    now = datetime.datetime.utcnow()
    daily_data = [
        (data_vendor_id, symbol_id, d[0], now, now, d[1], d[2], d[3], d[4], d[5], d[6])
        for d in daily_data
    ]

    column_str = """data_vendor_id, symbol_id, price_date, created_date,
                    last_updated_date, open_price, high_price, low_price,
                    close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = f"INSERT INTO daily_price ({column_str}) VALUES ({insert_str})"

    con = mdb.connect(db_host, db_user, db_pass, db_name)
    with con:
        cur = con.cursor()
        cur.executemany(final_str, daily_data)
        con.commit()

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print(f"Adding data for {t[1]}: {i+1} out of {lentickers}")
        yf_data = get_daily_historic_data_yahoo(t[1])
        if yf_data:
            insert_daily_data_into_db('1', t[0], yf_data)
        else:
            print(f"No data returned for ticker {t[1]}")
    print("Successfully added Yahoo Finance pricing data to DB.")