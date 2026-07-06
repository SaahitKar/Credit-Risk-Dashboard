# src/analytics_engine.py
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
import config
from src.database import engine

class CreditPortfolioAnalyticsEngine:
    """Computes quantitative risk metrics across a loan portfolio."""
    
    def __init__(self):
        self.conn_str = f"sqlite:///{config.DB_PATH}"

    def load_portfolio_dataframe(self) -> pd.DataFrame:
        """Extracts native SQL database contents directly into an analysis frame."""
        df = pd.read_sql_table("loan_facilities", con=self.conn_str)
        return df

    def compute_portfolio_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies institutional credit metrics calculations including Expected Loss."""
        df = df.copy()
        
        # Exposure At Default (EAD) tracking calculation (Drawn + Factor * Undrawn Credit Line)
        # Using a standard credit conversion factor (CCF) proxy of 50% for undrawn balances
        ccf = 0.50
        undrawn = df["committed_exposure"] - df["drawn_balance"]
        df["EAD"] = df["drawn_balance"] + (ccf * undrawn)
        
        # Classical Structural Expected Loss Framework
        df["Expected_Loss"] = df["probability_of_default"] * df["loss_given_default"] * df["EAD"]
        
        # Risk-Weighted Asset (RWA) simplified proxy mapping
        df["RWA"] = df["EAD"] * df["loss_given_default"] * 2.5
        
        # Yield Generation Metrics
        df["annual_interest_income"] = df["drawn_balance"] * df["interest_rate"]
        
        return df

    def generate_summary_statistics(self) -> dict:
        """Aggregates comprehensive credit metrics across the total portfolio."""
        df = self.load_portfolio_dataframe()
        if df.empty:
            return {}
            
        df_calc = self.compute_portfolio_metrics(df)
        
        summary = {
            "total_committed": float(df_calc["committed_exposure"].sum()),
            "total_drawn": float(df_calc["drawn_balance"].sum()),
            "total_ead": float(df_calc["EAD"].sum()),
            "portfolio_weighted_pd": float(np.average(df_calc["probability_of_default"], weights=df_calc["EAD"])),
            "portfolio_weighted_lgd": float(np.average(df_calc["loss_given_default"], weights=df_calc["EAD"])),
            "total_expected_loss": float(df_calc["Expected_Loss"].sum()),
            "total_rwa": float(df_calc["RWA"].sum()),
            "net_portfolio_yield": float(df_calc["annual_interest_income"].sum() / df_calc["drawn_balance"].sum())
        }
        return summary

if __name__ == "__main__":
    engine_calc = CreditPortfolioAnalyticsEngine()
    stats = engine_calc.generate_summary_statistics()
    for k, v in stats.items():
        print(f"{k}: {v:,.4f}")