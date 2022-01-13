from itertools import islice
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from requests import Response


def get_folder_name(link: str) -> str:
    return link.rsplit('/', 2)[-2]


def get_file_name(link: str) -> str:
    return link.rsplit('/', 1)[-1]


def download_file(url: str, filename: str, path: Path) -> None:
    with open(path.joinpath(filename), 'wb') as out_file:
        content: bytes = requests.get(url, stream=True).content
        out_file.write(content)


def download_all(url: str, path: Path, start_from: int = 1) -> None:
    path.mkdir(exist_ok=True)

    req: Response = requests.get(url)
    soup: BeautifulSoup = BeautifulSoup(req.text, 'html.parser')

    for tag in islice(soup.find_all('a'), start_from, None):
        link: str = tag.get('href')

        if link.endswith('/'):
            folder_name: str = get_folder_name(link)
            download_all(url + f'/{folder_name}/', path.joinpath(Path(folder_name)))
        else:
            file_name: str = get_file_name(link)
            download_file(url + file_name, file_name, path)


if __name__ == '__main__':
    url_: str = ''
    path_: Path = Path('testmedia')

    download_all(url_, Path().absolute().joinpath(path_), start_from=1)
