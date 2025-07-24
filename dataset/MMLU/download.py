import os
import requests
import tarfile
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def download():
    this_file_path = os.path.split(__file__)[0]
    tar_path = os.path.join(this_file_path, "data.tar")
    if not os.path.exists(tar_path):
        url = "https://people.eecs.berkeley.edu/~hendrycks/data.tar"
        print(f"Downloading {url}")
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        r = session.get(url, allow_redirects=True)
        with open(tar_path, 'wb') as f:
            f.write(r.content)
        print(f"Saved to {tar_path}")

    data_path = os.path.join(this_file_path, "data")
    if not os.path.exists(data_path):
        tar = tarfile.open(tar_path)
        tar.extractall(this_file_path)
        tar.close()
        print(f"Saved to {data_path}")


if __name__ == "__main__":
    download()