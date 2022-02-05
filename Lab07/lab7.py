import numpy as np
import argparse
import os
import matplotlib.pyplot as plt
import time
from PIL import Image
import numba
from rich.console import Console

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


def make_image(n, arr, curr_step, image, f):
    for i in range(n):
        for j in range(n):
            if arr[i, j] == 1:
                image.paste(Image.open("./data/spin_up2.png"), (20 * j + 1, 20 * i + 1))
            else:
                image.paste(Image.open("./data/spin_down2.png"), (20 * j + 1, 20 * i + 1))
    image.save(f"./output/{f}{curr_step:0>3}.png")


@numba.njit()
def hamiltonian(n, J, B, arr):
    E_spins = 0
    E_int = 0
    for i in range(n):
        for j in range(n):
            E_spins += -B * arr[i, j]
            if j != n - 1:
                E_int += -J * arr[i, j] * arr[i, j+1]
            if i != n - 1:
                E_int += -J * arr[i, j] * arr[i+1, j]
    return E_spins + E_int


@numba.njit()
def step(n, J, beta, B, arr, H):
    i, j = np.random.randint(n), np.random.randint(n)
    H_0 = H
    arr[i, j] *= -1
    H_1 = hamiltonian(n, J, B, arr)
    if H_1 - H_0 < 0 or np.random.rand() < np.exp(-beta * (H_1 - H_0)):
        H = H_1
    else:
        arr[i, j] *= -1
    return arr, H


@numba.njit()
def magnetization(n, arr, curr_step, m):
    m[curr_step] = np.sum(arr)/(n * n)


@numba.njit()
def monte_carlo(n, J, beta, B, curr_step, arr, H, m):
    for i in range(n * n):
        a, h = step(n, J, beta, B, arr, H)
        arr = a
        H = h
    curr_step += 1
    magnetization(n, arr, curr_step, m)
    return arr, curr_step


n = args.N  # dim. of spins grid (n * n)
J = args.J  # Integral
beta = args.beta  # Beta parameter
B = args.B  # Magnetic field value
steps = args.steps  # Number of steps of Monte-Carlo method
curr_step = 0  # Current step of MC method
d = np.around(args.d, 2)  # Density of "up" spins
f = args.f  # Name of image files
arr = np.ones((n, n))  # Matrix of spin states
arr.flat[np.random.choice(n * n, int(n * n * (1 - d)), replace=False)] = (-1)
H = hamiltonian(n, J, B, arr)  # Hamiltonian of the system
m = np.zeros(steps + 1)  # Array of magnetization as function of step
magnetization(n, arr, curr_step, m)
image = Image.new("RGB", (20 * n + 2, 20 * n + 2), (0, 0, 0))
make_image(n, arr, curr_step, image, f)

console = Console()
console.clear()

for i in range(steps):
    arr, curr_step = monte_carlo(n, J, beta, B, curr_step, arr, H, m)
    make_image(n, arr, curr_step, image, f)

t2 = time.time()

print(t2-t1)

plt.plot(range(args.steps + 1), m)
plt.ylabel("Magnetization")
plt.ylim((-1.1, 1.1))
plt.xlabel("Step")
plt.title("Magnetization as a function of step")
plt.grid()
plt.show()




