import tkinter as tk  # Importing the Tkinter library for creating graphical user interfaces (GUIs)
from tkinter import messagebox, ttk  # Importing specific modules from Tkinter for message boxes and themed widgets
import db, funcs, ttkthemes  # Importing custom database functions (db), helper functions (funcs), and the 'ttkthemes' module for theming the GUI
import matplotlib.pyplot as plt  # Importing the 'matplotlib' library for generating plots and charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Allows embedding Matplotlib figures in Tkinter canvas


# Create the main application window with a themed appearance
window = ttkthemes.ThemedTk(theme='radiance')  # Initialize the main window using the 'radiance' theme

# Set the title of the window to "GetFit App"
window.title('GetFit App')

# Define the size of the window (500x500 pixels)
window.geometry('500x500')

# Set the background color of the window to a light peach color
window.configure(bg='#FCEED2')

# Set the application icon using a .ico file located at the specified path
window.iconbitmap("icon.ico")

# Create a label for entering the user's name, styled with a specific font and color
name_label = ttk.Label(window, text='Enter your name: ', font=('Bahnschrift', 16), background='#FCEED2', foreground='black')
name_label.pack(pady=10)  # Add the label to the window with padding on the y-axis

# Create an entry widget for the user to input their name, styled with a specific font size
name_entry = tk.Entry(window, font=('Arial', 13))
name_entry.pack(pady=5, ipadx=10, ipady=5)  # Add the entry widget to the window with padding on the y-axis


def submit_name():
    # Retrieve and strip any leading or trailing whitespace from the name entered by the user
    name = name_entry.get().strip()

    # Check if the name is empty using a helper function from the 'funcs' module
    if funcs.check_empty(name) is None:
        # Show an error message if the name is empty
        messagebox.showerror('Error', 'Name cannot be empty!')
        return  # Exit the function early to prevent further processing

    # Check if the user already exists in the database using a function from the 'db' module
    if db.check_user(name):
        # Show a welcome message if the user is already registered
        messagebox.showinfo('Welcome!', f"Welcome back {name}!")
    else:
        # Register the new user in the database if they are not already registered
        db.user_registration(name)
        # Show a success message confirming registration
        messagebox.showinfo('Registration', f'User {name} registered successfully!')

    # Open the home screen for the user after registration or login
    open_home(name)

    # Hide the initial window to transition to the home screen
    window.withdraw()  # Close the initial window


def delete_workout(user_name):
    # Create a new top-level window for deleting a workout
    delete_window = tk.Toplevel(home_screen)  # This window is a child of the main home screen
    delete_window.title("Delete Workout")  # Set the title of the delete window
    delete_window.geometry("500x500")  # Set the dimensions of the window
    delete_window.iconbitmap("icon.ico")  # Set the window icon
    delete_window.configure(bg='#FCEED2')  # Set the background color of the window

    # Create and pack a label prompting the user to enter the date of the workout to be deleted
    date_label = ttk.Label(delete_window, foreground='black', text="Enter date of the workout to be deleted (DD-MM-YYYY):", background='#FCEED2')
    date_label.pack(pady=10)  # Add vertical padding for spacing

    # Create an entry widget for the user to input the date of the workout
    date_entry = tk.Entry(delete_window, font=('Arial', 13))  # Increased font size for better readability
    date_entry.pack(pady=5, ipadx=10, ipady=5)  # Add padding for aesthetics and make the entry field larger

    # Create a button that triggers the delete confirmation process when clicked
    delete_button = ttk.Button(delete_window, text="Delete", command=lambda: confirm_delete(user_name, date_entry.get(), delete_window))
    delete_button.pack(pady=10)  # Add padding for aesthetics

    # Create a button to cancel the delete operation and close the delete window
    close_button = ttk.Button(delete_window, text="Cancel", command=delete_window.destroy)
    close_button.pack(pady=5)  # Add padding for aesthetics


def confirm_delete(user_name, date, delete_window):
    # Check if the date entered is in the correct format
    if funcs.check_date(date) is None:
        messagebox.showerror("Error",
                             "Invalid date format! Please use YYYY-MM-DD.")  # Show error if format is incorrect
        return  # Exit the function if the date format is invalid

    # Retrieve the user ID associated with the given username
    user_id = db.get_user_id(user_name)
    if user_id is None:
        messagebox.showerror("Error", "User not found!")  # Show error if the user ID could not be found
        return  # Exit the function if the user is not found

    # Call the database function to delete the workout for the specified user and date
    db.del_workout(user_id, date)

    # Show a success message indicating the workouts have been deleted
    messagebox.showinfo("Success", f"Workouts on {date} deleted successfully!")

    # Close the delete window after the operation
    delete_window.destroy()

    # Re-show the home screen window, allowing the user to continue using the app
    home_screen.deiconify()


def log_workout(user_id):
    global log_window  # Declare log_window as a global variable to access it outside this function
    log_window = tk.Toplevel(home_screen)  # Create a new top-level window for logging workouts
    log_window.title("Log Workout")  # Set the title of the log window
    log_window.geometry("500x500")  # Define the dimensions of the log window
    log_window.iconbitmap("icon.ico")  # Set the window icon

    # Set background color for log window to a light peach
    log_window.configure(bg='#FCEED2')

    # Create a label and entry for entering the exercise name
    exercise_label = ttk.Label(log_window, text="Enter Exercise Name:", background='#FCEED2', foreground='black')
    exercise_label.grid(row=0, column=0, padx=20, pady=5, sticky="ew")  # Position the label in the grid
    exercise_entry = tk.Entry(log_window, font=('Arial', 13))  # Entry field for exercise name with larger font
    exercise_entry.grid(row=0, column=1, padx=20, pady=5, ipadx=10, ipady=5, sticky="ew")  # Position the entry field

    # Create a label and entry for entering the date of the workout
    date_label = ttk.Label(log_window, text="Enter Date (DD-MM-YYYY):", background='#FCEED2', foreground='black')
    date_label.grid(row=1, column=0, padx=20, pady=5, sticky="ew")  # Position the label in the grid
    date_entry = tk.Entry(log_window, font=('Arial', 13))  # Entry field for date with larger font
    date_entry.grid(row=1, column=1, padx=20, pady=5, ipadx=10, ipady=5, sticky="ew")  # Position the entry field

    # Create a label and entry for entering the duration of the workout
    duration_label = ttk.Label(log_window, text="Enter Duration (minutes):", background='#FCEED2', foreground='black')
    duration_label.grid(row=2, column=0, padx=20, pady=5, sticky="ew")  # Position the label in the grid
    duration_entry = tk.Entry(log_window, font=('Arial', 13))  # Entry field for duration with larger font
    duration_entry.grid(row=2, column=1, padx=20, pady=5, ipadx=10, ipady=5, sticky="ew")  # Position the entry field

    # Create a label and entry for entering the calories burned during the workout
    calories_label = ttk.Label(log_window, text="Enter Calories Burned:", background='#FCEED2', foreground='black')
    calories_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")  # Position the label in the grid
    calories_entry = tk.Entry(log_window, font=('Arial', 13))  # Entry field for calories with larger font
    calories_entry.grid(row=3, column=1, padx=20, pady=5, ipadx=10, ipady=5, sticky="ew")  # Position the entry field

    # Create a submit button that triggers the confirm_log function when clicked
    submit_button = ttk.Button(log_window, text="Submit", command=lambda: confirm_log(user_id, exercise_entry.get(), date_entry.get(), duration_entry.get(), calories_entry.get(), log_window))
    submit_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")  # Position the button in the grid

    # Create a cancel button that closes the log window when clicked
    cancel_button = ttk.Button(log_window, text="Cancel", command=log_window.destroy)
    cancel_button.grid(row=4, column=1, padx=20, pady=10, sticky="ew")  # Position the button in the grid


def confirm_log(user_id, exercise, date, duration, calories, log_window):
    # Check if the exercise name is empty
    if funcs.check_empty(exercise) is None:
        messagebox.showerror("Error", "Please enter valid details!")  # Show an error message if empty
        return  # Exit the function if validation fails

    # Validate the date format
    if funcs.check_date(date) is None:
        messagebox.showerror("Error", "Please enter date in DD-MM-YYYY format")  # Show an error message for invalid date
        return  # Exit the function if validation fails

    # Check if duration and calories are positive numbers
    duration = funcs.check_pos_num(duration)
    calories = funcs.check_pos_num(calories)

    # If either duration or calories is invalid (None), show an error
    if duration is None or calories is None:
        messagebox.showerror("Error", "Please enter valid numerical values for duration and calories!")  # Show error message
        return  # Exit the function if validation fails

    # Log the workout in the database using the provided details
    db.log_workout(user_id, exercise, date, duration, calories)

    messagebox.showinfo("Success", "Workout logged successfully!")  # Show success message to the user
    log_window.destroy()  # Close the log window after logging the workout


def open_home(name):
    # Create a new window (home screen) for the user after logging in or registering
    global home_screen  # Make home_screen a global variable to access in other functions
    home_screen = tk.Toplevel(window)  # Create a new top-level window (separate from the main one)
    home_screen.title(f"{name}'s home")  # Set the title of the home screen with the user's name
    home_screen.geometry('500x500')  # Set the window size
    home_screen.resizable(True, True)  # Allow the user to resize the window
    home_screen.configure(bg='#FCEED2')  # Set the background color to match the app theme
    home_screen.iconbitmap("icon.ico")  # Set a custom window icon

    # Display a welcome message with the user's name
    welcome = ttk.Label(home_screen, text=f'Welcome {name}!', font=('Arial', 18), background='#FCEED2', foreground='black')
    welcome.pack(pady=20)  # Position the label with padding for better spacing

    # Get the user's ID from the database, which will be used for various operations
    user_id = db.get_user_id(name)

    # Button to log a new workout, passing the user ID to the log_workout function
    log_button = ttk.Button(home_screen, text='Log Workout', command=lambda: log_workout(user_id))
    log_button.pack(pady=10)  # Add padding around the button for better UI spacing

    # Button to delete a workout, passing the user's name to the delete_workout function
    del_button = ttk.Button(home_screen, text='Delete Workout', command=lambda: delete_workout(name))
    del_button.pack(pady=10)  # Add padding around the button for better UI spacing

    # Button to view statistics of logged workouts, passing the user ID to the view_stats function
    view_button = ttk.Button(home_screen, text='View Stats', command=lambda: view_stats(user_id))
    view_button.pack(pady=10)  # Add padding around the button for better UI spacing

    # Button to view a graphical analysis of workouts, passing the user ID to the view_analysis function
    analysis_button = ttk.Button(home_screen, text='Graphical Analysis', command=lambda: view_analysis(user_id))
    analysis_button.pack(pady=10)  # Add padding around the button for better UI spacing

    # Button to log out of the app, calling the logout function to return to the login screen or close the app
    logout_button = ttk.Button(home_screen, text='Log Out', command=lambda: logout())
    logout_button.pack(pady=10)  # Add padding around the button for better UI spacing


def logout():
    # Restore the initial login/registration window by showing it again
    window.deiconify()  # Re-display the main window (hidden during user navigation to home)

    # Close the current home screen window to prevent duplicate windows
    home_screen.destroy()  # This removes the user's home screen window


def view_analysis(user_id):
    # Retrieve all workout data for the given user
    workout_data = db.get_workout_data(user_id)

    # Check if workout data is available, show error if none exists
    if not workout_data:
        messagebox.showerror("Error", "No workout data found!")
        return

    # Process the workout data to calculate total calories burned per day
    calories_per_day = {}
    for exercise, date, duration, calories in workout_data:
        # Accumulate calories for each date, creating a dictionary
        if date not in calories_per_day:
            calories_per_day[date] = 0
        calories_per_day[date] += calories

    # Sort dates and get total calories burned for each date
    dates = sorted(calories_per_day.keys())
    total_calories_per_day = [calories_per_day[date] for date in dates]

    # Create a new window for displaying the analysis
    analysis_window = tk.Toplevel(home_screen)
    analysis_window.title("Graphical Analysis")
    analysis_window.geometry("600x600")
    analysis_window.resizable(True, True)
    analysis_window.configure(bg='#FCEED2')
    analysis_window.iconbitmap("icon.ico")

    # Create a scrollable frame to hold the graphs
    scrollable_frame = tk.Frame(analysis_window)
    scrollable_frame.pack(fill=tk.BOTH, expand=True)

    # Set up a canvas and scrollbar for scrolling through the graphs
    canvas = tk.Canvas(scrollable_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = tk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas for holding the graph widgets
    graph_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=graph_frame, anchor='nw')

    # First Graph: Line plot for calories burned per day
    line_canvas = FigureCanvasTkAgg(plt.Figure(), master=graph_frame)
    line_canvas.get_tk_widget().pack(pady=5)

    # Plotting the line graph showing calories burned on each date
    line_ax = line_canvas.figure.add_subplot(211)
    line_ax.plot(dates, total_calories_per_day, marker='o', color='orange')
    line_ax.set_title('Calories Burned Per Day')
    line_ax.set_xlabel('Date')
    line_ax.set_ylabel('Calories')
    line_ax.tick_params(axis='x', rotation=25)  # Rotate date labels for clarity

    # Second Graph: Bar chart for average calories burned per exercise
    bar_canvas = FigureCanvasTkAgg(plt.Figure(), master=graph_frame)
    bar_canvas.get_tk_widget().pack(pady=5)

    # Calculate the average calories burned for each exercise type
    avg_calories_per_exercise = {}
    for exercise, _, _, calories in workout_data:
        if exercise not in avg_calories_per_exercise:
            avg_calories_per_exercise[exercise] = []
        avg_calories_per_exercise[exercise].append(calories)

    exercises = list(avg_calories_per_exercise.keys())
    avg_calories = [sum(calories) / len(calories) for calories in avg_calories_per_exercise.values()]

    # Plotting the bar chart showing average calories burned for each exercise
    bar_ax = bar_canvas.figure.add_subplot(212)
    bar_ax.bar(exercises, avg_calories, color='orange')
    bar_ax.set_title('Average Calories Burned Per Exercise')
    bar_ax.set_xlabel('Exercise')
    bar_ax.set_ylabel('Average Calories')
    bar_ax.tick_params(axis='x', rotation=25)  # Rotate exercise names for clarity

    # Render the graphs on the canvas
    line_canvas.draw()
    bar_canvas.draw()

    # Update the scrollable region to fit the full graph content
    graph_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


def view_stats(user_id):
    # Create a new window for displaying the workout stats
    stats_window = tk.Toplevel(home_screen)
    stats_window.title("Workout Stats")
    stats_window.geometry("500x500")
    stats_window.resizable(True, True)
    stats_window.configure(bg='#FCEED2')  # Set background color
    stats_window.iconbitmap("icon.ico")  # Set the window icon

    # Retrieve stats from the database (total workouts, average duration, and average calories)
    total_workouts, avg_duration, avg_calories = db.get_avg_stats(user_id)

    # Display total workouts in a label
    total_workouts_label = ttk.Label(stats_window, foreground='black', text=f"Total Workouts: {total_workouts}", background='#FCEED2')
    total_workouts_label.pack(pady=5)

    # Display average workout duration in a label, formatted to two decimal places
    avg_duration_label = ttk.Label(stats_window, foreground='black', text=f"Average Workout Duration: {avg_duration:.2f} minutes", background='#FCEED2')
    avg_duration_label.pack(pady=5)

    # Display average calories burned per workout in a label, formatted to two decimal places
    avg_calories_label = ttk.Label(stats_window, foreground='black', text=f"Average Calories Burned: {avg_calories:.2f}", background='#FCEED2')
    avg_calories_label.pack(pady=5)

    # Button to close the stats window
    close_button = ttk.Button(stats_window, text="Close", command=stats_window.destroy)
    close_button.pack(pady=10)


# Create a 'submit' button widget in the window
submit_button = ttk.Button(window, text='Submit', command=submit_name)

# Add the button to the window and apply padding of 20 pixels on the Y-axis
submit_button.pack(pady=20)

# Starts the main event loop, which keeps the window active and responsive
window.mainloop()
