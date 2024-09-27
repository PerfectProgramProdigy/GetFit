# Function to check if the input is a positive integer
def check_pos_num(val):
    try:
        # Attempt to convert the input to an integer
        val = int(val)
    except ValueError:
        # If conversion fails (i.e., the input is not a valid integer), return None
        return None
    else:
        # If the conversion succeeds, check if the value is greater than 0
        if val > 0:
            return val  # Return the value if it's positive
        else:
            return None  # Return None if the value is 0 or negative

# Function to check if the date is in the correct format (DD-MM-YYYY)
def check_date(date):
    import datetime  # Import the datetime module to handle date formatting
    try:
        # Try to parse the input date string to ensure it follows the format 'DD-MM-YYYY'
        datetime.datetime.strptime(date, '%d-%m-%Y')
        return date  # Return the date if the format is correct
    except ValueError:
        # Return None if the date format is incorrect or invalid
        return None

# Function to check if a given input is empty
def check_empty(val):
    # If the input is empty or None, return None
    if not val:
        return None
    else:
        # Return the input value if it is not empty
        return val
