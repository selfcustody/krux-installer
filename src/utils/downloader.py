import os
import io
import requests
import time
import sys
import typing
from fake_useragent import UserAgent

def progress_bar(total_len: int, downloaded_len: int, start):
    """
    Default :attr:`on_data` for :function:`download_zip_file`
    """
    done = int(30 * downloaded_len / int(total_len))
    sys.stdout.write("\r[%s%s] %s Mbps" % ('=' * done, ' ' * (30-done), downloaded_len // (time.perf_counter() -start) / 100000))
    if (done == 30):
        print()

def download_zip_file(
    url: str, 
    dest_dir: str,
    chunk_size: int = 1024,
    on_data: typing.Callable = progress_bar
) -> str:
    """
    Given a url, download a large file in a streaming manner. It yields a
    tuple of (chunk_data, amount_downloaded, total, percentage), until reaches
    the 100%. Then return the name
    """
    filename = os.path.basename(url)
    destfile = os.path.join(dest_dir, filename)
    user_agent = UserAgent()
    headers = {
        "Content-Disposition": f"attachment filename={filename}",
        "User-Agent": str(user_agent.random),
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
