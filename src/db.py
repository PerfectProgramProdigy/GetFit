import sqlite3 as sql

# Function to connect to the SQLite database (GetFit.db)
def connect_db():
    return sql.connect("GetFit.db")

# Function to create the necessary tables if they don't already exist
def create_tables():
    con = connect_db()  # Connect to the database
    c = con.cursor()    # Create a cursor to execute SQL commands
    # Create the 'users' table to store user information
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL)""")  # Username cannot be null
    # Create the 'workouts' table to store workout data
    c.execute("""CREATE TABLE IF NOT EXISTS workouts(
        workoutId integer PRIMARY KEY AUTOINCREMENT,
        user_id integer,
        exercise text NOT NULL,
        date text,
        duration integer,
        calories integer,
        FOREIGN KEY(user_id) REFERENCES users(user_id))""")  # Links to 'users' table
    con.commit()  # Save the changes
    con.close()   # Close the database connection

# Function to check if a user with the given name already exists in the database
def check_user(name):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Query to find if the username exists
    c.execute("SELECT name FROM users WHERE name = ?", (name,))
    result = c.fetchone()  # Fetch the first matching record
    con.close()  # Close the database connection
    # Return True if the user is found, else return None
    return True if result is not None else None

# Function to register a new user in the 'users' table and return their unique user ID
def user_registration(name):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Insert a new user record with the given name
    c.execute("INSERT INTO users (name) VALUES (?)", (name,))
    con.commit()  # Save the changes
    user_id = c.lastrowid  # Get the auto-generated user ID for the new record
    return user_id  # Return the user ID to the calling function

# Function to log a workout in the 'workouts' table for the specified user
def log_workout(user_id, exercise, date, duration, calories):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Insert a new workout record with the provided details
    c.execute("""INSERT INTO workouts (user_id, exercise, date, duration, calories)
                 VALUES (?, ?, ?, ?, ?)""",
                 (user_id, exercise, date, duration, calories))
    con.commit()  # Save the changes
    con.close()   # Close the database connection

# Function to delete workouts for a specific user on a given date
def del_workout(user_id, date):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Delete workout(s) matching the user ID and date
    c.execute("DELETE FROM workouts WHERE user_id = ? and date = ?", (user_id, date,))
    con.commit()  # Save the changes
    con.close()   # Close the database connection

# Function to retrieve the user ID based on their name
def get_user_id(name):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Query to get the user ID associated with the given name
    c.execute("SELECT user_id FROM users WHERE name = ?", (name,))
    result = c.fetchone()  # Fetch the result
    con.close()  # Close the database connection
    # Return the user ID if found, else return None
    if result:
        return result[0]
    else:
        return None

# Function to retrieve workout stats (total workouts, average duration, average calories) for a specific user
def get_avg_stats(user_id):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Query to count total workouts, and calculate average duration and calories for the user
    c.execute("""SELECT COUNT(*), AVG(duration), AVG(calories) 
                  FROM workouts 
                  WHERE user_id = ?""", (user_id,))
    stats = c.fetchone()  # Fetch the stats from the result
    con.close()  # Close the database connection

    # Assign default values if no workouts are found (handle None values)
    total_workouts = stats[0] if stats[0] is not None else 0
    avg_duration = stats[1] if stats[1] is not None else 0
    avg_calories = stats[2] if stats[2] is not None else 0

    return total_workouts, avg_duration, avg_calories  # Return the calculated stats

# Function to get all workout data (exercise, date, duration, calories) for a specific user
def get_workout_data(user_id):
    con = connect_db()  # Connect to the database
    c = con.cursor()
    # Query to fetch all workout details for the user
    c.execute("SELECT exercise, date, duration, calories FROM workouts WHERE user_id = ?", (user_id,))
    workout_data = c.fetchall()  # Fetch all matching records
    con.close()  # Close the database connection
    return workout_data  # Return the workout data

# Call the function to create tables when the program starts
create_tables()
