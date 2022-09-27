#              |************|
#              |*U1**U2**U3*|
#              |************|
#              |*U4**U5**U6*|
#              |************|
#              |*U7**U8**U9*|
#              |************|
#  ************|************|************|************
#  *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
#  ************|************|************|************
#  *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
#  ************|************|************|************
#  *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
#  ************|************|************|************
#              |************|
#              |*D1**D2**D3*|
#              |************|
#              |*D4**D5**D6*|
#              |************|
#              |*D7**D8**D9*|
#              |************|

import numpy as np
import random

GREEN = 'G'
ORANGE = 'O'
YELLOW = 'Y'
WHITE = 'W'
BLUE = 'B'
RED = 'R'

FRONT = 'Front'
BACK = 'Back'
LEFT = 'Left'
RIGHT = 'Right'
UP = 'Up'
DOWN = 'Down'

CLOCKWISE = (1, 0)
COUNTER_CLOCKWISE = (0, 1)

DEBUG = False
MOVES = ["D", "D'", "D2", "E", "E'", "E2", "U", "U'", "U2", "R", "R'", "R2", "M", "M'", "M2", "L", "L'", "L2", "B", "B'", "B2", "S", "S'", "S2", "F", "F'", "F2"]


class Cube:
    def __init__(self, name, scramble) -> None:
        self.name = name

        self.faces = {
            UP: np.full((3, 3), WHITE),
            RIGHT: np.full((3, 3), RED),
            LEFT: np.full((3, 3), ORANGE),
            FRONT: np.full((3, 3), GREEN),
            BACK: np.full((3, 3), BLUE),
            DOWN: np.full((3, 3), YELLOW)
        }

        self.moves_lookup = {
            # horizontal
            "D": self.D, "D'": self.D_prime, "D2": self.D2,
            "E": self.E, "E'": self.E_prime, "E2": self.E2,
            "U": self.U, "U'": self.U_prime, "U2": self.U2,
            # # vertical
            "R": self.R, "R'": self.R_prime, "R2": self.R2,
            "M": self.M, "M'": self.M_prime, "M2": self.M2,
            "L": self.L, "L'": self.L_prime, "L2": self.L2,
            # # z
            "B": self.B, "B'": self.B_prime, "B2": self.B2,
            "S": self.S, "S'": self.S_prime, "S2": self.S2,
            "F": self.F, "F'": self.F_prime, "F2": self.F2
            # full rotations
            # TODO
        }

        self.move_history = []
        self.execute(scramble)
        self.fitness = 0
        self.random_move()
        self.random_move()

    def execute(self, moves):
        if DEBUG:
            print(f"Cube {self.name}")
        moves = moves.split(" ")
        for move in moves:
            if DEBUG:
                print('Executing ' + move)
            self.moves_lookup[move]()
            self.move_history.append(move)
        self.__calculate_fitness()
        if DEBUG:
            print(self.move_history)

    def __calculate_fitness(self):
        wrong_stickers = 0

        for k, face in self.faces.items():
            center = face[1, 1]

            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != center:
                        wrong_stickers += 1

        self.fitness = wrong_stickers

    def is_solved(self):
        return self.fitness == 0

    # move functions
    # horizontal moves
    def D(self):
        self.faces[DOWN] = np.rot90(self.faces[DOWN], axes=CLOCKWISE)
        self.__swap_x((FRONT, 2), (RIGHT, 2), (BACK, 2), (LEFT, 2))

    def D_prime(self):
        self.faces[DOWN] = np.rot90(self.faces[DOWN], axes=COUNTER_CLOCKWISE)
        self.__swap_x((FRONT, 2), (LEFT, 2), (BACK, 2), (RIGHT, 2))

    def D2(self):
        self.D()
        self.D()

    def E(self):
        self.__swap_x((FRONT, 1), (RIGHT, 1), (BACK, 1), (LEFT, 1))

    def E_prime(self):
        self.__swap_x((FRONT, 1), (LEFT, 1), (BACK, 1), (RIGHT, 1))

    def E2(self):
        self.E()
        self.E()

    def U(self):
        self.faces[UP] = np.rot90(self.faces[UP], axes=CLOCKWISE)
        self.__swap_x((FRONT, 0), (LEFT, 0), (BACK, 0), (RIGHT, 0))

    def U_prime(self):
        self.faces[UP] = np.rot90(self.faces[UP], axes=COUNTER_CLOCKWISE)
        self.__swap_x((FRONT, 0), (RIGHT, 0), (BACK, 0), (LEFT, 0))

    def U2(self):
        self.U()
        self.U()

    def __swap_x(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])
        self.__copy_row(self.faces[t4[0]][t4[1]], backup)
        self.__copy_row(self.faces[t3[0]][t3[1]], self.faces[t4[0]][t4[1]])
        self.__copy_row(self.faces[t2[0]][t2[1]], self.faces[t3[0]][t3[1]])
        self.__copy_row(self.faces[t1[0]][t1[1]], self.faces[t2[0]][t2[1]])
        self.__copy_row(backup, self.faces[t1[0]][t1[1]])

    def __copy_row(self, origin, destination):  
        destination[0] = origin[0]
        destination[1] = origin[1]
        destination[2] = origin[2]

    # vertical moves
    def R(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=CLOCKWISE)
        self.__swap_y((DOWN, 2, False), (FRONT, 2, False), (UP, 2, True), (BACK, 0, True))

    def R_prime(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=COUNTER_CLOCKWISE)
        self.__swap_y((DOWN, 2, True), (BACK, 0, True), (UP, 2, False), (FRONT, 2, False))

    def R2(self):
        self.R()
        self.R()

    def M(self):
        self.__swap_y((DOWN, 1, True), (BACK, 1, True), (UP, 1, False), (FRONT, 1, False))

    def M_prime(self):
        self.__swap_y((DOWN, 1, False), (FRONT, 1, False), (UP, 1, True), (BACK, 1, True))

    def M2(self):
        self.M()
        self.M()

    def L(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=CLOCKWISE)
        self.__swap_y((DOWN, 0, True), (BACK, 2, True), (UP, 0, False), (FRONT, 0, False))

    def L_prime(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=COUNTER_CLOCKWISE)
        self.__swap_y((DOWN, 0, False), (FRONT, 0, False), (UP, 0, True), (BACK, 2, True))

    def L2(self):
        self.L()
        self.L()

    def __swap_y(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])

        if t4[2]:
            self.__copy_row(np.flip(self.faces[t4[0]][:, t4[1]]), backup)
        else:
            self.__copy_row(self.faces[t4[0]][:, t4[1]], backup)

        if t3[2]:
            self.__copy_row(np.flip(self.faces[t3[0]][:, t3[1]]), self.faces[t4[0]][:, t4[1]])
        else:
            self.__copy_row(self.faces[t3[0]][:, t3[1]], self.faces[t4[0]][:, t4[1]])

        if t2[2]:
            self.__copy_row(np.flip(self.faces[t2[0]][:, t2[1]]), self.faces[t3[0]][:, t3[1]])
        else:
            self.__copy_row(self.faces[t2[0]][:, t2[1]], self.faces[t3[0]][:, t3[1]])

        if t1[2]:
            self.__copy_row(np.flip(self.faces[t1[0]][:, t1[1]]), self.faces[t2[0]][:, t2[1]])
        else:
            self.__copy_row(self.faces[t1[0]][:, t1[1]], self.faces[t2[0]][:, t2[1]])

        self.__copy_row(backup, self.faces[t1[0]][:, t1[1]])

    # z moves
    def B(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=CLOCKWISE)
        self.__swap_z((DOWN, 2, True), (RIGHT, 2, False), (UP, 0, True), (LEFT, 0, False))

    def B_prime(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=COUNTER_CLOCKWISE)
        self.__swap_z((DOWN, 2, False), (LEFT, 0, True), (UP, 0, False), (RIGHT, 2, True))

    def B2(self):
        self.B()
        self.B()

    def S(self):
        self.__swap_z((DOWN, 1, False), (LEFT, 1, True), (UP, 1, False), (RIGHT, 1, True))

    def S_prime(self):
        self.__swap_z((DOWN, 1, True), (RIGHT, 1, False), (UP, 1, True), (LEFT, 1, False))

    def S2(self):
        self.S()
        self.S()

    def F(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=CLOCKWISE)
        self.__swap_z((DOWN, 0, False), (LEFT, 2, True), (UP, 2, False), (RIGHT, 0, True))

    def F_prime(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=COUNTER_CLOCKWISE)
        self.__swap_z((DOWN, 0, True), (RIGHT, 0, False), (UP, 2, True), (LEFT, 2, False))

    def F2(self):
        self.F()
        self.F()

    def __swap_z(self, t1, t2, t3, t4):
        backup = np.array(["", "", ""])

        if t4[2]:
            self.__copy_row(np.flip(self.faces[t4[0]][:, t4[1]]), backup)
        else:
            self.__copy_row(self.faces[t4[0]][:, t4[1]], backup)

        if t3[2]:
            self.__copy_row(np.flip(self.faces[t3[0]][t3[1]]), self.faces[t4[0]][:, t4[1]])
        else:
            self.__copy_row(self.faces[t3[0]][t3[1]], self.faces[t4[0]][:, t4[1]])

        if t2[2]:
            self.__copy_row(np.flip(self.faces[t2[0]][:, t2[1]]), self.faces[t3[0]][t3[1]])
        else:
            self.__copy_row(self.faces[t2[0]][:, t2[1]], self.faces[t3[0]][t3[1]])

        if t1[2]:
            self.__copy_row(np.flip(self.faces[t1[0]][t1[1]]), self.faces[t2[0]][:, t2[1]])
        else:
            self.__copy_row(self.faces[t1[0]][t1[1]], self.faces[t2[0]][:, t2[1]])

        self.__copy_row(backup, self.faces[t1[0]][t1[1]])
                
    # TODO
    # full rotations

    def random_move(self):
        move = MOVES[random.randint(0, len(MOVES) - 1)]
        self.execute(move)
        self.move_history.append(move)