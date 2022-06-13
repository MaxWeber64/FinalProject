import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sqlite3
import csv
from xlsxwriter.workbook import Workbook


shel = yf.download('SHEL', start='2019-01-01', end='2022-05-31', interval='1d')
aapl = yf.download('AAPL', start='2019-01-01', end='2022-05-31', interval='1d')
tsla = yf.download('TSLA', start='2019-01-01', end='2022-05-31', interval='1d')
btc = yf.download('BTC-USD', start='2019-01-01', end='2022-05-31', interval='1d')
shel.to_csv('shel.csv')
aapl.to_csv('aapl.csv')
tsla.to_csv('tsla.csv')
btc.to_csv('btc.csv')
shel = pd.read_csv('shel.csv')
aapl = pd.read_csv('aapl.csv')
tsla = pd.read_csv('tsla.csv')
btc = pd.read_csv('btc.csv')
conn = sqlite3.connect('mix.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE Shell (Dat, S);''')
c.execute('''CREATE TABLE Apple (Dat, A);''')
c.execute('''CREATE TABLE Bitcoin (Dat, B);''')
c.execute('''CREATE TABLE Tesla (Dat, T);''')
with open('shel.csv', 'r') as fin:
    dr = csv.DictReader(fin, delimiter=",")
    to_db = [(i['Date'], i['Close']) for i in dr]
c.executemany("INSERT INTO Shell (Dat, S) VALUES (?, ?);", to_db)
with open('aapl.csv', 'r') as fin:
    dr = csv.DictReader(fin, delimiter=",")
    to_db = [(i['Date'], i['Close']) for i in dr]
c.executemany("INSERT INTO Apple (Dat, A) VALUES (?, ?);", to_db)
with open('tsla.csv', 'r') as fin:
    dr = csv.DictReader(fin, delimiter=",")
    to_db = [(i['Date'], i['Close']) for i in dr]
c.executemany("INSERT INTO Tesla (Dat, T) VALUES (?, ?);", to_db)
with open('btc.csv', 'r') as fin:
    dr = csv.DictReader(fin, delimiter=",")
    to_db = [(i['Date'], i['Close']) for i in dr]
c.executemany("INSERT INTO Bitcoin (Dat, B) VALUES (?, ?);", to_db)
workbook = Workbook('mix.xlsx')
worksheet = workbook.add_worksheet()
sel = c.execute("SELECT S, B, A, T FROM ("
                "SELECT * FROM ("
                "SELECT Shell.Dat, S, B FROM Shell LEFT OUTER JOIN Bitcoin ON Shell.Dat = Bitcoin.Dat"
                ") LEFT OUTER JOIN Tesla USING(Dat)"
                ") LEFT OUTER JOIN Apple USING(Dat)")
for i, row in enumerate(sel):
    for j, value in enumerate(row):        worksheet.write(i, j, value)
workbook.close()
conn.commit()
conn.close()
price = pd.read_excel('mix.xlsx')
mean = np.array(price.mean())
var = np.array(price.var())
print('Hello, world!')
