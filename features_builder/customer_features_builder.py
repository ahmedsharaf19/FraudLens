import pandas as pd
from constants.config import E


class CustomerFeaturesBuilder:
    """
    This class is responsible for building customer-related features from transaction data.
    It includes methods to add day and week information, calculate daily and weekly transaction counts,
    """

    @staticmethod
    def add_day(df: pd.DataFrame) -> pd.Series:
        """Return the day index computed from 'step' (hours divided by 24)."""
        return df['step'] // 24

    @staticmethod
    def add_week(df: pd.DataFrame) -> pd.Series:
        """Return the week index computed from 'day' (days divided by 7)."""
        return df['day'] // 7

    @staticmethod
    def daily_tx_count_sender(g_day) -> pd.Series:
        """Return the number of transactions per sender per day."""
        return g_day['amount'].transform('size')

    @staticmethod
    def daily_total_amount_sender(g_day) -> pd.Series:
        """Return the total transaction amount per sender per day."""
        return g_day['amount'].transform('sum')

    @staticmethod
    def weekly_tx_count_sender(g_week) -> pd.Series:
        """Return the number of transactions per sender per week."""
        return g_week['amount'].transform('size')

    @staticmethod
    def weekly_avg_amount_sender(g_week) -> pd.Series:
        """Return the average transaction amount per sender per week."""
        return g_week['amount'].transform('mean')

    @staticmethod
    def daily_tx_velocity(df: pd.DataFrame) -> pd.Series:
        """Compute daily transaction velocity for each sender.

        The metric is the sender's daily transaction count normalized by active days.
        """
        active_days = df.groupby('nameOrig')['day'].transform('nunique')
        return df['daily_tx_count_sender'] / (active_days + E)

    @staticmethod
    def balance_gap_sender(df: pd.DataFrame) -> pd.Series:
        """Compute the balance gap for the sender after the transaction."""
        return df['oldbalanceOrg'] - df['amount']- df['newbalanceOrig']

    @staticmethod
    def build(df: pd.DataFrame) -> pd.DataFrame:
        """Build and append customer-level features to a copy of the DataFrame."""
        features = df.copy()
        features['day'] = CustomerFeaturesBuilder.add_day(features)
        features['week'] = CustomerFeaturesBuilder.add_week(features)

        g_day = features.groupby(['nameOrig', 'day'], sort=False)
        g_week = features.groupby(['nameOrig', 'week'], sort=False)

        features['daily_tx_count_sender'] = CustomerFeaturesBuilder.daily_tx_count_sender(g_day)
        features['daily_total_amount_sender'] = CustomerFeaturesBuilder.daily_total_amount_sender(g_day)
        features['weekly_tx_count_sender'] = CustomerFeaturesBuilder.weekly_tx_count_sender(g_week)
        features['weekly_avg_amount_sender'] = CustomerFeaturesBuilder.weekly_avg_amount_sender(g_week)
        features['daily_tx_velocity'] = CustomerFeaturesBuilder.daily_tx_velocity(features)
        features['balance_gap_sender'] = CustomerFeaturesBuilder.balance_gap_sender(features)
        return features
