# Main Application (streamlit)
import streamlit as st
import pandas as pd
from data_processing import preprocess_data, reorder_columns, calculate_holdings

def main():
    st.title("Portfolio Dividend Tracker")
    st.write("Upload your transaction file to view its contents.")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read and preprocess data
        df = pd.read_csv(uploaded_file)
        df = preprocess_data(df)

        # Reorder columns
        df = reorder_columns(df)

        # Display the transactions dataframe
        st.write("### Transactions:")
        st.dataframe(df)

        # Compute and display holdings
        holdings_df = calculate_holdings(df)
        st.write("### Holdings Overview:")
        st.dataframe(holdings_df)

if __name__ == "__main__":
    main()