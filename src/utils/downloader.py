import os
import io
import requests
import time
import sys
import typing
from fake_useragent import UserAgent

def progress_bar_cli(
    total_len: int,
    downloaded_len: int,
    start_time: int,
    bar_size: int = 100
):
    """
    Default :attr:`on_data` for :function:`download_zip_file`. It writes
    a progress bar, the percent of amount downloaded and the velocity
    of download.
    """
    percent = downloaded_len / total_len
    bar_amount = int(bar_size * percent)
    total_bars = "=" * bar_amount
    missing_bars = " " * (bar_size - bar_amount)
    velocity = "{:.2f}".format((downloaded_len // (time.perf_counter() - start_time )) / 1000000)
    percent = "{:.2f}".format(percent * 100)
    sys.stdout.write(f"\r[{total_bars}{missing_bars}] ({percent}%) {velocity} Mb/s")
    if (bar_amount == bar_size):
        print()

def download_zip_file(
    url: str, 
    dest_dir: str,
    chunk_size: int = 1024,
    user_agent: str = str(UserAgent().random),
    on_data: typing.Callable = progress_bar_cli
) -> str:
    """
    Given a url, download a large file in a streaming manner.
    When a chunk of data (with some predefined size) is write on buffer, 
    tuple of (chunk_data, amount_downloaded, total, percentage), until reaches
    the 100%. Then return the name
    """
    filename = os.path.basename(url)
    destfile = os.path.join(dest_dir, filename)
    headers = {
        "Content-Disposition": f"attachment filename={filename}",
        "User-Agent": user_agent,
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept-Encoding": "gzip, deflate, br"
    }
    
    zip_buffer = io.BytesIO()
    start = time.perf_counter()
        
    res = requests.get(url=url, stream=True, headers=headers)
    res.raise_for_status()
    total_len = int(res.headers.get('Content-Length'))
    downloaded_len = 0

    for chunk in res.iter_content(chunk_size=chunk_size):        
        downloaded_len += len(chunk)
        zip_buffer.write(chunk)
        on_data(total_len, downloaded_len, start)

    res.close()
    zip_file = open(destfile, "wb")
    zip_file.write(zip_buffer.getvalue())
    zip_buffer.close()
    zip_file.close()
    
    return destfile 
