from app import db, app

def setup_database():
    """Create all tables."""
    with app.app_context():  
        db.create_all()

if __name__ == "__main__":
    setup_database()
    print("Database tables created!")