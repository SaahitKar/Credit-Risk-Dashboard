# Portfolio Credit Risk Analytics Dashboard Platform

A risk management platform and database layer designed to process a commercial loan portfolio, model exposure dynamics, and execute macroeconomic stress testing. This platform transitions from static entity-level classification to aggregate portfolio risk metrics, implementing the classical Basel credit risk framework. It establishes a relational data architecture utilizing the SQLAlchemy Object-Relational Mapper (ORM) and SQLite to simulate a bank's internal credit risk data warehouse.

## Setup & Run
```bash
1. python3 config.py
2. python3 src/database.py
3. python3 src/seed_data.py
4. python3 src/analytics_engine.py
5. python3 dashboard/app.py
6. streamlit run dashboard/app.py
```

## Platform Architecture & Directory Structure

```text
Credit-Risk-Dashboard/
│
├── README.md                           # Operational documentation & financial theory
├── requirements.txt                    # Environment dependencies
├── config.py                           # Application constants and credit segment configurations
│
├── src/
│   ├── database.py                     # SQLAlchemy ORM schemas and SQLite connection engine
│   ├── seed_data.py                    # Multi-segment commercial credit book generator
│   └── analytics_engine.py             # Quantitative Expected Loss and RWA calculators
│
└── dashboard/
    └── app.py                          # Streamlit & stress interface and analytical dashboard
