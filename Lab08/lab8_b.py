import requests
from bs4 import BeautifulSoup
import urllib.request
from PIL import Image
import time


def func(url, lst, n):
    filename = f"./output_2/{lst[n]}"
    urllib.request.urlretrieve(f"{url}{lst[n]}", filename)
    img = Image.open(filename)
    imgGray = img.convert('L')
    imgGray.save(filename)


t1 = time.time()
url = "http://if.pw.edu.pl/~mrow/dyd/wdprir/"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

lst = [a['href'] for a in soup.find_all('a', href=True) if a['href'][:3] == "img"]

for n in range(len(lst)):
    func(url, lst, n)

t2 = time.time()
print(f"Execution time: {t2-t1}")
