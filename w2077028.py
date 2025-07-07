#  Additional info
#  1. I declare that my work contins no examples of misconduct, such as
#  plagiarism, or collusion.
#  2. Any code taken from other sources is referenced within my code solution.
#  3. Student ID: W2077028
#  4. Date: 21/11/2024


from graphics import *
import csv
import math

# Asking if the user is an employee, only giving the options of yes or no. If, Elif and Else is used for the two options, and defult try again.
def check_if_employee():
    while True:
        employee_status = input('Are you an employee? (Y/N): ').lower()
        if employee_status in ['y', 'yes']:
            return True
        elif employee_status in ['n', 'no']:
            return False
        else:
            print('Invalid input. Please answer with "Y", "YES", "N", or "NO".')

# Function to validate the date inputs 
def get_valid_date(): # Using def to define the keyword so that i can reuse this later in the code if needed.
    while True: # Using the while functions makes it so if the user makes a mistake while tuping, they can rewrite without starting the program again.
        try: # Using the try function so that if the user inputs an invalid number, they will get the valueerror message. This stops the program from crashing.
           
            # Asking for the day
            date_day_input = input('Enter the day of the survey in the format DD:  ')
            if date_day_input.lower() == 'n':
                print('Exiting the program.')
                exit()  # Quit the program if 'n' is typed, gives the user control over the program.

            date_day = int(date_day_input)
            if not (1 <= date_day <= 31): # If the input isnt between these numbers, triggers the valueerror.
                raise ValueError('Out of range. Day must be between 1 and 31.')

            # Asking for the month
            date_month_input = input('Enter the month of the survey in the format MM:  ')
            if date_month_input.lower() == 'n':
                print('Exiting the program.')
                exit()  # Quit the program if 'n' is typed

            date_month = int(date_month_input)
            if not (1 <= date_month <= 12):
                raise ValueError('Out of range. Month must be between 1 and 12.')

            # Asking for the year
            date_year_input = input('Enter the year of the survey in the format YYYY, within the range of 2000 and 2024:  ')
            if date_year_input.lower() == 'n':
                print('Exiting the program.')
                exit()  # Quit the program if 'n' is typed

            date_year = int(date_year_input)
            if not (2000 <= date_year <= 2024):
                raise ValueError('Out of range. Year must be between 2000 and 2024.')

            return date_day, date_month, date_year # Allows the code to access the validated date.

        except ValueError as e:
            print(f'This is an invalid input: {e}. Please try again.') 

# Function to process the CSV data
def process_data():
    data_list = []  # List to hold data
    junction_data = {'Elm Avenue/Rabbit Road': [0] * 24, 'Hanley Highway/Westway': [0] * 24}  # Dictionary to store traffic by hour for each junction

    # Get valid date inputs
    date_day, date_month, date_year = get_valid_date()

    formatted_date = f'{date_day:02}{date_month:02}{date_year:04}'  # Format as DDMMYYYY
    print(f'Formatted date: {formatted_date}')

    # Construct the filename
    file_name = f'traffic_data{formatted_date}.csv'
    print(f'Trying to find file: {file_name}')


    # Checks to see if the file exists
    try:
        with open(file_name, 'r') as file:
            print(f'File {file_name} found!')
            csvreader = csv.reader(file)
            header = next(csvreader)  # Skip the header

            # Providing the variables a starting value.
            row_amount = 0
            truck_amount = 0
            two_wheeled_amount = 0
            bus_amount = 0
            bus_north = 0
            vehicle_no_turn = 0
            above_speed_limit = 0
            vehicle_Elms = 0
            vehicle_Hanley = 0
            bike_amount = 0
            scooter_amount = 0
            hourly_pass = [0] * 24
            rain_hours = set()
            total_rainy_hours = 0  


            for row in csvreader:
                data_list.append(row)
                row_amount += 1

                try:
                    timestamp = str(row[2])
                    hour = int(timestamp.split(':')[0])  # Extract the hour from the timestamp
                    # Adds traffic count for each junction
                    if 'elm avenue/rabbit road' in str(row[0]).lower():
                        junction_data['Elm Avenue/Rabbit Road'][hour] += 1
                    elif 'hanley highway/westway' in str(row[0]).lower():
                        junction_data['Hanley Highway/Westway'][hour] += 1
                except (ValueError, IndexError):
                    print(f'Ignoring the invalid or missing timestamp in Row: {row}')


                # Process specific vehicle types and conditions
                if len(row) > 9 and 'truck' in str(row[8]).lower(): #checks the number of elements in the row. Treating the numberas a string ensures no errors if the value isnt a string.
                    truck_amount += 1 # Adds 1 to the starting value everytime the keyword is found.

                if len(row) > 9 and 'bicycle' in str(row[8]).lower():
                    bike_amount += 1

                if len(row) > 9 and any(keyword in str(row[8]).lower() for keyword in ['bicycle', 'motorcycle', 'scooter']):
                    two_wheeled_amount += 1

                if len(row) > 9 and 'elm avenue/rabbit road' in str(row[0]).lower() and 'n' in str(row[4]).lower() and 'bus' in str(row[8]).lower():
                    bus_north += 1

                if len(row) > 9 and str(row[3]).lower() == str(row[4]).lower():
                    vehicle_no_turn += 1

                if row[7] > row[6]: # If row 7s value is bigger than row 6, they would be above the speed limit.
                    above_speed_limit += 1

                if len(row) > 9 and 'elm avenue/rabbit road' in str(row[0]).lower():
                    vehicle_Elms += 1

                if len(row) > 9 and 'hanley highway/westway' in str(row[0]).lower():
                    vehicle_Hanley += 1

                if len(row) > 9 and 'elm avenue/rabbit road' in str(row[0]).lower() and 'scooter' in str(row[8]).lower():
                    scooter_amount += 1

                try:
                    timestamp = str(row[2])
                    hour = int(timestamp.split(':')[0])  # Extracts the hour from the timestamp
                    hourly_pass[hour] += 1
                except (ValueError, IndexError):
                    print(f'Ignoring any invalid or missing timestamp in Row: {row}')

                # Check for rain data
                if len(row) > 6 and 'rain' in str(row[5]).lower():  # Assuming column 5 is Weather_Conditions
                    hour = row[2].split(':')[0]  # Extract the hour from timeOfDay
                    rain_hours.add(hour)  # Add the hour to the set
                    total_rainy_hours = len(rain_hours)  # Update the total rainy hours

        maximum_passed = max(hourly_pass) # Determins the highest value.
        peak_time = [
                f'Between {hour:02}:00 and {hour+1:02}:00'
                for hour, count in enumerate(hourly_pass) #Link 2
                if count == maximum_passed 
            ]

        vehicles_in_peak = sum(hourly_pass[hour] for hour, count in enumerate(hourly_pass) if count == maximum_passed) # Keeps no.of vehicles and hours in mind while only using te vehicles from the peak.

            # Calculating the percentages
        if truck_amount > 0:
                percentage_of_trucks = (truck_amount / row_amount) * 100
                percentage_rounded_trucks = math.ceil(percentage_of_trucks)

        if bike_amount > 0:
                percentage_of_bikes = (bike_amount / row_amount) * 100
                percentage_rounded_bikes = math.ceil(percentage_of_bikes)
                bikes_hourly = (bike_amount / 24)  # Number of hours per day is unchangeable
                actual_hourly = math.ceil(bikes_hourly)

        if row_amount > 0:
                percentage_of_scooters = (scooter_amount / row_amount) * 100
                percentage_rounded_scooters = math.ceil(percentage_of_scooters)
        else:
                percentage_rounded_scooters = 0

        # Displays the results to the user
        print('Data loaded successfully.')
        print(f'The name of the file selected: {file_name}')
        print(f'The total number of vehicles passing through all junctions is: {row_amount}')
        print(f'The total number of trucks passing through all junctions is: {truck_amount}')
        print(f'The total number of two wheeled vehicles passing through all junctions is: {two_wheeled_amount}')
        print(f'The total number of busses leaving Elm Avenue/Rabbit Road Junction heading North is: {bus_north}')
        print(f'The total number of vehicles passing through all junctions without turning is: {vehicle_no_turn}')
        print(f'The percentage of trucks passing through all junctions is: {percentage_rounded_trucks}')
        print(f'The average number of bicycles per hour passing through all junctions is: {actual_hourly}, as there are {bike_amount} bikes in total passing on this date.')
        print(f'The total number of vehicles recorded as over the speed limit is: {above_speed_limit}')
        print(f'The total number of vehicles recorded over Elm Avenue/Rabbit Road Junction is: {vehicle_Elms}')
        print(f'The total number of vehicles recorded over Hanley Highway/Westway Junction is: {vehicle_Hanley}')
        print(f'The percentage of scooters recorded over Elm Avenue/Rabbit Road Junction is: {percentage_rounded_scooters}')
        print(f'The peak hour for vehicles recorded over Hanley Highway/Westway Junction is: {', '.join(peak_time)}')
        print(f'The number of vehicles recorded in the peak hour(s) is: {vehicles_in_peak}')
        print(f'The total number of hours of rain on the selected date is: {total_rainy_hours}')
        print(f'Traffic data by hour for Elm Avenue/Rabbit Road: {junction_data['Elm Avenue/Rabbit Road']}')
        print(f'Traffic data by hour for Hanley Highway/Westway: {junction_data['Hanley Highway/Westway']}')


        # Save results to a specific file
        with open(f'results_all.txt', 'a') as results: #Link 1
            print(f'The name of the file selected: {file_name}', file=results)
            print(f'The total number of vehicles passing through all junctions is: {row_amount}', file=results)
            print(f'The total number of trucks passing through all junctions is: {truck_amount}', file=results)
            print(f'The total number of two wheeled vehicles passing through all junctions is: {two_wheeled_amount}', file=results)
            print(f'The total number of busses leaving Elm Avenue/Rabbit Road Junction heading North is: {bus_north}', file=results)
            print(f'The total number of vehicles passing through all junctions without turning is: {vehicle_no_turn}', file=results)
            print(f'The percentage of trucks passing through all junctions is: {percentage_rounded_trucks}', file=results)
            print(f'The average number of bicycles per hour passing through all junctions is: {actual_hourly}, as there are {bike_amount} bikes in total passing on this date.', file=results)
            print(f'The total number of vehicles recorded as over the speed limit is: {above_speed_limit}', file=results)
            print(f'The total number of vehicles recorded over Elm Avenue/Rabbit Road Junction is: {vehicle_Elms}', file=results)
            print(f'The total number of vehicles recorded over Hanley Highway/Westway Junction is: {vehicle_Hanley}', file=results)
            print(f'The percentage of scooters recorded over Elm Avenue/Rabbit Road Junction is: {percentage_rounded_scooters}', file=results)
            print(f'The peak hour for vehicles recorded over Hanley Highway/Westway Junction is: {', '.join(peak_time)}', file=results)
            print(f'The number of vehicles recorded in the peak hour(s) is: {vehicles_in_peak}', file=results)
            print(f'The total number of hours of rain on the selected date is: {total_rainy_hours}', file=results)
            print(f'Traffic data by hour for Elm Avenue/Rabbit Road: {junction_data['Elm Avenue/Rabbit Road']}', file=results)
            print(f'Traffic data by hour for Hanley Highway/Westway: {junction_data['Hanley Highway/Westway']}', file=results)
            results.write('\n')
        
    except FileNotFoundError:
        print(f'Error: File {file_name} not found.')
    

    # Now, creating the histogram using the graphics.py libary, Links 3 and 4
    win_width = 1300
    win_height = 600
    win = GraphWin('Traffic Data Histogram', win_width, win_height) #Link 3

    bar_width = (win_width - 100) / (24 * 2) * 0.7 # Bar was too big, minimised it by 30% to ensure visibility.
    spacing = bar_width # Makes the data more redaable.

    # Set up the title and axis labels, Link 4
    title = Text(Point(win_width / 2, 30), f'Traffic Data for {date_day}/{date_month}/{date_year}')
    title.setSize(20)
    title.setTextColor('black')
    title.draw(win) #Draws it on the window, Link 3

    # X and Y axes
    x_axis = Line(Point(50, win_height - 50), Point(win_width - 50, win_height - 50))  # X axis
    x_axis.draw(win)
    y_axis = Line(Point(50, win_height - 50), Point(50, 50))  # Y axis
    y_axis.draw(win)

    # Label X axis (Hours)
    for i in range(24):
        label_x = 50 + i * (bar_width * 2 + spacing) + bar_width  # Center label under both bars
        label = Text(Point(label_x, win_height - 30), f'{i}') 
        label.setSize(8)
        label.setTextColor('black')
        label.draw(win)

    # X-axis title
    x_title = Text(Point(win_width / 2, win_height - 40), 'Hours of the Day')  # Adjusted position
    x_title.setSize(8)
    x_title.setTextColor('black')
    x_title.draw(win)

    # Calculating max_traffic
    max_traffic = max(max(junction_data['Elm Avenue/Rabbit Road']), max(junction_data['Hanley Highway/Westway']))

    # Setting up the Y axis labels
    y_label_interval = int(max_traffic / 5)  # Defines interval for Y-axis values


    y_axis_label = Text(Point(25, win_height / 2), 'Number of\n Vehicles')
    y_axis_label.setSize(8)
    y_axis_label.setTextColor('black')
    y_axis_label.draw(win)

    # Im using a loop to place numerical Y-axis labels
    for i in range(0, max_traffic + 1, y_label_interval):
        # Calculating Y position 
        label_y_position = win_height - 50 - (i * (win_height - 100) / max_traffic)
        
        # Ensures the label stays within the space
        if label_y_position < 50:
            label_y_position = 50
        
        # Creates a text object for the numerical value at this Y position
        label_y = Text(Point(35, label_y_position), str(i))
        label_y.setSize(8)
        label_y.setTextColor('black')
        label_y.draw(win)


    # Drawing the bars for each junction
    for i in range(24):
        # Calculating the x-position for the purple  bar
        purple_bar_x1 = 50 + i * (bar_width * 2 + spacing)
        purple_bar_x2 = purple_bar_x1 + bar_width

        # Drawing the purple bar
        elm_height = (junction_data['Elm Avenue/Rabbit Road'][i] / max_traffic) * (win_height - 100)
        elm_bar = Rectangle(Point(purple_bar_x1, win_height - 50 - elm_height),
                            Point(purple_bar_x2, win_height - 50))
        elm_bar.setFill('purple')
        elm_bar.draw(win)

        # Calculateing the x-position for the pink bar
        pink_bar_x1 = purple_bar_x2  # Starting where the purple bar ends, to prevent overlap.
        pink_bar_x2 = pink_bar_x1 + bar_width

        # Drawing the pink bar
        hanley_height = (junction_data['Hanley Highway/Westway'][i] / max_traffic) * (win_height - 100)
        hanley_bar = Rectangle(Point(pink_bar_x1, win_height - 50 - hanley_height),
                                Point(pink_bar_x2, win_height - 50))
        hanley_bar.setFill('pink')
        hanley_bar.draw(win)

    # Creating the Legend
    purple_rect = Rectangle(Point(win_width - 150, 50), Point(win_width - 130, 70))
    purple_rect.setFill('purple') # Makes the colour purple to match the bar
    purple_rect.draw(win)
    purple_label = Text(Point(win_width - 110, 60), 'Elm Avenue/Rabbit Road')
    purple_label.setSize(8)
    purple_label.draw(win)

    pink_rect = Rectangle(Point(win_width - 150, 80), Point(win_width - 130, 100))
    pink_rect.setFill('pink') # Making the colour pink to match the bar. If i wrote red, it would become red.
    pink_rect.draw(win)
    pink_label = Text(Point(win_width - 110, 90), 'Hanley Highway/Westway')
    pink_label.setSize(8)
    pink_label.draw(win)

    # Waiting for the user to click before closing the window
    # Ensures the window is still open and ready for interaction
    try:
        win.getMouse()  # Wait for mouse click
    except GraphicsError:
        # If the window is closed (by pressing X), exits
        print('Window closed. Exiting program.')
    win.close() 
    


# Main function to handle the program's loop
def main():
    while True:
        # Asks if the user is an employee
        if check_if_employee():
            # Processing the data for an employee
            process_data()
        else:
            print('Access denied. Only employees can use this program.')
            break

        # Asks if the user wants to process another dataset
        while True:
            continue_processing = input('Do you want to select a data file for a different date? (Y/N): ').lower()

            if continue_processing == 'y' or continue_processing == 'yes':
                break  # Exits the loop and continues with the next data input

            elif continue_processing == 'n' or continue_processing == 'no':
                print('Thank you for using the program.')
                exit()  # Exits the program when user types 'n' or 'no'

            else:
                print('Invalid input. Please enter "Y" for Yes or "N" for No.')  # Handle invalid inputs

if __name__ == '__main__':
    main()



# Refrences/Links 
# 1) https://www.youtube.com/watch?v=QDKlz1mc_v0
# 2) https://www.simplilearn.com/tutorials/python-tutorial/count-in-python
# 3) https://stackoverflow.com/questions/15886455/simple-graphics-for-python
# 4) https://study.com/academy/lesson/using-graphical-objects-in-python.html


