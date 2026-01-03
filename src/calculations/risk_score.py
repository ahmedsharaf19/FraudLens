import pandas as pd
import numpy as np
from scipy.stats import zscore


class CustomerRiskScorer:
    """
    Calculate customer risk score using Z-score on customer features.
    """

    RISK_FEATURES = [
        'daily_tx_velocity',
        'weekly_tx_count_sender',
        'weekly_avg_amount_sender'
    ]

    @staticmethod
    def compute_zscore(df: pd.DataFrame) -> pd.DataFrame:
        """Compute absolute Z-scores for the configured risk features.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the risk features.

        Returns
        -------
        pd.DataFrame
            Copy of the input with the risk features replaced by their absolute Z-scores.
        """
        z_df = df.copy()
        z_df[CustomerRiskScorer.RISK_FEATURES] = (
            z_df[CustomerRiskScorer.RISK_FEATURES]
            .apply(lambda col: zscore(col, nan_policy='omit'))
            .abs()
        )
        return z_df

    @staticmethod
    def compute_risk_score(z_df: pd.DataFrame) -> pd.Series:
        """Compute the mean of configured Z-score features as a single risk score."""
        return z_df[CustomerRiskScorer.RISK_FEATURES].mean(axis=1)

    @staticmethod
    def risk_class(score: pd.Series) -> pd.Series:
        """Map numeric risk scores into categorical risk classes."""
        return pd.cut(
            score,
            bins=[-np.inf, 0.5, 1.0, 2.0, np.inf],
            labels=['low', 'medium', 'high', 'critical']
        )

    @staticmethod
    def build(customer_df: pd.DataFrame) -> pd.DataFrame:
        """Compute risk score and risk class for each record in the provided DataFrame."""
        df = customer_df.copy()

        z_df = CustomerRiskScorer.compute_zscore(df)

        df['risk_score'] = CustomerRiskScorer.compute_risk_score(z_df)
        df['risk_class'] = CustomerRiskScorer.risk_class(df['risk_score'])

        return df
