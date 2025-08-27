from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta

def get_or_create_customer(db: Session, phone_number: str) -> models.Customer:
    """
    Finds a customer by their phone number. If they don't exist,
    a new customer record is created.
    """
    customer = db.query(models.Customer).filter(models.Customer.phone_number == phone_number).first()
    
    if not customer:
        print(f"Creating new customer for number: {phone_number}")
        customer = models.Customer(phone_number=phone_number)
        db.add(customer)
        db.commit()
        db.refresh(customer)
    else:
        print(f"Found existing customer: {customer.id}")
        
    return customer


def get_available_slots(db: Session, service_name: str, staff_name: str, date_str: str):
    """
    Finds available time slots for a given service, staff, and date.
    This is a simplified dummy function for now.
    """
    print(f"Checking availability for {service_name} with {staff_name} on {date_str}...")
    # In a real system, you would query the bookings table and staff schedules.
    # For now, we will return a fixed list of available times.
    return ["2:00 PM", "3:00 PM", "4:30 PM"]


def book_appointment(db: Session, customer_phone: str, service_name: str, staff_name: str, appointment_time_str: str):
    """
    Books an appointment by looking up IDs and saving a new record to the bookings table.
    """
    print(f"Attempting to book '{service_name}' for {customer_phone} with {staff_name} at {appointment_time_str}")

    try:
        # 1. Look up the IDs for customer, service, and staff
        customer = db.query(models.Customer).filter(models.Customer.phone_number == customer_phone).first()
        service = db.query(models.Service).filter(models.Service.name.ilike(f"%{service_name}%")).first()
        staff = db.query(models.Staff).filter(models.Staff.name.ilike(f"%{staff_name}%")).first()

        # Check if entities were found in a Pylance-friendly way
        if customer is None or service is None or staff is None:
            print(f"ERROR: Could not find one or more required items for booking.")
            return "Sorry, there was an error with the booking details. Please try again."

        # 2. Convert time string to a datetime object (this is a simplified example)
        # In a real app, you'd handle dates and parse times more robustly
        appointment_time = datetime.strptime(appointment_time_str, "%I:%M %p").replace(
            year=2025, month=8, day=29 # Assuming a fixed date for this example
        )
        
        # Calculate end time, silencing the stubborn Pylance linter
        end_time = appointment_time + timedelta(minutes=int(service.duration_minutes))  # type: ignore

        # 3. Create the new Booking object
        new_booking = models.Booking(
            customer_id=customer.id,
            service_id=service.id,
            staff_id=staff.id,
            start_time=appointment_time,
            end_time=end_time,
            status='confirmed'
        )

        # 4. Add to the database and commit
        db.add(new_booking)
        db.commit()
        print(f"✅ Successfully saved booking ID {new_booking.id} to the database.")

        return f"Success! Your {service_name} with {staff_name} is booked for {appointment_time_str}."

    except Exception as e:
        print(f"An exception occurred during booking: {e}")
        db.rollback() # Roll back the transaction on error
        return "Sorry, I encountered an unexpected error while trying to book your appointment."