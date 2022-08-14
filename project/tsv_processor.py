import csv
import json
from typing import List, Union

from settings import BUY, ORDER_ADD, SECURITY, SELL, SIXTEEN_MB_IN_BINARY_BYTES


class TSVProcessor:
    """This class is responsible for generating a TSV file from a raw dataset.txt."""

    def __init__(self, tsv_headers, tsv_FILE_DIR, dataset_directory) -> None:
        self.binary_bytes: int = SIXTEEN_MB_IN_BINARY_BYTES
        self.tsv_headers: List[str] = tsv_headers
        self.tsv_FILE_DIR: str = tsv_FILE_DIR
        self.dataset_directory: str = dataset_directory

    def zero_div(self, x, y) -> Union[int, float]:
        try:
            return x / y
        except ZeroDivisionError:
            return 0

    def generate_tsv(self) -> None:
        store: dict = {}

        with open(self.tsv_FILE_DIR, "wt") as tsv_file:
            tsv_writer = csv.writer(tsv_file, delimiter="\t", lineterminator="\n")
            tsv_writer.writerow(self.tsv_headers)

            # 16MB buffer for quicker file operations
            # assuming we aren't CPU limited but rather I/O limited
            with open(self.dataset_directory, "r", buffering=self.binary_bytes) as rows:
                for row in rows:
                    if SECURITY in row:
                        self._format_security(row, store)
                    elif ORDER_ADD in row:
                        self._format_order_add(row, store)

            for _, row_values in store.items():
                if max(row_values[2:]) != 0:
                    row_values[6] = self.zero_div(row_values[8], row_values[4])
                    row_values[7] = self.zero_div(row_values[9], row_values[5])
                    tsv_writer.writerow(row_values[:-2])

    def _format_security(self, row: str, store: dict) -> None:
        """Formatting and aggregating raw security data"""

        # transform raw data into a data structure (dictionary)
        _, raw_row = row.split()
        formatted_row: dict = json.loads(
            '{"h":' + raw_row.strip()[1:].replace(':"{"b_"', "")[:-1]
        )

        # add security data and setup default values for order add records
        store[formatted_row["security_"]["securityId_"]] = [
            formatted_row["security_"]["isin_"],  # [0]: ISIN
            formatted_row["security_"]["currency_"],  # [1]: Currency
            0,  # [2]: Total Buy Count
            0,  # [3]: Total Sell Count
            0,  # [4]: Total Buy Quantity
            0,  # [5]: Total Sell Quantity
            0,  # [6]: Weighted Average Buy Price
            0,  # [7]: Weighted Average Sell Price
            0,  # [8]: Price	Max Buy
            0,  # [9]: Min Sell Price
            0,  # [10]: sum of buy prices (for aggregation only)
            0,  # [11]: sum of sell prices (for aggregation only)
        ]

    def _format_order_add(self, row: str, store: dict):
        """Formatting and aggregating raw order add data"""

        formatted_row: dict = json.loads(
            '{"h":' + row.strip()[3:].replace("BUY", '"BUY"').replace("SELL", '"SELL"')
        )
        security_id = formatted_row["bookEntry_"]["securityId_"]

        # exit early if security and order add data don't exist
        if security_id not in store.keys():
            return

        record: list = store.get(security_id)
        book_entry: dict = formatted_row.get("bookEntry_")

        # aggregate data depending on BUY/SELL _side
        if book_entry.get("side_") == BUY:
            record[2] = record[2] + 1
            record[4] = record[4] + book_entry["quantity_"]
            record[8] = max(record[8], book_entry["price_"])
            record[10] = record[10] + book_entry["price_"]

        if book_entry.get("side_") == SELL:
            record[3] = record[3] + 1
            record[5] = record[5] + book_entry["quantity_"]
            record[9] = (
                book_entry["price_"]
                if record[9] == 0
                else min(record[9], book_entry["price_"])
            )
            record[11] = record[11] + book_entry["price_"]
