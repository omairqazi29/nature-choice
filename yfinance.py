import yfinance as yf
import pandas as pd
import os

cola = "KO"
cola_y = yf.Ticker(cola)
esg_data = pd.DataFrame.transpose(cola_y.sustainability)
esg_data['company_ticker'] = str(cola_y.ticker)