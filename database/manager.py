import sqlite3
import os

# Configuration constants: These define the location of the database and its blueprint.
DB_PATH = "health_tracker.db"
SCHEMA_PATH = "database/schema.sql"


def initialize_database():
    """
    Sets up the database by creating the file and the required tables.
    This is generally executed once to prepare the application environment.
    """
    # Verify that the instruction file (schema.sql) exists to avoid errors.
    if not os.path.exists(SCHEMA_PATH):
        print(f"Error: Required file {SCHEMA_PATH} not found.")
        return

    try:
        # Establish a connection to the database file.
        # SQLite creates the file automatically if it does not exist.
        with sqlite3.connect(DB_PATH) as connection:
            with open(SCHEMA_PATH, "r") as schema_file:
                # Executescript runs all the SQL commands found in the schema file.
                connection.executescript(schema_file.read())
            # Commit ensures all changes are saved permanently to the disk.
            connection.commit()
        print("Database created and initialized successfully.")
    except sqlite3.Error as error:
        print(f"An error occurred during database setup: {error}")


def register_user(name, goal_weight):
    """
    Saves a new user profile and returns the unique ID assigned by the database.
    This ID is necessary to link food entries to this specific person.
    """

    # The '?' placeholders prevent security issues by cleaning the user input.
    query = "INSERT INTO users (name, goal_weight) VALUES (?, ?)"

    try:
        # Open pipe to db
        with sqlite3.connect(DB_PATH) as connection:
            # The cursor is the tool used to send commands to the database engine.
            cursor = connection.cursor()
            # Execute the query by safely inserting the name and weight values.
            cursor.execute(query, (name, goal_weight))
            # Save or commit the change in the database
            connection.commit()

            # Retrieve the unique ID number that was automatically created for this user.
            return cursor.lastrowid
    except sqlite3.Error as error:
        print(f"An error occurred while registering the user: {error}")
        return None


def save_food_log(user_id, food_data):
    """
    Records a meal entry and connects it to a user using their unique ID.
    """
    query = """
        INSERT INTO food_logs (user_id, food_name, calories, protein)
        VALUES (?, ?, ?, ?)
    """

    try:
        with sqlite3.connect(DB_PATH) as connection:
            # Insert the user ID along with the nutritional data from the API.
            connection.execute(
                query,
                (
                    user_id,
                    food_data["name"],
                    food_data["calories"],
                    food_data["protein"],
                ),
            )
            connection.commit()
            print(f"Food entry logged: {food_data['name']}")
    except sqlite3.Error as error:
        print(f"An error occurred while saving the food entry: {error}")
