import requests
from bs4 import BeautifulSoup


def download_list():
    page = requests.get("https://github.com/fish-shell/fish-shell/tree/master/share/completions")
    soup = BeautifulSoup(page.text, 'html.parser')
    files = soup.find(class_='file-wrap')
    each_file = files.find_all('a', 'js-navigation-open')
    return each_file[1:]


def download_file(file_tags):
    file_url = "https://github.com" + file_tags['href'].replace('blob', 'raw')
    file_data = requests.get(file_url)
    return file_data
    # with open(file_tags.text, 'w') as thefile:
    #     thefile.write(file_data.text)
