import numpy as np
from PIL import Image
from rich.console import Console
from rich.progress import track


class Simulation:

    def __init__(self, n, J, beta, B, steps, d, f):
        self.n = n  # dim. of spins grid (n * n)
        self.J = J  # Integral
        self.beta = beta  # Beta parameter
        self.B = B  # Magnetic field value
        self.steps = steps  # Number of steps of Monte-Carlo method
        self.curr_step = 0  # Current step of MC method
        self.d = d  # Density of "up" spins
        self.f = f  # Name of image files
        self.arr = self.init_arr()  # Matrix of spin states
        self.H = self.hamiltonian()  # Hamiltonian of the system
        self.m = np.zeros(self.steps + 1)  # Array of magnetization as function of step
        self.magnetization()
        self.image = Image.new("RGB", (20 * self.n + 2, 20 * self.n + 2), (0, 0, 0))
        self.make_image()
        self.console = Console()
        self.console.clear()
        self.console.rule("Projekt 2")
        self.console.print()

    def init_arr(self):
        a = np.ones((self.n, self.n))
        a.flat[np.random.choice(self.n * self.n, int(self.n * self.n * (1 - self.d)), replace=False)] = (-1)
        return a

    def make_image(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.arr[i, j] == 1:
                    self.image.paste(Image.open("./data/spin_up2.png"), (20 * j + 1, 20 * i + 1))
                else:
                    self.image.paste(Image.open("./data/spin_down2.png"), (20 * j + 1, 20 * i + 1))
        self.image.save(f"./output/{self.f}{self.curr_step:0>3}.png")

    def hamiltonian(self):
        E_spins, E_int = 0, 0
        for i in range(self.n):
            for j in range(self.n):
                E_spins += -self.B * self.arr[i, j]
                if j != self.n - 1:
                    E_int += -self.J * self.arr[i, j] * self.arr[i, j+1]
                if i != self.n - 1:
                    E_int += -self.J * self.arr[i, j] * self.arr[i+1, j]
        return E_spins + E_int

    def step(self):
        i, j = np.random.randint(self.n), np.random.randint(self.n)
        H_0 = self.H
        self.arr[i, j] *= -1
        H_1 = self.hamiltonian()
        if H_1 - H_0 < 0 or np.random.rand() < np.exp(-self.beta * (H_1 - H_0)):
            self.H = H_1
        else:
            self.arr[i, j] *= -1

    def monte_carlo(self):
        for i in range(self.n*self.n):
            self.step()
        self.curr_step += 1
        self.magnetization()

    def magnetization(self):
        self.m[self.curr_step] = np.sum(self.arr)/(self.n * self.n)

    def __iter__(self):
        for i in track(range(self.steps)):
            self.monte_carlo()
            yield self
