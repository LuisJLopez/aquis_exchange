from typing import List

URL: str = "https://aquis-public-files.s3.eu-west-2.amazonaws.com/market_data/current/pretrade_current.txt"

DATASET_FILE_DIR: str = "downloads/dataset.txt"
TSV_FILE_DIR: str = "generated_tsv/market_data.tsv"

TSV_HEADERS: List[str] = [
    "ISIN",
    "Currency",
    "Total Buy Count",
    "Total Sell Count",
    "Total Buy Quantity",
    "Total Sell Quantity",
    "Weighted Average Buy Price",
    "Weighted Average Sell Price",
    "Max Buy Price",
    "Min Sell Price",
]

ORDER_ADD: str = '"msgType_":12'
SECURITY: str = '"msgType_":8'

SELL: str = "SELL"
BUY: str = "BUY"

ONE_MB_IN_BINARY_BYTES: int = 1048576
SIXTEEN_MB_IN_BINARY_BYTES: int = 16777216
