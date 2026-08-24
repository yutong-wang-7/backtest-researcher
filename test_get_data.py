import yfinance as yf

df = yf.download(
    "AAPL",
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=False
)

df.columns = df.columns.get_level_values(0).str.lower()

df.to_csv("AAPL.csv")