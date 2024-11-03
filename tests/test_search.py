import unittest
from unittest.mock import patch
from meal_app import app
from dotenv import load_dotenv
import os

class SearchPageTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    #Test the GET request for the search page
    def test_search_page_get(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search', response.data)
        self.assertIn(b'Find a meal plan that works for you', response.data)
    
    #Mock the API response and test the POST request for the search
    @patch('requests.get')
    def test_search_page_post(self, mock_get):
        #Mock successful API response
        mock_data = {
            "hits": [
                {
                    "recipe": {
                        "label": "Chicken Parmesan",
                        "calories": 500,
                        "yield": 4,
                        "ingredientLines": ["Chicken", "Cheese", "Tomato Sauce"],
                        "url": "https://example.com/chicken-parmesan",
                        "source": "Example Source",
                        "totalNutrients": {
                            "PROCNT": {"quantity": 50, "unit": "g"}
                        }
                    }
                }
            ]
        }

        mock_get.return_value.json.return_value = mock_data

        #Data to send in the POST request
        form_data = {
            'searchbar': 'Chicken Parmesan',
            'mealtype': 'Dinner',
            'dishtype': 'Main Course',
            'maxIngredients': '5',
            'cuisinetype': 'Italian'
        }

        response = self.app.post('/search', data=form_data)

        #Checking the status code
        self.assertEqual(response.status_code, 200)

        #Verifying that the correct data is displayed in the response
        self.assertIn(b'Results for <b>Chicken Parmesan</b>', response.data)
        self.assertIn(b'Chicken Parmesan', response.data)
        self.assertIn(b'500 cal', response.data)
        self.assertIn(b'50g Protein', response.data)
        self.assertIn(b'https://example.com/chicken-parmesan', response.data)
        self.assertIn(b'Example Source', response.data)


if __name__ == '__main__':
    unittest.main()
