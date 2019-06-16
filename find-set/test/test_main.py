import unittest
from function.main import is_set


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


if __name__ == '__main__':
    unittest.main()


