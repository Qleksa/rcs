from ast import operator
from unittest.main import main


from src.Cube import Cube
import time
import operator

SCRAMBLES = [
    "B F L' R B2 L2 B' L' R' B2 U F2 L F2 D2 U' B' L' B2 R2 U' F D' B2 F2 L2 B2 L R2 U2",
]

def solve():
    start_time = time.time()
    cubes = []
    for r in range(0, 3):
        cube = Cube(SCRAMBLES[0])
        cubes.append(cube)

    for r in range(0, 20):
        cubes.sort(key=operator.attrgetter('fitness'))

        for i in range(0, len(cubes)):
            print(i, cubes[i].fitness)
            if cubes[i].fitness == 0:
                print('Solution found')
                print(f"{cubes[i].all_moves()}")
                print(f"{time.time() - start_time} seconds")
                return

            cubes[i].random_move()

if __name__ == '__main__':
    solve()

