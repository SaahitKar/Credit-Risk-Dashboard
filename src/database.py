import sys
from pathlib import Path
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

sys.path.append(str(Path(__file__).resolve().parents[1]))
import config

Base = declarative_base()
engine = create_engine(f"sqlite:///{config.DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

class LoanFacility(Base):
    """SQL Schema definition for corporate loan facilities."""
    __tablename__ = "loan_facilities"
    
    facility_id = Column(String, primary_key=True, index=True)
    borrower_name = Column(String, nullable=False)
    segment = Column(String, nullable=False)
    committed_exposure = Column(Float, nullable=False)
    drawn_balance = Column(Float, nullable=False)
    probability_of_default = Column(Float, nullable=False)
    loss_given_default = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    maturity_date = Column(DateTime, default=datetime.datetime.utcnow)

def initialize_database():
    """Builds structural database schema tables."""
    Base.metadata.create_all(bind=engine)
    print(f"[+] Initialized target SQLite relational database at: {config.DB_PATH}")

if __name__ == "__main__":
    initialize_database()