from src.Cube import Cube
import time
import operator
import random as rnd

PERMUTATIONS = [
    # permutes two edges: U face, bottom edge and right edge
    "F' L' B' R' U' R U' B L F R U R' U",
    # permutes two edges: U face, bottom edge and left edge
    "F R B L U L' U B' R' F' L' U' L U'",
    # permutes two corners: U face, bottom left and bottom right
    "U2 B U2 B' R2 F R' F' U2 F' U2 F R'",
    # permutes three corners: U face, bottom left and top left
    "U2 R U2 R' F2 L F' L' U2 L' U2 L F'",
    # permutes three centers: F face, top, right, bottom
    "U' B2 D2 L' F2 D2 B2 R' U'",
    # permutes three centers: F face, top, right, left
    "U B2 D2 R F2 D2 B2 L U",
    # U face: bottom edge <-> right edge, bottom right corner <-> top right corner
    "D' R' D R2 U' R B2 L U' L' B2 U R2",
    # U face: bottom edge <-> right edge, bottom right corner <-> left right corner
    "D L D' L2 U L' B2 R' U R B2 U' L2",
    # U face: top edge <-> bottom edge, bottom left corner <-> top right corner
    "R' U L' U2 R U' L R' U L' U2 R U' L U'",
    # U face: top edge <-> bottom edge, bottom right corner <-> top left corner
    "L U' R U2 L' U R' L U' R U2 L' U R' U",
    # permutes three corners: U face, bottom right, bottom left and top left
    "F' U B U' F U B' U'",
    # permutes three corners: U face, bottom left, bottom right and top right
    "F U' B' U F' U' B U",
    # permutes three edges: F face bottom, F face top, B face top
    "L' U2 L R' F2 R",
    # permutes three edges: F face top, B face top, B face bottom
    "R' U2 R L' B2 L",
    # H permutation: U Face, swaps the edges horizontally and vertically
    "M2 U M2 U2 M2 U M2"
]

ROTATIONS = ["x", "x'", "x2", "y", "y'", "y2"]

SCRAMBLES = [
    "B F L' R B2 L2 B' L' R' B2 U F2 L F2 D2 U' B' L' B2 R2 U' F D' B2 F2 L2 B2 L R2 U2",
]

POPULATION_SIZE = 500
ELITISM_NUMBER = 50


def random_perm():
    return PERMUTATIONS[rnd.randint(0, len(PERMUTATIONS) - 1)]


def random_rot():
    return ROTATIONS[rnd.randint(0, len(ROTATIONS) - 1)]


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
        print(f"Best fitness {cubes[0].fitness}")
        for i in range(0, len(cubes)):
            #print(i, cubes[i].fitness)
            if cubes[i].fitness == 0:
                solution_found = True
                print(f"Solution found in {time.time() - start_time} seconds")
                print('Solution')
                cubes[i].print_solution()
                return

            if i > ELITISM_NUMBER:
                copy_cube(cubes[rnd.randint(0, ELITISM_NUMBER)], cubes[i])

                evo_type = rnd.randint(0, 3)

                if evo_type == 0:
                    cubes[i].execute(random_perm())
                elif evo_type == 1:
                    cubes[i].execute(random_perm())
                    cubes[i].execute(random_perm())
                elif evo_type == 2:
                    cubes[i].execute(random_rot())
                    cubes[i].execute(random_perm())
                elif evo_type == 3:
                    cubes[i].execute(random_perm())
                    cubes[i].execute(random_rot())


if __name__ == '__main__':
    solve()
