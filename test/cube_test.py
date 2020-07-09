import unittest

from src.cube import Cube, FRONT, BACK, LEFT, RIGHT, TOP, BOTTOM


class CubeTest(unittest.TestCase):
    def test_is_solved(self):
        cube = Cube()
        self.assertTrue(cube.is_solved())
        cube.execute(["F"])
        self.assertFalse(cube.is_solved())

    def test_fitness(self):
        cube = Cube()
        self.assertEqual(0, cube.fitness)
        cube.execute("F' L' B' R' U' R U' B L F R U R' U".split(" "))
        self.assertEqual(4, cube.fitness)

        cube2 = Cube()
        cube2.execute("D' R' D R2 U' R B2 L U' L' B2 U R2".split(" "))
        self.assertEqual(8, cube2.fitness)

    def test_clockwise(self):
        cube = Cube()
        scramble = "U L D R F B M E S U L D R F B M E S".split(" ")
        expected_back = "B B B - O B R - Y G O"
        expected_bottom = "R W G - R Y O - B W R"
        expected_front = "R O Y - B G W - W B O"
        expected_left = "O Y Y - G O Y - Y W G"
        expected_right = "G Y R - O R B - W G B"
        expected_top = "W R W - G W R - G Y O"

        cube.execute(scramble)
        print(str(cube))
        self.assertEqual(expected_back, cube.get_face_as_str(BACK))
        self.assertEqual(expected_bottom, cube.get_face_as_str(BOTTOM))
        self.assertEqual(expected_front, cube.get_face_as_str(FRONT))
        self.assertEqual(expected_left, cube.get_face_as_str(LEFT))
        self.assertEqual(expected_right, cube.get_face_as_str(RIGHT))
        self.assertEqual(expected_top, cube.get_face_as_str(TOP))
        self.assertEqual(scramble, cube.get_scramble())
        # rotations
        cube.execute(["x", "x", "x", "x", "y", "y", "y", "y", "z", "z", "z", "z"])
        print(str(cube))
        self.assertEqual(expected_back, cube.get_face_as_str(BACK))
        self.assertEqual(expected_bottom, cube.get_face_as_str(BOTTOM))
        self.assertEqual(expected_front, cube.get_face_as_str(FRONT))
        self.assertEqual(expected_left, cube.get_face_as_str(LEFT))
        self.assertEqual(expected_right, cube.get_face_as_str(RIGHT))
        self.assertEqual(expected_top, cube.get_face_as_str(TOP))

    def test_counterclockwise(self):
        cube = Cube()
        scramble = "U' L' D' R' F' B' M' E' S' U' L' D' R' F' B' M' E' S'".split(" ")
        expected_back = "Y O R - W G R - O G W"
        expected_bottom = "G W R - R Y B - R W B"
        expected_front = "G G G - G B R - O B Y"
        expected_left = "Y B O - B R Y - B Y Y"
        expected_right = "R W B - G O O - G Y W"
        expected_top = "B Y O - O W R - W O W"

        cube.execute(scramble)
        self.assertEqual(expected_back, cube.get_face_as_str(BACK))
        self.assertEqual(expected_bottom, cube.get_face_as_str(BOTTOM))
        self.assertEqual(expected_front, cube.get_face_as_str(FRONT))
        self.assertEqual(expected_left, cube.get_face_as_str(LEFT))
        self.assertEqual(expected_right, cube.get_face_as_str(RIGHT))
        self.assertEqual(expected_top, cube.get_face_as_str(TOP))
        self.assertEqual(scramble, cube.get_scramble())
        # rotations
        cube.execute(["x", "x", "x", "x", "y", "y", "y", "y", "z", "z", "z", "z"])
        print(str(cube))
        self.assertEqual(expected_back, cube.get_face_as_str(BACK))
        self.assertEqual(expected_bottom, cube.get_face_as_str(BOTTOM))
        self.assertEqual(expected_front, cube.get_face_as_str(FRONT))
        self.assertEqual(expected_left, cube.get_face_as_str(LEFT))
        self.assertEqual(expected_right, cube.get_face_as_str(RIGHT))
        self.assertEqual(expected_top, cube.get_face_as_str(TOP))

    def test_scramble1(self):
        cube = Cube()
        cube.execute("D B2 F2 D F' L2 R2 U2 F' L2 U2 B2 F R' U2 B L' B' F2 D' U L2 R2 F2 D L2 U B2 L' R".split(" "))
        print(str(cube))
        self.assertEqual("R R O - B B G - G Y G", cube.get_face_as_str(BACK))
        self.assertEqual("O R B - W Y W - R O O", cube.get_face_as_str(BOTTOM))
        self.assertEqual("R B B - Y G W - Y G Y", cube.get_face_as_str(FRONT))
        self.assertEqual("W O Y - O O G - W G G", cube.get_face_as_str(LEFT))
        self.assertEqual("Y Y W - B R R - R R W", cube.get_face_as_str(RIGHT))
        self.assertEqual("B Y B - W W B - G O O", cube.get_face_as_str(TOP))

    def test_scramble2(self):
        cube = Cube()
        cube.execute("B2 R' B' L2 U2 B R2 F' L B' F L R2 B F' D2 R2 D' B2 F R2 B D2 B2 R' U2 F2 L' D2 R2".split(" "))
        print(str(cube))
        self.assertEqual("B B W - O B R - O W B", cube.get_face_as_str(BACK))
        self.assertEqual("W Y G - W Y G - R R G", cube.get_face_as_str(BOTTOM))
        self.assertEqual("O G G - B G R - O B R", cube.get_face_as_str(FRONT))
        self.assertEqual("B G Y - G O W - Y O G", cube.get_face_as_str(LEFT))
        self.assertEqual("R R R - B R Y - Y O Y", cube.get_face_as_str(RIGHT))
        self.assertEqual("O O W - W W Y - B Y W", cube.get_face_as_str(TOP))

    def test_info(self):
        cube = Cube()
        # scramble
        cube.execute("F B".split(" "))
        # algo
        cube.execute("B2 R'".split(" "))
        print(str(cube))
        self.assertEqual("F B".split(" "), cube.get_scramble())
        self.assertEqual("B2 R'".split(" "), cube.get_algorithm())
        self.assertEqual("B2 R'", cube.get_algorithm_str())


if __name__ == '__main__':
    unittest.main()
