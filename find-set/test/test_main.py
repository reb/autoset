import unittest
from main import is_set, find_set


class IsSet(unittest.TestCase):

    def test_correct_sets(self):
        self.assertTrue(is_set("1REW", "1RHW", "1RFW"))
        self.assertTrue(is_set("1REW", "2RHW", "3RFW"))
        self.assertTrue(is_set("1RED", "2RHW", "3RFP"))
        self.assertTrue(is_set("1RED", "2BHW", "3GFP"))

    def test_invalid_sets(self):
        self.assertFalse(is_set("2REW", "1RHW", "1RFW"))
        self.assertFalse(is_set("1REW", "2BHW", "3RFW"))
        self.assertFalse(is_set("1RFD", "2RHW", "3RFP"))
        self.assertFalse(is_set("1RED", "2BHW", "3BWP"))


class FindSet(unittest.TestCase):
    def test_correct_set(self):
        cards = [
            {'name': '1ED', 'bounding_box': [0.373840332, 0.728388488, 0.621475697, 0.892044723]},
            {'name': '1HD', 'bounding_box': [0.385559499, 0.440285, 0.633674562, 0.60816741]},
            {'name': '1FD', 'bounding_box': [0.343466312, 0.138860583, 0.589227438, 0.328077763]},
            {'name': '2ED', 'bounding_box': [0.373840332, 0.728388488, 0.621475697, 0.892044723]},
            {'name': '1HW', 'bounding_box': [0.385559499, 0.440285, 0.633674562, 0.60816741]},
            {'name': '3FW', 'bounding_box': [0.343466312, 0.138860583, 0.589227438, 0.328077763]},
        ]

        found_set = (
            {'name': '1ED', 'bounding_box': [0.373840332, 0.728388488, 0.621475697, 0.892044723]},
            {'name': '1HD', 'bounding_box': [0.385559499, 0.440285, 0.633674562, 0.60816741]},
            {'name': '1FD', 'bounding_box': [0.343466312, 0.138860583, 0.589227438, 0.328077763]},
        )
        self.assertEqual(find_set(cards), found_set)


if __name__ == '__main__':
    unittest.main()


