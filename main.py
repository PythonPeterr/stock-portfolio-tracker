import streamlit as st
import os
from werkzeug.utils import secure_filename

# Set up the upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if the uploaded file is a valid CSV."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Streamlit app
def main():
    st.title("Portfolio Dividend Tracker")
    st.write("Welcome to the Portfolio Dividend Tracker. Upload your transaction file to get started.")

    # File upload section
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        if allowed_file(uploaded_file.name):
            # Save the uploaded file
            file_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.name))
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} uploaded successfully!")

            # Display basic file information
            st.write("### Uploaded File Contents:")
            import pandas as pd
            df = pd.read_csv(file_path)
            st.dataframe(df)
        else:
            st.error("Invalid file format. Please upload a CSV file.")

if __name__ == "__main__":
    main()
