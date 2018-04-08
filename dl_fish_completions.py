import asyncio
import async_timeout
import os
import click
from aiohttp import ClientSession
import requests
from bs4 import BeautifulSoup


def download_list():
    page = requests.get("https://github.com/fish-shell/fish-shell/tree/master/share/completions")
    soup = BeautifulSoup(page.text, 'html.parser')
    files = soup.find(class_='file-wrap')
    each_file = files.find_all('a', 'js-navigation-open')
    return each_file[1:]


def select_files(files):
    installed_completions = set(os.listdir("/usr/share/fish/completions"))
    available_completions = set([f.text for f in files])
    needed_completions = list(available_completions - installed_completions)
    return [f for f in files if f.text in needed_completions]


async def download_file(session, file_tags, save_path):
    file_url = "https://github.com" + file_tags['href'].replace('blob', 'raw')
    # file_data = requests.get(file_url)
    # print(f"downloading {file_tags.text}")
    async with async_timeout.timeout(20):
        async with session.get(file_url) as response:
            file_data = await response.read()
            # print(f"{file_tags.text}: {file_data[:30]}")
    with open(os.path.join(save_path, file_tags.text), 'wb') as thefile:
        thefile.write(file_data)
    # return file_data, file_tags.text
    # return file_data
    # with open(file_tags.text, 'w') as thefile:
    #     thefile.write(file_data.text)


async def run(files, save_path):
    tasks = []
    async with ClientSession() as session:
        for file_ in files:
            task = asyncio.ensure_future(download_file(session, file_, save_path))
            tasks.append(task)

        await asyncio.gather(*tasks)


@click.command()
@click.option("-p", "--path",
              help="path to save new completions. Defaults to ~/.config/fish/completions")
def cli(path):
    if path is None:
        path = os.path.expanduser('~/.config/fish/completions')
    os.makedirs(path, exist_ok=True)
    files = download_list()
    needed_files = select_files(files)
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(run(needed_files, path))
    loop.run_until_complete(future)

