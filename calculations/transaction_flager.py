import pandas as pd
from scipy.stats import zscore


class TransactionFlagger:
    """
    Flag suspicious transactions using Z-score.
    """

    FLAG_FEATURES = [
        'amount_weekly_ratio',
        'amount_daily_ratio',
        'balance_change_ratio_sender'
    ]

    @staticmethod
    def compute_flags(df: pd.DataFrame, threshold: float = 3.0) -> pd.Series:
        """Compute binary transaction flags based on configured features and threshold.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with features used for flagging.
        threshold : float
            Z-score threshold above which a transaction is considered anomalous.

        Returns
        -------
        pd.Series
            Binary series where 1 indicates a flagged transaction.
        """
        z = (
            df[TransactionFlagger.FLAG_FEATURES]
            .apply(lambda col: zscore(col, nan_policy='omit'))
            .abs()
        )
        return (z.max(axis=1) > threshold).astype(int)

    @staticmethod
    def build(df: pd.DataFrame) -> pd.DataFrame:
        """Append a `transaction_flag` column to a copy of the DataFrame."""
        flagged = df.copy()
        flagged['transaction_flag'] = (
            TransactionFlagger.compute_flags(flagged)
        )
        return flagged
