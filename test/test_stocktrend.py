import unittest, sys, os, json
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')
from stocktrend import getstockjson, getstockclosingprice, getstocktrend, getjsonreturn

class TestStockTrend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Setting up class')
        cls._symbol = 'MSFT'
        cls._apikey = 'demo'
        with open('testfile.json') as json_file:
            cls._testjson = json.load(json_file)
        cls._lastclose = 117.5200
        cls._computed_3_day_trend = -0.04
        cls._computed_4_day_trend = 1.39

    def test_getjsonreturn(self):
        result = getjsonreturn(TestStockTrend._lastclose, TestStockTrend._computed_3_day_trend)
        result = json.loads(result)
        self.assertEqual(result["lastclose"], TestStockTrend._lastclose)
        self.assertEqual(result["trend"], TestStockTrend._computed_3_day_trend)

    def test_getstocktrendDecrease(self):
        result = getstocktrend(TestStockTrend._testjson, 3)
        self.assertEqual(result, TestStockTrend._computed_3_day_trend)

    def test_getstocktrendIncrease(self):
        result = getstocktrend(TestStockTrend._testjson, 4)
        self.assertEqual(result, TestStockTrend._computed_4_day_trend)

    def test_getstockclosingprice(self):
        result = getstockclosingprice(TestStockTrend._testjson, 1)
        self.assertEqual(result, TestStockTrend._lastclose)

    def test_getstockjson(self):
        result = getstockjson(TestStockTrend._apikey, TestStockTrend._symbol)
        self.assertEqual(TestStockTrend._symbol, result["Meta Data"]["2. Symbol"])

    @classmethod
    def tearDownClass(cls):
        print('Tearing down class')

if __name__ == '__main__':
    unittest.main()