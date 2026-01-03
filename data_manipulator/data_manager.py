import pandas as pd
import os
from typing import List, Dict
from constants.config import DATA_PATH, COLUMNS


class DataManager:
    """
    DataManager is responsible for loading transaction datasets
    from disk and validating their schema.

    Responsibilities:
    - Load CSV files from a directory
    - Validate required column names
    - Merge valid datasets into a single DataFrame
    """

    def __init__(self):
        """
        Initialize DataManager.
        """
        pass

    @staticmethod
    def _get_all_files(path: str) -> List[str]:
        """
        Retrieve all file names from a given directory.

        Parameters
        ----------
        path : str
            Path to the directory containing data files.

        Returns
        -------
        List[str]
            List of file names in the directory.
            Returns an empty list if the path is invalid.
        """
        if os.path.isdir(path):
            return os.listdir(path)
        return []

    @staticmethod
    def _csv_files(files: List[str]) -> List[str]:
        """
        Filter CSV files from a list of file names.

        Parameters
        ----------
        files : List[str]
            List of file names.

        Returns
        -------
        List[str]
            List containing only files with `.csv` extension.
        """
        return list(filter(lambda x: x.split('.')[-1] == 'csv', files))

    @staticmethod
    def _valid_columns_name(columns: List[str]) -> bool:
        """
        Validate that all required columns exist in the dataset.

        Parameters
        ----------
        columns : List[str]
            Column names from a DataFrame.

        Returns
        -------
        bool
            True if all required columns are present.
            False otherwise.
        """
        for col in COLUMNS:
            if col not in columns:
                return False
        return True

    @staticmethod
    def read_csv(path: str) -> Dict[str, object]:
        """
        Load and validate CSV datasets from a directory.

        The method:
        - Reads all CSV files in the directory
        - Validates their column schema
        - Merges valid files into a single DataFrame
        - Tracks valid and invalid files

        Parameters
        ----------
        path : str
            Path to the directory containing CSV files.

        Returns
        -------
        Dict[str, object]
            Dictionary with the following keys:
            - 'data_frame': pandas.DataFrame
                Merged DataFrame of valid CSV files.
                Empty DataFrame if no valid files exist.
            - 'matches': List[str]
                Names of CSV files with valid schema.
            - 'not_matches': List[str]
                Names of CSV files with invalid schema.
        """
        info = {
            'data_frame': None,
            'matches': [],
            'not_matches': []
        }

        files = DataManager._get_all_files(path)
        if not files:
            info['data_frame'] = pd.DataFrame()
            return info

        matches = []
        not_matches = []
        data_frames = []

        for file in DataManager._csv_files(files):
            file_path = os.path.join(path, file)
            current_data = pd.read_csv(file_path)

            if not DataManager._valid_columns_name(current_data.columns):
                not_matches.append(file)
            else:
                matches.append(file)
                data_frames.append(current_data)

        info['data_frame'] = (
            pd.concat(data_frames) if len(data_frames) else pd.DataFrame()
        )
        info['matches'] = matches
        info['not_matches'] = not_matches

        return info


