import pandas as pd
from datetime import datetime

def preprocess_date_columns(file_path: str) -> pd.DataFrame:
    """Process the uploaded CSV file and return a cleaned DataFrame."""
    df = pd.read_csv(file_path)

    # Convert 'Datum' to datetime with format %d-%m-%Y (Day-Month-Year)
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce', format='%d-%m-%Y').dt.date

    # Convert 'Tijd' to time, handling errors
    df['Tijd'] = pd.to_datetime(df['Tijd'], errors='coerce', format='%H:%M').dt.time

    # Combine 'Datum' and 'Tijd' into a single string column for datetime representation
    df['Datetime_str'] = df['Datum'].astype(str) + ' ' + df['Tijd'].astype(str)

    # Convert 'Datetime_str' into a proper datetime object
    df['Datetime'] = pd.to_datetime(df['Datetime_str'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

    # Drop the temporary 'Datetime_str' column
    df.drop(columns=['Datetime_str'], inplace=True)

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename and reorder columns in a DataFrame."""
    
    # Column renaming map
    column_map = {
        'Datum': 'trade_date',
        'Tijd': 'timestamp',
        'Valutadatum': 'value_date',
        'Product': 'product',
        'ISIN': 'isin',
        'Omschrijving': 'description',
        'FX': 'fx_rate',
        'Mutatie': None,  # Drop this column
        'Unnamed: 8': 'amount',
        'Saldo': 'currency',
        'Unnamed: 10': 'account_balance',
        'Order Id': 'order_id',
        'Datetime': 'date_time'
    }

    # Rename columns
    df = df.rename(columns=column_map)

    # Drop the 'Mutatie' column as it's not needed
    df = df.drop(columns=['Mutatie'], errors='ignore')

    # Reorder the columns as per the requested structure
    desired_column_order = [
        'date_time',
        'trade_date',
        'timestamp',
        'value_date',
        'isin',
        'product',
        'description',
        'fx_rate',
        'currency',
        'amount',
        'account_balance',
        'order_id'
    ]
    
    # Ensure all desired columns are present in the final DataFrame
    df = df[desired_column_order]

    return df
