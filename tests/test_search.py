import unittest
from unittest.mock import patch
from meal_app import app
from flask import request,session
from dotenv import load_dotenv
import os
import datetime

class SearchPageTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the GET request for the search page
    def test_search_page_get(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search', response.data)
        self.assertIn(b'Find a meal plan that works for you', response.data)

    # Mock the API response and test the POST request for the search
    @patch('requests.get')
    def test_search_page_post(self, mock_get):
        # Mock successful API response
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

        # Data to send in the POST request
        form_data = {
            'searchbar': 'Chicken Parmesan',
            'mealtype': 'Dinner',
            'dishtype': 'Main Course',
            'maxIngredients': '5',
            'cuisinetype': 'Italian'
        }

        response = self.app.post('/search', data=form_data)

        # Checking the status code
        self.assertEqual(response.status_code, 200)

        # Verifying that the correct data is displayed in the response
        self.assertIn(b'Results for <b>Chicken Parmesan</b>', response.data)
        self.assertIn(b'Chicken Parmesan', response.data)
        self.assertIn(b'500 cal', response.data)
        self.assertIn(b'50g Protein', response.data)
        self.assertIn(b'https://example.com/chicken-parmesan', response.data)
        self.assertIn(b'Example Source', response.data)

    # Test the POST request for recipe_scaling route
    def test_recipe_scaling(self):
        form_data = {
            'ingredient': ['Chicken', 'Cheese'],
            'ingredient_selected_1': 'on',
            'amount_on_hand_1': '2.0',
            'amount_needed_1': '4.0',
            'ingredient_selected_2': 'on',
            'amount_on_hand_2': '1.5',
            'amount_needed_2': '3.0'
        }

        response = self.app.post('/recipe_scaling', data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Chicken', response.data)
        self.assertIn(b'Cheese', response.data)
        self.assertIn(b'"scaledAmount": 0.5', response.data)  # Checking scaled amount

    # Test the POST request for scale_recipe route
    def test_scale_recipe(self):
        form_data = {
            'ingredients[]': ['2 Chicken Breasts', '1 Cup Cheese', '1 Tbsp Oil']
        }

        response = self.app.post('/scale_recipe', data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Chicken Breasts', response.data)
        self.assertIn(b'2.0', response.data)  # Checking parsed amount
        self.assertIn(b'Cup Cheese', response.data)
        self.assertIn(b'Tbsp Oil', response.data)
    
    def test_calorie_tracking_get(self):
        with patch('meal_app.db.collection') as mock_db:
            # Mock a logged-in user and mock database fetch
            session['user'] = 'test_user@example.com'
            mock_user_ref = mock_db.return_value.document.return_value
            mock_user_ref.get.return_value.to_dict.return_value = {
                'daily_calorie_goal': 2000
            }
            mock_calorie_entries_ref = mock_user_ref.collection.return_value
            mock_calorie_entries_ref.stream.return_value = []

            response = self.app.get('/calorie_tracking')

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Calorie Tracker', response.data)
            self.assertIn(b'Daily Goal: 2000 calories', response.data)

    # Test the POST request for setting the daily calorie goal
    def test_set_daily_calorie_goal(self):
        form_data = {
            'calorie_goal': '2500'
        }
        with patch('meal_app.db.collection') as mock_db:
            # Mock logged-in user
            session['user'] = 'test_user@example.com'
            mock_user_ref = mock_db.return_value.document.return_value

            response = self.app.post('/daily_calorie_goal', data=form_data)

            # Check if the goal was updated
            mock_user_ref.update.assert_called_with({'daily_calorie_goal': 2500})
            self.assertEqual(response.status_code, 302)  # Redirects back to calorie tracking

    # Test the POST request for adding a calorie entry
    def test_add_calorie_entry(self):
        form_data = {
            'item_name': 'Apple',
            'calories': '95',
            'date': datetime.utcnow().strftime('%Y-%m-%d')
        }
        with patch('meal_app.db.collection') as mock_db:
            session['user'] = 'test_user@example.com'
            mock_user_ref = mock_db.return_value.document.return_value
            mock_calorie_entries_ref = mock_user_ref.collection.return_value

            response = self.app.post('/calorie_tracking', data=form_data)

            # Check if the entry was added
            mock_calorie_entries_ref.add.assert_called()
            self.assertEqual(response.status_code, 302)  # Redirect back to calorie tracking page
            self.assertIn(b'Entry added successfully!', response.data)

    # Test the POST request for deleting a calorie entry
    def test_delete_calorie_entry(self):
        entry_id = 'test_entry_id'
        form_data = {
            'entry_id': entry_id
        }
        with patch('meal_app.db.collection') as mock_db:
            session['user'] = 'test_user@example.com'
            mock_user_ref = mock_db.return_value.document.return_value
            mock_calorie_entries_ref = mock_user_ref.collection.return_value
            mock_entry_ref = mock_calorie_entries_ref.document.return_value

            response = self.app.post('/delete_entry', data=form_data)

            # Check if the delete method was called
            mock_entry_ref.delete.assert_called()
            self.assertEqual(response.status_code, 302)  # Redirect back to calorie tracking page

    # Test the POST request for the calorie tracking page when no entries exist
    def test_no_entries(self):
        with patch('meal_app.db.collection') as mock_db:
            session['user'] = 'test_user@example.com'
            mock_user_ref = mock_db.return_value.document.return_value
            mock_user_ref.get.return_value.to_dict.return_value = {
                'daily_calorie_goal': 2000
            }
            mock_calorie_entries_ref = mock_user_ref.collection.return_value
            mock_calorie_entries_ref.stream.return_value = []

            response = self.app.get('/calorie_tracking')

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'No entries yet. Add some!', response.data)

if __name__ == '__main__':
    unittest.main()