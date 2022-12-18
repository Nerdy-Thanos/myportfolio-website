import matplotlib
matplotlib.use('Agg')
from yfinance import Ticker
import os
from seaborn import pairplot
from matplotlib.pyplot import figure, plot, legend, savefig, xlabel, ylabel, title
import datetime
from dateutil import parser


def fetch_data(stock, start_date, end_date):
    today = datetime.datetime.now()
    end_date_dt = parser.parse(end_date)
    if end_date_dt>today:
        end_date=today.strftime("%Y-%m-%d")
    ticker = Ticker(stock)
    data = ticker.history(start=start_date, end=end_date)
    return data


def plot_all_stocks(data, stock):
    figure(figsize=(10, 6))
    plot(data.index, data["Open"], label="Open")
    plot(data.index, data["Close"], label="Close")
    xlabel("Time Period")
    ylabel("Stock Price")
    title(str(stock))
    legend()
    savefig("src/webapp/static/img/graphs/all.png")


def plot_volume(data, stock):
    figure(figsize=(10, 6))
    plot(data.index, data["Volume"], label="Volume Traded")
    xlabel("Time Period")
    ylabel("Stock Price")
    title(str(stock))
    legend()
    savefig("src/webapp/static/img/graphs/volume.png")


def multi_variate_analysis(data):
    snsfig = pairplot(data[["Open", "High", "Low", "Close", "Volume"]])
    pltfig = snsfig.fig
    pltfig.savefig("src/webapp/static/img/graphs/multi.png")


def daily_change(data):
    data["daily_change"] = ((data["Close"] - data["Open"]) / data["Close"]) * 100
    snsfig = pairplot(data[["Open", "Close", "daily_change"]])
    pltfig = snsfig.fig
    pltfig.savefig("src/webapp/static/img/graphs/daily.png")

def clean_static_dir():
    path="src/webapp/static/img/graphs/"
    files = os.listdir(path)
    for file in files:
        if os.path.exists(path+file):
            os.remove(path+file)
