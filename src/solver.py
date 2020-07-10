import random as rnd
import cProfile
import time
import operator
from src.cube import Cube

SINGLE_MOVES = ["U", "U'", "U2", "D", "D'", "D2",
                "R", "R'", "R2", "L", "L'", "L2",
                "F", "F'", "F2", "B", "B'", "B2"]

FULL_ROTATIONS = ["x", "x'", "x2", "y", "y'", "y2"]

ORIENTATIONS = ["z", "z'", "z2"]

PERMUTATIONS = [
    # permutes two edges: U face, bottom edge and right edge
    "F' L' B' R' U' R U' B L F R U R' U".split(" "),
    # permutes two edges: U face, bottom edge and left edge
    "F R B L U L' U B' R' F' L' U' L U'".split(" "),
    # permutes two corners: U face, bottom left and bottom right
    "U2 B U2 B' R2 F R' F' U2 F' U2 F R'".split(" "),
    # permutes three corners: U face, bottom left and top left
    "U2 R U2 R' F2 L F' L' U2 L' U2 L F'".split(" "),
    # permutes three centers: F face, top, right, bottom
    "U' B2 D2 L' F2 D2 B2 R' U'".split(" "),
    # permutes three centers: F face, top, right, left
    "U B2 D2 R F2 D2 B2 L U".split(" "),
    # U face: bottom edge <-> right edge, bottom right corner <-> top right corner
    "D' R' D R2 U' R B2 L U' L' B2 U R2".split(" "),
    # U face: bottom edge <-> right edge, bottom right corner <-> left right corner
    "D L D' L2 U L' B2 R' U R B2 U' L2".split(" "),
    # U face: top edge <-> bottom edge, bottom left corner <-> top right corner
    "R' U L' U2 R U' L R' U L' U2 R U' L U'".split(" "),
    # U face: top edge <-> bottom edge, bottom right corner <-> top left corner
    "L U' R U2 L' U R' L U' R U2 L' U R' U".split(" "),
    # permutes three corners: U face, bottom right, bottom left and top left
    "F' U B U' F U B' U'".split(" "),
    # permutes three corners: U face, bottom left, bottom right and top right
    "F U' B' U F' U' B U".split(" "),
    # permutes three edges: F face bottom, F face top, B face top
    "L' U2 L R' F2 R".split(" "),
    # permutes three edges: F face top, B face top, B face bottom
    "R' U2 R L' B2 L".split(" "),
    # H permutation: U Face, swaps the edges horizontally and vertically
    "M2 U M2 U2 M2 U M2".split(" ")
]


class Solver:

    def __init__(self, population_size, max_generations, max_resets, elitism_num):
        self.population_size = population_size
        self.max_generations = max_generations
        self.max_resets = max_resets
        self.elitism_num = elitism_num

    def solve(self, scramble, verbose=False):
        start_time = time.time()

        if verbose:
            print("Starting...")

        for r in range(0, self.max_resets):
            # initialize population
            cubes = []
            for i in range(0, self.population_size):
                cube = Cube()
                cube.execute(scramble)
                # randomize it
                # cube.execute(self.__rnd_rotation())
                cube.execute(self.__rnd_single_move())
                cube.execute(self.__rnd_single_move())
                cubes.append(cube)

            # evolve population
            for g in range(0, self.max_generations):
                # sort by fitness
                cubes.sort(key=operator.attrgetter('fitness'))

                if verbose and g % 20 == 0 and g != 0:
                    print(f"World: {r + 1} - Generation: {g}")
                    print(f"Best solution so far")
                    print(f"{cubes[0].get_algorithm_str()}")
                    print("")

                # the goal is to minimize the fitness function
                # 0 means that the cube is solved
                for i in range(0, len(cubes)):
                    if cubes[i].fitness == 0:
                        print("Solution found")
                        print(f"World: {r + 1} - Generation: {g + 1}")
                        print(f"Scramble: {cubes[i].get_scramble_str()}")
                        print(f"Solution")
                        print(f"{cubes[i].get_algorithm_str()}")
                        print(f"Moves: {len(cubes[i].get_algorithm())}")
                        print(f"{time.time() - start_time} seconds")
                        print("")
                        return

                    # elitism: the best performers move to the next generation without changes
                    if i > self.elitism_num:
                        # copy a random top performer cube
                        self.__copy(cubes[i], cubes[rnd.randint(0, self.elitism_num)])
                        evolution_type = rnd.randint(0, 5)

                        if evolution_type == 0:
                            cubes[i].execute(self.__rnd_permutation())
                        elif evolution_type == 1:
                            cubes[i].execute(self.__rnd_permutation())
                            cubes[i].execute(self.__rnd_permutation())
                        elif evolution_type == 2:
                            cubes[i].execute(self.__rnd_full_rotation())
                            cubes[i].execute(self.__rnd_permutation())
                        elif evolution_type == 3:
                            cubes[i].execute(self.__rnd_orientation())
                            cubes[i].execute(self.__rnd_permutation())
                        elif evolution_type == 4:
                            cubes[i].execute(self.__rnd_full_rotation())
                            cubes[i].execute(self.__rnd_orientation())
                            cubes[i].execute(self.__rnd_permutation())
                        elif evolution_type == 5:
                            cubes[i].execute(self.__rnd_orientation())
                            cubes[i].execute(self.__rnd_full_rotation())
                            cubes[i].execute(self.__rnd_permutation())

            if verbose:
                print(f"Resetting the world")

        # if a solution was found we returned
        print("")
        print(f"Solution not found")
        print(f"{time.time() - start_time} seconds")

    # copy.deepcopy was very slow for the whole cube because it tries to figure out what changed
    def __copy(self, cube_to, cube_from):
        for f in cube_from.faces:
            for i in range(0, 3):
                for j in range(0, 3):
                    cube_to.faces[f][i, j] = cube_from.faces[f][i, j]

        cube_to.move_history = [item for item in cube_from.move_history]
        cube_to.fitness = cube_from.fitness

    def __rnd_single_move(self):
        r = rnd.randint(0, len(SINGLE_MOVES) - 1)
        return [SINGLE_MOVES[r]]

    def __rnd_permutation(self):
        r = rnd.randint(0, len(PERMUTATIONS) - 1)
        return PERMUTATIONS[r]

    def __rnd_full_rotation(self):
        r = rnd.randint(0, len(FULL_ROTATIONS) - 1)
        return [FULL_ROTATIONS[r]]

    def __rnd_orientation(self):
        r = rnd.randint(0, len(ORIENTATIONS) - 1)
        return [ORIENTATIONS[r]]


def main():
    # p = cProfile.Profile()
    # p.enable()

    # scramble_str = "R' U' L2 B2 U2 F L2 B' L' B D R B F2 L F R' B2 F' L B' D B2 R2 D' U B2 F' D R2"
    # scramble_str = "U2 B' F L B' F2 D' U B2 R' U B' F U F' R' U2 L' R' D F2 R' F' D2 L' R2 B' D L U2"
    # scramble_str = "B' R' U2 B' F D2 R2 B F' L2 R' B2 D2 L2 F' U L B2 D F L' F R B2 D' U' B' L' B' F2"
    # scramble_str = "F2 D2 U L' R' B2 L2 R2 B F L D' L2 D U' L' D' B2 D2 R' U L R' D' U L' R2 U F' L'"
    scramble_str = "D' B2 D2 L2 U' L R' F L2 R2 U' L2 B' L D' B2 R2 B' R F U2 R B2 F' L' B2 L2 R F2 L'"
    scramble = scramble_str.split(" ")

    population_size = 500
    max_generations = 300
    max_resets = 10
    elitism_num = 50

    solver = Solver(population_size, max_generations, max_resets, elitism_num)
    # for _ in range(0, 5):
    #     solver.solve(scramble, False)
    solver.solve(scramble, verbose=True)

    # # Disable profiling
    # p.disable()
    # # Print the stats
    # p.print_stats()
    # # Dump the stats to a file
    # p.dump_stats("profile.txt")


if __name__ == '__main__':
    main()
