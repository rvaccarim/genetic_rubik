import numpy as np
from typing import List

GREEN = "G"
ORANGE = "O"
RED = "R"
WHITE = "W"
YELLOW = "Y"
BLUE = "B"

FRONT = "Front"
LEFT = "Left"
BACK = "Back"
RIGHT = "Right"
TOP = "Top"
BOTTOM = "Bottom"

CLOCKWISE = (1, 0)
COUNTERCLOCKWISE = (0, 1)


class Cube:

    def __init__(self):

        self.faces = {
            FRONT: np.full((3, 3), GREEN),
            LEFT: np.full((3, 3), ORANGE),
            RIGHT: np.full((3, 3), RED),
            TOP: np.full((3, 3), WHITE),
            BOTTOM: np.full((3, 3), YELLOW),
            BACK: np.full((3, 3), BLUE),
        }

        self.moves_lookup = {
            # hortizontal
            "D": self.D, "D'": self.D_prime, "D2": self.D2,
            "E": self.E, "E'": self.E_prime, "E2": self.E2,
            "U": self.U, "U'": self.U_prime, "U2": self.U2,
            # vertical
            "L": self.L, "L'": self.L_prime, "L2": self.L2,
            "R": self.R, "R'": self.R_prime, "R2": self.R2,
            "M": self.M, "M'": self.M_prime, "M2": self.M2,
            # z
            "B": self.B, "B'": self.B_prime, "B2": self.B2,
            "F": self.F, "F'": self.F_prime, "F2": self.F2,
            "S": self.S, "S'": self.S_prime, "S2": self.S2,
            # full rotations
            "x": self.x_full, "x'": self.x_prime_full, "x2": self.x2_full,
            "y": self.y_full, "y'": self.y_prime_full, "y2": self.y2_full,
            "z": self.z_full, "z'": self.z_prime_full, "z2": self.z2_full,
        }

        self.move_history = []
        self.fitness = 0  # less is better, it means 0 misplaced sticker

    # for example moves = ["L", "R", "F", "R'", "D"]
    def execute(self, moves: 'List'):
        for m in moves:
            self.moves_lookup[m]()

        # we assume that the first one is the scramble
        self.move_history.append(moves)
        self.__calculate_fitness()

    def __calculate_fitness(self):
        misplaced_stickers = 0

        for k, face in self.faces.items():
            # centers are fixed in a Rubik cube
            center = face[1, 1]

            for i in range(0, 3):
                for j in range(0, 3):
                    if face[i, j] != center:
                        misplaced_stickers += 1

        self.fitness = misplaced_stickers

    def is_solved(self):
        if self.fitness == 0:
            return True
        return False

    # ------------------------------------------------------------------------------------
    # X Axis movements - D, E and U
    # ------------------------------------------------------------------------------------
    def D(self):
        self.faces[BOTTOM] = np.rot90(self.faces[BOTTOM], axes=CLOCKWISE)
        self.__swap_x((FRONT, 2), (RIGHT, 2), (BACK, 2), (LEFT, 2))

    def D_prime(self):
        self.faces[BOTTOM] = np.rot90(self.faces[BOTTOM], axes=COUNTERCLOCKWISE)
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
        self.faces[TOP] = np.rot90(self.faces[TOP], axes=CLOCKWISE)
        self.__swap_x((FRONT, 0), (LEFT, 0), (BACK, 0), (RIGHT, 0))

    def U_prime(self):
        self.faces[TOP] = np.rot90(self.faces[TOP], axes=COUNTERCLOCKWISE)
        self.__swap_x((FRONT, 0), (RIGHT, 0), (BACK, 0), (LEFT, 0))

    def U2(self):
        self.U()
        self.U()

    def __swap_x(self, t1, t2, t3, t4):
        # t1, t2, t3 and t4 are tuples
        # index 0 = face
        # index 1 = row index
        # This means: put t1 into t2, t2 into t3, t3 into t4, t4 into t1
        # we do it backwards to avoid unnecesary temporary variables
        backup = np.array(["", "", ""])
        self.__copy_stickers(backup, self.faces[t4[0]][t4[1]])
        self.__copy_stickers(self.faces[t4[0]][t4[1]], self.faces[t3[0]][t3[1]])
        self.__copy_stickers(self.faces[t3[0]][t3[1]], self.faces[t2[0]][t2[1]])
        self.__copy_stickers(self.faces[t2[0]][t2[1]], self.faces[t1[0]][t1[1]])
        self.__copy_stickers(self.faces[t1[0]][t1[1]], backup)

    def __copy_stickers(self, destination, origin):
        destination[0] = origin[0]
        destination[1] = origin[1]
        destination[2] = origin[2]

    # ------------------------------------------------------------------------------------
    # Y Axis movements - L, R and M
    # ------------------------------------------------------------------------------------
    def L(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=CLOCKWISE)
        self.__swap_y((BOTTOM, 0, True), (BACK, 2, True), (TOP, 0, False), (FRONT, 0, False))

    def L_prime(self):
        self.faces[LEFT] = np.rot90(self.faces[LEFT], axes=COUNTERCLOCKWISE)
        self.__swap_y((BOTTOM, 0, False), (FRONT, 0, False), (TOP, 0, True), (BACK, 2, True))

    def L2(self):
        self.L()
        self.L()

    def M(self):
        self.__swap_y((BOTTOM, 1, True), (BACK, 1, True), (TOP, 1, False), (FRONT, 1, False))

    def M_prime(self):
        self.__swap_y((BOTTOM, 1, False), (FRONT, 1, False), (TOP, 1, True), (BACK, 1, True))

    def M2(self):
        self.M()
        self.M()

    def R(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=CLOCKWISE)
        self.__swap_y((BOTTOM, 2, False), (FRONT, 2, False), (TOP, 2, True), (BACK, 0, True))

    def R_prime(self):
        self.faces[RIGHT] = np.rot90(self.faces[RIGHT], axes=COUNTERCLOCKWISE)
        self.__swap_y((BOTTOM, 2, True), (BACK, 0, True), (TOP, 2, False), (FRONT, 2, False))

    def R2(self):
        self.R()
        self.R()

    def __swap_y(self, t1, t2, t3, t4):
        # t1, t2, t3 and t4 are 3-tuples
        # Index 0 = face
        # Index 1 = column
        # Index 2 = boolean, flip values
        # This means: put t1 into t2, t2 into t3, t3 into t4, t4 into t1
        backup = np.array(["", "", ""])

        if t4[2]:
            self.__copy_stickers(backup, np.flip(self.faces[t4[0]][:, t4[1]]))
        else:
            self.__copy_stickers(backup, self.faces[t4[0]][:, t4[1]])

        if t3[2]:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], np.flip(self.faces[t3[0]][:, t3[1]]))
        else:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], self.faces[t3[0]][:, t3[1]])

        if t2[2]:
            self.__copy_stickers(self.faces[t3[0]][:, t3[1]], np.flip(self.faces[t2[0]][:, t2[1]]))
        else:
            self.__copy_stickers(self.faces[t3[0]][:, t3[1]], self.faces[t2[0]][:, t2[1]])

        if t1[2]:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], np.flip(self.faces[t1[0]][:, t1[1]]))
        else:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], self.faces[t1[0]][:, t1[1]])

        self.__copy_stickers(self.faces[t1[0]][:, t1[1]], backup)

    # ------------------------------------------------------------------------------------
    # Z Axis movements - B and F
    # ------------------------------------------------------------------------------------
    def B(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=CLOCKWISE)
        self.__swap_z((BOTTOM, 2, True), (RIGHT, 2, False), (TOP, 0, True), (LEFT, 0, False))

    def B_prime(self):
        self.faces[BACK] = np.rot90(self.faces[BACK], axes=COUNTERCLOCKWISE)
        self.__swap_z((BOTTOM, 2, False), (LEFT, 0, True), (TOP, 0, False), (RIGHT, 2, True))

    def B2(self):
        self.B()
        self.B()

    def F(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=CLOCKWISE)
        self.__swap_z((BOTTOM, 0, False), (LEFT, 2, True), (TOP, 2, False), (RIGHT, 0, True))

    def F_prime(self):
        self.faces[FRONT] = np.rot90(self.faces[FRONT], axes=COUNTERCLOCKWISE)
        self.__swap_z((BOTTOM, 0, True), (RIGHT, 0, False), (TOP, 2, True), (LEFT, 2, False))

    def F2(self):
        self.F()
        self.F()

    def S(self):
        self.__swap_z((BOTTOM, 1, False), (LEFT, 1, True), (TOP, 1, False), (RIGHT, 1, True))

    def S_prime(self):
        self.__swap_z((BOTTOM, 1, True), (RIGHT, 1, False), (TOP, 1, True), (LEFT, 1, False))

    def S2(self):
        self.S()
        self.S()

    def __swap_z(self, t1, t2, t3, t4):
        # t1, t2, t3 and t4 are 3-tuples
        # Index 0 = face
        # Index 1 = row or col index (moving along the Z axis involves both)
        # Index 2 = boolean, flip values
        # This means: put t1 into t2, t2 into t3, t3 into t4, t4 into t1
        # we do it backwards to avoid unnecesary temporary variables
        backup = np.array(["", "", ""])

        if t4[2]:
            self.__copy_stickers(backup, np.flip(self.faces[t4[0]][:, t4[1]]))
        else:
            self.__copy_stickers(backup, self.faces[t4[0]][:, t4[1]])

        if t3[2]:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], np.flip(self.faces[t3[0]][t3[1]]))
        else:
            self.__copy_stickers(self.faces[t4[0]][:, t4[1]], self.faces[t3[0]][t3[1]])

        if t2[2]:
            self.__copy_stickers(self.faces[t3[0]][t3[1]], np.flip(self.faces[t2[0]][:, t2[1]]))
        else:
            self.__copy_stickers(self.faces[t3[0]][t3[1]], self.faces[t2[0]][:, t2[1]])

        if t1[2]:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], np.flip(self.faces[t1[0]][t1[1]]))
        else:
            self.__copy_stickers(self.faces[t2[0]][:, t2[1]], self.faces[t1[0]][t1[1]])

        self.__copy_stickers(self.faces[t1[0]][t1[1]], backup)

    # ------------------------------------------------------------------------------------
    # Full rotations
    # ------------------------------------------------------------------------------------
    def x_full(self):
        self.L_prime()
        self.M_prime()
        self.R()

    def x_prime_full(self):
        self.L()
        self.M()
        self.R_prime()

    def x2_full(self):
        self.x_full()
        self.x_full()

    def y_full(self):
        self.U()
        self.E_prime()
        self.D_prime()

    def y_prime_full(self):
        self.U_prime()
        self.E()
        self.D()

    def y2_full(self):
        self.y_full()
        self.y_full()

    def z_full(self):
        self.F()
        self.S()
        self.B_prime()

    def z_prime_full(self):
        self.F_prime()
        self.S_prime()
        self.B()

    def z2_full(self):
        self.z_full()
        self.z_full()

    # ------------------------------------------------------------------------------------
    # Util
    # ------------------------------------------------------------------------------------
    def get_face_as_str(self, face):
        m = self.faces[face]
        return f"{m[0, 0]} {m[0, 1]} {m[0, 2]} - {m[1, 0]} {m[1, 1]} {m[1, 2]} - {m[2, 0]} {m[2, 1]} {m[2, 2]}"

    def get_scramble(self):
        return self.move_history[0]

    def get_scramble_str(self):
        return " ".join(self.get_scramble())

    def get_algorithm(self):
        # we don't want to include the scramble
        flat_list = [item for sublist in self.move_history[1:] for item in sublist]
        return flat_list

    def get_algorithm_str(self):
        return " ".join(self.get_algorithm())

    def __str__(self):
        state = [f"Scramble: {self.get_scramble_str()}", f"Algorithm: {self.get_algorithm_str()}"]

        for k, v in sorted(self.faces.items()):
            state.append(f"{'{:<8}'.format(k + ':')}  {v[0, 0]} {v[0, 1]} {v[0, 2]}")
            state.append(f"{'{:<8}'.format('')}  {v[1, 0]} {v[1, 1]} {v[1, 2]}"),
            state.append(f"{'{:<8}'.format('')}  {v[2, 0]} {v[2, 1]} {v[2, 2]}")

        return "\n".join(state)
