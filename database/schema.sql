-- Initial schema for Health Tracker App

CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY AUTOINCREMENT, 			-- Auto-incremented ID
	name TEXT NOT NULL,								-- NOT NULL: Avoid saving an user if they don't have a name
	goal_weight REAL,								-- REAL: Real number or with decimals
	start_date DATE DEFAULT CURRENT_DATE			-- DEFAULT CURRENT_DATE: Automatically assign the system date 
													-- by default if there are no registered date
); 

CREATE TABLE IF NOT EXISTS food_logs (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,						-- The FOREIGN KEY
	food_name TEXT NOT NULL,
	calories REAL NOT NULL,
	protein REAL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,	-- "When" it's eated
	FOREIGN KEY (user_id) REFERENCES users(id)		-- Field that directly points to the unique ID in the users 
													-- table (link the food with an user)
);