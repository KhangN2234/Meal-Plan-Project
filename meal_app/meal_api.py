import requests

def fetch_meals_by_category(category):
    base_url = "https://www.themealdb.com/api/json/v1/1/filter.php"
    try:
        response = requests.get(base_url, params={"c": category})
        response.raise_for_status()  
        data = response.json()
        
        return data.get("meals", [])
    except requests.RequestException as e:
        print(f"Error fetching meals for category {category}: {e}")
        return []
