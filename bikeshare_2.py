import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

# Information about functions in different modules has been taken from https://docs.python.org/3/library/

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_city():
    """
    Asks user to specify a city to analyze.

    Returns:
        (str) name of the city to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city.lower() not in ['chicago', 'new york', 'washington']:
        city = input('\nWould you like to see data for Chicago, New York, or'
                     ' Washington?\n')
        if city.lower() == 'chicago':
            return 'chicago.csv'
        elif city.lower() == 'new york':
            return 'new_york_city.csv'
        elif city.lower() == 'washington':
            return 'washington.csv'
        else:
            print('I apologize but I do not understand your response. Please input either '
                  'Chicago, New York, or Washington.')

def get_time_filter():
    """Asks the user for a time period to analyze.
    
    Returns:
        (str) Time filter to analyze.
    """
    time_filter = ''
    while time_filter.lower() not in ['month', 'day', 'none']:
        time_filter = input('\nWould you like to filter the data by month, day,'
                            ' or not at all? Please type "none" for no filter.\n')
        if time_filter.lower() not in ['month', 'day', 'none']:
            print('I apologize but I do not understand your response.')
    return time_filter

def get_month():
    """Asks the user for a month to analyze.
    
    Returns:
        (tuple) Lower limit, upper limit of month to analyze.
    """
    month_response = ''
    months_dictionary = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                   'may': 5, 'june': 6}
    while month_response.lower() not in months_dictionary.keys():
        month_response = input('\nWhich month would you like to see data for?'
                                ' January, February, March, April, May, or June?\n')
        if month_response.lower() not in months_dictionary.keys():
            print('I apologize but I do not understand your response. Please type in a '
                  'month between January and June')
    month = months_dictionary[month_response.lower()]
    return ('2017-{}'.format(month), '2017-{}'.format(month + 1))

def get_day():
    """Asks the user for a day to analyze.

    Returns:
        (tuple) Lower limit, upper limit of date to analyze.
    """
    chosen_month = get_month()[0]
    month = int(chosen_month[5:])
    valid_date = False
    while valid_date == False:    
        is_int = False
        day = input('\nWhich day would you like to see data for?' 
                    ' Please input an integer.\n')
        while is_int == False:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print('I apologize but I do not understand your response. Please input'
                      ' an integer.')
                day = input('\nWhich day would you like to see data for?'
                            ' Please input an integer.\n')
        try:
            start_date = datetime(2017, month, day)
            valid_date = True
        except ValueError as e:
            print(str(e).capitalize())
    end_date = start_date + timedelta(days=1)
    return (str(start_date), str(end_date))


def popular_month(df):
    """Finds and prints the most common month of travel.
    Arguments:
        city dataframe
    Returns:
        none
    """
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode())
    most_common_month = months[index - 1]
    print('The most popular month is {}.'.format(most_common_month))

def popular_day(df):
    """Finds and prints the most common day of the week of travel.
    Arguments:
        city dataframe
    Returns:
        none
    """
    daysofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode())
    most_common_day = daysofweek[index]
    print('The most popular day of week is {}.'.format(most_common_day))

def popular_hour(df):
    """Finds and prints the most common hour of day of travel.
    Arguments:
        city dataframe
    Returns:
        none
    """
    most_common_hour = int(df['start_time'].dt.hour.mode())
    if most_common_hour == 0:
        am_pm = 'am'
        readable_common_hour = 12
    elif 1 <= most_common_hour < 13:
        am_pm = 'am'
        readable_common_hour = most_common_hour
    elif 13 <= most_common_hour < 24:
        am_pm = 'pm'
        readable_common_hour = most_common_hour - 12
    print('The most popular hour of day is {}{}.'.format(readable_common_hour, am_pm))

def popular_stations(df):
    """Finds and prints the most common start and end stations.
    Arguments:
        city dataframe
    Returns:
        none
    """
    common_start = df['start_station'].mode().to_string(index = False)
    common_end = df['end_station'].mode().to_string(index = False)
    print('The most popular start station is {}.'.format(common_start))
    print('The most popular end station is {}.'.format(common_end))

def popular_trip(df):
    """Finds and prints the most common trip.
    Arguments:
        city dataframe
    Returns:
        none
    """
    most_common_trip = df['trip'].mode().to_string(index = False)
    # The 'trip' column is created in the statistics() function.
    print('The most popular trip is {}.'.format(most_common_trip))

def trip_duration(df):
    """Finds and prints the total and average travel times in
       hours, minutes, and seconds.
    Arguments:
        city dataframe
    Returns:
        none
    """
    total_time = df['trip_duration'].sum()
    minute, second = divmod(total_time, 60)
    hour, minute = divmod(minute, 60)
    print('The total travel time is {} hours, {} minutes and {}'
          ' seconds.'.format(hour, minute, second))
    average_time = round(df['trip_duration'].mean())
    m, s = divmod(average_time, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print('The average travel time is {} hours, {} minutes and {}'
              ' seconds.'.format(h, m, s))
    else:
        print('The average travel time is {} minutes and {} seconds.'.format(m, s))

def users_info(df):
    """Finds and prints the counts of each user type.
    Arguments:
        city dataframe
    Returns:
        none
    """
    subscribers = df.query('user_type == "Subscriber"').user_type.count()
    customers = df.query('user_type == "Customer"').user_type.count()
    print('There are {} Subscribers and {} Customers.'.format(subscribers, customers))

def gender_info(df):
    """Finds and prints the counts of each gender(only available for NYC and Chicago).
    Arguments:
        city dataframe
    Returns:
        none
    """
    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Female"').gender.count()
    print('There are {} male and {} female users.'.format(male_count, female_count))

def birth_year_info(df):
    """ Finds and prints the earliest, most recent and most popular birth years.
    Arguments:
        city dataframe
    Returns:
        none
    """
    earliest = int(df['birth_year'].min())
    recent = int(df['birth_year'].max())
    popular = int(df['birth_year'].mode())
    print('The oldest users are born in {}.\nThe youngest users are born in {}.'
          '\nThe most popular birth year is {}.'.format(earliest, recent, popular))

def display_data(df):
    """Raw data is displayed upon request by the user in this manner: Script prompts the user 
       if they want to see 5 lines of raw data, that data is displayed if the answer is 'yes', and 
       these prompts are continued and displays until the user says 'no'.
    Arguments:
        dataframe
    Returns:
        none
    """
    def is_valid(display):
        if display.lower() in ['yes', 'no']:
            return True
        else:
            return False
    head = 0
    tail = 5
    valid_input = False
    while valid_input == False:
        display = input('\nWould you like to view individual trip data? '
                        'Type \'yes\' or \'no\'.\n')
        valid_input = is_valid(display)
        if valid_input == True:
            break
        else:
            print("I apologize but I do not understand your response. Please input 'yes' or"
                  " 'no'.")
    if display.lower() == 'yes':
        # Prints every column except the 'trip' column created in main()
        print(df[df.columns[0:-1]].iloc[head:tail])
        display_more = ''
        while display_more.lower() != 'no':
            valid_input_2 = False
            while valid_input_2 == False:
                display_more = input('\nWould you like to view more individual'
                                     ' trip data? Type \'yes\' or \'no\'.\n')
                valid_input_2 = is_valid(display_more)
                if valid_input_2 == True:
                    break
                else:
                    print("I apologize but I do not understand your response. Please input "
                          "'yes' or 'no'.")
            if display_more.lower() == 'yes':
                head += 5
                tail += 5
                print(df[df.columns[0:-1]].iloc[head:tail])
            elif display_more.lower() == 'no':
                break

def main():
    """Calculates and prints out the descriptive statistics about a city and
    time period specified by the user via input.
    Arguments:
        none.
    Returns:
        none.
    """
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    print('Loading data...')
    df = pd.read_csv(city, parse_dates = ['Start Time', 'End Time'])
    
    # All column names are changed to lowercase letters and spaces are replaced with underscores
    new_labels = []
    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels
    
    # The column width is increased so that the longer strings in the 'trip' column can be displayed fully
    pd.set_option('max_colwidth', 100)
    
    # A 'trip' column is formed to concatenate 'start_station' with 
    # 'end_station' for use in popular_trip() function
    df['trip'] = df['start_station'].str.cat(df['end_station'], sep=' to ')

    # Filter by time period (month, day, none)
    time_filter = get_time_filter()
    if time_filter == 'none':
        filtered_dataframe = df
    elif time_filter == 'month' or time_filter == 'day':
        if time_filter == 'month':
            filter_lower, filter_upper = get_month()
        elif time_filter == 'day':
            filter_lower, filter_upper = get_day()
        print('Filtering data...')
        filtered_dataframe = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nCalculating the first statistic...')

    if time_filter == 'none':
        start_time = time.time()
        
        # Most popular month
        start_time = time.time()
        popular_month(filtered_dataframe)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
    
    if time_filter == 'none' or time_filter == 'month':
        start_time = time.time()
        
        # Most popular day of week
        start_time = time.time()
        popular_day(filtered_dataframe)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")    

    # Most popular hour of the day
    start_time = time.time()
    popular_hour(filtered_dataframe)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")

   # Most popular start and end stations
    start_time = time.time()
    popular_stations(filtered_dataframe)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")

    # Most popular trip
    start_time = time.time()
    popular_trip(filtered_dataframe)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")

    # Total trip duration and average trip duration
    start_time = time.time()
    trip_duration(filtered_dataframe)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")

    # Counts of each user type
    start_time = time.time()
    users_info(filtered_dataframe)
    print("That took %s seconds." % (time.time() - start_time))
    
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print("\nCalculating the next statistic...")
        
        # Counts of gender
        start_time = time.time()
        gender_info(filtered_dataframe)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")

        # The earliest, most recent and most popular birth years
        start_time = time.time()
        birth_year_info(filtered_dataframe)
        print("That took %s seconds." % (time.time() - start_time))

    # Display five lines of data at a time if the user responds that they would like to
    display_data(filtered_dataframe)

if __name__ == "__main__":
    main()