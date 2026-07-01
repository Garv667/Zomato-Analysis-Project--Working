# Zomato Restaurant Analysis 🍽️

An interactive Streamlit dashboard for exploring the Zomato restaurant dataset — ratings, pricing, online ordering, and table booking trends across restaurant types.

## Features

- **Filters**: restaurant type, online order availability, table booking, cost range, rating range
- **Key metrics**: restaurant count, average rating, average cost, total votes
- **Visualizations**:
  - Rating distribution histogram
  - Cost vs. rating scatter plot
  - Restaurant type breakdown (pie chart)
  - Online order & table booking comparison
- **Top rated restaurants table** (adjustable top N)
- **Data explorer** with name search and CSV export

## Project Structure

```
.
├── app.py                  # Main Streamlit app
├── data/
│   └── Zomato-data.csv     # Dataset
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the app locally:
   ```bash
   streamlit run app.py
   ```

## Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repo, branch, and set the main file path to `app.py`.
4. Click **Deploy**.

## Dataset

The dataset (`data/Zomato-data.csv`) contains 148 restaurant records with the following columns:

| Column | Description |
|---|---|
| `name` | Restaurant name |
| `online_order` | Whether online ordering is available (Yes/No) |
| `book_table` | Whether table booking is available (Yes/No) |
| `rate` | Rating out of 5 |
| `votes` | Number of votes |
| `approx_cost(for two people)` | Approximate cost for two people (₹) |
| `listed_in(type)` | Restaurant type (Buffet, Cafes, Dining, other) |
