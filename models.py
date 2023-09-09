from database import db

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(50))
    description = db.Column(db.String(500))
    price = db.Column(db.Float) # This is for the most recent price from the yfinance API

    def __init__(self, ticker, name, sector, description):
        self.ticker = ticker
        self.name = name
        self.sector = sector
        self.description = description

    def __repr__(self):
        return f"<Company {self.name}>"