import requests
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor
import urllib.request
from PIL import Image


def func(url, lst, n):
    filename = f"./output/{lst[n]}"
    urllib.request.urlretrieve(f"{url}{lst[n]}", filename)
    img = Image.open(filename)
    imgGray = img.convert('L')
    imgGray.save(filename)


def worker(url, lst, n):
    fun = func(url, lst, n)


url = "http://if.pw.edu.pl/~mrow/dyd/wdprir/"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

lst = [a['href'] for a in soup.find_all('a', href=True) if a['href'][:3] == "img"]

if __name__ == '__main__':
    pool = ProcessPoolExecutor(10)
    for n in range(len(lst)):
        pool.submit(worker, url, lst, n)
