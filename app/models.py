from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    bookings = relationship("Booking", back_populates="customer")

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    bookings = relationship("Booking", back_populates="staff")

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    bookings = relationship("Booking", back_populates="service")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    staff_id = Column(Integer, ForeignKey('staff.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default='confirmed')
    customer = relationship("Customer", back_populates="bookings")
    staff = relationship("Staff", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")