import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data by renaming columns, creating a datetime column,
    and converting date/time columns to proper formats.
    """
    column_map = {
        'Datum': 'date',
        'Tijd': 'time',
        'Product': 'product',
        'ISIN': 'isin',
        'Beurs': 'exchange',
        'Uitvoeringsplaats': 'execution_market',
        'Aantal': 'quantity',
        'Koers': 'price_local',
        'Unnamed: 8': 'currency',
        'Lokale waarde': 'local_value',
        'Unnamed: 10': 'currency_2',
        'Waarde': 'base_value',
        'Unnamed: 12': 'base_currency',
        'Wisselkoers': 'fx_rate',
        'Transactiekosten en/of': 'transaction_cost',
        'Unnamed: 15': 'transaction_cost_currency',
        'Totaal': 'net_value_base',
        'Unnamed: 17': 'net_value_base_currency',
    }
    
    # Rename columns
    df = df.rename(columns=column_map)
    
    # Convert 'date' and 'time' columns to proper formats
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%d-%m-%Y').dt.date
    df['time'] = pd.to_datetime(df['time'], errors='coerce', format='%H:%M').dt.time
    
    # Create a new 'datetime' column combining 'date' and 'time'
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'].astype(str), errors='coerce')
    
    return df

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reorder columns as per the desired structure.
    """
    desired_order = [
        'date', 'time', 'datetime', 'product', 'isin', 'exchange', 'execution_market',
        'quantity', 'price_local', 'currency', 'local_value', 'currency_2', 'base_value',
        'base_currency', 'fx_rate', 'transaction_cost', 'transaction_cost_currency',
        'net_value_base', 'net_value_base_currency'
    ]
    
    df = df.reindex(columns=desired_order)
    return df

def calculate_vwap(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the VWAP (Volume Weighted Average Price) for each ISIN, 
    with a reset when the position is flat, and considering only future buys.
    """
    # Sort the dataframe by datetime to ensure transactions are processed in order
    df = df.sort_values(by='datetime')
    
    # Initialize dictionaries to track VWAPs and positions
    vwap_per_isin = {}
    position_per_isin = {}
    vwap_results = []
    
    for index, row in df.iterrows():
        product = row['product']
        quantity = row['quantity']
        price = row['price_local']
        
        # Handle when position becomes zero
        if product not in position_per_isin:
            position_per_isin[product] = 0  # Ensure there's an entry for product
        
        # If position is zero (flat), reset and discard previous buys
        if position_per_isin[product] == 0 and quantity < 0:
            vwap_per_isin[product] = None  # Discard any previous buys, VWAP becomes invalid for a moment
            position_per_isin[product] = 0  # Ensure position is zero
        
        elif quantity > 0:  # Only update VWAP for buys
            if position_per_isin[product] == 0:
                # If the position was flat, reset the VWAP to the first buy price
                vwap_per_isin[product] = price
                position_per_isin[product] = quantity
            else:
                # Update the VWAP incrementally with the new buy
                total_value = vwap_per_isin[product] * position_per_isin[product] + price * quantity
                position_per_isin[product] += quantity
                vwap_per_isin[product] = total_value / position_per_isin[product]
        
        # For sell transactions (quantity < 0), just update the position
        if quantity < 0:
            position_per_isin[product] -= abs(quantity)
        
        # Append the most recent VWAP
        vwap_results.append(vwap_per_isin.get(product, None))
    
    # Add the VWAP results to the dataframe
    df['vwap'] = vwap_results
    
    # Return the VWAP per product (only the last VWAP for each product)
    return df[['product', 'vwap']].groupby('product')['vwap'].last()



def calculate_holdings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the net holdings and average purchase price (GAK) for each product/ISIN.
    """
    df['is_buy'] = df['quantity'] > 0  # Assumption: positive quantity indicates a buy
    df['is_sell'] = df['quantity'] < 0  # Assumption: negative quantity indicates a sell
    
    # Fill missing fx_rate values and transaction costs
    df['fx_rate'].fillna(1, inplace=True)
    df['transaction_cost'].fillna(0, inplace=True)
    
    # Calculate the purchase value per transaction
    df['purchase_value'] = df['price_local'] * df['quantity'] + df['transaction_cost']
    df['adjusted_purchase_value'] = df['purchase_value'] * df['fx_rate']  # Adjust with FX rate
    
    # Group by ISIN/Product to calculate total quantity and purchase value
    holdings = df.groupby(['product', 'isin', 'currency']).agg(
        total_quantity=('quantity', 'sum'),
        total_transaction_cost=('transaction_cost', 'sum')
    ).reset_index()
    
    # Remove rows with zero total quantity (no holdings)
    holdings = holdings[holdings['total_quantity'] != 0]
    
    # Calculate the VWAP per ISIN using the updated calculate_vwap function
    vwap_per_isin = calculate_vwap(df)
    
    # Merge the VWAP results into the holdings dataframe
    holdings['vwap'] = holdings['product'].map(vwap_per_isin)
    
    return holdings
