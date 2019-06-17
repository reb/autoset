import unittest
from function.colour_detector import transform_point, identify
from os import listdir
from os.path import isfile, join


def p(x, y):
    point = lambda: None
    point.x = x
    point.y = y
    return point


class ColourDetector(unittest.TestCase):

    def test_transform_point(self):
        self.assertEqual(transform_point(p(0, 0), 10, 10), (0, 0))
        self.assertEqual(transform_point(p(1, 1), 10, 10), (10, 10))
        self.assertEqual(transform_point(p(0.5, 0.1), 10, 10), (5, 1))

    def test_identify(self):
        for file_name in listdir('test/images'):
            file = join('test/images', file_name)
            if isfile(file):
                expected_colour = file_name[1]
                with self.subTest(msg="Checking if image is colour", image=file, colour=expected_colour):
                    with open(file, 'rb') as image_file:
                        image_data = image_file.read()
                        self.assertEqual(identify(image_data, [p(0, 0), p(1, 1)]), expected_colour)


if __name__ == '__main__':
    unittest.main()
