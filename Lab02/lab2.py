import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
from Simulation import Simulation
import time

t1 = time.time()

parser = argparse.ArgumentParser(description="This script simulates Ising Method")
parser.add_argument("N", help="Dimensions of grid", type=int)
parser.add_argument("J", help="Integral", type=float)
parser.add_argument("beta", help="Beta", type=float)
parser.add_argument("B", help="Magnetic field value", type=float)
parser.add_argument("steps", help="Number of steps", type=int)
parser.add_argument("-d", help="Density of \"up\" spins", type=float, default=0.5, choices=np.around(np.arange(0, 1.01, 0.01), 2), metavar="[0.00-1.00]")
parser.add_argument("-f", help="Name of picture file", type=str, default="Step")
args = parser.parse_args()

for root, dirs, files in os.walk('./output'):
    for f in files:
        os.unlink(os.path.join(root, f))

S = Simulation(args.N, args.J, args.beta, args.B, args.steps, np.around(args.d, 2), args.f)

for s in S:
    s.make_image()

t2 = time.time()

print(t2-t1)

plt.plot(range(args.steps + 1), S.m)
plt.ylabel("Magnetization")
plt.ylim((-1.1, 1.1))
plt.xlabel("Step")
plt.title("Magnetization as a function of step")
plt.grid()
plt.show()




