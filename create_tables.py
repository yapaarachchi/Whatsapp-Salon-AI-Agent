# create_tables.py
from app.database import engine, Base
from app.models import Customer, Staff, Service, Booking

print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")