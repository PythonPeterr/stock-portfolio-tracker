import streamlit as st
import os
import pandas as pd
from werkzeug.utils import secure_filename
from data_processing import preprocess_date_columns, rename_columns

# Set up the upload folder and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file is a valid CSV."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(uploaded_file) -> str:
    """Save the uploaded file to the specified folder and return the file path."""
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.name))
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def main():
    st.title("Portfolio Dividend Tracker")
    st.write("Welcome to the Portfolio Dividend Tracker. Upload your transaction file to get started.")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            # Save the uploaded file and get the file path
            file_path = save_uploaded_file(uploaded_file)
            st.success(f"File {uploaded_file.name} uploaded successfully!")

            # Preprocess the data (processing date columns)
            df = preprocess_date_columns(file_path)

            # Rename and reorder columns
            df = rename_columns(df)

            # Display the processed and sorted data
            st.write("### Processed and Sorted File Contents:")
            df = df.sort_values(by='date_time')  # Ensure sorting by the new 'date_time' column

            # Filter out rows with invalid 'date_time' (NaT)
            df = df.dropna(subset=['date_time'])

            # Show the final dataframe
            st.dataframe(df)
        else:
            st.error("Invalid file format. Please upload a CSV file.")


if __name__ == "__main__":
    main()
