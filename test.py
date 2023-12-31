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
        
    def test_add_winemaker(self):
        data = {"country_code": "US", "winemaker_name": "test wine"}
        response = self.app.post('/wines', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("winemaker added successfully" in response.data.decode())
        
    def test_update_winemaker(self):
        data = {"country_code": "US", "winemaker_name": "test wine"}
        response = self.app.put('/wines/7', data=json.dumps(data), headers = {'Content-Type':'application/json'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("winemaker updated successfully" in response.data.decode())
        
    def test_delete_winemaker(self):
        response = self.app.delete('/wines/7')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("winemaker deleted successfully" in response.data.decode())
        
    def test_winemaker_search(self): 
        response = self.app.get("/wines/search?search_term=Bartell")
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Bartell" in response.data.decode())
        
        
        
if __name__ == "__main__":
    unittest.main()