import unittest
from budget_alert_gate import evaluate

def rule(kind='ACTUAL',mode='PERCENTAGE',threshold=80):
    return {'name':'r','type':kind,'threshold_type':mode,'threshold':threshold}
class GateTests(unittest.TestCase):
    def test_below(self): self.assertFalse(evaluate(100,79,0,[rule()])[0]['triggered'])
    def test_equal(self): self.assertTrue(evaluate(100,80,0,[rule()])[0]['triggered'])
    def test_above(self): self.assertTrue(evaluate(100,81,0,[rule()])[0]['triggered'])
    def test_forecast(self): self.assertTrue(evaluate(100,0,120,[rule('FORECAST')])[0]['triggered'])
    def test_absolute(self): self.assertTrue(evaluate(1000,80,0,[rule(mode='ABSOLUTE')])[0]['triggered'])
    def test_percent_scaled(self): self.assertFalse(evaluate(200,150,0,[rule()])[0]['triggered'])
    def test_decimal(self): self.assertTrue(evaluate('1','0.8',0,[rule()])[0]['triggered'])
    def test_zero_budget(self):
        with self.assertRaises(ValueError): evaluate(0,0,0,[])
    def test_bad_amounts(self):
        for bad in [-1,'bad','NaN','Infinity']:
            with self.subTest(bad=bad), self.assertRaises(ValueError): evaluate(100,bad,0,[])
    def test_bad_mode(self):
        with self.assertRaises(ValueError): evaluate(100,0,0,[rule(mode='bad')])
    def test_empty(self): self.assertEqual(evaluate(100,0,0,[]),[])
