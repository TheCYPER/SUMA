#!/usr/bin/env python3
"""
Database initialization script for SUMA LMS
Run this script to create the database and populate it with sample data
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.utils import create_sample_data

def init_database():
    """Initialize the database with tables and sample data"""
    print("Initializing SUMA LMS database...")
    
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created")
    
    # Create sample data
    print("Creating sample data...")
    db = SessionLocal()
    try:
        create_sample_data(db)
        print("✓ Sample data created")
    except Exception as e:
        print(f"✗ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n🎉 Database initialization complete!")
    print("\nSample accounts created:")
    print("  Admin: admin / admin123")
    print("  Teacher: teacher / teacher123")
    print("  Students: student1, student2 / student123")
    print("\nYou can now start the API server with: python -m app.main")

if __name__ == "__main__":
    init_database()
