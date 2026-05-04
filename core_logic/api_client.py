import requests
from config.keys import EDAMAM_APP_ID, EDAMAM_APP_KEY


def fetch_nutrition(food_query):
    """
    Connects to the Edamam API to retrieve nutritional information.
    Converts API-specific technical terms into clear, meaningful names.
    """
    # The API endpoint for food parsing
    api_url = "https://api.edamam.com/api/food-database/v2/parser"

    # Request parameters required by Edamam
    # 'ingr' stands for ingredient; it's the mandatory key for the search query
    query_params = {
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "ingr": food_query,  # ingr = ingredient
    }

    try:
        # Perform the HTTP GET request
        response = requests.get(api_url, params=query_params)

        # Check if the request was successful (Status 200)
        # It raises an exception for 4xx or 5xx HTTP errors
        response.raise_for_status()

        # Deserialize the JSON response into a Python dictionary
        api_data = response.json()

        # Data Extraction (Parsing)
        if api_data.get("parsed"):
            # Access the first matched food object
            raw_food_data = api_data["parsed"][0]["food"]
            nutrients = raw_food_data["nutrients"]

            # Return a cleaned dictionary with significant English names
            return {
                "name": raw_food_data.get("label"),
                "calories": nutrients.get("ENERC_KCAL", 0),
                "protein": nutrients.get("PROCNT", 0),
                "fat": nutrients.get("FAT", 0),
                "carbs": nutrients.get("CHOCDF", 0),
            }

        return None

    except requests.exceptions.RequestException as error:
        # Handle network-related errors (DNS, timeout, etc.)
        print(f"Network error during API communication: {error}")
        return None
