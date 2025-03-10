import numpy as np
import pandas as pd

def check_dataframe_quality(df, verbose = True):
   """
   Checks the quality of the DataFrame and reports issues such as missing values,
   infinite values, duplicates, and unique values.
   Parameters:
       df (pd.DataFrame): DataFrame to analyze.
   Returns:
       dict: A summary with the performed validations.
   """
   report = {}
   # Count missing values
   missing_values = df.isnull().sum().sum()
   report['Missing values'] = missing_values
   if verbose:
      print(f"Missing values found: {missing_values}") if missing_values else print("No missing values found.")
   # Count infinite values
   infinite_values = df.isin([np.inf, -np.inf]).any().sum()
   report['Infinite values'] = infinite_values
   if verbose:
      print(f"Columns with infinite values: {infinite_values}") if infinite_values else print("No infinite values found.")
   # Count duplicate rows
   duplicate_rows = df.duplicated().sum()
   report['Duplicate rows'] = duplicate_rows
   if verbose:
      print(f"Duplicate rows found: {duplicate_rows}") if duplicate_rows else print("No duplicate rows found.")
   return report
