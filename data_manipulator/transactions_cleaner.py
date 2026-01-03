import pandas as pd
from constants.config import DATA_PATH, NUMERIC_COLUMNS, CATEGORICAL_COLUMNS


class TransactionCleaner:
    """
    TransactionCleaner is responsible for cleaning and validating
    transaction-level data before feature engineering and risk analysis.

    Responsibilities:
    - Handle missing values
    - Enforce correct data types
    - Remove logically invalid values
    - Remove duplicate transactions

    """

    @staticmethod
    def _handle_missing(data: pd.DataFrame):
        """
        Remove rows containing missing values (NaN).

        Parameters
        ----------
        data : pd.DataFrame
            Input transaction DataFrame.

        Returns
        -------
        dict
            {
                'cleaned_data': pd.DataFrame,
                'number_of_removed_samples': int
            }
        """
        cleaned_data = data.dropna()
        number_of_removed_samples = data.shape[0] - cleaned_data.shape[0]
        return {
            'cleaned_data': cleaned_data,
            'number_of_removed_samples': number_of_removed_samples
        }

    @staticmethod
    def _handle_duplicates(data: pd.DataFrame):
        """
        Remove duplicate transaction rows.

        Parameters
        ----------
        data : pd.DataFrame
            Input transaction DataFrame.

        Returns
        -------
        dict
            {
                'cleaned_data': pd.DataFrame,
                'number_of_removed_samples': int
            }
        """
        cleaned_data = data.drop_duplicates()
        number_of_removed_samples = data.shape[0] - cleaned_data.shape[0]
        return {
            'cleaned_data': cleaned_data,
            'number_of_removed_samples': number_of_removed_samples
        }

    @staticmethod
    def _handle_data_types(data: pd.DataFrame):
        """
        Enforce correct data types for numeric and categorical columns.

        - Numeric columns are converted strictly.
        -  Rows failing conversion are removed.
        - Categorical columns are converted safely to strings.

        Parameters
        ----------
        data : pd.DataFrame
            Input transaction DataFrame.

        Returns
        -------
        dict
            {
                'cleaned_data': pd.DataFrame,
                'number_of_removed_samples': int
            }
        """
        df = data.copy()

        for col in NUMERIC_COLUMNS:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna(subset=NUMERIC_COLUMNS.keys())

        for col in CATEGORICAL_COLUMNS:
            df[col] = df[col].astype(str).str.strip()

        df = df.astype(NUMERIC_COLUMNS)

        number_of_removed_samples = data.shape[0] - df.shape[0]

        return {
            'cleaned_data': df,
            'number_of_removed_samples': number_of_removed_samples
        }

    @staticmethod
    def _values_check(data: pd.DataFrame):
        """
        Perform logical (sanity) checks on transaction values.

        Rules applied:
        - step >= 0
        - amount >= 0 (zero-amount transactions are allowed as they may indicate suspicious or fraudulent behavior)
        - All balances must be non-negative

        Parameters
        ----------
        data : pd.DataFrame
            Input transaction DataFrame.

        Returns
        -------
        dict
            {
                'cleaned_data': pd.DataFrame,
                'number_of_removed_samples': int
            }
        """
        df = data.copy()

        mask = (
            (df['step'] >= 0) &
            (df['amount'] >= 0) &
            (df['oldbalanceOrg'] >= 0) &
            (df['newbalanceOrig'] >= 0) &
            (df['oldbalanceDest'] >= 0) &
            (df['newbalanceDest'] >= 0)
        )

        df = df[mask]
        number_of_removed_samples = data.shape[0] - df.shape[0]

        return {
            'cleaned_data': df,
            'number_of_removed_samples': number_of_removed_samples
        }

    @staticmethod
    def clean(data: pd.DataFrame):
        """
        Apply the full cleaning pipeline to transaction data.

        Cleaning steps:
        1. Remove missing values
        2. Enforce correct data types
        3. Apply logical value checks
        4. Remove duplicate transactions

        Parameters
        ----------
        data : pd.DataFrame
            Raw transaction DataFrame.

        Returns
        -------
        dict
            {
                'cleaned_data': pd.DataFrame,
                'stats': dict
            }
        """
        stats = {}

        result = TransactionCleaner._handle_missing(data)
        df = result['cleaned_data']
        stats['removed_missing'] = result['number_of_removed_samples']

        result = TransactionCleaner._handle_data_types(df)
        df = result['cleaned_data']
        stats['removed_invalid_types'] = result['number_of_removed_samples']

        result = TransactionCleaner._values_check(df)
        df = result['cleaned_data']
        stats['removed_invalid_values'] = result['number_of_removed_samples']

        result = TransactionCleaner._handle_duplicates(df)
        df = result['cleaned_data']
        stats['removed_duplicates'] = result['number_of_removed_samples']

        return {
            'cleaned_data': df,
            'stats': stats
        }
