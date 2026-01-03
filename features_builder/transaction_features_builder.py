import pandas as pd
from constants.config import E


class TransactionFeaturesBuilder:
    """
    This class is responsible for building transaction-related features from transaction data.
    It includes methods to calculate ratios and shares related to transaction amounts and balances.
    """

    @staticmethod
    def amount_weekly_ratio(df: pd.DataFrame) -> pd.Series:
        """Return transaction amount divided by sender's weekly average amount."""
        return df['amount'] / (df['weekly_avg_amount_sender'] + E)

    @staticmethod
    def amount_daily_ratio(df: pd.DataFrame) -> pd.Series:
        """Return transaction amount divided by sender's daily total amount."""
        return df['amount'] / (df['daily_total_amount_sender'] + E)

    @staticmethod
    def transaction_share_of_day(df: pd.DataFrame) -> pd.Series:
        """Return the transaction's share within the sender's daily transactions."""
        return 1 / (df['daily_tx_count_sender'] + E)

    @staticmethod
    def balance_change_ratio_sender(df: pd.DataFrame) -> pd.Series:
        """Return ratio of transaction amount to sender's previous balance."""
        return df['amount'] / (df['oldbalanceOrg'] + E)

    @staticmethod
    def build(df: pd.DataFrame) -> pd.DataFrame:
        """Build and append transaction-level ratio features to the DataFrame."""
        features = df.copy()
        features['amount_weekly_ratio'] = TransactionFeaturesBuilder.amount_weekly_ratio(features)
        features['amount_daily_ratio'] = TransactionFeaturesBuilder.amount_daily_ratio(features)
        features['transaction_share_of_day'] = TransactionFeaturesBuilder.transaction_share_of_day(features)
        features['balance_change_ratio_sender'] = TransactionFeaturesBuilder.balance_change_ratio_sender(features)
        return features
