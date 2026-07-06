import sys
import random
import datetime
from pathlib import Path
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
import config
from src.database import SessionLocal, LoanFacility, initialize_database

def generate_synthetic_loan_book(num_loans=250):
    print(f"Generating {num_loans} synthetic credit facility profiles...")
    session = SessionLocal()
    
    # Clear existing records
    session.query(LoanFacility).delete()
    
    segments = list(config.SEGMENT_RULES.keys())
    borrower_names = [
        "Nexus Logistics", "Apex Manufacturing", "Vanguard Health", "Beacon Energy", "Summit Tech",
        "Titan Retail", "Omega Real Estate", "Horizon Infrastructure", "Caliber Automotive", "Element Materials"
    ]
    
    for i in range(num_loans):
        seg = random.choice(segments)
        rules = config.SEGMENT_RULES[seg]
        
        # Correlate PD with structural tier groupings
        if "Premium" in seg:
            pd = float(np.random.beta(a=1.5, b=15)) * 0.15 # Low PD
        elif "Unsecured" in seg:
            pd = float(np.random.beta(a=3.0, b=8)) * 0.35  # Elevated PD
        else:
            pd = float(np.random.beta(a=2.0, b=10)) * 0.20
            
        committed = round(random.uniform(500_000, 15_000_000), -3)
        utilization = random.uniform(0.4, 1.0)
        drawn = round(committed * utilization, -3)
        
        # Calculate LGD with minor variance around Basel baselines
        lgd = max(0.05, min(0.95, rules["base_lgd"] + random.uniform(-0.05, 0.05)))
        
        facility = LoanFacility(
            facility_id=f"FAC-{10000 + i}",
            borrower_name=f"{random.choice(borrower_names)} {random.randint(100, 999)}",
            segment=seg,
            committed_exposure=committed,
            drawn_balance=drawn,
            probability_of_default=pd,
            loss_given_default=lgd,
            interest_rate=round(random.uniform(0.045, 0.115), 4),
            maturity_date=datetime.datetime.now() + datetime.timedelta(days=int(rules["average_term"] * 365 * random.uniform(0.5, 1.5)))
        )
        session.add(facility)
        
    session.commit()
    session.close()
    print("[+] Core credit tables populated successfully with synthetic portfolio.")

if __name__ == "__main__":
    initialize_database()
    generate_synthetic_loan_book()