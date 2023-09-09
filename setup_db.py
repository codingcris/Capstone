from app import db, app

def setup_database():
    """Create all tables."""
    with app.app_context():  # This ensures the app context is used when running standalone scripts
        db.create_all()

if __name__ == "__main__":
    setup_database()
    print("Database tables created!")