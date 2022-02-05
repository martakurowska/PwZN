import argparse
from collections import defaultdict
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
import aiofiles
import asyncio
import time

parser = argparse.ArgumentParser(description="This script plots histogram of most used words in given file")
parser.add_argument("file", help="name of the file")
parser.add_argument("-n", help="number of words shown on histogram", type=int, default=10)
parser.add_argument("-m", help="minimal length of words considered in histogram", type=int, default=0)
parser.add_argument("-l", help="list of ignored words ex. \"this, that, sth\"", type=str, default="")
args = parser.parse_args()

t1 = time.time()


async def main():
    async with aiofiles.open(args.file, encoding="utf8", mode='r') as file:
        x = defaultdict(int)
        async for line in file:
            verse = line.lower().translate({ord(i): None for i in "123456789.,:;!?()«»…-—―*"}).strip().split()
            for i in verse:
                x[i] += 1
    return x


x = asyncio.run(main())
t2 = time.time()

ignored = args.l.translate({ord(i): None for i in ","}).split()
data = [(k, v) for k, v in x.items() if len(k) >= args.m and k not in ignored]
data.sort(key=lambda e: e[1], reverse=True)

data = vcolor(data[0:args.n], [Gre, Yel, Red])
graph = Pyasciigraph(line_length=60)

for line in graph.graph(f"Histogram słów w pliku {args.file}", data):
    print(line)

print(f"Time elapsed: {t2-t1}")
