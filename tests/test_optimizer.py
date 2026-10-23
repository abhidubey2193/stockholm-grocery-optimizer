import unittest
from optimizer import Price, best_basket

class BasketTests(unittest.TestCase):
    def setUp(self):
        self.prices = [Price("A", "milk", 10), Price("B", "milk", 9),
                       Price("A", "bread", 10), Price("B", "bread", 12)]
    def test_penalty_prefers_one_store(self):
        self.assertEqual(best_basket(["milk", "bread"], self.prices, 15)["stores"], ["A"])
    def test_zero_penalty(self):
        self.assertEqual(best_basket(["milk", "bread"], self.prices, 0)["total_sek"], 19)
    def test_missing_product(self):
        with self.assertRaises(ValueError):
            best_basket(["eggs"], self.prices)
    def test_invalid_prices(self):
        for value in (-1, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                best_basket(["milk"], [Price("A", "milk", value)])
    def test_invalid_penalty(self):
        for value in (-1, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                best_basket(["milk"], self.prices, value)

if __name__ == "__main__":
    unittest.main()
