from flask import Flask, jsonify, render_template, send_file
import yfinance as yf
import pandas as pd
import os
from flask_sqlalchemy import SQLAlchemy
from models import Company
from database import db
# from oldmodels import createModels

app = Flask(__name__)


# DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://")
# app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)

companies = [
    {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology",
        "description": "A global powerhouse in consumer electronics, software, and digital services, best known for its iPhone and Mac products."},
    {"ticker": "MSFT", "name": "Microsoft Corporation", "sector": "Technology",
        "description": "A multinational technology corporation, pivotal in the personal computing revolution and now leading in cloud computing, software, and hardware solutions."},
    {"ticker": "INTC", "name": "Intel Corporation", "sector": "Technology",
        "description": "A pioneering force in semiconductor manufacturing, renowned for its microprocessors which are a staple in many computers."},
    {"ticker": "KO", "name": "The Coca-Cola Company", "sector": "Consumer Goods",
        "description": "An iconic brand in the beverage industry, distributing its products in over 200 countries."},
    {"ticker": "PG", "name": "Procter & Gamble Co", "sector": "Consumer Goods",
        "description": "A leading name in the consumer goods space, with a diverse portfolio ranging from healthcare products to cleaning agents."},
    {"ticker": "AMZN", "name": "Amazon.com, Inc.", "sector": "E-commerce and Internet",
        "description": "From an online bookstore to a global e-commerce and cloud computing juggernaut, Amazon is a market leader influencing global shopping habits."},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "E-commerce and Internet",
        "description": "The parent company of Google, it's at the forefront of search, digital advertising, cloud computing, and AI innovations."},
    {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financials",
        "description": "A titan in the banking sector, offering a broad range of financial services with a global footprint."},
    {"ticker": "GS", "name": "Goldman Sachs Group Inc", "sector": "Financials",
        "description": "A prestigious investment banking firm, also engaged in securities, asset management, and other financial services."},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare",
        "description": "A healthcare behemoth with a vast range of products in pharmaceuticals, medical devices, and consumer goods."},
    {"ticker": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare",
        "description": "One of the world's largest pharmaceutical companies, it has been instrumental in medical breakthroughs and innovations."},
    {"ticker": "BA", "name": "The Boeing Company", "sector": "Industrials",
        "description": "An aerospace leader, Boeing is integral in the manufacturing of commercial jetliners and defense, space, and security systems."},
    {"ticker": "GE", "name": "General Electric Company", "sector": "Industrials",
        "description": "A diversified conglomerate with operations spanning aviation, healthcare, power, and more."},
    {"ticker": "XOM", "name": "Exxon Mobil Corporation", "sector": "Energy",
        "description": "A stalwart in the energy sector, engaged in oil exploration, production, refining, and marketing."},
    {"ticker": "CVX", "name": "Chevron Corporation", "sector": "Energy",
        "description": "One of the leading integrated energy companies, involved in every aspect from exploration to marketing."},
    {"ticker": "T", "name": "AT&T Inc.", "sector": "Telecom",
        "description": "A telecommunications heavyweight offering a wide spectrum of services, including wireless, broadband, and pay TV."},
    {"ticker": "VZ", "name": "Verizon Communications Inc.", "sector": "Telecom",
        "description": "A global leader in delivering broadband, video, and other wireless and wireline communications services."},
    {"ticker": "DIS", "name": "Walt Disney Co", "sector": "Entertainment",
        "description": "A multinational media conglomerate, known for its film studios, theme parks, and a diverse array of entertainment offerings."},
    {"ticker": "NFLX", "name": "Netflix, Inc.", "sector": "Entertainment",
        "description": "The pioneer in streaming media, Netflix offers a plethora of original and licensed content, revolutionizing the entertainment industry."},
    {"ticker": "F", "name": "Ford Motor Company", "sector": "Automotive",
        "description": "A historic name in the automotive industry, known for innovations and mass production of cars."},
    {"ticker": "GM", "name": "General Motors Company", "sector": "Automotive",
        "description": "One of the world's largest automakers, with a rich heritage in designing, manufacturing, and selling cars, trucks, and auto parts."}
]

models = createModels()


@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')


@app.route('/companies', methods=['GET'])
def get_companies():
    for company in companies:
        stock = yf.Ticker(company["ticker"])
        stock_price = stock.history(period="1d")['Close'].iloc[0]
        company['price'] = stock_price
    return jsonify(companies)


@app.route('/ticker/<ticker_string>', methods=['GET'])
def get_ticker_data(ticker_string):
    ticker = yf.Ticker(ticker_string)

    history_yf = ticker.history(period='max')
    history_yf.reset_index(inplace=True)

    history_yf = history_yf[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    history_yf['Date'] = pd.to_datetime(
        history_yf['Date']).dt.strftime('%Y-%m-%d')

    history_yf.rename(columns={
        'Date': 'time',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }, inplace=True)

    history_yf = history_yf.to_dict(orient='records')
    info = ticker.info

    data = {
        'history': history_yf,
        'info': info
    }

    return jsonify(data)


@app.route('/ticker/<ticker>/predict', methods=['GET'])
def predict(ticker):
    try:
        return send_file('models/predictions/' + ticker + '.json')
    except FileNotFoundError:
        return "File not found", 404


@app.route('/our-models', methods=['GET'])
def our_models():
    return render_template('Capstone.html')


if __name__ == "__main__":
    app.run(debug=True)
