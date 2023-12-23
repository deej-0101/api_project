import unittest
import warnings
import json
from api import app

class MyAppTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()
        
    warnings.simplefilter("ignore", category=DeprecationWarning)
    
    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")
    
    def test_getwine(self):
        response = self.app.get("/wines")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("ut" in response.data.decode())
    
    def test_get_wine_by_id(self):
        response = self.app.get("/wines/3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("saepe" in response.data.decode())
        
    def test_top_10_wine(self):
        response = self.app.get("/wines/top_10_expensive_wine")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Bradtke" in response.data.decode())
        
    def test_food_with_wine(self):
        response = self.app.get("/wines/food_paired_with_wine")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("quia" in response.data.decode())
    
    def test_winemaker_and_country(self):
        response = self.app.get("/wines/winemaker_and_country")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Italy" in response.data.decode())
        
if __name__ == "__main__":
    unittest.main()