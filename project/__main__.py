from constants import DATASET_FILE_DIR, TSV_FILE_DIR, TSV_HEADERS
from file_downloader import FileDownloader
from settings import MARKET_DATA_URL
from tsv_processor import TSVProcessor


def main():
    """Two main responsibilities:
    - Downloading latest market dataset via FileDownloader
    - Generating TSV by processing dataset and aggregating data via TSVProcessor
    """

    file_downloader: FileDownloader = FileDownloader(MARKET_DATA_URL, DATASET_FILE_DIR)
    file_downloader.download()

    tsv_processor: TSVProcessor = TSVProcessor(
        TSV_HEADERS, TSV_FILE_DIR, DATASET_FILE_DIR
    )
    tsv_processor.generate_tsv()


if __name__ == "__main__":
    """Script requires Python 3.9.5"""
    main()
