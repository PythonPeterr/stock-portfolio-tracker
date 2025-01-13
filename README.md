
# Portfolio Dividend Tracker

## Overview

The **Portfolio Dividend Tracker** is a Python-based web application designed to help investors track their stock portfolio performance, dividend income, and key metrics. The app allows users to upload transaction data (e.g., from DeGiro) and generates insightful dashboards to visualize portfolio performance and dividend growth.

This tool is perfect for both individual and professional investors who want a clear understanding of their investment journey.

---

## Key Features

- **Transaction Upload**:
  - Upload CSV files with your transaction history (buy/sell transactions, dividends).
- **Dynamic Dashboards**:
  - View key performance metrics such as:
    - Portfolio value over time.
    - Dividend income (monthly/yearly).
    - Asset allocation by sector/geography.
- **Data Analytics**:
  - Automatic calculations of:
    - Dividend yield.
    - Yield on cost.
    - Total return.
- **Interactive Visualizations**:
  - Charts and graphs powered by Plotly for a user-friendly experience.
- **Secure and Localized**:
  - No third-party data sharing. All data stays on your machine or private cloud.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual Environment (recommended)

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/PythonPeterr/portfolio-dividend-tracker.git
   cd portfolio-dividend-tracker
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate  # Mac/Linux
   .\env\Scripts\activate  # Windows
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:

   ```bash
   python app/main.py
   ```

5. **Access the Application**:

   - Open your browser and navigate to: `http://127.0.0.1:5000/`

---

## File Structure

```
portfolio-dividend-tracker/
├── app/
│   ├── static/          # CSS/JS files (for styling and interactivity)
│   ├── templates/       # HTML templates for the web UI
│   ├── __init__.py      # Initializes the app module
│   ├── main.py          # Entry point for the application
│   ├── routes.py        # Defines app routes
│   ├── models.py        # Database models (optional for now)
│   ├── utils.py         # Helper functions
│
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
├── LICENSE              # Licensing information
├── .gitignore           # Files to ignore in version control
```

---

## Roadmap

### Phase 1: Core Functionality

- Basic file upload.
- Parse DeGiro CSV format.
- Display portfolio overview.

### Phase 2: Advanced Analytics

- Add KPIs like yield on cost, dividend growth rate.
- Introduce benchmarking against indices.

### Phase 3: Interactive Dashboards

- Sector and geographic allocation visualization.
- Monthly/yearly dividend income trends.

### Phase 4: Deployment

- Host the app on Heroku or AWS.
- Add user authentication for personalized experience.

---

## Contributing

Contributions are welcome! Here’s how you can help:

- Report bugs by opening an issue.
- Suggest new features or improvements.
- Submit pull requests for review.

### Steps to Contribute:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and push the branch.
4. Open a pull request and describe your changes.

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software for commercial or personal purposes, provided attribution is given.

---

## Acknowledgments

- Inspired by tools like [Portfolio Dividend Tracker](https://portfoliodividendtracker.com/en) and [GetQuin](https://www.getquin.com/portfolio-tracker).
- Built with Python, Flask, and Plotly.

---

## Contact

- **GitHub**: [PythonPeterr](https://github.com/PythonPeterr)
- **Email**: [pythonpeterr@example.com](mailto\:pythonpeterr@example.com)
