import unittest
from print import ShoppingList

class TestShoppingList(unittest.TestCase):
    def setUp(self) -> None:
        self.shopping_list = ShoppingList({"zhijin": 8, "maozi": 10})
    def test_get_item_count(self):
        self.assertEqual(self.shopping_list.get_item_count(),2)

    def test_get_total_count(self):
        self.assertEqual(self.shopping_list.get_total_price(),18)