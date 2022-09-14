import os

MARKET_DATA_URL: str = os.environ.get(
    "MARKET_DATA_URL",
    "https://aquis-public-files.s3.eu-west-2.amazonaws.com/market_data/current/pretrade_current.txt",
)
