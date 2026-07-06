# config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "credit_portfolio.db"

# Portfolio Segment Risk Parameters (LGD Baselines based on Basel Frameworks)
SEGMENT_RULES = {
    "Corporate Premium": {"base_lgd": 0.40, "average_term": 5},
    "SME Commercial": {"base_lgd": 0.45, "average_term": 3},
    "Real Estate Secured": {"base_lgd": 0.25, "average_term": 10},
    "Unsecured Mid-Market": {"base_lgd": 0.75, "average_term": 2}
}