from src.Cube import Cube
import time
import operator
import random as rnd

SCRAMBLES = [
    "B F L' R B2 L2 B' L' R' B2 U F2 L F2 D2 U' B' L' B2 R2 U' F D' B2 F2 L2 B2 L R2 U2",
]

POPULATION_SIZE = 500
ELITISM_NUMBER = 50


def copy_cube(from_cube, to_cube):
    for f in from_cube.faces:
        for i in range(0, 3):
            for j in range(0, 3):
                to_cube.faces[f][i, j] = from_cube.faces[f][i, j]

    to_cube.move_history = [item for item in from_cube.move_history]
    to_cube.fitness = from_cube.fitness


def solve():
    start_time = time.time()
    cubes = []
    for c in range(0, POPULATION_SIZE):
        cube = Cube(c, SCRAMBLES[0])
        cubes.append(cube)

    #for r in range(0, 20):
    gen = 1
    solution_found = False
    while not solution_found:
        print(f"Generation {gen}")
        gen = gen + 1
        cubes.sort(key=operator.attrgetter('fitness'))

        for i in range(0, len(cubes)):
            print(i, cubes[i].fitness)
            if cubes[i].fitness == 0:
                solution_found = True
                print('Solution found')
                print(f"{cubes[i].move_history}")
                print(f"{time.time() - start_time} seconds")
                return

            if i > ELITISM_NUMBER:
                copy_cube(cubes[rnd.randint(0, ELITISM_NUMBER)], cubes[i])
                cubes[i].random_move()


if __name__ == '__main__':
    solve()

