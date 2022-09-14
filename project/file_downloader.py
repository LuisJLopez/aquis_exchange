import os
from datetime import datetime
from email.utils import formatdate, parsedate_to_datetime

import requests

from constants import ONE_MB_IN_BINARY_BYTES


class FileDownloader:
    """Responsible for downoading files."""

    def __init__(self, url: str, outbound_directory: str) -> None:
        self.url: str = url
        self.dataset_file_dir: str = outbound_directory
        self.chunk_size: str = ONE_MB_IN_BINARY_BYTES

    def download(self) -> None:
        headers = {}

        if os.path.exists(self.dataset_file_dir):
            modified_time: float = os.path.getmtime(self.dataset_file_dir)
            headers["if-modified-since"] = formatdate(modified_time, usegmt=True)

        response = requests.get(self.url, headers=headers, stream=True)
        response.raise_for_status()

        # if hosted file hasn't been modified, don't re-write it
        if response.status_code == requests.codes.not_modified:
            return

        if response.status_code == requests.codes.ok:
            # write file one line at a time, don't load all of it into memory
            with open(self.dataset_file_dir, "wb") as file:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    file.write(chunk)

            if last_modified := response.headers.get("last-modified"):
                new_modified_time = parsedate_to_datetime(last_modified).timestamp()
                os.utime(
                    self.dataset_file_dir,
                    times=(datetime.now().timestamp(), new_modified_time),
                )
